Flask-Pystmark
==============

[![PyPI version](https://badge.fury.io/py/Flask-Pystmark.png)](http://badge.fury.io/py/Flask-Pystmark)
[![Build Status](https://travis-ci.org/xsleonard/flask-pystmark.png)](https://travis-ci.org/xsleonard/flask-pystmark)
[![Coverage Status](https://coveralls.io/repos/xsleonard/flask-pystmark/badge.png)](https://coveralls.io/r/xsleonard/flask-pystmark)

Flask extension for [Pystmark](https://github.com/xsleonard/pystmark), a Postmark API library.

Flask-Pystmark supports Python 2.6, 2.7, 3.3 and PyPy.

[Read the complete docs](https://flask-pystmark.readthedocs.org)

To run the tests, do `python setup.py test`

Example:

```python
# app.py
from flask import Flask
from flask.ext.pystmark import Pystmark, Message
from pystmark import ResponseError

app = Flask(__name__)
app.config['PYSTMARK_API_KEY'] = 'your_api_key'
app.config['PYSTMARK_DEFAULT_SENDER'] = 'admin@example.com'
pystmark = Pystmark(app)

@app.route('/')
def send():
    m = Message(to='user@gmail.com', text='Welcome')
    resp = pystmark.send(m)
    try:
        resp.raise_for_status()
    except ResponseError as e:
        return 'Failed to send message. Reason: {}'.format(e)
    else:
        return 'Sent message to {}'.format(resp.message.to)
```
