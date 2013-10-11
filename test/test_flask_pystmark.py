import pystmark
from mock import patch
from unittest import TestCase
from flask import Flask
from flask_pystmark import Pystmark, Message


def test_flask_ext_import():
    try:
        import flask.ext.pystmark
    except ImportError:
        assert False
    else:
        assert flask.ext.pystmark


class FlaskPystmarkCreateTestBase(TestCase):

    def setUp(self):
        super(FlaskPystmarkCreateTestBase, self).setUp()
        self.app = Flask(__name__)
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        super(FlaskPystmarkCreateTestBase, self).tearDown()
        if self._ctx is not None:
            self._ctx.pop()


class FlaskPystmarkTestBase(FlaskPystmarkCreateTestBase):

    def setUp(self):
        super(FlaskPystmarkTestBase, self).setUp()
        self.p = Pystmark(app=self.app)
        self.api_key = 'xxx'
        self.app.config['PYSTMARK_API_KEY'] = self.api_key
        # used to test req_args:
        self.headers = dict(whatever='something')
        self.req_args = dict(headers=self.headers)


class FlaskPystmarkCreateTest(FlaskPystmarkCreateTestBase):

    def test_create(self):
        self.assertTrue(Pystmark())

    def test_create_with_app(self):
        p = Pystmark(app=self.app)
        self.assertEqual(self.app.pystmark, p)

    def test_init_app(self):
        p = Pystmark()
        p.init_app(self.app)
        self.assertEqual(self.app.pystmark, p)


@patch.object(Pystmark, '_pystmark_call')
class FlaskPystmarkAPITest(FlaskPystmarkTestBase):

    def test_send(self, mock_call):
        m = Message()
        self.p.send(m)
        mock_call.assert_called_with(pystmark.send, m)

    def test_send_req_args(self, mock_call):
        m = Message()
        self.p.send(m, **self.req_args)
        mock_call.assert_called_with(pystmark.send, m, headers=self.headers)

    def test_send_batch(self, mock_call):
        msgs = [Message(text='thing'), Message(text='other')]
        self.p.send_batch(msgs)
        mock_call.assert_called_with(pystmark.send_batch, msgs)

    def test_send_batch_req_args(self, mock_call):
        msgs = [Message(text='thing'), Message(text='other')]
        self.p.send_batch(msgs, **self.req_args)
        mock_call.assert_called_with(pystmark.send_batch, msgs,
                                     headers=self.headers)

    def test_get_delivery_stats(self, mock_call):
        self.p.get_delivery_stats()
        mock_call.assert_called_with(pystmark.get_delivery_stats)

    def test_get_delivery_stats_req_args(self, mock_call):
        self.p.get_delivery_stats(**self.req_args)
        mock_call.assert_called_with(pystmark.get_delivery_stats,
                                     headers=self.headers)

    def test_get_bounces(self, mock_call):
        self.p.get_bounces()
        mock_call.assert_called_with(pystmark.get_bounces)

    def test_get_bounces_req_args(self, mock_call):
        self.p.get_bounces(**self.req_args)
        mock_call.assert_called_with(pystmark.get_bounces,
                                     headers=self.headers)

    def test_get_bounce(self, mock_call):
        bounce_id = '1'
        self.p.get_bounce(bounce_id)
        mock_call.assert_called_with(pystmark.get_bounce, bounce_id)

    def test_get_bounce_req_args(self, mock_call):
        bounce_id = '1'
        self.p.get_bounce(bounce_id, **self.req_args)
        mock_call.assert_called_with(pystmark.get_bounce, bounce_id,
                                     headers=self.headers)

    def test_get_bounce_dump(self, mock_call):
        bounce_id = '1'
        self.p.get_bounce_dump(bounce_id)
        mock_call.assert_called_with(pystmark.get_bounce_dump, bounce_id)

    def test_get_bounce_dump_req_args(self, mock_call):
        bounce_id = '1'
        self.p.get_bounce_dump(bounce_id, **self.req_args)
        mock_call.assert_called_with(pystmark.get_bounce_dump, bounce_id,
                                     headers=self.headers)

    def test_get_bounce_tags(self, mock_call):
        self.p.get_bounce_tags()
        mock_call.assert_called_with(pystmark.get_bounce_tags)

    def test_get_bounce_tags_req_args(self, mock_call):
        self.p.get_bounce_tags(**self.req_args)
        mock_call.assert_called_with(pystmark.get_bounce_tags,
                                     headers=self.headers)

    def test_activate_bounce(self, mock_call):
        bounce_id = '1'
        self.p.activate_bounce(bounce_id)
        mock_call.assert_called_with(pystmark.activate_bounce, bounce_id)

    def test_activate_bounce_req_args(self, mock_call):
        bounce_id = '1'
        self.p.activate_bounce(bounce_id, **self.req_args)
        mock_call.assert_called_with(pystmark.activate_bounce, bounce_id,
                                     headers=self.headers)


class FlaskPystmarkInternalsTest(FlaskPystmarkTestBase):

    def setUp(self):
        super(FlaskPystmarkInternalsTest, self).setUp()
        self.unmocked_apply_config = Pystmark._apply_config

    def test_apply_config_defaults(self):
        d = self.p._apply_config(**dict(xxx='yyy'))
        self.assertEqual(d, dict(api_key=self.api_key, secure=True,
                                 test=False, xxx='yyy'))

    def test_apply_config_non_defaults(self):
        self.app.config['PYSTMARK_HTTPS'] = False
        self.app.config['PYSTMARK_TEST_API'] = True
        d = self.p._apply_config(**dict(xxx='yyy'))
        self.assertEqual(d, dict(api_key=self.api_key, secure=False,
                                 test=True, xxx='yyy'))

    def test_apply_config_non_defaults_but_overriding(self):
        self.app.config['PYSTMARK_HTTPS'] = False
        self.app.config['PYSTMARK_TEST_API'] = True
        kwargs = dict(api_key='zzz', secure=True, test=False, xxx='yyy')
        d = self.p._apply_config(**kwargs)
        self.assertEqual(d, kwargs)

    @patch.object(Pystmark, '_apply_config')
    @patch('flask_pystmark.send')
    def test_pystmark_call(self, mock_send, mock_apply_config):
        mock_apply_config.side_effect = self.unmocked_apply_config
        m = Message(text='hi')
        self.p._pystmark_call(mock_send, m)
        mock_apply_config.assert_called_once_with()
        mock_send.assert_called_with(m, api_key=self.api_key, test=False,
                                     secure=True)

    @patch.object(Pystmark, '_apply_config')
    @patch('flask_pystmark.send')
    def test_pystmark_call_req_args(self, mock_send, mock_apply_config):
        mock_apply_config.side_effect = self.unmocked_apply_config
        m = Message(text='hi')
        self.p._pystmark_call(mock_send, m, **self.req_args)
        mock_apply_config.assert_called_once_with(**self.req_args)
        mock_send.assert_called_with(m, api_key=self.api_key, test=False,
                                     secure=True, headers=self.headers)


class FlaskPystmarkMessageTest(FlaskPystmarkCreateTestBase):

    @patch('flask_pystmark._Message.__init__')
    def test_create(self, mock_init):
        Message()
        mock_init.assert_called_with(
            sender=None, reply_to=None, headers=None, verify=False, to=None,
            cc=None, bcc=None, subject=None, tag=None, html=None, text=None,
            attachments=None)

    @patch('flask_pystmark._Message.__init__')
    def test_create_with_configuration(self, mock_init):
        self.app.config['PYSTMARK_DEFAULT_SENDER'] = 'me@gmail.com'
        self.app.config['PYSTMARK_DEFAULT_REPLY_TO'] = 'you@gmail.com'
        headers = [dict(Name='x', Value='y')]
        self.app.config['PYSTMARK_DEFAULT_HEADERS'] = headers
        self.app.config['PYSTMARK_VERIFY_MESSAGES'] = True
        Message()
        mock_init.assert_called_with(
            sender='me@gmail.com', reply_to='you@gmail.com', headers=headers,
            verify=True, to=None, cc=None, bcc=None, subject=None, tag=None,
            html=None, text=None, attachments=None)

    @patch('flask_pystmark._Message.__init__')
    def test_create_with_configuration_but_overriding(self, mock_init):
        self.app.config['PYSTMARK_DEFAULT_SENDER'] = 'me@gmail.com'
        self.app.config['PYSTMARK_DEFAULT_REPLY_TO'] = 'you@gmail.com'
        headers = [dict(Name='x', Value='y')]
        self.app.config['PYSTMARK_DEFAULT_HEADERS'] = headers
        self.app.config['PYSTMARK_VERIFY_MESSAGES'] = True
        Message(sender='not_me@gmail.com', reply_to='not_you@gmail.com',
                headers=[], verify=False)
        mock_init.assert_called_with(
            sender='not_me@gmail.com', reply_to='not_you@gmail.com',
            headers=[], verify=False, to=None, cc=None, bcc=None, subject=None,
            tag=None, html=None, text=None, attachments=None)
