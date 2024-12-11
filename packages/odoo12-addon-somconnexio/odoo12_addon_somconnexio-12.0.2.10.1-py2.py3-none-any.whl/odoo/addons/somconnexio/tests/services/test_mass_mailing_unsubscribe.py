import odoo
from ..common_service import BaseEMCRestCaseAdmin
import json
from odoo.tests import patch
HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


class MassMailingUnsubscribeService(BaseEMCRestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.mailing_list = self.env['mail.mass_mailing'].create({
            'name': 'A',
        })
        self.email = 'test@example.com'
        partner = self.env['res.partner'].create({
            'name': 'test',
            'email': self.email
        })
        self.res_id = 1
        self.token = self.mailing_list._unsubscribe_token(
            self.res_id, partner.email
        )

    @patch('odoo.addons.base.models.res_partner.Partner.write')
    def test_unsubscribe_call(self, partner_write):
        url = "http://{}:{}/mail/mailing/unsubscribe".format(HOST, PORT)
        data = {
            'jsonrpc': "2.0",
            'method': 'call',
            'params': {
                'mailing_id': self.mailing_list.id,
                'opt_in_ids': None,
                'opt_out_ids': None,
                'email': 'test@example.com',
                'res_id': self.res_id,
                'token': self.token
            },
            'id': 1234,
        }
        response = self.session.post(url, json=data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.text)['result'], True)
        partner_write.assert_called_with({'only_indispensable_emails': True})
