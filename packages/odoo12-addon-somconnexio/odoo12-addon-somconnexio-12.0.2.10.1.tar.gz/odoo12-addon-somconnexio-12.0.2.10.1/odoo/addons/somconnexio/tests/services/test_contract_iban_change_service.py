import odoo
import json

from mock import patch, Mock
from odoo.exceptions import UserError, ValidationError
from odoo.addons.easy_my_coop_api.tests.common import BaseEMCRestCase
from ...services.contract_iban_change_process import ContractIbanChangeProcess
from ..helper_service import contract_fiber_create_data
HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


class BaseEMCRestCaseAdmin(BaseEMCRestCase):
    @classmethod
    def setUpClass(cls, *args, **kwargs):
        # Skip parent class in super to avoid recreating api key
        super(BaseEMCRestCase, cls).setUpClass(*args, **kwargs)

    def http_public_post(self, url, data, headers=None):
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.post(url, json=data)


class TestContractIBANChangeService(BaseEMCRestCaseAdmin):

    def setUp(self, *args, **kwargs):
        super().setUp()
        self.Contract = self.env["contract.contract"]
        self.partner = self.browse_ref("somconnexio.res_partner_2_demo")
        self.partner_ref = self.partner.ref
        partner_id = self.partner.id
        self.bank_b = self.env['res.partner.bank'].create({
            'acc_number': 'ES1720852066623456789011',
            'partner_id': partner_id
        })
        self.iban = 'ES6700751951971875361545'
        self.bank_new = self.env['res.partner.bank'].create({
            'acc_number': self.iban,
            'partner_id': partner_id
        })
        self.banking_mandate = self.partner.bank_ids[0].mandate_ids[0]
        self.banking_mandate_new = self.env['account.banking.mandate'].search([
            ('partner_bank_id', '=', self.bank_new.id),
        ])
        vals_contract = contract_fiber_create_data(self.env, self.partner)
        self.contract = self.env['contract.contract'].create(vals_contract)
        vals_contract_same_partner = vals_contract.copy()
        vals_contract_same_partner.update({
            'name': 'Test Contract Broadband B',
            'code': 'contract2test',
        })
        self.contract_same_partner = self.env['contract.contract'].with_context(
            tracking_disable=True
        ).create(
            vals_contract_same_partner
        )
        self.url = "/public-api/contract-iban-change"

    def test_route_right_run_wizard_all_contracts(self):
        data = {
            "partner_id": self.partner_ref,
            "iban": self.iban,
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        process.run_from_api(**data)
        self.assertEquals(self.contract.mandate_id, self.banking_mandate_new)
        self.assertEquals(
            self.contract_same_partner.mandate_id, self.banking_mandate_new
        )

    def test_route_right_run_wizard_one_contract(self):
        data = {
            "partner_id": self.partner_ref,
            "iban": self.iban,
            "contracts": "{}".format(self.contract.code)
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        process.run_from_api(**data)
        self.assertEquals(self.contract.mandate_id, self.banking_mandate_new)
        self.assertEquals(self.contract_same_partner.mandate_id, self.banking_mandate)

    def test_route_right_run_wizard_many_contracts(self):
        data = {
            "partner_id": self.partner_ref,
            "iban": self.iban,
            "contracts": "{};{}".format(
                self.contract.code, self.contract_same_partner.code
            )
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        process.run_from_api(**data)
        self.assertEquals(self.contract.mandate_id, self.banking_mandate_new)
        self.assertEquals(
            self.contract_same_partner.mandate_id, self.banking_mandate_new
        )

    def test_route_right_new_iban_existing_bank(self):
        missing_iban = 'ES6621000418401234567891'
        data = {
            "partner_id": self.partner_ref,
            "iban": missing_iban,
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        process.run_from_api(**data)
        acc_number = self.contract.mandate_id.partner_bank_id.acc_number
        self.assertEquals(
            acc_number.replace(' ', '').upper(),
            missing_iban
        )
        acc_number = self.contract_same_partner.mandate_id.partner_bank_id.acc_number
        self.assertEquals(
            acc_number.replace(' ', '').upper(),
            missing_iban
        )

    def test_route_right_new_iban_inexisting_bank(self):

        missing_bank_iban = 'LB913533I8Z6LY1FA76J5FYR3V5L'
        data = {
            "partner_id": self.partner_ref,
            "iban": missing_bank_iban,
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        self.assertRaisesRegex(
            ValidationError,
            'Invalid bank',
            process.run_from_api,
            **data
        )

    def test_route_bad_iban(self):
        data = {
            "partner_id": self.partner_ref,
            "iban": 'XXX',
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEqual(decoded_response, {"result": "OK"})

        with self.assertRaises(ValidationError):
            process = ContractIbanChangeProcess(self.env)
            process.run_from_api(**data)

    def test_route_bad_bank_inactive(self):
        self.browse_ref("l10n_es_partner.res_bank_es_2100").write({"active": False})
        data = {
            "partner_id": self.partner_ref,
            "iban": 'ES6621000418401234567891',
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        self.assertRaisesRegex(
            ValidationError,
            'Invalid bank',
            process.run_from_api,
            **data
        )

    def test_route_bad_unexpected_iban_error(self):
        self.partner.customer = False
        missing_iban = 'ES1000492352082414205416'
        data = {
            "partner_id": self.partner_ref,
            "iban": missing_iban,
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        self.assertRaises(UserError, process.run_from_api, **data)

    def test_route_bad_contract(self):
        data = {
            "partner_id": self.partner_ref,
            "iban": self.iban,
            "contracts": "{};XXX".format(self.contract)
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        self.assertRaises(UserError, process.run_from_api, **data)

    def test_route_missing_iban(self):
        data = {
            "partner_id": self.partner_ref,
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        self.assertRaises(UserError, process.run_from_api, **data)

    def test_route_missing_partner_id(self):
        data = {
            "iban": self.iban,
        }
        response = self.http_public_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})
        process = ContractIbanChangeProcess(self.env)
        self.assertRaises(UserError, process.run_from_api, **data)

    @patch('odoo.addons.somconnexio.wizards.contract_iban_change.contract_iban_change.UpdateTicketWithError',  # noqa
           return_value=Mock(spec_set=["run", "article", "ticket_id", "df_dct"]))
    def test_route_notify_OTRS_new_iban_inexisting_bank(
            self, MockUpdateTicketWithError):
        missing_bank_iban = 'LB913533I8Z6LY1FA76J5FYR3V5L'
        data = {
            "partner_id": self.partner.ref,
            "iban": missing_bank_iban,
            "ticket_id": "12352"
        }
        expected_error = {
            "title": "Error en el canvi d'IBAN",
            "body": "Banc del nou IBAN desconegut: {}.\n".format(missing_bank_iban) +
                    "Després d'afegir el seu banc corresponent al registre d'ODOO, " +
                    "torna a intentar aquesta petició."
        }
        self.env['contract.iban.change.wizard'].run_from_api(**data)

        MockUpdateTicketWithError.assert_called_once_with(
            data["ticket_id"],
            expected_error,
            {"ibanKO": 1}
        )
        MockUpdateTicketWithError.return_value.run.assert_called_once_with()


class TestContractIBANChangeServiceJob(BaseEMCRestCaseAdmin):

    @classmethod
    def setUpClass(cls):
        super(TestContractIBANChangeServiceJob, cls).setUpClass()
        # disable tracking test suite wise
        cls.env = cls.env(context=dict(
            cls.env.context,
            tracking_disable=True,
            test_queue_job_no_delay=False,
        ))

    def test_route_enqueue_job_change_iban(self):
        jobs_domain = [
            ('method_name', '=', 'run_from_api'),
            ('model_name', '=', 'contract.iban.change.wizard'),
        ]
        queued_jobs_before = self.env['queue.job'].search(jobs_domain)
        self.assertFalse(queued_jobs_before)

        url = "/public-api/contract-iban-change"
        partner = self.browse_ref('somconnexio.res_partner_2_demo')
        data = {
            "partner_id": partner.ref,
            "iban": "ES1720852066623456789011",
        }
        response = self.http_public_post(url, data=data)

        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})

        queued_jobs_after = self.env['queue.job'].search(jobs_domain)
        self.assertEquals(len(queued_jobs_after), 1)
