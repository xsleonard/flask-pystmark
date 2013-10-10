import pystmark
from mock import patch
from unittest import TestCase
from flask import Flask
from flask_pystmark import Pystmark, Message


class FlaskPystmarkTest(TestCase):

    def setUp(self):
        super(FlaskPystmarkTest, self).setUp()
        self.app = Flask(__name__)

    def tearDown(self):
        super(FlaskPystmarkTest, self).tearDown()

    def test_create(self):
        p = Pystmark()
        self.assertTrue(hasattr(p, 'outbox')
        self.assertEqual(p.outbox, [])

    def test_create_with_app(self):
        p = Pystmark(app=self.app)
        self.assertEqual(self.app.pystmark, p)

    def test_init_app(self):
        p = Pystmark()
        p.init_app(self.app)
        self.assertEqual(self.app.pystmark, p)

    @patch.object(Pystmark, '_pystmark_call')
    def test_send(self, mock_call):
        m = Message()
        p = Pystmark(app=self.app)
        p.send(m)
        mock_call.assert_called_with(pystmark.send, m)

    @patch.object(Pystmark, '_pystmark_call')
    def test_send_req_args(self, mock_call):
        m = Message()
        p = Pystmark(app=self.app)
        headers = dict(whatever='something')
        p.send(m, **dict(headers=headers))
        mock_call.assert_called_with(pystmark.send, m, header=headers)
