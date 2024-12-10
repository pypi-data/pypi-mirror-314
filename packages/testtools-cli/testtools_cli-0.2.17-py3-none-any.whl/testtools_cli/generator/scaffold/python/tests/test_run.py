import tempfile
from pathlib import Path

from src.run import run_testcases_from_args
from testsolar_testtool_sdk.file_reader import read_file_test_result
from testsolar_testtool_sdk.model.test import TestCase
from testsolar_testtool_sdk.model.testresult import ResultType, LogLevel

testdata_dir: str = str(Path(__file__).parent.absolute().joinpath("testdata"))


def test_run_testcases_from_args():
    with tempfile.TemporaryDirectory() as tmpdir:
        run_testcases_from_args(
            args=["run.py", Path.joinpath(Path(testdata_dir), "entry.json")],
            workspace=testdata_dir,
            file_report_path=tmpdir,
        )

        re = read_file_test_result(
            report_path=Path(tmpdir),
            case=TestCase(Name="a/b/c?d"),
        )
        assert re.Test.Name == "a/b/c?d"
        assert re.ResultType == ResultType.SUCCEED
        assert re.StartTime
        assert re.EndTime
        assert len(re.Steps) == 1
        assert re.Steps[0].ResultType == ResultType.SUCCEED
        assert re.Steps[0].Title == "a/b/c?d"
        assert len(re.Steps[0].Logs) == 1
        assert re.Steps[0].Logs[0].Level == LogLevel.INFO
        assert re.Steps[0].Logs[0].Content == "Test Output"
