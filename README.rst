=============
pytest-himark
=============

.. image:: https://img.shields.io/pypi/v/pytest-himark.svg
    :target: https://pypi.org/project/pytest-himark
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-himark.svg
    :target: https://pypi.org/project/pytest-himark
    :alt: Python versions

.. image:: https://github.com/supermete/pytest-himark/actions/workflows/main.yml/badge.svg
    :target: https://github.com/supermete/pytest-himark/actions/workflows/main.yml
    :alt: See Build Status on GitHub Actions

A plugin that reads a json file in your test root directory, searches the 'markers' key, lists the markers declared as 'true' as enabled markers and automatically adds -m option to the command line with an OR on the enabled markers.

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Requirements
------------

* json >= 2.0.9


Installation
------------

You can install "pytest-himark" via `pip`_ from `PyPI`_::

    $ pip install pytest-himark


Usage
-----

After installing this plugin, pytest will automatically load it when launching tests.
You will simply need to add the --json option to the command line with the path to the
json containing the markers you want to enable. Alternatively, you can add the --json
option and the path in the pytest.ini directly, in the addopts variable.

Example:
    - pytest.ini:
    .. code-block:: INI

        addopts = --json=path/to/my/config.json

    - config.json:
.. code-block:: JSON

        {
            "markers": {
                "my_marker1": true,
                "my_marker2": true,
                "my_marker3": false
            }
        }

..

    Launching pytest now will automatically add he following to the command line:

.. code-block:: python

    >> pytest -m "my_marker1 or my_marker2"


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-himark" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: https://opensource.org/licenses/MIT
.. _`BSD-3`: https://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: https://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: https://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/supermete/pytest-himark/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
