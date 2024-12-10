from typing import Optional
from pydantic import BaseModel, Field


class DownloadInfo(BaseModel):
    url: str = Field(description="download url")
    filename: Optional[str] = Field(description="local filename")


class ToolInfo(BaseModel):
    tool_name: str = Field(description="tool name")
    version: str = Field(description="tool version")
