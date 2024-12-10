import unittest
from unittest.mock import MagicMock
from plugin import GraphsPlugin  # 替换为实际的类名

class TestGraphsPlugin(unittest.TestCase):
    
    def setUp(self):
        """在每个测试之前初始化环境"""
        fake_context = MagicMock()
        
        # 创建 GraphsPlugin 实例并传递 context
        self.plugin = GraphsPlugin(context=fake_context) 
        self.plugin.batch_id = '-1'  # 设置为 -1 来触发 _process_subnode 中的判断逻辑
        self.plugin.step_id = '-1'   # 设置为 -1 来触发 _process_subnode 中的判断逻辑

        self.plugin._current_file_data = {
            "NPU": {
                "node": {
                    "npu_node_1": {
                        "matched_node_link": []
                    }
                }
            },
            "Bench": {
                "node": {
                    "bench_node_1": {
                        "matched_node_link": []
                    }
                }
            },
            "match": [],
            'task': 'md5'
        }
        
        # 模拟 json_get 方法
        # self.plugin.json_get = MagicMock(side_effect=self.mock_json_get)
        
    def test_get_all_nodeName_with_valid_batch_and_step(self):
        # 模拟 request.args
        mock_request = MagicMock()
        mock_request.args.get.return_value = '0'  # 模拟 batch=0 和 step=0
        
        # 构造 json_data
        json_data = {
            'NPU': {
                'root': 'root_node',
                'node': {
                    'root_node': {
                        'micro_step_id': 0,
                        'subnodes': ['subnode1', 'subnode2']
                    },
                    'subnode1': {'micro_step_id': 0},
                    'subnode2': {'micro_step_id': 0},
                }
            },
            'Bench': {
                'node': {
                    'bench1': {},
                    'bench2': {}
                }
            }
        }

        # 调用 get_all_nodeName 方法
        npu_ids, bench_ids = self.plugin.get_all_nodeName(json_data, mock_request)

        # 验证返回的 npu_ids 和 bench_ids
        self.assertEqual(npu_ids, ['subnode1', 'subnode2'])
        self.assertEqual(bench_ids, ['bench1', 'bench2'])

    def test_dfs_collect_nodes_with_valid_batch_and_step(self):
        # 模拟 request.args
        mock_request = MagicMock()
        mock_request.args.get.side_effect = lambda x: '0' if x == 'batch' else '0'  # 模拟 batch=0 和 step=1
        
        # 构造 json_data
        json_data = {
            'NPU': {
                'node': {
                    'node1': {'micro_step_id': 0, 'step_id': 0, 'subnodes': []},
                    'node2': {'micro_step_id': 0, 'step_id': 0, 'subnodes': []},
                    'node3': {'micro_step_id': 1, 'step_id': 1, 'subnodes': []},
                    'node4': {'micro_step_id': 0, 'step_id': 1, 'subnodes': ['subnode1']}
                }
            }
        }

        # 调用 dfs_collect_nodes 方法
        all_node_names = self.plugin.dfs_collect_nodes(json_data, mock_request)

        # 验证返回的 all_node_names
        self.assertEqual(all_node_names, ['node1', 'node2'])

    def test_group_precision_set_with_even_number_of_elements(self):
        # 测试正常的输入（偶数个元素）
        precision_set = [1, 2, 3, 4, 5, 6]
        expected_result = [[1, 2], [3, 4], [5, 6]]
        
        # 调用 group_precision_set 方法
        result = self.plugin.group_precision_set(precision_set)
        
        # 验证结果是否正确
        self.assertEqual(result, expected_result)

    def test_group_precision_set_with_odd_number_of_elements(self):
        # 测试输入长度为奇数的情况
        precision_set = [1, 2, 3]
        
        # 验证是否抛出 ValueError 异常
        with self.assertRaises(ValueError) as context:
            self.plugin.group_precision_set(precision_set)
        
        self.assertEqual(str(context.exception), 'The number of elements in precision_set is not even')

    def test_process_data_with_md5_mismatch(self):
        # 测试 md5 不匹配的情况
        data = []
        data_set = {
            'npu_keys': ['npu_key_1'],
            'bench_keys': ['bench_key_1'],
            'input_data': {'npu_key_1': [1, 2, 3], 'md5': 'abcd'},
            'output_data': {'bench_key_1': [1, 2, 3], 'md5': 'efgh'},
            'precision_index': 0,
            'file_path': 'test_path',
            'data_type': 'test_type',
        }
        NPU_node = 'test_node'

        # 调用方法
        result = self.plugin.process_data(data, data_set, NPU_node)

        # 验证结果
        self.assertEqual(result, 0)
        self.assertEqual(data_set['precision_index'], 0)

    def test_should_update_node_with_valid_batch_and_step(self):
        # 模拟 json_data 和 subnode_id_data
        subnode_id_data = {'micro_step_id': '-1', 'step_id': '-1', 'matched_node_link': ['N___subnode_1']}
        subgraph = {'node': {}}
        json_data = {
            'StepList': ['0', '1', '2']  # 测试 StepList 数据
        }
        
        prefix = 'N___'
        subnode_id = 'subnode_1'
        
        # 调用 _process_subnode 方法
        self.plugin._process_subnode(subgraph, prefix, subnode_id, subnode_id_data, json_data)
        
        # 验证 subnode_id 是否更新
        self.assertIn(prefix + subnode_id, subgraph['node'])
        self.assertEqual(subgraph['node'][prefix + subnode_id], subnode_id_data)

    def mock_json_get(self, *args):
        """ 模拟 json_get 方法，返回不同层级的数据 """
        if len(args) == 4 and args[1] == "node":
            # 返回节点的 matched_node_link 数据
            return self.plugin._current_file_data[args[0]][args[1]].get(args[2], {}).get('matched_node_link', [])
        return None

    def test_should_update_node_with_invalid_batch_or_step(self):
        # 测试 batch_id 和 step_id 为无效值时不会更新
        self.plugin.batch_id = '-1'
        self.plugin.step_id = '-1'
        
        subnode_id_data = {'micro_step_id': '1', 'step_id': '1', 'matched_node_link': []}
        subgraph = {'node': {}}
        json_data = {
            'StepList': ['0', '1', '2']
        }
        
        prefix = 'B___'
        subnode_id = 'subnode_1'
        
        # 调用 _process_subnode 方法
        self.plugin._process_subnode(subgraph, prefix, subnode_id, subnode_id_data, json_data)
        
        # 验证 subnode_id 是否被更新
        self.assertIn(prefix + subnode_id, subgraph['node'])
        self.assertEqual(subgraph['node'][prefix + subnode_id], subnode_id_data)
    
    def test_update_matched_node_links(self):
        subnode_id_data = {
            'matched_node_link': ['link_1', 'link_2']
        }
        prefix = 'B___'
        
        # 模拟常量 SETS
        constants = MagicMock()
        constants.SETS = {
            'test_prefix': ['', 'new_prefix']
        }
        
        # 调用 _update_matched_node_links 方法
        self.plugin._update_matched_node_links(subnode_id_data, prefix)
        
        # 验证 matched_node_link 是否被正确更新
        self.assertEqual(subnode_id_data['matched_node_link'], ['N___link_1', 'N___link_2'])
    
    def test_no_update_matched_node_links(self):
        subnode_id_data = {
            'matched_node_link': ['link_1', 'link_2']
        }
        prefix = 'N___'
        
        # 模拟常量 SETS
        constants = MagicMock()
        constants.SETS = {
            'Bench': ('Bench', 'B___', 'N___'),
            'NPU': ('NPU', 'N___', 'B___'),
            'B___': ('Bench', 'N___'),
            'N___': ('NPU', 'B___')
        }
        
        # 不更新第一个 matched_node_link
        subnode_id_data['matched_node_link'][0] = 'prefixlink_1'
        
        # 调用 _update_matched_node_links 方法
        self.plugin._update_matched_node_links(subnode_id_data, prefix)
        
        # 验证 linked node 是否正确更新
        self.assertEqual(subnode_id_data['matched_node_link'], ['B___prefixlink_1', 'B___link_2'])

    def test_info_route(self):
        # 模拟 request 对象
        mock_request = MagicMock()
        fake_context = MagicMock()
        
        # 创建 GraphsPlugin 实例并传递模拟的 request 对象
        self.plugin = GraphsPlugin(fake_context)
        
        # 模拟 info_impl 方法返回的信息
        self.plugin.info_impl = MagicMock(return_value={"status": "ok", "data": "some_info"})
        print(mock_request)
        # 调用 info_route 方法
        response = self.plugin.info_route(mock_request)
        
        # 验证返回的响应
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), '{"status": "ok", "data": "some_info"}')
        self.assertEqual(response.content_type, "application/json")

if __name__ == '__main__':
    unittest.main()
