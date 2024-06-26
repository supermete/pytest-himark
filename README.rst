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

pytest-himark is a plugin that creates markers from a json configuration to filter pytest's test collection.

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

- In pytest.ini:

    .. code-block:: INI

        addopts = --json=path/to/my/config.json

    ..

- Or by command line:

    .. code-block::

        >> pytest --json=path/to/my/config.json

    ..

The markers can be configured in 4 ways to give more flexibility to the end user.
The first way is having a 'markers' key containing a dictionary with the name of the markers as key, and a boolean as value.
If the boolean is true, the marker with the specified name will be created.

Example:

.. code-block:: JSON

    {
        'markers': {
            'marker1': true,
            'marker2': true,
            'marker3': false,
            'marker4': false
        }
    }
..

This json will result in the following marker filtering:

.. code-block::

    -m '(marker1 or marker2)'
..

Another way of specifying marker is to define a 'devices' key, with a list of dictionaries as value.
Each key from the 'devices' list can be refered to as a 'device' and should contain a key named 'name' as a string and a key named 'used' as a boolean.
If the 'used' key of a device is set to true, a marker will be created and named with the 'name' string.

Example:

.. code-block:: JSON

    {
        'devices': [
             {
                'name': "device1",
                'used': true,
             },
             {
                'name': "device2",
                'used': false,
             }
        ]
    }
..

This json will result in the following marker filtering:

.. code-block::

    -m '(device1)'
..

Another way to specifying marker is to have a key named 'type' in a device-specific dictionary (see above), defined as a string.
A marker with the string value of the 'type' will be created.

Example:

.. code-block:: JSON

    {
        'devices': [
             {
                'name': "device1",
                'type': "my_type"
                'used': true,
             },
             {
                'name': "device2",
                'used': false,
             }
        ]
    }
..

This json will result in the following marker filtering:

.. code-block::

    -m '(device1 or my_type)'
..

One last way to specifying marker is to have keys named 'do', 'di' and/or 'ai' in a device-specific dictionary (see above), defined as list of strings.
A marker will be created for every string in those arrays.

Example:

.. code-block:: JSON

    {
        'devices': [
            {
                "name": "device1",
                "do": [
                    "do1"
                ],
                "di": [
                    "di1"
                ],
                "ai": [
                    "ai1"
                ],
                "used": true,
             }
            {
                "name": "device2",
                "used": false,
             }
        ]
    }

..

This json will result in the following marker filtering:

.. code-block::

    -m '(device1 or do1 or di1 or ai1)'
..


Launching pytest now will then automatically add the filter to the command line, e.g.:

.. code-block:: python

    >> pytest -m '(device1 or do1 or di1 or ai1)'
..

Finally, after pytest test collection has completed, this plugin will also filter out any test that is marked with an undefined marker.
For example consider the following config:

.. code-block:: JSON

    {
        'markers': {
            'marker1': true
        }
    }

..

And the following test:

.. code-block:: python

    @pytest.mark.marker1
    @pytest.mark.marker2
    def test_mytest():
        assert True
..

This test is marked with *marker1* which is defined in the configuration, but also with *marker2* which is not. Therefore, despite being initially collected by pytest, this plugin will remove it from the selection.

Note that any empty string as marker will be ignored by the plugin, and any leading or trailing spaces will be removed.

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
