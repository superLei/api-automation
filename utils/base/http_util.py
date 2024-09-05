# -*- coding: UTF-8 -*-
import json
import logging

import requests
from requests.exceptions import MissingSchema, InvalidURL, ConnectionError
from utils.base.req_data import ReqData
from utils.base.env_conf_util import get_host_ip_from_conf

"""
__author__ = maxsulei
"""


class ReqHandler:
    def __init__(self, rev_url, rev_method="get"):
        self.__url = rev_url
        self.__method = rev_method.lower()
        self.with_session = requests.session()

    def request(self, session=False, *args, **kwargs):
        CONNECTION_ERROR_MSG = (
            "Please check the network connectivity and api response time"
        )
        if session:
            session_obj = self.with_session
        else:
            session_obj = requests

        try:
            if self.__method == "get":
                return session_obj.get(self.__url, *args, **kwargs)
            elif self.__method == "post":
                return session_obj.post(self.__url, *args, **kwargs)
            elif self.__method == "put":
                return session_obj.put(self.__url, *args, **kwargs)
            elif self.__method == "delete":
                return session_obj.delete(self.__url, **kwargs)
            elif self.__method == "head":
                return session_obj.head(self.__url, **kwargs)
            elif self.__method == "options":
                return session_obj.options(self.__url, **kwargs)
            else:
                raise ValueError(f"check method={self.__method} is correct")
        except (MissingSchema, InvalidURL):
            logging.exception(f"check url={self.__url}is correct")
        except ConnectionError:
            logging.exception(CONNECTION_ERROR_MSG)


class ParseResponse:
    def __init__(self, rev_resp):
        self.__resp = rev_resp

    @property
    def url(self):
        return self.__resp.url

    @property
    def status_code(self):
        return self.__resp.status_code

    @property
    def headers(self):
        return self.__resp.headers

    @property
    def str_content(self):
        return self.__resp.content

    def dict_content(self):
        try:
            return self.__resp.json()
        except:
            logging.error("the response data's type is not json")
            return self.__resp.content

    @property
    def text(self):
        return self.__resp.text

    @property
    def cookies(self):
        cookies_str = ""
        for cookie in self.__resp.cookies:
            cookies_str += f"{cookie.name}={cookie.value};"
        return cookies_str if cookies_str else self.__resp.cookies


def send_http_request(req_content: ReqData, *args, **kwargs) -> ParseResponse:
    """
    发送 HTTP 请求并获取响应。

    Args:
        req_content: 请求数据对象。
        *args: 可变位置参数。
        **kwargs: 可变关键字参数。

    Returns:
        ParseResponse: 响应数据对象。
    """
    body = req_content.body
    header = req_content.header
    # if user don't specify the Content-Type field, the default value is 'application/json'
    if 'files' not in kwargs:
        if not header.get("Content-Type"):
            header.setdefault("Content-Type", "application/json")
        if "json" in header["Content-Type"]:
            body = json.dumps(body)
    req_content = handle_param_path(req_content)
    logging.info(
        "|request info| => [url]: %s $$ [method]: %s $$ [header]: %s $$ [body]: %s $$ [query_params]: %s \n",
        req_content.url,
        req_content.method,
        json.dumps(header),
        body,
        json.dumps(req_content.query_param),
    )
    req_handler = ReqHandler(req_content.url, req_content.method)
    response = req_handler.request(
        session=True,
        params=req_content.query_param,
        data=body,
        headers=header,
        verify=False,
        *args,
        **kwargs,
    )

    res_model = ParseResponse(response)
    if isinstance(res_model.dict_content(), dict):
        content = json.dumps(res_model.dict_content())
    else:
        content = res_model.dict_content()
    logging.info(f"|response info|[http.code={res_model.status_code}] => {content} \n")
    return res_model


def handle_param_path(req_model: ReqData) -> ReqData:
    """
    替换请求路径中的参数占位符。like '/api/get/{id}' => '/api/get/3'
    本function主要是处理swagger中定义的url
    Args:
        req_content: 请求数据对象。

    Returns:
        ReqData: 替换参数后的请求数据对象。
    """
    if "{" in req_model.path:
        url_sub_paths = req_model.path.split("/")
        for i, sub_path in enumerate(url_sub_paths):
            if "{" in sub_path:
                url_sub_paths[i] = str(
                    req_model.path_param.get(
                        sub_path.replace("{", "").replace("}", ""), ""
                    )
                )
        req_model.path = "/".join(url_sub_paths)
    return req_model


class HttpUtil(object):
    @staticmethod
    def request(req_content: ReqData, *args, **kwargs):
        res_analysis = send_http_request(req_content, *args, **kwargs)
        return res_analysis

    @staticmethod
    def request_with_yaml(
        req_content: ReqData,
        service_host_ip_label="",
        service_env="",
        url="",
        *args,
        **kwargs,
    ) -> dict:
        """
        使用配置文件中的环境信息发送 HTTP 请求并获取响应。

        Args:
            req_content: 请求数据对象。
            service_host_ip_label: 服务主机标签。
            service_env: 服务环境名称。
            *args: 可变位置参数。
            **kwargs: 可变关键字参数。

        Returns:
            dict: 响应数据字典。
        """
        if url:
            req_content.host = url
        else:
            req_content.host = get_host_ip_from_conf(
                service_env=service_env, service_host_ip_label=service_host_ip_label
            )
        # 检查并添加斜杠
        if not req_content.host.endswith("/"):
            req_content.host += "/"
        res_model = send_http_request(req_content, *args, **kwargs)
        # assert res_model.status_code == 200, 'http status code is error'
        return res_model.dict_content()


if __name__ == "__main__":
    reqs = ReqData()
    reqs.path = "/api/get/{id}"
    reqs.path_param = {"id": 3}
    r = handle_param_path(req_model=reqs)
    print(r.path)
