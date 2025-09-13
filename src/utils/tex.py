from __future__ import annotations

from typing import Any, Dict
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def escape_latex(text: str) -> str:
    if not isinstance(text, str):
        return text

    text = text.replace("\\", r"\textbackslash{}")
    text = text.replace("{", r"\{")
    text = text.replace("}", r"\}")
    text = text.replace("&", r"\&")
    text = text.replace("%", r"\%")
    text = text.replace("$", r"\$")
    text = text.replace("#", r"\#")
    text = text.replace("^", r"\textasciicircum{}")
    text = text.replace("_", r"\_")
    text = text.replace("~", r"\textasciitilde{}")

    return text


def escape_latex_recursive(data: Any) -> Any:
    if isinstance(data, str):
        return escape_latex(data)
    elif isinstance(data, dict):
        return {key: escape_latex_recursive(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [escape_latex_recursive(item) for item in data]
    else:
        return data


def render_tex(
    resume_data: Dict[str, Any],
    output_tex_path: Path,
    template_name: str,
    templates_dir: Path,
) -> None:
    escaped_data = escape_latex_recursive(resume_data)

    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.block_start_string = "<<%"
    env.block_end_string = "%>>"
    env.variable_start_string = "<<"
    env.variable_end_string = ">>"
    env.comment_start_string = "<#!"
    env.comment_end_string = "!#>"
    template = env.get_template(template_name)
    rendered = template.render(resume=escaped_data)

    output_tex_path.parent.mkdir(parents=True, exist_ok=True)
    output_tex_path.write_text(rendered, encoding="utf-8")
