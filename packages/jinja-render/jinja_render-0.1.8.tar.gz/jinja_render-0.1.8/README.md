<a href="https://www.islas.org.mx/"><img src="https://www.islas.org.mx/img/logo.svg" align="right" width="256" /></a>
# Jinja Render
[![codecov](https://codecov.io/gh/IslasGECI/jinja_render/graph/badge.svg?token=ia1J0LyJiQ)](https://codecov.io/gh/IslasGECI/jinja_render)
![licencia](https://img.shields.io/github/license/IslasGECI/jinja_render)
![languages](https://img.shields.io/github/languages/top/IslasGECI/jinja_render)
![commits](https://img.shields.io/github/commit-activity/y/IslasGECI/jinja_render)
![PyPI - Version](https://img.shields.io/pypi/v/jinja_render)

Base functinos to use Jinja2

Here we use the `jinja_render` module, as example, from `robinson_code` repo
# Example
This example is from [muestreo-aves-marinas-ipbc](https://bitbucket.org/IslasGECI/muestreo-aves-marinas-ipbc/src/43dba1b46b492393baa508fbbb73d3ff9ade42be/Makefile#lines-946)
``` sh
typer jinja_render run \
--report-name="time_series_results_section" \
--summary-path="tests/data/mergulo_punta.json"
```
