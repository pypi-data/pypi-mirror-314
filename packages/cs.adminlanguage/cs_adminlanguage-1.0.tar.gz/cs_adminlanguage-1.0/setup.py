"""Installer for the cs.adminlanguage package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="cs.adminlanguage",
    version="1.0",
    description="Addon to set the admin language",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords="Python Plone",
    author="Lur Ibargutxi",
    author_email="libargutxi@codesyntax.com",
    url="https://github.com/collective/cs.adminlanguage",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/cs.adminlanguage",
        "Source": "https://github.com/collective/cs.adminlanguage",
        "Tracker": "https://github.com/collective/cs.adminlanguage/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["cs"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "AccessControl",
        "plone.app.registry",
        "plone.registry",
        "plone.z3cform",
        "Products.CMFCore",
        "Products.CMFPlone",
        "Products.GenericSetup",
        "zope.component",
        "zope.i18n",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.publisher",
        "zope.schema",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.api",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
            "plone.browserlayer",
            "plone.testing>=5.0.0",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = cs.adminlanguage.locales.update:update_locale
    """,
)
