import logging
import os
from pathlib import Path
from typing import Optional, Tuple

from pydantic import BaseModel

from solar_registry.service.testtool import get_testtool_by_file_path

log = logging.getLogger("rich")


class LeftToDos(BaseModel):
    file: Path
    line: int
    content: str


class ScaffoldChecker:
    def __init__(self, workdir: Optional[Path] = None):
        self.workdir = workdir or Path.cwd()

    def check_test_tool(self) -> None:
        """
        检查文件中的TODO，并输出到控制台提示用户还有多少个需要
        """
        self.check_test_tool_yaml()
        self.show_todos()

    def check_test_tool_yaml(self) -> None:
        yaml_file = Path(self.workdir / "testtool.yaml")
        log.info(f"Checking testtool yaml file: {yaml_file}")
        get_testtool_by_file_path(yaml_file)

    def show_todos(self) -> None:
        todos: list[LeftToDos] = []
        recommand_todos: list[LeftToDos] = []
        for dirpath, dirnames, filenames in os.walk(self.workdir):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]

            # 检查filenames里面有没有TODO
            for filename in filenames:
                file_to_check = Path(dirpath) / filename
                file_todos, file_recommand_todos = self._get_todos(file_to_check)
                todos.extend(file_todos)
                recommand_todos.extend(file_recommand_todos)

        if todos:
            log.error(
                f"You still have {len(todos)} TODOs.Please fix these todos below:"
            )
            for todo in todos:
                log.error(f"  {todo.file}:{todo.line}:\t\t{todo.content}")
        if recommand_todos:
            log.warning(
                f"You still have {len(recommand_todos)} RECOMMANDED TODOs.We suggest you fix these todos below:"
            )
            for todo in recommand_todos:
                log.warning(f"  {todo.file}:{todo.line}:\t\t{todo.content}")
        if not todos and not recommand_todos:
            log.info("✅ No Problem found.")

    @staticmethod
    def _get_todos(file_to_check: Path) -> Tuple[list[LeftToDos], list[LeftToDos]]:
        if file_to_check.name.startswith("."):
            return ([], [])

        todo: list[LeftToDos] = []
        recommand_todo: list[LeftToDos] = []
        # noinspection PyBroadException
        try:
            content = file_to_check.read_text(encoding="utf-8")
            for i, line_content in enumerate(content.splitlines()):
                if "__TODO__" in line_content:
                    todo.append(
                        LeftToDos(file=file_to_check, line=i + 1, content=line_content)
                    )
                if "__RECOMMANDTODO__" in line_content:
                    recommand_todo.append(
                        LeftToDos(file=file_to_check, line=i + 1, content=line_content)
                    )
            return (todo, recommand_todo)
        except Exception:
            return ([], [])
