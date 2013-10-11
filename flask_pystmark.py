from flask import current_app
from pystmark import (send, send_batch, get_delivery_stats, get_bounces,
                      get_bounce, get_bounce_dump, get_bounce_tags,
                      activate_bounce, Message as _Message)
from __about__ import __version__, __title__, __description__

__all__ = ['__version__', '__title__', '__description__', 'Pystmark',
           'Message']


class Pystmark(object):
    ''' A wrapper around the Simple API of pystmark.

    Refer to http://pystmark.readthedocs.org/en/latest/api.html#simple-api for
    more details.

    :param app: Flask app to initialize with. Defaults to `None`
    '''

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        ''' Initialize Pystmark with a Flask app '''
        app.pystmark = self

    def send(self, message, **request_args):
        '''Send a message.

        :param message: Message to send.
        :type message: `dict` or :class:`Message`
        :param \*\*request_args: Keyword arguments to pass to
            :func:`requests.request`.
        :rtype: :class:`pystmark.SendResponse`
        '''
        return self._pystmark_call(send, message, **request_args)

    def send_batch(self, messages, **request_args):
        '''Send a batch of messages.

        :param messages: Messages to send.
        :type message: A list of `dict` or :class:`Message`
        :param \*\*request_args: Keyword arguments to pass to
            :func:`requests.request`.
        :rtype: :class:`pystmark.BatchSendResponse`
        '''
        return self._pystmark_call(send_batch, messages, **request_args)

    def get_delivery_stats(self, **request_args):
        '''Get delivery stats for your Postmark account.

        :param \*\*request_args: Keyword arguments to pass to
            :func:`requests.request`.
        :rtype: :class:`pystmark.DeliveryStatsResponse`
        '''
        return self._pystmark_call(get_delivery_stats, **request_args)

    def get_bounces(self, **request_args):
        '''Get a paginated list of bounces.

        :param \*\*request_args: Keyword arguments to pass to
            :func:`requests.request`.
        :rtype: :class:`pystmark.BouncesResponse`
        '''
        return self._pystmark_call(get_bounces, **request_args)

    def get_bounce_tags(self, **request_args):
        '''Get a list of tags for bounces associated with your Postmark server.

        :param \*\*request_args: Keyword arguments to pass to
            :func:`requests.request`.
        :rtype: :class:`pystmark.BounceTagsResponse`
        '''
        return self._pystmark_call(get_bounce_tags, **request_args)

    def get_bounce(self, bounce_id, **request_args):
        '''Get a single bounce.

        :param bounce_id: The bounce's id. Get the id with :func:`get_bounces`.
        :param \*\*request_args: Keyword arguments to pass to
            :func:`requests.request`.
        :rtype: :class:`pystmark.BounceResponse`
        '''
        return self._pystmark_call(get_bounce, bounce_id, **request_args)

    def get_bounce_dump(self, bounce_id, **request_args):
        '''Get the raw email dump for a single bounce.

        :param bounce_id: The bounce's id. Get the id with :func:`get_bounces`.
        :param \*\*request_args: Keyword arguments to pass to
            :func:`requests.request`.
        :rtype: :class:`pystmark.BounceDumpResponse`
        '''
        return self._pystmark_call(get_bounce_dump, bounce_id, **request_args)

    def activate_bounce(self, bounce_id, **request_args):
        '''Activate a deactivated bounce.

        :param bounce_id: The bounce's id. Get the id with :func:`get_bounces`.
        :param \*\*request_args: Keyword arguments to pass to
            :func:`requests.request`.
        :rtype: :class:`pystmark.BounceActivateResponse`
        '''
        return self._pystmark_call(activate_bounce, bounce_id, **request_args)

    def _pystmark_call(self, method, *args, **kwargs):
        ''' Wraps a call to the pystmark Simple API, adding configured
        settings
        '''
        kwargs = self._apply_config(**kwargs)
        return method(*args, **kwargs)

    @staticmethod
    def _apply_config(**kwargs):
        '''Adds the current_app's pystmark configuration to a dict. If a
        configuration value has been specified in \*\*kwargs, it will not
        be overriden by the app's configuration.

        :param kwargs: Keyword arguments to be passed to the pystmark Simple
            API
        '''
        kwargs = dict(**kwargs)
        kwargs.setdefault('api_key', current_app.config['PYSTMARK_API_KEY'])
        kwargs.setdefault('secure', current_app.config.get('PYSTMARK_HTTPS',
                                                           True))
        kwargs.setdefault('test', current_app.config.get('PYSTMARK_TEST_API',
                                                         False))
        return kwargs


class Message(_Message):
    ''' A container for message(s) to send to the Postmark API.
    You can populate this message with defaults for initializing an
    :class:`Interface` from the pystmark library. The message will be combined
    with the final message and verified before transmission.

    Refer to http://pystmark.readthedocs.org/en/latest/api.html#message-object
    for more details.

    :param sender: Email address of the sender. Defaults to
        PYSTMARK_DEFAULT_SENDER if defined.
    :param to: Destination email address.
    :param cc: A list of cc'd email addresses.
    :param bcc: A list of bcc'd email address.
    :param subject: The message subject.
    :param tag: Tag your emails with this.
    :param html: HTML body content.
    :param text: Text body content.
    :param reply_to: Email address to reply to.  Defaults to
        PYSTMARK_DEFAULT_REPLY_TO, if defined.
    :param headers: Additional headers to include with the email. If you do
        not have the headers formatted for the Postmark API, use
        :meth:`Message.add_header`. Defaults to PYSTMARK_DEFAULT_HEADERS, if
        defined.
    :type headers: A list of `dict`, each with the keys 'Name' and
        'Value'.
    :param attachments: Attachments to include with the email. If you do not
        have the attachments formatted for the Postmark API, use
        :meth:`Message.attach_file` or :meth:`Message.attach_binary`.
    :type attachments: A list of `dict`, each with the keys 'Name',
        'Content' and 'ContentType'.
    :param verify: Verify the message when initialized.
        Defaults to PYSTMARK_VERIFY_MESSAGES if provided, otherwise `False`.
    '''

    def __init__(self, sender=None, to=None, cc=None, bcc=None, subject=None,
                 tag=None, html=None, text=None, reply_to=None, headers=None,
                 attachments=None, verify=None):
        if sender is None:
            sender = current_app.config.get('PYSTMARK_DEFAULT_SENDER')
        if reply_to is None:
            reply_to = current_app.config.get('PYSTMARK_DEFAULT_REPLY_TO')
        if headers is None:
            headers = current_app.config.get('PYSTMARK_DEFAULT_HEADERS')
        if verify is None:
            verify = current_app.config.get('PYSTMARK_VERIFY_MESSAGES', False)
        super(Message, self).__init__(sender=sender, to=to, cc=cc, bcc=bcc,
                                      subject=subject, tag=tag, html=html,
                                      text=text, reply_to=reply_to,
                                      headers=headers, attachments=attachments,
                                      verify=verify)
