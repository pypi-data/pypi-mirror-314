import traceback
import logging
import platform
from .util import download_files_concurrently, get_cpu_architecture, get_os_type
from testtools_cli.conf import settings

log = logging.getLogger("rich")


class TestToolInstaller:
    def __init__(self) -> None:
        self._os = get_os_type()
        if self._os == "":
            raise Exception(f"Unsupported OS [{platform.system()}]")
        self._arch = get_cpu_architecture()
        if self._arch == "":
            raise Exception(f"Unsupported architecture [{platform.architecture()}]")
        self._os_arch = f"{self._os}-{self._arch}"

    def install(self) -> None:
        url_list: list[str] = []
        for tool in settings.tool_list:
            filename = self._get_tool_file_name(tool.tool_name, self._os)
            url_list.append(
                f"{settings.tool_download_domain}/cli/{tool.tool_name}/{tool.version}/{self._os_arch}/{filename}",
            )
        try:
            download_files_concurrently(url_list)
        except Exception:
            log.error(f"❌ Download tool failed:\n{traceback.format_exc()}")
        else:
            log.info("✨ Download tool completed")

    def _get_tool_file_name(self, tool: str, os: str) -> str:
        if os == "windows":
            return f"{tool}.exe"
        else:
            return tool
