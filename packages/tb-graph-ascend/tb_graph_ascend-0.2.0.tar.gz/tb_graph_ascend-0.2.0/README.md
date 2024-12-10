# tb-graph-ascend

### 介绍

模型分级可视化代码

### python 依赖说明

```
python >= 3.7
tensorboard >= 2.11.2
numpy <= 1.26.3
```

### 打包教程

1.  进入前端工程，安装依赖

```
cd fe/
npm install
```

2.  打包前端项目

```
npm run build
```

3.  前端打包完成后，进入项目根目录，打包 whl 包

```
python setup.py bdist_wheel
```
