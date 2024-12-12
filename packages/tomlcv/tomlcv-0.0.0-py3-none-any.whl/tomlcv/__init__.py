import base64
from datetime import date, datetime
from importlib.resources import open_text

import toml
import typer
from jinja2 import Environment, StrictUndefined


def res2str(name: str):
    with open_text('tomlcv', name) as f:
        return f.read()


def main(
        *,
        in_toml: str = 'resume.toml',
        out_html: str = 'resume.html',
        date_format: str = "%b %Y"):

    def format_date(date: date):
        return date.strftime(date_format)

    env = Environment(
        undefined=StrictUndefined)

    env.filters['date'] = format_date

    resume = toml.load(in_toml)
    img = resume['basics']['image']

    with open(img, 'rb') as f:
        resume['basics']['image'] = base64.encodebytes(f.read()).decode()

    template = env.from_string(res2str('resume.j2'))

    resume_html = template.render(resume)

    with open(out_html, 'w') as f:
        f.write(resume_html)

    print(datetime.now(), f'{out_html} created')


if __name__ == "__main__":
    typer.run(main)
