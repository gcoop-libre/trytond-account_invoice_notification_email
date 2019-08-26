# The COPYRIGHT file at the top level of this repository contains the
# full copyright notices and license terms.

try:
    from trytond.modules.account_invoice_notification_email.tests.test_account_invoice_notification_email import suite
except ImportError:
    from .test_account_invoice_notification_email import suite

__all__ = ['suite']
