import os
import stat
import logging
import requests
import shutil
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

log = logging.getLogger("rich")


def get_system_path() -> str:
    if platform.system() == "Windows":
        system_path = os.path.join(os.getenv("SYSTEMROOT", "C:\\Windows"), "System32")
    else:
        system_path = "/usr/local/bin"
    return system_path


def download_file(url: str, file_path: str) -> None:
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
    else:
        raise Exception(f"Failed to download file: {response.status_code}")


def set_file_to_executable_on_unix(file_path: str) -> None:
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)
    log.debug(f"File permissions set to executable for {file_path}")


def download_and_make_executable(url: str) -> None:
    file_path = os.path.join(get_system_path(), os.path.basename(url))
    log.debug(f"Download tool from {url} to {file_path}")
    log.info(f"⏳ Downloading tool [{os.path.basename(url)}]...")
    download_file(url, file_path)
    log.info(f"✅ Download tool [{os.path.basename(url)}] successfully")
    if platform.system() != "Windows":
        set_file_to_executable_on_unix(file_path)


def download_files_concurrently(url_list: list[str]) -> None:
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_file = {
            executor.submit(download_and_make_executable, url): url for url in url_list
        }
        for future in as_completed(future_to_file):
            url = future_to_file[future]
            try:
                future.result()
            except Exception as exc:
                log.error(f"download file from {url} generated an exception: {exc}")
                raise exc


def get_cpu_architecture() -> str:
    cpu_arch = platform.machine().lower()

    if cpu_arch in ["x86_64", "amd64"]:
        return "amd64"
    elif cpu_arch in ["arm64", "aarch64"]:
        return "arm64"
    else:
        return ""


def get_os_type() -> str:
    os_type = platform.system().lower()

    if os_type == "darwin":
        return "darwin"
    elif os_type == "windows":
        return "windows"
    elif os_type == "linux":
        return "linux"
    else:
        return ""
