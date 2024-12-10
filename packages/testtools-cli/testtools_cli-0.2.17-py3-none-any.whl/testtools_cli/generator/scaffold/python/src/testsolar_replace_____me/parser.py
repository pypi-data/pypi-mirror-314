from pathlib import Path
from typing import List
from loguru import logger

from testsolar_testtool_sdk.model.test import TestCase


def parse_testcase(workdir: Path, test_selectors: List[str]) -> List[TestCase]:
    """
    对apdtest用例进行解析并过滤

    :param workdir: 用例数据文件
    :param test_selectors: 用户选择用例选择器
    :return: 过滤后的用例列表
    """

    logger.debug(f"parsing workdir [{workdir}], test_selectors={test_selectors}")
    return [TestCase(Name="a/b/c?d")]
