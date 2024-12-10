from src.testtools_cli.generator.template_generator import TemplateGenerator


def test_render_template_with_custom_tag():
    gen = TemplateGenerator(tool_name="moka")
    ret = gen.render_template(
        """
        [[package]]                                                                                                                                                                                                               │
        name = "replace_____me"
        """.strip()
    )

    assert (
        ret
        == """
        [[package]]                                                                                                                                                                                                               │
        name = "moka"
    """.strip()
    )
