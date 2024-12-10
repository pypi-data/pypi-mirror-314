Welcome to django-vanityurls's documentation!
==============================================


**Django VanityURLs** is a Django app which helps the user to create vanity URLs for pages on their site via the Django admin.

By way of an example, if your website has a lengthy URL, say *example.org/complicated/path/to/page?page=1234*, which you wish to share with the public, you can set up *example.org/niceurl* for convenience and memorability.

.. contents::
   :local:

============
How It Works
============

``django-vanityurls`` works via a Django middleware. The middleware intercepts the HTTP response once your views have executed. In the event of a 404 (page not found) error response, the middleware attempts to find a ``VanityUrl`` model object matching the requested path. If a match is found, a 301 permanent redirect is issued, directing the client to the longer, canonical URL.

In this way, ``django-vanityurls`` will only query the database in the event of a 404, rather than on every request. This also means that it requires minimal configuration: for example, your ``urls.py`` need not be modified at all.


============
Installation
============

Download
~~~~~~~~

The preferred way to get hold of ``django-vanityurls`` is via ``pip``::

    $ pip install django-vanityurls

This may be a good time to add ``django-vanityurls`` to your project's ``requirements.txt``.

The ``django-vanityurls`` source code is also available via `the project's GitHub repository <https://github.com/simonharris/django-vanityurls>`_.

Initial Configuration
~~~~~~~~~~~~~~~~~~~~~

There are two changes to make to your project's ``settings.py``:

1) add the app to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'vanityurls',
        ...
    ]


2) enable the ``django-vanityurls`` middleware by adding the following entry to ``MIDDLEWARE``::

    MIDDLEWARE = [
        ...
        'vanityurls.middleware.VanityUrlsMiddleware',
        ...
    ]


Database Migration
~~~~~~~~~~~~~~~~~~

Apply the database migration to create the table needed by ``django-vanityurls``:


.. code-block:: console

    $ python manage.py migrate vanityurls


You should now be good to go, and should have a VANITYURLS section in Django admin.


========
See Also
========

* Browse the `django-vanityurls source code repository <https://github.com/simonharris/django-vanityurls>`_ on Github
* Visit `django-vanityurls on the Python Package Index <https://pypi.org/project/django-vanityurls/>`_  (PyPI)
