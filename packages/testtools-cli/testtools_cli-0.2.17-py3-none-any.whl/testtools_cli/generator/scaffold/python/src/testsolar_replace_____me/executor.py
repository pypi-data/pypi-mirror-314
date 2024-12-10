from datetime import datetime
from pathlib import Path
from time import sleep
from typing import List

from loguru import logger
from testsolar_testtool_sdk.model.param import EntryParam
from testsolar_testtool_sdk.model.test import TestCase
from testsolar_testtool_sdk.model.testresult import (
    TestResult,
    ResultType,
    TestCaseStep,
    TestCaseLog,
    LogLevel,
)
from testsolar_testtool_sdk.reporter import FileReporter


def run_testcases(entry: EntryParam) -> None:
    reporter = FileReporter(Path(entry.FileReportPath))

    logger.info(f"running testcase in workdir [{entry.ProjectPath}]")

    cases = [TestCase(Name="a/b/c?d")]

    for case in cases:
        run_single_case(case, reporter)


def run_single_case(case: TestCase, reporter: FileReporter) -> None:
    logger.info(f"Running case {case.Name}")
    # 1. (optional) report the running status before executing the test cases.
    start_time = datetime.now()
    tr = TestResult(
        Test=case,
        StartTime=start_time,
        ResultType=ResultType.RUNNING,
        Message="",
    )
    reporter.report_case_result(tr)
    # 2. __TODO__: execute test cases based on `entry_param`
    # The following are the parameters that need attention:
	#   entry_param.TestSelectors: expected list of test cases to execute, possibly with multiple inputs
    #   example:
    #     - tests                                 // expected test case directory to be executed
    #     - tests/test_hello.py                   // expected test case file to be executed
    #     - tests/test_hello.py?name=MathTest     // expected test case to be executed
    #     - tests/test_hello.py?MathTest/test_add // equivalent to the previous example, the 'name' parameter can be omitted
    #   entry_param.ProjectPath: test cases root directory, example: /data/workspace
	#   entry_param.TaskId: task id, as the unique identifier for this task, example: task-xxx
	#   entry_param.FileReportPath: local test case result save file path, example: /data/report
    sleep(1)
    
    # 3. __TODO__: After test cases had been executed, construct the test case results and report.
    # TestResult: test case execution result
    #     Test: test case name
    #           Name: name of testcase, example: tests/test_hello.py?MathTest/test_add
    #           Attributes: test case attributes, represented in key-value pair form
    #     StartTime: test case start time
    #     EndTime: test case end time
    #     ResultType: execution result of the test case
    #     TestCaseStep: execution steps of the test case, 
    #                   one test case result can contain multiple steps, 
    #                   and each step can contain multiple logs
    #                   Title: step name
    #                   Steps: test case logs in current step
    #                   [
    #                       TestCaseStep: single test case log
    #                           Time: record time   
    #                           Level: log level
    #                           Content: log content                 
    #                   ]
    #                   StartTime: step start time
    #                   EndTime: step end time
    #                   ResultType: step result
    step_logs: List[TestCaseLog] = [
        TestCaseLog(Time=datetime.now(), Level=LogLevel.INFO, Content="Test Output")
    ]

    logger.info(f"Finished running case {case.Name}")

    tr_result: ResultType = ResultType.SUCCEED
    tr.ResultType = tr_result
    tr.Steps.append(
        TestCaseStep(
            Title=case.Name,
            StartTime=start_time,
            ResultType=tr_result,
            EndTime=datetime.now(),
            Logs=step_logs,
        )
    )
    tr.EndTime = datetime.now()
    reporter.report_case_result(tr)
