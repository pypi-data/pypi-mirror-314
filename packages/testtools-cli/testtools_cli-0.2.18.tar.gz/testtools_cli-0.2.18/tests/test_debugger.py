import os
from subprocess import CompletedProcess
from unittest.mock import patch
from src.testtools_cli.debug.debugger import TestToolDebugger


@patch("subprocess.run")
@patch("shutil.which")
def test_debug(which_mock, process_run_mock):
    process_run_mock.return_value = CompletedProcess(
        args=[""], returncode=0, stdout="", stderr=""
    )
    which_mock.return_value = True
    TestToolDebugger(
        root=os.getcwd(), tool_path=os.getcwd(), target=["."]
    ).execute_test_case()
    if os.path.exists("testcontainer.yaml"):
        os.remove("testcontainer.yaml")
