import logging
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from loguru import logger
from rich.logging import RichHandler
from rich.traceback import install as traceback_install
from typing_extensions import Annotated

from testtools_cli.generator.scaffold_checker import ScaffoldChecker
from .generator.scaffold_generator import ScaffoldGenerator, LangType
from .install.installer import TestToolInstaller
from .debug.debugger import TestToolDebugger

traceback_install(show_locals=True)

FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

app = typer.Typer(rich_markup_mode="markdown")

log = logging.getLogger("rich")


@app.command()
def init(
    verbose: Annotated[Optional[bool], typer.Option(help="Verbose output")] = False,
    workdir: Annotated[
        Optional[str],
        typer.Option(
            help="Where you want the scaffolding code to be stored, defaulting to the current directory"
        ),
    ] = None,
) -> None:
    """
    **Init** a testsolar testtool with guide

    Current supported languages:

    - python

    - golang

    - javascript

    - java
    """
    if verbose:
        log.setLevel(logging.DEBUG)
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")

    tool_name = typer.prompt("Name of the test tool?")

    pre_langs = "/".join([e.value for e in LangType])
    lang = LangType(
        typer.prompt(f"The language you want to use for development({pre_langs})?")
    )

    assert tool_name

    gen = ScaffoldGenerator(lang=lang, testtool_name=tool_name, workdir=workdir)
    gen.generate()


@app.command()
def check(
    verbose: Annotated[Optional[bool], typer.Option(help="Verbose output")] = False,
    workdir: Annotated[
        Optional[str],
        typer.Option(
            help="The test tool dir to check, defaulting to the current directory"
        ),
    ] = None,
) -> None:
    """
    **Check** if the testing tools are effective

    - Check the validity of the testing tool metadata

    - Check the validity of the testing tool scripts
    """
    if verbose:
        log.setLevel(logging.DEBUG)
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")

    working_dir = Path(workdir) if workdir else Path.cwd()
    checker = ScaffoldChecker(working_dir)
    checker.check_test_tool()


@app.command()
def install(
    verbose: Annotated[Optional[bool], typer.Option(help="Verbose output")] = False,
) -> None:
    """
    **Install** install dependencies required for developing test tool

    installation tools include:

    - solarctl

    """
    if verbose:
        log.setLevel(logging.DEBUG)
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")

    TestToolInstaller().install()


@app.command()
def debug(
    verbose: Annotated[Optional[bool], typer.Option(help="Verbose output")] = False,
    target: Annotated[
        Optional[list[str]],
        typer.Option(
            help="list of test cases to execute, by default, execute all test cases in the test case library"
        ),
    ] = None,
    root: Annotated[
        Optional[str],
        typer.Option(
            "--case-root",
            help="the root directory of test cases, by default is the current directory",
        ),
    ] = None,
    tool: Annotated[
        Optional[str],
        typer.Option(
            help="the directory of the developed test tool, by default is the current directory"
        ),
    ] = None,
    commands: Annotated[
        Optional[list[str]],
        typer.Option(help="custom commands executed during the image building process"),
    ] = None,
) -> None:
    """
    **Debug** debug the developed test tool
    """
    if verbose:
        log.setLevel(logging.DEBUG)
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")

    TestToolDebugger(
        root=root or os.getcwd(),
        tool_path=tool or os.getcwd(),
        target=target or ["."],
        commands=commands or [],
    ).execute_test_case()


def cli_entry() -> None:
    app()


if __name__ == "__main__":
    app()
