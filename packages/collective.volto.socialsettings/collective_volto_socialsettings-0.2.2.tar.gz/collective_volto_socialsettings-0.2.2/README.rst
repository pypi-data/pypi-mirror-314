
=====================
Volto Social Settings
=====================

.. image:: https://travis-ci.com/collective/collective.volto.socialsettings.svg?branch=master
    :target: https://travis-ci.com/collective/collective.volto.socialsettings

Add-on for manage a list of social network links on Volto

Features
--------

- Control panel for plone registry to manage social links settings.
- Restapi view that exposes these settings for Volto

Volto endpoint
--------------

Anonymous users can't access registry resources by default with plone.restapi (there is a special permission).

To avoid enabling registry access to everyone, this package exposes a dedicated restapi route with the list of social links: *@social-links*::

    > curl -i http://localhost:8080/Plone/@social-links -H 'Accept: application/json'

And the result is something like this::

    [
        {
            "title":"foo",
            "icon": "bar",
            "url": "http://foo.com"
        },
        ...
    ]

Control panel
-------------

You can edit settings directly from Volto because the control has been registered on Plone and available with plone.restapi.



Volto integration
-----------------

To use this product in Volto, your Volto project needs to include a new plugin: https://github.com/collective/volto-social-settings


Translations
------------

This product has been translated into

- Italian

- Spanish


Installation
------------

Install collective.volto.socialsettings by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.volto.socialsettings


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.volto.socialsettings/issues
- Source Code: https://github.com/collective/collective.volto.socialsettings


License
-------

The project is licensed under the GPLv2.

Authors
-------

This product was developed by **RedTurtle Technology** team.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
