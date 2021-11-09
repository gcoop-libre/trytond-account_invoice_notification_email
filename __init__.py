# This file is part account_invoice_notification_email module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import invoice


def register():
    Pool.register(
        invoice.Invoice,
        module='account_invoice_notification_email', type_='model')
    Pool.register(
        invoice.InvoiceTriggerEmail,
        module='account_invoice_notification_email', type_='wizard')
    Pool.register(
        invoice.InvoiceReport,
        invoice.EmailSendInvoice,
        module='account_invoice_notification_email', type_='report')
