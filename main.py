# -*- coding: UTF-8 -*-
import argparse
import logging
import os
import logging.config
import pytest
import yaml

from utils.base.env_conf_util import IAC_API_AZ_HOST
from utils.business.iac_uss import merge_env_conf_file


LOGGING_CONFIG_PATH = "logging.yaml"
DEFAULT_REPORT_PATH = "report"
DEFAULT_CASE_PATH = "testcase"


def setup_logging(logging_config_path=LOGGING_CONFIG_PATH, default_level=logging.INFO):
    """
    设置日志记录配置。

    Args:
        logging_config_path: 日志配置文件路径。
        default_level: 默认日志级别。
    """
    if os.path.exists(logging_config_path):
        with open(logging_config_path, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def init_report_files(project_report):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    report_dir = "report"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir, exist_ok=True)

    project_report_dir = f"report/{project_report}"
    if not os.path.exists(project_report_dir):
        os.makedirs(project_report_dir, exist_ok=True)


def exec_pytest():
    """
    解析命令行参数并执行相应操作。
    """
    parser = argparse.ArgumentParser(description="Process mark name.")
    parser.add_argument(
        "--name", default="toc", required=True, help="Name of the project."
    )
    parser.add_argument("--junitxml", help="Path to store JUnit XML report.")
    parser.add_argument("--junit_suite_name", help="Name of the JUnit test suite.")
    parser.add_argument(
        "--junit_prefix", help="Prefix for test case names in JUnit report."
    )
    parser.add_argument("--mark", help="Pytest marker.")
    parser.add_argument("--allure_story", help="allure story")
    parser.add_argument("--allure_feature", help="allure feature")
    parser.add_argument("--reruns", help="rerun times for failcases")
    parser.add_argument("--cookie", help="cookie")

    args = parser.parse_args()
    report_path = os.path.join(DEFAULT_REPORT_PATH, args.name)
    case_path = os.path.join(DEFAULT_CASE_PATH, args.name)

    pytest_args = [
        case_path,
    ]
    pytest_args.extend(
        [
            f"--alluredir={report_path}",
        ]
    )
    if args.junitxml:
        pytest_args.append(f"--junitxml={args.junitxml}")

    if args.junit_suite_name:
        # override pytest.ini
        pytest_args.extend(["-o", f"junit_suite_name={args.junit_suite_name}"])

    if args.junit_prefix:
        pytest_args.append(f"--junit-prefix={args.junit_prefix}")

    if args.mark:
        pytest_args.extend(["-m", args.mark])

    if args.allure_story:
        pytest_args.append(f"--allure-story={args.allure_story}")

    if args.allure_feature:
        pytest_args.append(f"--allure-feature={args.allure_feature}")

    if args.reruns:
        pytest_args.append(f"--reruns={args.reruns}")

    if args.cookie:
        pytest_args.append(f"--cookie={args.cookie}")

    init_report_files(project_report=args.name)

    # setup_logging()

    # detail for https://docs.pytest.org/en/latest/reference/reference.html#command-line-flags
    pytest.main([arg for arg in pytest_args])


def prepare_iac_tasks():
    iac_az_name = os.environ.get(IAC_API_AZ_HOST, "")
    if iac_az_name:
        merge_env_conf_file()


if __name__ == "__main__":
    prepare_iac_tasks()
    exec_pytest()
