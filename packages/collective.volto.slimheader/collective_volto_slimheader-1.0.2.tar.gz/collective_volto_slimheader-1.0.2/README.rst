.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

===========================
collective.volto.slimheader
===========================

Volto Slim Header


Features
--------

- Control panel for plone registry to manage slimheader configuration.
- Restapi view that exposes these settings for Volto.

This addon only add a registry entry where store some configuration data. You need to provide
the edit interface in your Volto theme.

Volto endpoint
--------------

The data is available on this enpoint *@slimheader*::

    > curl -i http://localhost:8080/Plone/@slimheader -H 'Accept: application/json'


The response is something similar to this::

    [
        ...Volto JSON data here
    ]


Control panel
-------------

You can edit settings directly from Volto because the control has been registered on Plone and available with plone.restapi.

Volto integration
-----------------

To use this product in Volto, your Volto project needs to include a new plugin: volto-slimheader_.

.. _volto-slimheader: https://github.com/collective/volto-slimheader


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install collective.volto.slimheader by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.volto.slimheader


and then running ``bin/buildout``


Authors
-------

RedTurtle


Contributors
------------

- folix-01


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.volto.slimheader/issues
- Source Code: https://github.com/collective/collective.volto.slimheader
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: info@redurtle.it


License
-------

The project is licensed under the GPLv2.
