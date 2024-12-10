from pathlib import Path


class TemplateGenerator:
    def __init__(self, tool_name: str):
        self.tool_name = tool_name

    def render_template_path(self, template_path: Path) -> str:
        with template_path.open() as f:
            return self.render_template(f.read())

    def render_template(self, template_string: str) -> str:
        return template_string.replace("replace_____me", self.tool_name)
