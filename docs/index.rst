.. _flask_pystmark:

.. toctree::
   :maxdepth: 2

**************
Flask-Pystmark
**************

.. module:: flask_pystmark

Flask-Pystmark is a Flask extension for the `Postmark API`_ library `Pystmark`_.

The extension contains two objects, ``Pystmark`` and ``Message``.  ``Pystmark``
wraps the `Simple API`_ of the ``pystmark`` module.  Both inject **Flask-Pystmark**
configuration variables into the functions or objects they wrap.

.. seealso:: `Pystmark Documentation`_

Flask-Pystmark supports Python 2.6, 2.7, 3.2, 3.3 and PyPy.

.. _usecase:
    In Flask, one way to have your site available as both example.com and
    www.example.com is to have two separate application instances with the
    SERVER_NAME configured for each.

.. _flask_pystmark_source: https://github.com/xsleonard/flask-pystmark

.. _Simple API: http://pystmark.readthedocs.org/en/latest/api.html#simple-api

.. _Pystmark: https://github.com/xsleonard/pystmark

.. _Pystmark Documentation: http://pystmark.readthedocs.org/en/latest/

.. _Postmark API: http://developer.postmarkapp.com/

.. _installation:

Installation
============

.. code-block:: bash

    $ pip install Flask-Pystmark

Configuration
=============

**Flask-Pystmark** is configured through the standard Flask config API. Any of
them can be overridden in calls to the `Pystmark` methods or ``Message`` construction.
These are the available options:

* **PYSTMARK_API_KEY** : Required. Your API key for postmarkapp.com

* **PYSTMARK_HTTPS** : default `True`. Use https for requests to postmarkapp.com

* **PYSTMARK_TEST_API** : default `False`. Use the Postmark test API. *Note: a request is still made to postmarkapp.com, but accesses their sandbox.*

* **PYSTMARK_DEFAULT_SENDER** : default `None`. Default sender email to use for outgoing messages

* **PYSTMARK_DEFAULT_REPLY_TO** : default `None`. Default reply_to email to use for outgoing messages

* **PYSTMARK_DEFAULT_HEADERS** : default `None`. Default headers to apply to outgoing messages.  They must be in the format required by Postmark. *Note: these are headers in the email. If you need headers in the request sent to postmarkapp.com, pass them in to the API wrappers as you would in a call to requests.request*

* **PYSTMARK_VERIFY_MESSAGES** : default `False`. Apply sanity checks to all messages when created.  Will raise `pystmark.MessageError` if it appears invalid.

* **TESTING** : This is a standard Flask configuration variable. If `True`, messages sent with ``Pystmark.send`` or ``Pystmark.send_batch`` will be stored in an ``outbox`` on your app's Pystmark instance. *Note: This does not mock the request to postmarkapp.com for you.*

.. _example:

Example
=======

.. code-block:: python

    # app.py
    from flask import Flask
    from flask.ext.pystmark import Pystmark, Message

    app = Flask(__name__)
    app.config['PYSTMARK_DEFAULT_SENDER'] = 'admin@example.com'
    pystmark = Pystmark(app)

    @app.route('/')
    def send():
        m = Message(to='user@gmail.com', text='Welcome')
        resp = pystmark.send(m)
        if resp.message == 'OK':
            return 'Sent message to {}'.format(resp.to)
        else:
            return 'Failed to send message. Reason: {}'.format(resp.message)


.. _api:

API
===

.. _pystmark_object:

Pystmark Object
===============

.. autoclass:: flask_pystmark.Pystmark
    :inherited-members:

.. _message_object:

Message Object
==============

.. autoclass:: flask_pystmark.Message
    :inherited-members:
