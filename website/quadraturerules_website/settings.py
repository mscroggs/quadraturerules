"""Settings."""

import os as _os
import typing as _typing

from webtools import settings

dir_path = _os.path.join(_os.path.dirname(_os.path.realpath(__file__)), "..")
root_path = _os.path.join(dir_path, "..")
template_path = _os.path.join(dir_path, "template")
files_path = _os.path.join(dir_path, "files")
pages_path = _os.path.join(dir_path, "pages")
rules_path = _os.path.join(root_path, "rules")
html_path = _os.path.join(dir_path, "_html")

github_token: _typing.Optional[str] = None

processes = 1

owners = ["mscroggs"]
editors: _typing.List[str] = []
url = "https://quadraturerules.org"
website_name = [
    "The online encyclopedia of quadrature rules",
    "the online encyclopedia of quadrature rules",
]
repo = "mscroggs/quadraturerules"

settings.dir_path = dir_path
settings.html_path = html_path
settings.template_path = template_path
settings.github_token = github_token
settings.owners = owners
settings.editors = editors
settings.url = url
settings.website_name = website_name
settings.repo = repo


def set_html_path(path):
    """Set HTML path."""
    global html_path
    html_path = path
    settings.html_path = path


def set_github_token(token):
    """Set GitHub token."""
    global github_token
    github_token = token
    settings.github_token = token
