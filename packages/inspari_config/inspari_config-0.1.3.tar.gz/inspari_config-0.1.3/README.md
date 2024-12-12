This repository provides Python configuration utilities.

### Usage

The most common usage pattern is to create a `config.py` file that _defines_ the configuration. The configuration itself
is parsed from environment variables. They are typically read from a `.env` file during local development.

A minimal example is bundled, with the configuration defined in `example_config.py`, a few variables in `example.env`, 
and the typical access pattern (i.e. how settings are access in application code) illustrated in `example_usage.py`.

### Development

Create a new Python environment with all dependencies installed,

```bash
poetry install
```

That's it! You can validate that the environment is setup correctly by running the tests,

```bash
poetry run coverage run -m pytest
```

### Deployment

Update the version in `pyproject.toml`, and add a new entry in `CHANGELOG.md`. Build the project via Poetry,

```bash
poetry build
```

and push it to pypi,

```bash
poetry publish -u __token__ -p $INSPARI_PYPI_TOKEN
```