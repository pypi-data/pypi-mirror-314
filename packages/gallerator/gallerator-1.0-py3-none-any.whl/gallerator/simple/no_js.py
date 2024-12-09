import json
import shutil
from pathlib import Path

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    select_autoescape,
)

from gallerator import data_types


def jinja2_env():
    loader = ChoiceLoader(
        [
            PackageLoader("gallerator"),
            FileSystemLoader(Path(__file__).parent / "templates"),
        ]
    )
    return Environment(loader=loader, autoescape=select_autoescape())


class Photoswipe(data_types.Renderer):
    def __init__(self):
        self.jenv = jinja2_env()

    def render(self, template_vars: data_types.TemplateVars):
        template = self.jenv.get_template("page.html")
        vars = template_vars.__dict__.copy()
        vars["data_types"] = data_types
        return template.render(vars)

    def copy_static(self, gallery_path: Path):
        for src in [
            Path(__file__).parent.parent / "static",
            Path(__file__).parent / "static",
        ]:
            shutil.copytree(src, gallery_path / "static", dirs_exist_ok=True)
        (gallery_path / "static" / "README.md").unlink()


def renderer() -> data_types.Renderer:
    return Photoswipe()
