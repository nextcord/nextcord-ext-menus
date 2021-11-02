import re
import sys
import os


project = "nextcord-ext-menus"
copyright = "2021, nextcord"
author = "nextcord"

sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("extensions"))

_version_regex = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'

with open("../nextcord/ext/menus/__init__.py") as stream:
    match = re.search(_version_regex, stream.read(), re.MULTILINE)

version = match.group(1)

if version.endswith(("a", "b", "rc")):
    # append version identifier based on commit count
    try:
        import subprocess

        p = subprocess.Popen(
            ["git", "rev-list", "--count", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += out.decode("utf-8").strip()
        p = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except Exception:
        pass

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
    "sphinxcontrib_trio",
    "attributetable",
]


autodoc_typehints = "none"

intersphinx_mapping = {
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
    "nextcord": ("https://nextcord.readthedocs.io/en/latest", None),
}

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
"""

highlight_language = "python3"
html_theme = "sphinx_rtd_theme"
master_doc = "index"
pygments_style = "friendly"
source_suffix = ".rst"

# These folders are copied to the documentation's HTML output
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
