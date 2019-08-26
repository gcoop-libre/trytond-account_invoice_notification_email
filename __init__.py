# This file is part account_invoice_notification_email module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from . import invoice
from . import routes

__all__ = ['register', 'routes']


def register():
    Pool.register(
        invoice.EmailSendInvoice,
        module='account_invoice_notification_email', type_='report')
