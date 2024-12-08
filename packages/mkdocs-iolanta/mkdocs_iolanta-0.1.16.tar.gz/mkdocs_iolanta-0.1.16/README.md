# 📖 [mkdocs](https://mkdocs.org) + 👁️ [iolanta](https://iolanta.tech)

[![License](https://img.shields.io/github/license/iolanta-tech/mkdocs-iolanta)](https://github.com/iolanta-tech/mkdocs-iolanta/blob/main/LICENSE)
[![Deploy](https://github.com/iolanta-tech/mkdocs-iolanta/actions/workflows/deploy.yml/badge.svg)](https://github.com/iolanta-tech/mkdocs-iolanta/actions)
[![Stars](https://img.shields.io/github/stars/iolanta-tech/mkdocs-iolanta)](https://github.com/iolanta-tech/mkdocs-iolanta/stargazers)
[![Forks](https://img.shields.io/github/forks/iolanta-tech/mkdocs-iolanta)](https://github.com/iolanta-tech/mkdocs-iolanta/network/members)
[![Issues](https://img.shields.io/github/issues/iolanta-tech/mkdocs-iolanta)](https://github.com/iolanta-tech/mkdocs-iolanta/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/iolanta-tech/mkdocs-iolanta)](https://github.com/iolanta-tech/mkdocs-iolanta/pulls)
[![Last Commit](https://img.shields.io/github/last-commit/iolanta-tech/mkdocs-iolanta)](https://github.com/iolanta-tech/mkdocs-iolanta/commits/main)
[![Contributors](https://img.shields.io/github/contributors/iolanta-tech/mkdocs-iolanta)](https://github.com/iolanta-tech/mkdocs-iolanta/graphs/contributors)


![](docs/assets/cover.png)

## Features

By integrating MkDocs static site builder with Iolanta knowledge management workspace, you can empower your static site with:

* Automatic page → page [🔗 links](https://mkdocs.iolanta.tech/link/);
* [Tables](https://tables.iolanta.tech) generated from YAML data;
* Project [roadmaps](https://roadmap.iolanta.tech);
* [Architecture Decision Records](https://adr.iolanta.tech).
* Something missing? Or anything doesn't work? Submit [➕ an issue](https://github.com/iolanta-tech/mkdocs-iolanta/issues)!

## Installation

Python ⩾ 3.10 required.

`mkdocs-iolanta` is on [PyPI](https://pypi.org/project/mkdocs-iolanta).

```bash
pip install mkdocs-iolanta
```

## Configuration

Open your `mkdocs.yml` configuration file and configure its `plugins` section as follows:

```yaml
plugins:
  - search                  # (1)!
  - …
  - iolanta                 # (2)!
  - macros:                 # (3)!
      on_error_fail: true   # (4)!
  - …
```

1. The `search` plugin is built-in and automatically enabled if `mkdocs.yml` does not specify any `plugins` at all. But if it does, this built-in plugin must be enabled explicitly.
2. Support `iolanta` capabilities for this documentation site.
3. This enables [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io) which is required to utilize Iolanta capabilities on MkDocs pages, such as {% raw %}{{ render("render") }}{% endraw %} macro.
4. This setting is highly recommended. If there is an error during rendering MkDocs macros, including those macros provided by Iolanta, the site build will throw an error — making the issue easier to notice both on local development and in CI.
