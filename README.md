# Api-Test

## 项目介绍

本项目主要是针对http协议的接口测试, 支持导入postman,swagger2,curl接口数据并自动生成测试代码, 支持多环境数据管理等功能.

### 目录结构

```angular2html
.
├── conf
│   ├── env_live.yaml
│   └── env_test.yaml
├── main.py
├── testcase
│   ├── conftest.py
│   └── toc
│       ├── serverapi
│       ├── toc_auth
│       └── toc_sql
├── testdata
│   └── toc
│       ├── api_info.yaml
│       └── tool.yaml
└── utils
    ├── base
    │   ├── env_conf_util.py
    │   ├── http_util.py
    │   └── mysql_handler.py
    └── business
        └── path_util.py
```

## 依赖安装

``` shell
# 安装poetry
curl -sSL https://install.python-poetry.org | python3 -
# 安装项目依赖
poetry install
# 添加项目依赖
poetry add xxx
# update package
poetry update
```

## 代码自动生成

1. 安装cli工具`pip3 install gentccode`
2. 将(一个或多个)接口的curl命令复制到`curls.txt`文件中
3. 运行下面命令后,会在当前目录下生成测试代码和yaml格式的接口信息

``` bash
gtc curl curl.txt -a res.code=0
gtc postman path/postman.json
gtc swagger2 path/swagger.json
==============================
gtc --help
```
