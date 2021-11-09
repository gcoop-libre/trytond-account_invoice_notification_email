# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
#from Crypto.Cipher import AES
import base64
from urllib.parse import (
    urlsplit, parse_qsl, urlencode, urlunsplit, quote, urljoin)

from trytond.model import fields
from trytond.wizard import Wizard, StateTransition
from trytond.report import Report
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.config import config
from trytond.url import HOSTNAME

USE_SSL = bool(config.get('ssl', 'certificate'))
URL_BASE = config.get('invoice_notification_email', 'automation_base',
    default=urlunsplit(
        ('http' + ('s' if USE_SSL else ''), HOSTNAME, '', '', '')))


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    email_sent = fields.Boolean('Email sent', readonly=True)

    @staticmethod
    def default_email_sent():
        return False

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._check_modify_exclude.update({'email_sent'})

    @classmethod
    def trigger_email(cls, invoices):
        cls._trigger_email(invoices, False)
        cls._trigger_email(invoices, True)

    @classmethod
    def _trigger_email(cls, invoices, boolean):
        to_write = []
        for invoice in invoices:
            if invoice.state not in {'posted', 'paid'}:
                continue
            to_write.append([invoice])
            to_write.append({'email_sent': boolean})
        if to_write:
            cls.write(*to_write)


class EmailSendInvoice(Report):
    __name__ = 'account.invoice.email_send_invoice'

    @classmethod
    def get_context(cls, records, header, data):
        context = super().get_context(records, header, data)
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
        res = super().execute(ids, data)
        title = '[%s] te acerca tu comprobante' % company.rec_name
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


class InvoiceReport(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def execute(cls, ids, data):
        Invoice = Pool().get('account.invoice')

        res = super().execute(ids, data)
        if len(ids) > 1:
            res = (res[0], res[1], True, res[3])
        else:
            invoice = Invoice(ids[0])
            report_name = 'comprobante'
            periodo = ''
            if invoice.invoice_date:
                periodo = invoice.invoice_date.strftime("%m%Y")
            else:
                periodo = str(invoice.id)
            if invoice.party:
                report_name = '%s-%s' % (report_name, invoice.party.rec_name)

            report_name += '-%s' % periodo

            if invoice.number:
                report_name = '%s-%s' % (report_name, invoice.number)

            res = (res[0], res[1], res[2], report_name)
        return res


class InvoiceTriggerEmail(Wizard):
    'Invoice Trigger Email'
    __name__ = 'account.invoice.trigger_email'

    start_state = 'trigger_email'
    trigger_email = StateTransition()

    def transition_trigger_email(self):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        invoices = Invoice.browse(Transaction().context['active_ids'])
        if invoices:
            Invoice.trigger_email(invoices)
        return 'end'
