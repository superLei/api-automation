import json
import pytest

from utils.base.mysql_handler import MysqlHandler
from utils.base.env_conf_util import get_db_config
from utils.base.http_util import HttpUtil
from utils.base.parse import ParseUtil
from utils.business.path_util import PathUtil


@pytest.mark.skip()
class TestDemo(object):
    def setup_class(self):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        self.header_auth = {
            "Authorization": "ApiToken eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0b2MiLCJpYXQiOjE2NjUzOTEzMDksImp0aSI6Im9HN3dicFJjREVvMFlIMjdqM3RtTHBvU1lWemNzNDFkIiwidWlkIjoxMDAwMDIxLCJleHAiOjQ4MTg5OTEzMDl9.YzWb2aSZ_CO2HNBgAq2H_jBPzdkiONx-EbHUXecSzfs"
        }
        self.toc_yaml_path = PathUtil.get_toc_api_v1_yaml_path()

    def test_case_with_yaml(self):
        # 读取yaml数据,并组装请求参数
        yaml_data = ParseUtil.parse_api_info_from_yaml(self.toc_yaml_path)
        # 获取封装后请求参数实体
        request_data = yaml_data["api_v1_server_tag-vars_3_post"]
        # 添加新的header字段
        # request_data.header.update(header_auth)
        request_data.header = self.header_auth
        # 发送请求
        response = HttpUtil.request_with_yaml(request_data, service_host_ip_label="toc")
        # check result
        assert response["error"] != 0
        assert "TagVarsCreate" in response["error_msg"]

    # ----------------------------------------------
    # db 操作
    def test_db_operator(self):
        db_conf = get_db_config(project_name="autoscaler")
        mysql_handler = MysqlHandler(db_conf)
        sql = "SELECT id, project, module, env, cid, idc, mattermost_webhook, spec, full_project_name, state, project_name, created_at, updated_at FROM service_info_tab WHERE project='autoscaler' AND module='mockserver' AND env='test' AND cid='sg' AND idc='sg2'"
        data = mysql_handler.query(sql_exp=sql)
        data[0]["spec"] = json.loads(data[0]["spec"])  # type: ignore
        data = json.dumps(data)

    # ----------------------------------------------
    # 控制用例依赖关系
    @pytest.mark.dependency()
    @pytest.mark.xfail(reason="deliberate fail")
    def test_a():
        assert False

    @pytest.mark.dependency()
    def test_b():
        pass

    @pytest.mark.dependency(depends=["test_a"])
    def test_c():
        pass

    @pytest.mark.dependency(depends=["test_b"])
    def test_d():
        pass

    @pytest.mark.dependency(depends=["test_b", "test_c"])
    def test_e():
        pass

    # ----------------------------------------------
