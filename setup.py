import os
from setuptools import setup
import re

version = ""
with open("nextcord/ext/menus/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("version is not set")

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


def long_description():
    # check if README.md exists
    if not os.path.exists("README.md"):
        return ""
    # return README contents
    with open("README.md", "r") as fh:
        return fh.read()


def requirements():
    # check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        return []
    # return requirements.txt contents
    with open("requirements.txt") as f:
        return f.read().splitlines()


extras_require = {
    "docs": [
        "sphinx",
        "sphinxcontrib_trio",
        "sphinx-book-theme",
    ],
}

setup(
    name="nextcord-ext-menus",
    version=version,
    author="Nextcord Developers",
    description="An extension module to make reaction based menus with nextcord",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/nextcord/nextcord-ext-menus",
    project_urls={
        "Bug Tracker": "https://github.com/nextcord/nextcord-ext-menus/issues",
    },
    packages=["nextcord.ext.menus"],
    license="MIT",
    python_requires=">=3.8.0",
    install_requires=[requirements()],
    extras_require=extras_require,
)
