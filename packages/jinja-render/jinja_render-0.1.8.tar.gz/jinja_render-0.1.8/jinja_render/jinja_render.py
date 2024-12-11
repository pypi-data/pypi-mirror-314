import os
import json
from jinja2 import Environment, FileSystemLoader

from jinja_render.get_info_top import add_repo_info

import typer

app = typer.Typer()


@app.command()
def write_tex(report_name: str = "", summary_path=None):
    rendered_report = get_rendered_report(report_name, summary_path)
    with open(f"reports/{report_name}.tex", "w") as report_tex:
        report_tex.writelines(rendered_report)


def load_json(path):
    with open(path, encoding="utf8") as info_file:
        information = json.load(info_file)
    return information


def get_jinja_latex():
    latex_jinja_env = Environment(
        variable_start_string="\\VAR{",
        variable_end_string="}",
        comment_start_string="\\#{",
        comment_end_string="}",
        loader=FileSystemLoader(os.path.abspath(".")),
    )
    return latex_jinja_env


def get_rendered_report(report_name, path=None):
    effort_summary = {}
    if path is not None:
        effort_summary = load_json(path)
    effort_summary_with_top_info = add_repo_info(effort_summary)
    latex_jinja_env = get_jinja_latex()
    template = latex_jinja_env.get_template(f"reports/templates/{report_name}.tex")
    return template.render(effort_summary_with_top_info)
