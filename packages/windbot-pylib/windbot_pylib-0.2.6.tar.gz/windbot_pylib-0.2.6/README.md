# Windbot Python Lib

windbot-pylib contains core python functionality needed by other windbot python projects such as the logger and the api.

## Installation

### poetry

```bash
poetry add windbot-pylib --repository windbot-pypi
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
$ poetry config repositories.windbot-pypi http://127.0.0.1:8081
$ poetry config http-basic.windbot-pypi windbot p4p4y40fd00m
$ poetry publish --build --repository windbot-pypi
```


## FAQ

### poetry update windbot-pylib doesn't find the latest version on PyPI

This is most likely do to caching. Clear the PyPI cache with the following command

```bash
$ poetry cache clear pypi --all
```

and then run `poetry update`
