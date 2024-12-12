# orcestra-downloader

=============================

Simplified access to download data from orcestra.ca

[![pixi-badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json&style=flat-square)](https://github.com/prefix-dev/pixi)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![Built with Material for MkDocs](https://img.shields.io/badge/mkdocs--material-gray?logo=materialformkdocs&style=flat-square)](https://github.com/squidfunk/mkdocs-material)


[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/orcestra-downloader)](https://pypi.org/project/orcestra-downloader/)
[![PyPI - Version](https://img.shields.io/pypi/v/orcestra-downloader)](https://pypi.org/project/orcestra-downloader/)
[![PyPI - Format](https://img.shields.io/pypi/format/orcestra-downloader)](https://pypi.org/project/orcestra-downloader/)
[![Downloads](https://static.pepy.tech/badge/orcestra-downloader)](https://pepy.tech/project/orcestra-downloader)

<!-- ![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version?file=https://raw.githubusercontent.com/bhklab/orcestra-downloader/refs/heads/main/pyproject.toml) -->

![GitHub last commit](https://img.shields.io/github/last-commit/bhklab/orcestra-downloader?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/bhklab/orcestra-downloader?style=flat-square)
![GitHub pull requests](https://img.shields.io/github/issues-pr/bhklab/orcestra-downloader?style=flat-square)

![GitHub contributors](https://img.shields.io/github/contributors/bhklab/orcestra-downloader?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/bhklab/orcestra-downloader?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/bhklab/orcestra-downloader?style=flat-square)

![GitHub release (latest by date)](https://img.shields.io/github/v/release/bhklab/orcestra-downloader?style=flat-square)

## Installation

To install the package, use pip:

```console
pip install orcestra-downloader
```

To install using `pixi`:

```console
pixi add --pypi orcestra-downloader
```

## Usage

### Examples

![orcestra-gif](./tapes/orcestra.gif)

### Refreshing Cache

`orcestra-downloader` uses a cache to store downloaded data.
This should be located at ~/.cache/orcestra-downloader.

By default, the tool will only update cache when used 7 days after the last update.
To refresh the cache, use the `--refresh` flag.

```console
orcestra --refresh
```
