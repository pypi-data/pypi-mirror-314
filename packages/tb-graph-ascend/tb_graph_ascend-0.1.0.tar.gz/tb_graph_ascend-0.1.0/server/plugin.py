# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2024, Huawei Technologies.
# Adapt to the model hierarchical visualization data collected by the msprobe tool
# ==============================================================================
"""The TensorBoard Graphs plugin."""

import json
import os
from werkzeug import wrappers, Response, exceptions

from tensorboard import errors
from tensorboard.backend import http_util
from tensorboard.plugins import base_plugin
from tensorboard.util import tb_logging
from . import constants

logger = tb_logging.get_logger()

class GraphsPlugin(base_plugin.TBPlugin):
    """Graphs Plugin for TensorBoard."""

    plugin_name = constants.PLUGIN_NAME
    headers = [('X-Content-Type-Options', 'nosniff')]

    def __init__(self, context):
        """Instantiates GraphsPlugin via TensorBoard core.

        Args:
          context: A base_plugin.TBContext instance.
        """
        super().__init__(context)
        self._data_provider = context.data_provider
        self.logdir = os.path.abspath(context.logdir.rstrip('/'))
        self._current_file_path = None  # Store the path of the currently loaded file
        self._current_file_data = None  # Store the data of the currently loaded file
        self._current_tag = None # Store the tag of the currently loaded file
        self.batch_id = 0  # 将 batch_id 声明为实例变量
        self.step_id = 0   # 可以同样声明 step_id
        self.dfs_node_ids = [] # batch和step没变的话就将所有的nodename存起来，方便快速读取
        self.check_batch_id = 0  # 来配合node_ids监察用的，他不变node_ids就不用重新读取了
        self.check_step_id = 0   # 同上
        self.check_tag = None

    def get_plugin_apps(self):
        return {
            '/index.js': self.static_file_route,
            '/index.html': self.static_file_route,
            "/info": self.info_route,
            "/compoments": self.get_all_data,
            "/expandnodes": self.get_all_upnodes,
            "/precision": self.get_all_precisonNodes,
            "/unmatch": self.get_unmatch,
            "/match": self.get_match,
            "/parent": self.get_parent_node,
            "/subgraph": self.subgraph_route,
        }

    def is_active(self):
        """The graphs plugin is active iff any run has a graph."""
        for _, _, files in os.walk(self.logdir):
            for file in files:
                if file.endswith('.vis'):
                    return True
        return False

    def data_plugin_names(self):
        return (
            constants.PLUGIN_NAME,
            constants.PLUGIN_NAME_RUN_METADATA_WITH_GRAPH,
        )

    def frontend_metadata(self):
        return base_plugin.FrontendMetadata(
            es_module_path='/index.js',
            disable_reload=True,
        )

    def info_impl(self):
        """Returns a dict of all runs and their data availabilities, including a flag indicating if a .vis file is present."""
        result = {}

        def add_row_item(run, tag=None, is_vis=False):
            run_item = result.setdefault(
                run,
                {
                    "run": run,
                    "tags": {},
                    "run_graph": False,
                },
            )

            tag_item = None
            if tag:
                tag_item = run_item.get("tags").setdefault(
                    tag,
                    {
                        "tag": tag,
                        "conceptual_graph": False,
                        "op_graph": False,
                        "profile": False,
                    },
                )
            return (run_item, tag_item)

        run_tag_pairs = self._get_run_dirs()
        for run, tag in run_tag_pairs:
            add_row_item(run, tag, is_vis=True)
        return result

    # 拿jsondata的
    def get_jsondata(self, request):
        run = request.args.get("run")
        tag = request.args.get("tag")
        json_data = None
        error_message = None

        if run is None or tag is None:
            error_message = 'The query parameters "run" and "tag" are required'
            return json_data, error_message
        
        run_dir = os.path.join(self.logdir, run)
        file_path = self._load_json_file(run_dir, tag)
        json_data = self._read_json_file(file_path)
        self._current_file_data = json_data
        if json_data is None:
            error_message = f'vis file for tag "{tag}" not found in run "{run}"'

        return json_data, error_message
    
    # 拿所有nodename的
    def get_all_nodeName(self, json_data, request):
        npu_ids, bench_ids = [], []
        try:
            batch = int(request.args.get("batch"))
            step = int(request.args.get("step"))
        except ValueError:
            logger.error('The param "batch" or "step" does not exist or not a valid value')
        # 获取 NPU 和 Bench 数据
        npu_data = self.json_get(json_data, 'NPU')
        bench_data = self.json_get(json_data, 'Bench')
        def extract_ids(nodes_data, id_list):
            for node_name in nodes_data.get("node"):
                id_list.append(node_name)
        def traverse_npu(subnodes):
            for node in subnodes:
                node_data = self.json_get(npu_data, 'node', node) if npu_data else self.json_get(json_data, 'node', node)
                micro_step_id = node_data.get('micro_step_id')
                if micro_step_id == batch or micro_step_id is None:
                    npu_ids.append(node)
                    traverse_npu(node_data.get('subnodes', []))

        # 提取 NPU 节点 ID
        if batch == -1 and step == -1:
            extract_ids(npu_data or json_data, npu_ids)
        else:
            root = (npu_data or json_data).get('root')
            root_subnodes = self.json_get((npu_data or json_data), 'node', root, 'subnodes')
            traverse_npu(root_subnodes)

        # 提取 Bench 节点 ID
        extract_ids(bench_data or json_data, bench_ids)
        # 返回格式为 [[NPU节点ID列表], [Bench节点ID列表]]
        return [npu_ids, bench_ids]

    def dfs_collect_nodes(self, json_data, request):
        all_node_names = []
        try:
            batch = int(request.args.get("batch"))
            step = int(request.args.get("step"))
        except ValueError:
            logger.error('The param "batch" or "step" does not exist or not a valid value')
        def should_include_node(micro_step_id, step_id):
            return (micro_step_id is batch or batch == -1 or micro_step_id is None) and (step_id is step or step == -1 or step_id is None)

        nodes_data = self.json_get(json_data, 'NPU', 'node') or self.json_get(json_data, 'node')
        for node in nodes_data:
            micro_step_id = self.json_get(nodes_data, node, 'micro_step_id')
            step_id = self.json_get(nodes_data, node, 'step_id')
            if should_include_node(micro_step_id, step_id) and not self.json_get(nodes_data, node, 'subnodes'):
                all_node_names.append(node)
        return all_node_names
    
    #拿所有precisonNodes的，与controls的精度筛选联动
    @wrappers.Request.application
    def get_all_precisonNodes(self, request):
        grouped_precision_set, precision_node_ids = [], []
        precision_set = request.args.get("precison")
        precision_set_str = precision_set.split(',')
        precision_none = 0
        if '无匹配节点' in precision_set_str:
            precision_set_str = [p for p in precision_set_str if p != '无匹配节点']
            precision_none = 1
        grouped_precision_set = [list(map(float, precision_set_str[i:i+2])) for i in range(0, len(precision_set_str), 2)]    
        tag = request.args.get("tag")
        json_data = self.check_jsondata(request)
        def has_conditions_changed(tag):
            return (
                self.check_batch_id != self.batch_id or
                self.check_step_id != self.step_id or
                self.check_tag != tag or
                self.check_tag is None
            )
        if has_conditions_changed(tag):
            self.dfs_node_ids = self.dfs_collect_nodes(json_data, request)
            self.check_batch_id = self.batch_id
            self.check_step_id = self.step_id
            self.check_tag = tag
        node_ids = self.dfs_node_ids
        for node in node_ids:
            node_data = self.json_get(json_data, 'NPU', 'node', node, 'data') or self.json_get(json_data, 'node', node, 'data')
            precision = node_data.get('precision_index') if node_data is not None else None
            # 检查 precision 是否在 grouped_precision_set 的任何子列表中
            if precision is not None:
                for group in grouped_precision_set:
                    if all(g is not None for g in group) and group[0] <= precision <= group[1]:  # 判断 precision 是否在某个子列表中
                        precision_node_ids.append(node)
            else:
                if precision_none == 1:
                    precision_node_ids.append(node)
        return http_util.Respond(request, precision_node_ids, "application/json")
    
    def group_precision_set(self, precision_set):
        if len(precision_set) % 2 != 0:
            raise ValueError('The number of elements in precision_set is not even')
        grouped_precision_set = [precision_set[i:i+2] for i in range(0, len(precision_set), 2)]
        return grouped_precision_set
    
    def get_all_unmatchedNodes(self, allNodeName, request):
        json_data = self.check_jsondata(request)
        is_npu_present = 'NPU' in json_data
        def collect_unmatched_nodes(node_list, *path):
            return [node for node in node_list if not self.json_get(json_data, *path, node, 'matched_node_link')]
        NPU_Unmatched = collect_unmatched_nodes(allNodeName[0], 'NPU', 'node') if is_npu_present else \
                        collect_unmatched_nodes(allNodeName[0], 'node')
        Bench_Unmatched = collect_unmatched_nodes(allNodeName[1], 'Bench', 'node') if is_npu_present else []
        return [NPU_Unmatched, Bench_Unmatched]

    @wrappers.Request.application
    def get_match(self, request):
        NPU_node = request.args.get("NPU")[4:]
        Bench_node = request.args.get("Bench")[4:]
        run = request.args.get('run')
        tag = request.args.get('tag')
        file_path = os.path.join(run, f"{tag}.vis")
        json_data = self.check_jsondata(request)
        NPU_node_data = self.json_get(json_data, 'NPU', 'node', NPU_node)
        Bench_node_data = self.json_get(json_data, 'Bench', 'node', Bench_node)
        # 获取输入输出数据
        NPU_input_data, Bench_input_data, NPU_output_data, Bench_output_data = self.get_input_output_data(
            NPU_node_data, Bench_node_data)
        # 计算输入输出的最小长度
        input_min_length, output_min_length = self.calculate_min_length(NPU_input_data, Bench_input_data,
                                                                       NPU_output_data, Bench_output_data)
        precision_index, max_precision_index, result = -1, -1, 0
        input, output = [], []
        if input_min_length > 0:
            npu_input_keys, bench_input_keys = self.get_keys(NPU_input_data, Bench_input_data)
            # 处理输入数据
            data_type = 'input_data'
            data_set = {
                'input_data': NPU_input_data,
                'output_data': Bench_input_data,
                'npu_keys': npu_input_keys,
                'bench_keys': bench_input_keys,
                'data_type': data_type,
                'precision_index': precision_index,
                'file_path': file_path
            }
            max_precision_index = self.process_input_data(input, data_set, NPU_node)
            if max_precision_index > precision_index:
                precision_index = max_precision_index

        if output_min_length > 0:
            npu_output_keys, bench_output_keys = self.get_keys(NPU_output_data, Bench_output_data)
            # 处理输出数据
            data_type = 'output_data'
            data_set = {
                'input_data': NPU_output_data,
                'output_data': Bench_output_data,
                'npu_keys': npu_output_keys,
                'bench_keys': bench_output_keys,
                'data_type': data_type,
                'precision_index': precision_index,
                'file_path': file_path
            }
            max_precision_index = self.process_output_data(output, data_set, NPU_node)
            if max_precision_index > precision_index:
                precision_index = max_precision_index
                
        result = [request.args.get("NPU"), precision_index, input, output]

        if not input and not output and precision_index == -1:
            return http_util.Respond(request, [], "application/json")

        # 添加匹配的节点链接
        matched_result = self.add_matched_node_link(NPU_node, Bench_node)
        if not matched_result:
            result = {"error": f"Unable to link matched nodes for NPU_node: {NPU_node} and Bench_node: {Bench_node}"}
            return http_util.Respond(request, result, "application/json", status_code=400)
        
        precision_result = self.add_precision_index(NPU_node, precision_index)
        if not precision_result:
             result = {"error": f"Unable to add precision index for NPU_node: {NPU_node} with precision_index: {precision_index}"}
             return http_util.Respond(request, result, "application/json", status_code=400)
        
        # 保存修改后的内容
        self.save_results(file_path)

        return http_util.Respond(request, result, "application/json")

    def get_input_output_data(self, NPU_node_data, Bench_node_data):
        """提取输入输出数据"""
        NPU_input_data = self.json_get(NPU_node_data, 'input_data')
        Bench_input_data = self.json_get(Bench_node_data, 'input_data')
        NPU_output_data = self.json_get(NPU_node_data, 'output_data')
        Bench_output_data = self.json_get(Bench_node_data, 'output_data')
        return NPU_input_data, Bench_input_data, NPU_output_data, Bench_output_data

    def calculate_min_length(self, NPU_input_data, Bench_input_data, NPU_output_data, Bench_output_data):
        """计算输入输出数据的最小长度"""
        input_min_length, output_min_length = 0, 0
        if NPU_input_data and Bench_input_data:
            input_min_length = min(len(NPU_input_data), len(Bench_input_data))
        if NPU_output_data and Bench_output_data:
            output_min_length = min(len(NPU_output_data), len(Bench_output_data))
        return input_min_length, output_min_length

    def get_keys(self, NPU_data, Bench_data):
        """提取数据的keys"""
        npu_keys = list(NPU_data.keys())
        bench_keys = list(Bench_data.keys())
        return npu_keys, bench_keys

    def safe_float_conversion(self, value, default=None):
        """安全地转换为float"""
        try:
            return float(value)
        except ValueError:
            return None

    def calculate_diff_and_relative_error(self, npu_data, bench_data):
        """计算最大值、最小值、均值和L2范数的差异以及相对误差"""
        results = {}
        
        for key in ['Max', 'Min', 'Mean', 'Norm']:
            NPU_value = self.safe_float_conversion(npu_data.get(key, 0))
            Bench_value = self.safe_float_conversion(bench_data.get(key, 0))
            
            # 计算差异
            if NPU_value is not None:
                results[f'NPU_{key}'] = NPU_value
            else:
                results[f'NPU_{key}'] = 'N/A'
            if Bench_value is not None:
                results[f'Bench_{key}'] = Bench_value
            else:
                results[f'Bench_{key}'] = 'N/A'
            
            # 计算相对误差
            if NPU_value is not None and Bench_value is not None and Bench_value != 0:
                results[f'{key}_relative_err'] = f"{abs(NPU_value - Bench_value) / float(Bench_value) * 100:.6f}%"
            else:
                results[f'{key}_relative_err'] = "N/A"
        
        return results

    def process_data(self, data, data_set, NPU_node):
        """处理数据的公共逻辑"""
        for npu_key, bench_key in zip(data_set['npu_keys'], data_set['bench_keys']):
            if data_set['input_data'].get(npu_key) not in ['None', None] and data_set['output_data'].get(bench_key) not in ['None', None]:
                npu_value = data_set['input_data'][npu_key]
                bench_value = data_set['output_data'][bench_key]

                if self._current_file_data.get('task') == 'md5':
                    if data_set['input_data'].get('md5') != data_set['output_data'].get('md5'):
                        data_set['precision_index'] = 0
                        break
                    data_set['precision_index'] = 1

                # 计算差异和相对误差
                results = self.calculate_diff_and_relative_error(npu_value, bench_value)

                # 提取计算的结果
                NPU_max, Bench_max = results['NPU_Max'], results['Bench_Max']
                NPU_min, Bench_min = results['NPU_Min'], results['Bench_Min']
                NPU_mean, Bench_mean = results['NPU_Mean'], results['Bench_Mean']
                NPU_norm, Bench_norm = results['NPU_Norm'], results['Bench_Norm']
                
                max_relative_err = results['Max_relative_err']
                min_relative_err = results['Min_relative_err']
                mean_relative_err = results['Mean_relative_err']
                norm_relative_err = results['Norm_relative_err']

                # 创建数据条目
                data_entry = [
                    ['Max diff', NPU_max - Bench_max],
                    ['Min diff', NPU_min - Bench_min],
                    ['Mean diff', NPU_mean - Bench_mean],
                    ['L2norm diff', NPU_norm - Bench_norm],
                    ['MaxRelativeErr', max_relative_err],
                    ['MinRelativeErr', min_relative_err],
                    ['MeanRelativeErr', mean_relative_err],
                    ['NormRelativeErr', norm_relative_err]
                ]

                # 更新最大差异
                Max_value = max(abs(NPU_max - Bench_max), abs(NPU_min - Bench_min), abs(NPU_mean - Bench_mean), abs(NPU_norm - Bench_norm))
                if Max_value > data_set['precision_index']:
                    data_set['precision_index'] = Max_value

                # 将数据添加到列表中
                data.append(data_entry)

                # 保存数据到文件
                self.save_data(data_set['file_path'], NPU_node, npu_key, data_entry, data_set['data_type'])

        return data_set['precision_index']

    def process_input_data(self, input, data_set, NPU_node):
        """处理输入数据"""
        return self.process_data(input, data_set, NPU_node)

    def process_output_data(self, output, data_set, NPU_node):
        """处理输出数据"""
        return self.process_data(output, data_set, NPU_node)

    def save_data(self, file_path, NPU_node, npu_key, data, data_type):
        """保存数据到文件"""
        for key, value in data:
            self.json_get(self._current_file_data, "NPU", "node", NPU_node, data_type, npu_key)[key] = value
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self._current_file_data, file, ensure_ascii=False, indent=4)

    def add_matched_node_link(self, NPU_node, Bench_node):
        """添加匹配的节点链接"""
        # 获取匹配的节点链接
        NPU_matched_node_link = self.json_get(self._current_file_data, "NPU", "node", NPU_node, "matched_node_link")
        Bench_matched_node_link = self.json_get(self._current_file_data, "Bench", "node", Bench_node, "matched_node_link")

        # 检查是否为可变列表类型
        if isinstance(NPU_matched_node_link, list) and isinstance(Bench_matched_node_link, list):
            NPU_matched_node_link.append(Bench_node)
            Bench_matched_node_link.append(NPU_node)
        else:
            logger.error(f'Error: add matched_node_link failed.')
            return False

        # 更新 match 列表
        if self._current_file_data.get('match') is None:
            self._current_file_data["match"] = []

        self._current_file_data.get('match').append([NPU_node, Bench_node])
        return True

    def add_precision_index(self, NPU_node, precision_index):
        """添加精度误差"""
        # 获取 NPU 数据
        NPU_precison_index = self.json_get(self._current_file_data, "NPU", "node", NPU_node, "data")

        # 检查 NPU_precison_index 是否为字典类型
        if isinstance(NPU_precison_index, dict):
            NPU_precison_index["precision_index"] = precision_index
        else:
            logger.error(f'Error: add precision_index failed.')
            return False
        return True
        
    def save_results(self, file_path):
        """保存修改后的结果"""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self._current_file_data, file, ensure_ascii=False, indent=4)

    
    @wrappers.Request.application
    def get_unmatch(self, request):
        # 需要处理的项目为input, output, matched_node_link data里面的precision_index 和 来判断的
        NPU_node = request.args.get("NPU", "")[4:]  # 防止获取为空字符串
        Bench_node = request.args.get("Bench", "")[4:]
        run = request.args.get('run', "")
        tag = request.args.get('tag', "")
        file_path = os.path.join(run, f"{tag}.vis")

        # precision_index
        try:
            npu_node_data = self._current_file_data.get("NPU", {}).get("node", {}).get(NPU_node, {}).get('data', {})
            if "precision_index" in npu_node_data:
                del npu_node_data["precision_index"]
        except Exception as e:
            error = {"error": f"Error removing precision_index: {str(e)}"}
            return http_util.Respond(request, error, "application/json", status_code=500)

        # matched_node_link
        try:
            self._current_file_data["NPU"]["node"][NPU_node]["matched_node_link"] = []
            self._current_file_data["Bench"]["node"][Bench_node]["matched_node_link"] = []
        except Exception as e:
            error = {"error": f"Error resetting matched_node_link: {str(e)}"}
            return http_util.Respond(request, error, "application/json", status_code=500)

        # input
        input_data = self.json_get(self._current_file_data, "NPU", "node", NPU_node, "input_data")
        if input_data is None:
            error = {"error": f"Error resetting input_data: {str(e)}"}
            return http_util.Respond(request, error, "application/json", status_code=500)
        for item in input_data:
            keys_to_remove = [key for key, value in input_data[item].items() if key in constants.UNMATCH_NAME_SET]
            for key in keys_to_remove:
                del input_data[item][key]

        # output
        output_data = self.json_get(self._current_file_data, "NPU", "node", NPU_node, "output_data")
        if output_data is None:
            error = {"error": f"Error resetting output_data: {str(e)}"}
            return http_util.Respond(request, error, "application/json", status_code=500)
        for item in output_data:
            keys_to_remove = [key for key, value in output_data[item].items() if key in constants.UNMATCH_NAME_SET]
            for key in keys_to_remove:
                del output_data[item][key]
        # match
        self._current_file_data.get('match').remove([NPU_node, Bench_node])

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self._current_file_data, file, ensure_ascii=False, indent=4)
        result = 'unmatched!!!'
        return http_util.Respond(request, result, "application/json")
    
    @wrappers.Request.application
    def get_parent_node(self, request):
        node = request.args.get("node")[4:]  # 获取节点信息
        prefix = request.args.get("node")[:4]  # 获取前缀
        json_data = self.check_jsondata(request)  # 检查请求中的 JSON 数据

        def find_upnode(node):
            matched_node_link_list = self.json_get(json_data, constants.PREFIX_MAP[prefix], 'node', node, 'matched_node_link')
            
            if matched_node_link_list:
                result = matched_node_link_list[-1]  # 获取匹配的最后一个节点
                return http_util.Respond(request, result, "application/json")  # 返回响应

            # 如果没有找到 matched_node_link，继续递归查找上级节点
            else:
                upnode = self.json_get(json_data, constants.PREFIX_MAP[prefix], 'node', node, 'upnode')
                if upnode:
                    return find_upnode(upnode)  # 递归查找上级节点
                else:
                    return http_util.Respond(request, {}, "application/json")  # 如果没有找到上级节点，返回空响应

        return find_upnode(node)

    #拿json_data里面所有配置数据的
    @wrappers.Request.application
    def get_all_data(self, request):
        """Returns all data in json format."""
        keys = ['ToolTip', 'Colors']
        response_data = {}
        tag = request.args.get("tag")
        json_data = self.check_jsondata(request)
        allNodeName = self.get_all_nodeName(json_data, request)
        response_data['Menu'] = allNodeName
        response_data['UnMatchedNode'] = self.get_all_unmatchedNodes(allNodeName , request)
        self._current_tag = tag
        for field in ['MicroSteps', 'StepList', 'match']:
            if json_data.get(field, {}):
                keys.append(field)
        for key in keys:
            if key == 'StepList' and 'ALL' not in json_data.get('StepList', {}):
                json_data[key].insert(0, 'ALL')
            response_data[key] = json_data.get(key, {})
        return http_util.Respond(request, response_data, "application/json")
    
    @wrappers.Request.application
    def static_file_route(self, request):
        filename = os.path.basename(request.path)
        extension = os.path.splitext(filename)[1]
        if extension == '.html':
            mimetype = 'text/html'
        elif extension == '.js':
            mimetype = 'application/javascript'
        else:
            mimetype = 'application/octet-stream'
        filepath = os.path.join(os.path.dirname(__file__), 'static', filename)
        try:
            with open(filepath, 'rb') as infile:
                contents = infile.read()
        except IOError as e:
            raise exceptions.NotFound('404 Not Found') from e
        return Response(
            contents, content_type=mimetype, headers=GraphsPlugin.headers
        )
    
    #方便多层级展开的upnodes节点集合，与tf-graph的_menuSelectedNodeExpand联动
    @wrappers.Request.application
    def get_all_upnodes(self, request):
        npu_upnodes_list, matched_upnodes_list, node_list = [], [], []
        node, matched_node, prefix = '', '', ''
        node_arg = request.args.get('node')
        json_data = self.check_jsondata(request)
        prefix = str(node_arg)[:4] if str(node_arg)[:4] in constants.PREFIX_MAP else ''
        node = node_arg[4:] if prefix in constants.PREFIX_MAP else node_arg
        if prefix in constants.PREFIX_MAP and json_data.get(constants.PREFIX_MAP[prefix], {}):
            node_list = json_data[constants.PREFIX_MAP[prefix]].get('node', {})
        else:
            node_list = json_data.get('node', {})
        matched_node = (
            node_list.get(node, {}).get('matched_node_link', [])[-1]
            if node_list.get(node, {}).get('matched_node_link')
            else None
        )
        def get_upnodes(node, prefix):
            upnodes_list = []
            if prefix == '':
                node_list = json_data.get('node', {})
            else:
                node_list = json_data.get('NPU' if prefix == 'N___' else 'Bench', {}).get('node', {})
            while node in node_list:
                upnode = node_list[node].get('upnode')
                if not upnode or upnode == 'None':
                    break
                upnodes_list.insert(0, upnode)
                node = upnode
            return upnodes_list
        npu_upnodes_list = get_upnodes(node, prefix)
        # 如果 matched_node 是 None 的话
        if matched_node is None:
            previous_node = None  # 用于跟踪上一个 node
            for node in reversed(npu_upnodes_list):
                if node_list.get(node, {}).get('matched_node_link'):  # 判断条件
                    matched_node = previous_node  # 将 matched_node 设置为上一个 node
                    break
                previous_node = node  # 更新 previous_node 为当前 node
        if prefix in constants.PREFIX_MAP:
            matched_upnodes_list = get_upnodes(matched_node, prefix)
        return http_util.Respond(request, [[prefix], npu_upnodes_list, matched_upnodes_list], "application/json")
    
    # 检查到底是读一般还是用之前存的
    def check_jsondata(self, request):
        tag = request.args.get("tag")
        if self._current_tag is None or self._current_tag != tag:
            json_data, error_message = self.get_jsondata(request)
            if error_message:
                return http_util.Respond(request, error_message, "text/plain", 400)
        else:
            json_data = self._current_file_data
        return json_data
    
    # 处理xx.get
    def json_get(self, data, *args):
        result = data
        for key in args:
            if result is None:
                return None
            result = result.get(key)
        return result

    # 获取子图数据，最核心且基本的所在
    @wrappers.Request.application
    def subgraph_route(self, request):
        """Returns a subgraph for a given node id, modified to use run and tag from query parameters."""
        json_data = self.check_jsondata(request)
        node_id = request.args.get("node")
        self.batch_id = request.args.get("batch")
        self.step_id = request.args.get("step")
        if node_id is None:
            return http_util.Respond(
                request, 'The query parameter "node" is required', "text/plain", 400
            )
        if node_id == 'root':
            if json_data.get('Bench', {}):
                subgraph_pbtxt_set = {}
                for node_type in ('Bench', 'NPU'):
                    subgraph = {'node': {}, 'edge': {}}
                    node = self.json_get(json_data, constants.SETS[node_type][0], 'root')
                    node_data = self.json_get(json_data ,constants.SETS[node_type][0], 'node', node)
                    node = constants.SETS[node_type][1] + node
                    matched_node_link = node_data['matched_node_link']
                    if matched_node_link[0][:4] != constants.SETS[node_type][2]:
                        matched_node_link[0] = constants.SETS[node_type][2] + matched_node_link[0]
                    subgraph['node'][node] = node_data
                    subgraph_pbtxt_set[node_type] = self._convert_to_protobuf_format(subgraph)
                subgraph_pbtxt = subgraph_pbtxt_set.get('NPU', '') + subgraph_pbtxt_set.get('Bench', '')
            else:
                subgraph = {'node': {}, 'edge': {}}
                node = json_data.get('root')
                node_data = self.json_get(json_data, 'node', node)
                subgraph['node'][node] = node_data
                subgraph_pbtxt = self._convert_to_protobuf_format(subgraph)
        else:
            subgraph = self._extract_subgraph(json_data, node_id)
            subgraph_pbtxt = self._convert_to_protobuf_format(subgraph)
        return http_util.Respond(request, subgraph_pbtxt, "text/x-protobuf")
    
    @wrappers.Request.application
    def info_route(self, request):
        info = self.info_impl()
        return http_util.Respond(request, info, "application/json")

    #同上二者一体
    def _extract_subgraph(self, json_data, node_id):
        """提取子图，支持多种节点前缀逻辑"""
        subgraph = {'node': {}, 'edge': []}

        # 检查前缀并获取节点集合
        prefix = node_id[:4]
        if prefix in constants.SETS and len(prefix) == 4:
            node_id = node_id[4:]
            node_set = self.json_get(json_data, constants.SETS[prefix][0], 'node')
        else:
            prefix = ''
            node_set = json_data.get('node', {})
        
        # 获取当前节点数据
        node_data = node_set.get(node_id, {})
        subnodes = node_data.get('subnodes', [])
        
        # 遍历子节点
        for subnode_id in subnodes:
            subnode_id_data = node_set.get(subnode_id, {})
            if subnode_id_data.get('micro_step_id') is not None:
                self._process_subnode(subgraph, prefix, subnode_id, subnode_id_data, json_data)
            else:
                self._process_non_root_subnode(subgraph, prefix, subnode_id, subnode_id_data)
        
        return subgraph

    def _process_non_root_subnode(self, subgraph, prefix, subnode_id, subnode_id_data):
        """处理非根子节点"""
        # 更新匹配的节点链接
        self._update_matched_node_links(subnode_id_data, prefix)
        
        # 添加前缀并存入子图
        full_subnode_id = prefix + subnode_id
        subgraph['node'][full_subnode_id] = subnode_id_data

    #针对分micro_step_id和step_id取的部分节点
    def _process_subnode(self, subgraph, prefix, subnode_id, subnode_id_data, json_data):
        batchid = subnode_id_data.get('micro_step_id')
        stepid = subnode_id_data.get('step_id')
        steplist = json_data.get('StepList')

        def should_update_node():
            """判断是否需要更新节点的条件逻辑"""
            if self.batch_id == '-1':
                if self.step_id == '-1':  # batch_id 和 step_id 都为 -1
                    return True
                return stepid == str(steplist[int(self.step_id) + 1])  # 匹配 step_id
            else:  # batch_id 有效
                if self.step_id != '-1':  # step_id 有效
                    return batchid == int(self.batch_id) and stepid == str(steplist[int(self.step_id) + 1])
                return batchid == int(self.batch_id)  # 仅匹配 batch_id

        if should_update_node():
            self._update_matched_node_links(subnode_id_data, prefix)
            subnode_id = prefix + subnode_id
            subgraph['node'][subnode_id] = subnode_id_data

    def _update_matched_node_links(self, subnode_id_data, prefix):
        if 'matched_node_link' in subnode_id_data:
            for index, matched_node_link in enumerate(subnode_id_data['matched_node_link']):
                if matched_node_link[:4] != constants.SETS[prefix][1]:
                    matched_node_link = constants.SETS[prefix][1] + matched_node_link
                subnode_id_data['matched_node_link'][index] = matched_node_link

    #拼接成类json
    def _convert_to_protobuf_format(self, subgraph):
        """Converts subgraph data to the protobuf text format expected by the frontend."""
        nodes = subgraph.get('node', {})
        protobuf_format = ""
        for node_id, node_data in nodes.items():
            protobuf_format += f'node {{\n  name: "{node_id}"\n  op: "{node_data.get("id")}"\n'
            protobuf_format += f'  node_type: {node_data.get("node_type", 0)}\n'
            if node_data.get("matched_node_link"):
                protobuf_format += f'  matched_node_link: {node_data.get("matched_node_link")}\n'
            protobuf_format += f'  attr: "{node_data.get("data", "{}")}"\n'.replace('True', 'true').replace('False', 'false')
            protobuf_format += f'  precision_index: {(node_data.get("data", "{}").get("precision_index"))}\n'
            if node_data.get("input_data"):
                protobuf_format += f'  input_data: "{node_data.get("input_data", "{}")}"\n'
            if node_data.get("output_data"):
                protobuf_format += f'  output_data: "{node_data.get("output_data", "{}")}"\n'
            protobuf_format += f'  suggestions: "{node_data.get("suggestions", "{}")}"\n'
            if not node_data.get("subnodes"):
                protobuf_format += f'  isLeaf: true\n'
            else:
                protobuf_format += f'  isLeaf: false\n'
                protobuf_format += f'  subnodes: {node_data.get("subnodes")}\n'
            if node_data.get("stack_info"):
                protobuf_format += f'  stack_info: {node_data.get("stack_info")}\n'
            protobuf_format += '}\n'
        return protobuf_format

    def _get_run_dirs(self):
        """Scan logdir for directories containing .vis files, modified to return a tuple of (run, tag)."""
        run_tag_pairs = []
        for root, _, files in os.walk(self.logdir):
            for file in files:
                if file.endswith('.vis'):  # check for .vis extension
                    run = os.path.abspath(root)
                    tag = os.path.splitext(file)[0]  # Use the filename without extension as tag
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if file_size > constants.MAX_FILE_SIZE:
                        logger.error(f'Error: the vis file "{file_path}" exceeds the maximum limit size of 1GB and will be skipped.')
                        continue
                    run_tag_pairs.append((run, tag))
        return run_tag_pairs
    
    def _load_json_file(self, run_dir, tag):
        """Load a single .vis file from a given directory based on the tag."""
        file_path = os.path.join(run_dir, f"{tag}.vis")
        if os.path.exists(file_path):
            # Store the path of the current file instead of loading it into memory
            self._current_file_path = file_path
            return file_path
        return None

    def _read_json_file(self, file_path):
        """Read and parse a JSON file from disk."""
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except Exception as e:
                    logger.error(f'Error: the vis file "{file_path}" is not a legal JSON file!')
        else:
            logger.error(f'Error: the vis file "{file_path}" is not a legal JSON file!')
        return None
