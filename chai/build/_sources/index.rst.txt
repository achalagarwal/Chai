.. Chai documentation master file, created by
   sphinx-quickstart on Sun Jul 22 07:42:50 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Chai's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

**Django Framework** has been used to expose the functions to the port 8060 which can be accessed using https://chai.dunzo.in/sub-directory/function

There are two subdirectories: *info* and *sku*

- **info** -> Contains functions that involve getting some kind of information
.. py:function:: check_alcohol_limit(request)

  Returns the Alcohol details in an order when requested.

  :param request: POST Request with order list and city id in the body

- **sku** -> Contains functions that involve getting a list of standard sku match
.. py:function:: complete_query(request)

  Returns a list of probable autocomplete items

  :param request: GET Request containing a parameter i.e. user search query


.. py:function:: enumerate(sequence[, start=0])

  Return an iterator that yields tuples of an index and an item of the
  *sequence*. (And so on.)

.. include:: modules.rst


Contents
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
