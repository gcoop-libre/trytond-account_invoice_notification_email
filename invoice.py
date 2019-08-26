# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
#from Crypto.Cipher import AES
import base64
from urllib.parse import (
    urlsplit, parse_qsl, urlencode, urlunsplit, quote, urljoin)

from trytond.config import config
from trytond.report import Report
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.url import HOSTNAME

USE_SSL = bool(config.get('ssl', 'certificate'))
URL_BASE = config.get('invoice_notification_email', 'automation_base',
    default=urlunsplit(
        ('http' + ('s' if USE_SSL else ''), HOSTNAME, '', '', '')))


class EmailSendInvoice(Report):
    __name__ = 'account.invoice.email_send_invoice'

    @classmethod
    def get_context(cls, records, data):
        context = super(EmailSendInvoice, cls).get_context(records, data)
        context['tw'] = "#"
        context['fb'] = "#"
        context['github'] = "#"
        context['logo'] = "#"
        context['vis_uri'] = "#"
        context['tw_uri'] = "#"
        context['fb_uri'] = "#"
        context['github_uri'] = "#"
        context['ts_uri'] = "#"
        context['pw_uri'] = "#"
        context['sp_uri'] = "#"
        context['faq_uri'] = "#"
        context['format_vi'] = cls.format_vi
        return context

    @classmethod
    def execute(cls, ids, data):
        Company = Pool().get('company.company')
        company = Company(Transaction().context.get('company'))
        res = super(EmailSendInvoice, cls).execute(ids, data)
        title = '[%s] te acerca tu factura' % company.rec_name
        return res[0], res[1], res[2], title

    @classmethod
    def format_vi(cls, r):
        def to_url(value):
            return base64.urlsafe_b64encode(value.encode('utf-8'))

        r = str(r)
        parts = urlsplit(urljoin(
                URL_BASE, quote('/%(database)s/i/report' % {
                        'database': Transaction().database.name,
                        })))
        query = parse_qsl(parts.query)
        query.append(('r', to_url(r)))
        parts = list(parts)
        parts[3] = urlencode(query)
        return urlunsplit(parts)
