# Score Algorithm

![PyPi][pypi-badge] ![Publish][publish-badge] ![Lint][lint-badge]

A Python library (`audio-case-grade`) containing a score algorithm to score audio medical case studies.

## 💻 Technology

- Python
- [uv][uv]
- [Jupyter][jupyter]

## 🚀 Getting Started

This project uses Python (see the `.python-version`). uv handles the virtual environment and the package is installed into the environment with `--editable` or `-e` flag.

1. Install Python
2. Install [uv][uv-install]
3. Setup [virtual environment][uv-venv] `uv venv`
4. Sync dev dependencies `uv sync --dev`
5. Install package `uv pip install -e .`

## 🧱 Build

`uv build`

## ✅ Lint

Ensure that the [pylint version matches superlinter][superlinter-pylint].

- Lint - `uv run pylint src`
- Type Check - `uv run mypy src`

## 🧪 Testing

`uv run pytest`

<!-- Relative Links -->

[pypi-badge]: https://img.shields.io/pypi/v/audio-case-grade
[publish-badge]: https://github.com/audio-case-grade/Algorithms/actions/workflows/publish.yml/badge.svg
[lint-badge]: https://github.com/audio-case-grade/Algorithms/actions/workflows/lint.yml/badge.svg
[jupyter]: https://jupyter.org/
[uv]: https://docs.astral.sh/uv/
[uv-install]: https://docs.astral.sh/uv/getting-started/installation/
[uv-venv]: https://docs.astral.sh/uv/pip/environments/
[superlinter-pylint]: https://github.com/super-linter/super-linter/blob/v7.2.0/dependencies/python/pylint.txt
