from typing import Optional
from pydantic import BaseModel, Field


class TestTool(BaseModel):
    use: str


class BuildSource(BaseModel):
    src: str = "."
    dst: Optional[str] = None


class Build(BaseModel):
    sources: list[BuildSource] = [BuildSource()]
    commands: list[str]


class TestContainer(BaseModel):
    test_tool: TestTool = Field(alias="testTool")
    build: Optional[Build] = None
    workspace: str = Field(alias="testWorkspace", default="/data/workspace")
