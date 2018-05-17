=========================
django-codenerix-products
=========================

Codenerix Products is a module that enables `CODENERIX.com <http://www.codenerix.com/>`_ to set products on several platforms in a general manner

.. image:: http://www.codenerix.com/wp-content/uploads/2018/05/codenerix.png
    :target: http://www.codenerix.com
    :alt: Try our demo with Codenerix Cloud

****
Demo
****

Coming soon...

**********
Quickstart
**********

1. Install this package::

    For python 2: sudo pip2 install django-codenerix-products
    For python 3: sudo pip3 install django-codenerix-products

2. Add "codenerix_extensions" and "codenerix_products" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'codenerix_extensions',
        'codenerix_products',
    ]

3. Add in settings the params::

    # path for codenerix_products
    CDNX_PRODUCTS_URL = "products"
    # if you show the products without stock
    CDNX_PRODUCTS_SHOW_ONLY_STOCK = False
    # number of the days for one products to be considered new
    CDNX_PRODUCTS_NOVELTY_DAYS = 5
    # No force stock by default
    CDNX_PRODUCTS_FORCE_STOCK = False

4. Since Codenerix Products is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us? `Codenerix <http://www.codenerix.com/>`_


*******
Credits
*******

This project has been possible thanks to `Centrologic <http://www.centrologic.com/>`_.
