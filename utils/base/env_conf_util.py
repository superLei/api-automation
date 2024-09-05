# -*- coding: UTF-8 -*-
import os
import yaml


API_TEST_ENV = "API_ENV"
API_TEST_SPECIFY_HOST_ENV = "API_TEST_HOST"
IAC_API_AZ_HOST = "IAC_AZ_NAME"


def get_envs():
    env = os.environ.get(API_TEST_ENV, "test")
    iac_az_name = os.environ.get(IAC_API_AZ_HOST, "")
    specify_host = os.environ.get(API_TEST_SPECIFY_HOST_ENV, "")
    return {"env": env, "iac_az_name": iac_az_name, "specify_host": specify_host}


def get_env_conf() -> dict:
    """choose online or offline config

    Returns:
        _type_: dict
    """
    env = os.environ.get(API_TEST_ENV, "test")
    env_path = f"./conf/env_{env}.yaml"
    with open(env_path, "rt", encoding="utf-8") as f:
        env_config = yaml.safe_load(f.read())
    return env_config


def get_db_config(project_name: str, db_label=None) -> str:
    env_config = get_env_conf()
    db_env = env_config["DB"]
    if db_label is None:
        result = db_env[project_name]["default"]
    else:
        result = db_env[project_name][db_label]
    return result


def get_host_ip_from_conf(service_env: str, service_host_ip_label: str) -> str:
    """
     1. TODO(暂时针对iac这样做,后面优化) 先读取iac_az_name来从uss中拿到iac master url
     2. 优先根据系统中的环境变量specify_service_host来设置来请求哪个host;
     3. 代码里面指定了service_env参数,则读取此标签对应的host;
     4. 如果以上都没设置,则读取默认的host.

    Args:
        service_env (str): yaml中定义的service标签
        service_host_ip_label (str): ip对应的key value

    Returns:
        str: host in url
    """
    env_config = get_env_conf()
    iac_az_name = os.environ.get(IAC_API_AZ_HOST, "")
    specify_service_host = os.environ.get(API_TEST_SPECIFY_HOST_ENV, "")
    service_dict = env_config["SERVICE"][service_host_ip_label]
    if iac_az_name:
        if service_dict.get(iac_az_name):
            host = env_config["SERVICE"][service_host_ip_label][iac_az_name]
        else:
            host = service_dict.get("default")
    elif specify_service_host:
        host = specify_service_host
    elif service_env:
        host = env_config["SERVICE"][service_host_ip_label][service_env]
    else:
        host = env_config["SERVICE"][service_host_ip_label]["default"]
    return host


if __name__ == "__main__":
    print(get_envs())
