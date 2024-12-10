import time
from pathlib import Path

from loguru import logger
from testsolar_testtool_sdk.model.load import LoadResult, LoadError
from testsolar_testtool_sdk.model.param import EntryParam
from testsolar_testtool_sdk.model.test import TestCase
from testsolar_testtool_sdk.reporter import FileReporter


def collect_testcases(entry_param: EntryParam) -> None:
    logger.info(f"loading testcase from workdir [{entry_param.ProjectPath}]")
    load_result: LoadResult = LoadResult(
        Tests=[],
        LoadErrors=[],
    )
    # 1. __TODO__: load test cases based on `entry_param`
    # The following are the parameters that need attention:
	#   entry_param.TestSelectors: expected list of test cases to load, possibly with multiple inputs
    #   example:
    #     - tests                                 // expected test case directory to be loaded
    #     - tests/test_hello.py                   // expected test case file to be loaded
    #     - tests/test_hello.py?name=MathTest     // expected test case to be loaded
    #     - tests/test_hello.py?MathTest/test_add // equivalent to the previous example, the 'name' parameter can be omitted
    #   entry_param.ProjectPath: test cases root directory, example: /data/workspace
	#   entry_param.TaskId: task id, as the unique identifier for this task, example: task-xxx
	#   entry_param.FileReportPath: local test case result save file path, example: /data/report
    time.sleep(1)
    
    # 2. __TODO__: after loading the test cases, report the results.
    # successfully loaded test cases can be added to load_result.Tests
	# and failed test cases can be added to load_result.LoadErrors
    # Tests: 
    #   [
    #        TestCase: single test case
    #           Name: test case name, example: tests/test_hello.py?MathTest/test_add
    #           Attributes: test case attributes, represented in key-value pair form
    #   ]
    # LoadErrors:
    #   [
    #       LoadError: single load error
    #           name: load error name, example: tests/test_hello.py or tests/test_hello.py?LoadErrorTest
    #           message: load error message
    #   ]
    load_result.Tests.append(TestCase(Name="a/b/c?d"))
    load_result.LoadErrors.append(
        LoadError(name="load xxx.py failed", message="backtrace here")
    )
    reporter = FileReporter(report_path=Path(entry_param.FileReportPath))
    reporter.report_load_result(load_result)
