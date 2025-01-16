# A set of useful tools for security

## Precondition

Please make sure you have a recent version of Python installed

## Development

### Installing `poetry`

This project uses `poetry`. You can install `poetry` by following the instructions on the poetry website https://python-poetry.org/.

If you want virtual environments to be created by poetry in general in `.venv` within your python folder (recommeded for development with VS Code), run:

```bash
poetry config --local virtualenvs.in-project true
```

### Install all packages with poetry

For development including tools for generating documentation, use:

```bash
poetry install --no-root
```

For installing only the packages required to run the tool, use:

```bash
poetry install --without dev --no-root
```

### Runing the code

In general, the code can be run with poetry like this:

```bash
poetry run python <src-file> [<arg>]
```

Alternatively, you can open a `poetry shell` and run `python` from there:

```bash
poetry shell
```

### Examples

List all organizations by running

```bash
poetry run python src/decode_jwks.py -u <URL of a JWKS endpoint>
```

## License

Copyright Eike Thaden, 2025.

See LICENSE file
