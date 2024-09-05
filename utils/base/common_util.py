# -*- coding: UTF-8 -*-
import base64
from datetime import datetime, timedelta
import time
import uuid
from random import Random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

"""
__author__ = maxsulei
"""


class CommonUtil(object):
    @staticmethod
    def _get_time():
        """获取系统当前时间"""
        now_date = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        return now_date

    @staticmethod
    def _get_pre_time(days):
        """获取系统当前时间"""
        pre_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d%H%M%S")
        return pre_date

    @staticmethod
    def _get_uuid():
        """获取uuid,基于MAC地址,时间戳,随机数来生成唯一的uuid,可以保证全球范围内的唯一性."""
        return str(uuid.uuid1())

    @staticmethod
    def _get_random_id():
        num = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + str(
            Random().randint(10, 99)
        )
        return num

    @staticmethod
    def _get_short_id():
        num = time.strftime("%d%M%H", time.localtime(time.time())) + str(
            Random().randint(100, 999)
        )
        return num

    @staticmethod
    def dict_compare(d1, d2):
        """比较两个dict,比较差异

        Args:
            d1 (_type_): dict
            d2 (_type_): dict

        Returns:
            _type_: added->d2比d1增加的项, removed->d2比d1少的项
        """
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        shared_keys = d1_keys.intersection(d2_keys)
        added = d2_keys - d1_keys
        removed = d1_keys - d2_keys
        modified = {k: (d1[k], d2[k]) for k in shared_keys if d1[k] != d2[k]}
        same = set(k for k in shared_keys if d1[k] == d2[k])
        return added, removed, modified, same

    @staticmethod
    def base64_decode(s) -> str:
        content_bytes = base64.b64decode(str(s))
        content_str = content_bytes.decode("utf-8")
        return content_str

    @staticmethod
    def base64_encode(s: str) -> str:
        # 将字符串编码为Base64
        encoded_bytes = base64.b64encode(s.encode("utf-8"))
        # 将字节对象转换为字符串
        encoded_string = encoded_bytes.decode("utf-8")
        return encoded_string

    @staticmethod
    def time_difference(start_time: datetime, end_time: datetime) -> float:
        # 计算时间差
        time_difference = end_time - start_time
        return time_difference.total_seconds()

    @staticmethod
    def convert_file_to_dict(key_list: list, file_path: str) -> list:
        """将文件中的多行数据作为dict中的给定的key的value

        Args:
            key_list (list): 指定dict的key
            file_path (str): 对应key的value

        Returns:
            list: 由文件中的value和给定的key组合成的dict的集合
        """
        input_str_list = []
        with open(file_path, "r") as f:
            input_str_list = [line for line in f.readlines()]
        res_list = []
        for input_str in input_str_list:
            res_dict = {}
            input_list = input_str.split(" ")
            try:
                input_list.remove("")
            except:
                pass
            if len(input_list) < 1 and len(key_list) != len(input_list):
                continue
            for i in range(len(key_list)):
                res_dict[key_list[i]] = input_list[i].replace("\n", "")
            res_list.append(res_dict)
        return res_list

    @staticmethod
    def fill_none_to_dict_value(lst: list) -> list:
        res_list = []
        for item in lst:
            for k in item.keys():
                copyed_item = item.copy()
                copyed_item[k] = None  # type: ignore
                res_list.append(copyed_item)
        return res_list


def generate_key(password):
    # 生成随机的盐值
    salt = b"\x8d\x19\x8f\x9e\x93\x8a\x88\x8b"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


class AesUtil:

    @staticmethod
    def encrypt(message, password):
        key = generate_key(password)
        if key is None:
            return None

        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(message.encode())
        return cipher_text

    @staticmethod
    def decrypt(cipher_text, password):
        key = generate_key(password)
        if key is None:
            return None

        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(cipher_text)
        return plain_text.decode()


if __name__ == "__main__":
    file_path = "testcase/iac/test_scripts/tmp"
    param_list = ["service_tag", "ip_lan"]
    res = CommonUtil.convert_file_to_dict(key_list=param_list, file_path=file_path)
    res = CommonUtil.fill_none_to_dict_value(lst=res)
    print(res)
