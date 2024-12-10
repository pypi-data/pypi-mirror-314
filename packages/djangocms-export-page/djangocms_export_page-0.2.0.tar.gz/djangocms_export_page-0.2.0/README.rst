
Django CMS Export Page
=================================================

:Version: 0.2.0
:Source: https://bitbucket.org/maykinmedia/djangocms-export-page
:Keywords: ``django`` ``cms`` ``export`` ``docx``
:PythonVersion: 3.11

|build-status| |code-quality| |black| |coverage|

|python-versions| |django-versions| |pypi-version|

Export a Django CMS page or a model view to a DOCX document

.. contents::

.. section-numbering::

Features
========

* Adds a menu entry in the CMS toolbar to export the current page
* Ability to export a custom model, including placeholder fields

.. image:: img/page-export-menu.png

Installation
============

Requirements
------------

* Python 3.11 or above
* Django 3.2 or above
* Django CMS 4.1 or above


Install
-------

.. code-block:: bash

    pip install djangocms-export-page


Usage
=====

In your Django settings:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'djangocms_export_page',
        ...
    ]



CMS Page
--------

CMS Page don't need any extra configuration to work.

If a Plugin has a reverse ForeignKey that would behave like children,
add the following to the CMSPlugin model class:

.. code-block:: python

    _export_page = {
        'children': 'items'
    }

    @property
    def items(self):
        return self.frequentlyaskedquestion_set.all()

where `items` is a iterable attribute of the model class.

And for on the ForeignKey Django model class:

.. code-block:: python

    _export_page = {
        'fields': ['name', ... ]
    }

If you want to export the contents of a ForeignKey or OneToOneField inside the regular model you can use
`_export_page_field_names`. Now these fields will be put in the some level as the plugin fields.

.. code-block:: python

    _export_page_field_names = ['number', 'title', 'lead', 'display_date', 'date', 'location']


Django Model
------------

If you need to export a Django model included in a AppHook,
add the following to the model class:

.. code-block:: python

    _export_page = {
        'sections': [{
            'name': 'Meta',
            'fields': ['title', ... ]
        }, {
            'name': 'Body',
            'fields': ['content']
        }],
    }

It's better to put the PlaceholderField (here `content`) in a separate section.


Static Placeholders
-------------------

If you also want to export the static placeholders of a page, some extra configuration
is required. There is a setting called `EXPORT_STATIC_PLACEHOLDERS`.

.. code-block:: python

    EXPORT_STATIC_PLACEHOLDERS = {
        'template_name': ['static_placeholder_code']
    }

So with the cms settings it will look like this:

.. code-block:: python

    # test.html
    <div>
        {% static_placeholder 'test-placeholder' %}
    </div>

    # settings.py
    CMS_TEMPLATES = [
        ('test.html', _('Test page')),
    ]

    EXPORT_STATIC_PLACEHOLDERS = {
        'test.html': ['test-placeholder']
    }

.. |build-status| image:: https://github.com/maykinmedia/djangocms-export-page/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/djangocms-export-page/actions?query=workflow%3A%22Run+CI%22

.. |requirements| image:: https://requires.io/github/maykinmedia/djangocms-export-page/requirements.svg?branch=develop
    :target: https://requires.io/github/maykinmedia/djangocms-export-page/requirements/?branch=develop
    :alt: Requirements status

.. |coverage| image:: https://codecov.io/gh/maykinmedia/djangocms-export-page/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/djangocms-export-page
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/djangocms-export-page.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/djangocms-export-page.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/djangocms-export-page.svg
    :target: https://pypi.org/project/djangocms-export-page/

.. |code-quality| image:: https://github.com/maykinmedia/djangocms-export-page/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/djangocms-export-page/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
