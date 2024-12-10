from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from .constant import SOLARCTL_NAME, SOLARCTL_VERSION, CLI_DOWNLOAD_DOMAIN


class ToolInfo(BaseModel):
    tool_name: str = Field(description="tool name")
    version: str = Field(description="tool version")


class Settings(BaseSettings):
    tool_download_domain: str = CLI_DOWNLOAD_DOMAIN
    tool_list: list[ToolInfo] = [
        ToolInfo(tool_name=SOLARCTL_NAME, version=SOLARCTL_VERSION)
    ]


settings = Settings()
