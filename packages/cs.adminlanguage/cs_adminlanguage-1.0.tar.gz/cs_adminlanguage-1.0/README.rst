.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

================
cs.adminlanguage
================

This package provides a control panel to configure in which language do you want to show the admin interface.

This is useful if you need to configure a website in a language you don't know.

This package is based in Silvuple_ a package that use to do this and more for Plone 3.

Installation
------------

Install cs.adminlanguage by adding it to your buildout::

    [buildout]

    ...

    eggs =
        cs.adminlanguage


and then running ``bin/buildout``.
Then start Plone and activate the add-on in the Add-ons control panel.

Now you can go to the Language Admin Settings control panel from this add-on and set the preferred admin language.
This language will be used for all translation messages in domains that start with "plone" or "collective" (or the "linguaplone" domain).

Now any authenticated user with the "cs.adminlanguage: ViewinAdminLanguage" permission will see messages from those domains in the chosen admin language.
The suggested way for configuring this, is to go to the Groups control panel, select the Administrators and Site Administrators groups, and grant them the AdminLanguageReader role.


Contribute
----------

- Issue Tracker: https://github.com/codesyntax/cs.adminlanguage/issues
- Source Code: https://github.com/codesyntax/cs.adminlanguage


Support
-------

If you are having issues, please let us know adding an issue in Github


License
-------

The project is licensed under the GPLv2.


.. _Silvuple: https://github.com/miohtama/silvuple/
