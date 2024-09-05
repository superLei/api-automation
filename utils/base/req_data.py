# -*- coding: UTF-8 -*-

"""
__author__ = maxsulei
"""


class ReqData(object):
    __slots__ = [
        "__path",
        "__method",
        "__body",
        "__header",
        "__query_param",
        "__path_param",
        "__original_url",
        "__temp_api_label",
        "__host",
        "__response",
    ]

    def __init__(self, dd: dict = None):  # type: ignore
        self.__host = ""
        self.__path = ""
        self.__method = ""
        self.__body = {}
        self.__header = {}
        self.__query_param = {}
        self.__path_param = {}
        self.__original_url = ""
        self.__temp_api_label = ""
        self.__response = {}

        if dd:
            self.update(dd)

    def update(self, dd: dict):
        for key, value in dd.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def temp_api_label(self) -> str:
        return self.__temp_api_label

    @temp_api_label.setter
    def temp_api_label(self, value: str):
        self.__temp_api_label = value

    @property
    def url(self) -> str:
        return self.__host + self.__path

    @property
    def original_url(self) -> str:
        return self.__original_url

    @original_url.setter
    def original_url(self, value: str):
        self.__original_url = value

    @property
    def method(self) -> str:
        return self.__method

    @method.setter
    def method(self, value: str):
        self.__method = value

    @property
    def body(self) -> dict:
        return self.__body

    @body.setter
    def body(self, value: dict):
        self.__body = value

    @property
    def header(self) -> dict:
        return self.__header

    @header.setter
    def header(self, value: dict):
        self.__header = value

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, value: str):
        self.__host = value

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value

    @property
    def query_param(self) -> dict:
        return self.__query_param

    @query_param.setter
    def query_param(self, value: dict):
        self.__query_param = value

    @property
    def path_param(self) -> dict:
        return self.__path_param

    @path_param.setter
    def path_param(self, value: dict):
        self.__path_param = value

    @property
    def response(self) -> dict:
        return self.__response

    @response.setter
    def response(self, value: dict):
        self.__response = value


if __name__ == "__main__":
    req = ReqData()
    print(req.body)
    dd = {"path": "123"}
    req2 = ReqData(dd)
    print(req2.path)
