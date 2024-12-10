import os
import yaml
import shutil
from .model import Build, TestContainer, TestTool
from .util import execute_command_in_directory, get_absolute_path

SOLARCTL_RUN = ["solarctl", "run", "--debug", "--root", "--remove", "-c"]


class TestToolDebugger:
    def __init__(
        self, root: str, tool_path: str, target: list[str], commands: list[str] = []
    ):
        self._root = get_absolute_path(root)
        self._tool_path = get_absolute_path(tool_path)
        self._target = target
        self._cmd = commands

    def execute_test_case(self) -> None:
        if not self._validate_execute_conditions():
            raise Exception("❌ solarctl is not installed")
        return_code = execute_command_in_directory(
            SOLARCTL_RUN + [self._generate_testcontainer_yaml()],
            self._root,
            self._get_targets_param(),
        )
        if return_code != 0:
            raise Exception(f"❌ solarctl failed to run, return code: {return_code}")

    def _get_targets_param(self) -> list[str]:
        args: list[str] = []
        for t in self._target:
            args.append("-t")
            args.append(t)
        return args

    def _generate_testcontainer_yaml(self) -> str:
        test_container = TestContainer(testTool=TestTool(use=self._tool_path))
        if self._cmd:
            test_container.build = Build(commands=self._cmd)
        d = test_container.dict(by_alias=True, exclude_none=True)
        yaml_path = os.path.join(self._root, "testcontainer.yaml")
        with open(yaml_path, "w") as f:
            yaml.dump(d, f, default_flow_style=False)
        return yaml_path

    def _validate_execute_conditions(self) -> bool:
        return bool(shutil.which("solarctl")) and os.path.exists(self._root)
