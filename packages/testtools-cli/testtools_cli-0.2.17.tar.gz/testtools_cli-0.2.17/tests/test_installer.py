from requests import Response
from unittest.mock import patch
from src.testtools_cli.install.installer import TestToolInstaller


def generate_tool(fsrc, fdst):
    fdst.write("testtool")


@patch("shutil.copyfileobj", side_effect=generate_tool)
@patch("requests.get")
def test_install(get_mock, copyfileobj_mock):
    mock_rsp = Response()
    mock_rsp.status_code = 200
    mock_rsp.raw = ""
    get_mock.return_value = mock_rsp
    TestToolInstaller().install()
