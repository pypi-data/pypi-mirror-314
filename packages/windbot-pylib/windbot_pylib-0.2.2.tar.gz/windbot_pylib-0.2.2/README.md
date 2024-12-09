# Windbot Python Lib

windbot-pylib contains core python functionality needed by other windbot python projects such as the logger and the api.

## Installation

### poetry

```bash
poetry add windbot-pylib
```

### pip

```bash
pip install windbot-pylib
```

## Contributing

### Versioning

windbot-pylib uses semantic versioning.

- Major - bump the major version when there are breaking changes to an interface which are not backwards compatible.
- Minor - bump the minor version when adding functionality that is backwards compatible with previous versions.
- Patch - bump the patch version when you make backwards compatible bug fixes.

To bump one of the above versions using poetry:

```bash
$ poetry version major
```

### Publish changes to PyPI

```bash
$ poetry config pypi-token.pypi your-api-token
$ poetry publish --build
```
