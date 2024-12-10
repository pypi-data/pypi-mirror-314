import tempfile
from pathlib import Path

from src.load import collect_testcases_from_args
from testsolar_testtool_sdk.file_reader import read_file_load_result

testdata_dir: Path = Path(__file__).parent.absolute().joinpath("testdata")


def test_collect_testcases_from_args():
    with tempfile.TemporaryDirectory() as tmpdir:
        report_file = Path(tmpdir) / "result.json"
        collect_testcases_from_args(
            args=["load.py", Path.joinpath(Path(testdata_dir), "entry.json")],
            workspace=(testdata_dir / "cases").as_posix(),
            file_report_path=report_file.as_posix(),
        )

        re = read_file_load_result(report_file)

        assert len(re.Tests) == 1

        assert re.Tests[0].Name == "a/b/c?d"

        assert len(re.LoadErrors) == 1
        assert re.LoadErrors[0].name == "load xxx.py failed"
        assert re.LoadErrors[0].message == "backtrace here"
