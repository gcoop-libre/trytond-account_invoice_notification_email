# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import base64
from werkzeug.wrappers import Response

from trytond.transaction import Transaction
from trytond.protocols.wrappers import with_pool, with_transaction
from trytond.wsgi import app


@app.route('/<database_name>/i/report', methods=['GET'])
@with_pool
@with_transaction(readonly=False)
def report(request, pool):

    def to_python(value):
        return base64.urlsafe_b64decode(value).decode('utf-8')

    Record = pool.get('account.invoice')
    Report = pool.get('account.invoice', type='report')
    record = Record(to_python(request.args['r']))
    data = {
        'model': Record.__name__,
        }
    with Transaction().set_context(language=record.company.party.lang):
        ext, content, _, _ = Report.execute([record.id], data)
    assert ext == 'pdf'
    return Response(content, 200, content_type='application/pdf')


@app.route('/i/empty.gif')
def empty(request):
    fp = file_open('marketing_automation/empty.gif', mode='rb')
    return Response(fp, 200, content_type='image/gif', direct_passthrough=True)
