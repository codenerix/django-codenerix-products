=========================
django-codenerix-products
=========================

Codenerix Products is a module that enables `CODENERIX.com <http://www.codenerix.com/>`_ to set products on several platforms in a general manner

.. image:: http://www.centrologic.com/wp-content/uploads/2017/01/logo-codenerix.png
    :target: http://www.codenerix.com
    :alt: Try our demo with Centrologic Cloud

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

4. Since Codenerix Products is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us? `Centrologic <http://www.centrologic.com/>`_

******************
Commercial support
******************

This project is backed by `Centrologic <http://www.centrologic.com/>`_. You can discover more in `CODENERIX.com <http://www.codenerix.com/>`_.
If you need help implementing or hosting django-codenerix-products, please contact us:
http://www.centrologic.com/contacto/

.. image:: http://www.centrologic.com/wp-content/uploads/2015/09/logo-centrologic.png
    :target: http://www.centrologic.com
    :alt: Centrologic is supported mainly by Centrologic Computational Logistic Center
