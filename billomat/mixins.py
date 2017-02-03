# -*- coding: UTF-8 -*-
from __future__ import unicode_literals, print_function

from . import base


class CompleteMixin(object):
    def complete(self, template_id=None):
        if template_id:
            data = {'complete': {'template_id': template_id}}
        else:
            data = {'complete': {}}

        self.objects.client.query(
            resource='%s/%s/complete' % (self.endpoint_name, self.id.value),
            method=base.Client.METHOD_PUT,
            data=data,
        )


class CancelMixin(object):
    def cancel(self):
        self.objects.client.query(
            resource='%s/%s/cancel' % (self.endpoint_name, self.id.value),
            method=base.Client.METHOD_PUT,
        )

    def uncancel(self):
        self.objects.client.query(
            resource='%s/%s/uncancel' % (self.endpoint_name, self.id.value),
            method=base.Client.METHOD_PUT,
        )


class SendEmailMixin(object):
    def send_email(self, recipient, email_template_id=None):
        email_data = {'recipients': {'to': recipient}}
        if email_template_id:
            email_data['email_template_id'] = email_template_id
        self.objects.client.query(
            resource='%s/%s/email' % (self.endpoint_name, self.id.value),
            method=base.Client.METHOD_POST,
            data={'email': email_data}
        )


class StatusAndEmailMixin(CompleteMixin, CancelMixin, SendEmailMixin):
    pass
