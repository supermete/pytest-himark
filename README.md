# pytest-himark

[![PyPI version](https://img.shields.io/pypi/v/pytest-himark.svg)](https://pypi.org/project/pytest-himark)

[![Python versions](https://img.shields.io/pypi/pyversions/pytest-himark.svg)](https://pypi.org/project/pytest-himark)

[![See Build Status on GitHub Actions](https://github.com/supermete/pytest-himark/actions/workflows/main.yml/badge.svg)](https://github.com/supermete/pytest-himark/actions/workflows/main.yml)

A plugin that reads a json file in your test root directory, searches
the \'markers\' key, lists the markers declared as \'true\' as enabled
markers and automatically adds -m option to the command line with an OR
on the enabled markers.

------------------------------------------------------------------------

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated
with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with
[\@hackebrot](https://github.com/hackebrot)\'s
[cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin)
template.

## Requirements

-   json \>= 2.0.9

## Installation

You can install \"pytest-himark\" via
[pip](https://pypi.org/project/pip/) from
[PyPI](https://pypi.org/project):

    $ pip install pytest-himark

## Usage

After installing this plugin, pytest will automatically load it when
launching tests. You will simply need to add the \--json option to the
command line with the path to the json containing the markers you want
to enable. Alternatively, you can add the \--json option and the path in
the pytest.ini directly, in the addopts variable.

Example:

- pytest.ini: 

``` CFG
    addopts = \--json=path/to/my/config.json
```

- config.json:

``` JSON
{
    "markers": {
        "my_marker1": true,
        "my_marker2": true,
        "my_marker3": false,
        "my_marker4": false
    }
}
```

Launching pytest now will automatically add he following to the
command line:

``` python
>> pytest -m "(my_marker1 or my_marker2) and not (my_marker3 or my_marker4)"
```

## Contributing

Contributions are very welcome. Tests can be run with
[tox](https://tox.readthedocs.io/en/latest/), please ensure the coverage
at least stays the same before you submit a pull request.

## License

Distributed under the terms of the
[MIT](https://opensource.org/licenses/MIT) license, \"pytest-himark\" is
free and open source software

## Issues

If you encounter any problems, please [file an
issue](https://github.com/supermete/pytest-himark/issues) along with a
detailed description.
