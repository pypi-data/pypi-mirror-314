"""This module defines CLI interaction when using `portray`.

This is powered by [hug](https://github.com/hugapi/hug) which means unless necessary
it should maintain 1:1 compatibility with the programmatic API definition in the
[API module](/reference/portray/api)

- `portray as_html`: Renders the project as HTML into the `site` or other specified output directory
- `portray in_browser`: Runs a server with the rendered documentation pointing a browser to it
- `portray server`: Starts a local development server (by default at localhost:8000)
- `portray project_configuration`: Returns back the project configuration as determined by` portray`
"""
from pprint import pprint

import click
from portray import api, logo

@click.group()
def cli():
    ...

@cli.command()
@click.option("--directory", default="", help="The root folder of your project.")
@click.option("--config_file", default="pyproject.toml", help="The [TOML](https://github.com/toml-lang/toml#toml) formatted config file you wish to use.")
@click.option("--message", default=None, help="The commit message to use when uploading your documentation.")
@click.option("--force", "-f", is_flag=True, default=False, help="Force the push to the repository.")
@click.option("--ignore_version", is_flag=True, default=False, help="Ignore check that build is not being deployed with an old version.")
@click.option("--modules", default=None, help="One or more modules to render reference documentation for")
def on_github_pages(**kwargs) -> None:
    """Regenerates and deploys the documentation to GitHub pages."""
    api.on_github_pages(**kwargs)
