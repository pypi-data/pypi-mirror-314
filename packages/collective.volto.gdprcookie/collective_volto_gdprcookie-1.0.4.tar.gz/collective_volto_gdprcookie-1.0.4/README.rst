.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.volto.gdprcookie/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.volto.gdprcookie/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.volto.gdprcookie/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.volto.gdprcookie?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.volto.gdprcookie/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.volto.gdprcookie

.. image:: https://img.shields.io/pypi/v/collective.volto.gdprcookie.svg
    :target: https://pypi.python.org/pypi/collective.volto.gdprcookie/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.volto.gdprcookie.svg
    :target: https://pypi.python.org/pypi/collective.volto.gdprcookie
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.volto.gdprcookie.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.volto.gdprcookie.svg
    :target: https://pypi.python.org/pypi/collective.volto.gdprcookie/
    :alt: License

.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=================
Volto GDPR Cookie
=================

Add-on for manage GDPR Cookie banner on Volto based on GDPR law.

Features
--------

- Control panel in plone registry to manage GDPR cookie settings.
- Restapi endpoint that exposes these settings for Volto.

@gdpr-cookie-settings
---------------------

Anonymous users can't access registry resources by default with plone.restapi (there is a special permission).

To avoid enabling registry access to everyone, this package exposes a dedicated restapi route with GDPR cookie settings: *@gdpr-cookie-settings*::

    > curl -i http://localhost:8080/Plone/@gdpr-cookie-settings -H 'Accept: application/json' --user admin:admin


Volto integration
-----------------

To use this product in Volto, your Volto project needs to include a new plugin: https://github.com/collective/XXX


Translations
------------

This product has been translated into

- Italian



Installation
------------

Install collective.volto.gdprcookie by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.volto.gdprcookie


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.volto.gdprcookie/issues
- Source Code: https://github.com/collective/collective.volto.gdprcookie


License
-------

The project is licensed under the GPLv2.
