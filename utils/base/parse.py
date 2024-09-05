# -*- coding: UTF-8 -*-
from typing import Dict
from utils.base.req_data import ReqData
import yaml
import json
import logging


class ParseUtil(object):

    @staticmethod
    def parse_api_info_from_yaml(yaml_file_path: str) -> Dict[str, ReqData]:
        result = {}
        """读取yaml格式的http请求数据"""
        with open(yaml_file_path, "rt") as f:
            try:
                cases = yaml.safe_load(f)
            except Exception as ex:
                logging.exception("read yaml error: " + yaml_file_path)
                raise ex

        for key, case in cases.items():
            req_data = ReqData()
            req_data.path = case.get("path")
            req_data.method = case.get("method")
            if not req_data.path or not req_data.method:
                logging.error("the url path or method is null in yaml file")
                continue

            req_data.path_param = case.get("path_param", {})
            if isinstance(req_data.path_param, str):
                req_data.path_param = json.loads(case.get("path_param", "{}"))

            req_data.body = case.get("body", {})
            if isinstance(req_data.body, str):
                req_data.body = json.loads(case.get("body", "{}"))

            req_data.header = case.get("header", {})
            if isinstance(req_data.header, str):
                req_data.header = json.loads(case.get("header", "{}"))

            # only when request method is get, there will include params field
            if req_data.method.lower() == "get":
                req_data.query_param = case.get("query_param", {})
                if isinstance(req_data.query_param, str):
                    req_data.query_param = json.loads(case.get("query_param", "{}"))

            req_data.original_url = case.get("original_url", "")
            result[key] = req_data

        return result
