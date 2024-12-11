from mock import patch, Mock, ANY
from datetime import date

from odoo.exceptions import UserError

from ..sc_test_case import SCTestCase
from ..helper_service import contract_fiber_create_data
from ...somoffice.errors import SomOfficeUserChangeEmailError


class TestPartnerEmailChangeWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.env.ref('somconnexio.res_partner_2_demo')
        vals_contract = contract_fiber_create_data(self.env, self.partner)
        self.Contract = self.env['contract.contract']
        self.contract = self.Contract.create(vals_contract)
        vals_contract_same_partner = vals_contract.copy()
        vals_contract_same_partner.update({
            'name': 'Test Contract Broadband B'
        })
        self.contract_same_partner = self.Contract.create(
            vals_contract_same_partner
        )
        self.partner_email_b = self.env["res.partner"].create({
            'name': 'Email b',
            'email': 'email_b@example.org',
            'type': 'contract-email',
            'parent_id': self.env.ref('somconnexio.res_partner_2_demo').id
        })
        self.user_admin = self.browse_ref('base.user_admin')
        self.expected_activity_args = {
            'res_model_id': self.env.ref('contract.model_contract_contract').id,
            'user_id': self.user_admin.id,
            'activity_type_id': self.env.ref('somconnexio.mail_activity_type_contract_data_change').id,  # noqa
            'date_done': date.today(),
            'date_deadline': date.today(),
            'summary': 'Email change',
            'done': True,
        }

    @patch(
        'odoo.addons.somconnexio.wizards.partner_email_change.partner_email_change.ChangePartnerEmails',  # noqa
        return_value=Mock(spec=["change_contracts_emails"])
    )
    def test_change_contracts_emails_one_email_change_ok(self, MockChangePartnerEmails):
        wizard = self.env['partner.email.change.wizard'].with_context(
            active_id=self.partner.id
        ).sudo(
            self.user_admin
        ).create({
            'change_contact_email': 'no',
            'change_contracts_emails': 'yes',
            'contract_ids': [(6, 0, [
                self.contract_same_partner.id, self.contract.id
            ])],
            'email_ids': [(6, 0, [self.partner_email_b.id])]
        })
        self.assertFalse('start_date' in dir(wizard))
        wizard.button_change()
        MockChangePartnerEmails.assert_called_once_with(
            ANY,
            self.partner
        )
        MockChangePartnerEmails.return_value.change_contracts_emails.assert_called_once_with(  # noqa
            self.Contract.browse([self.contract_same_partner.id, self.contract.id]),
            self.partner_email_b,
            self.expected_activity_args
        )

    @patch(
        'odoo.addons.somconnexio.wizards.partner_email_change.partner_email_change.ChangePartnerEmails',  # noqa
        return_value=Mock(spec=["change_contracts_emails"])
    )
    def test_change_contracts_emails_many_email_change_ok(
            self, MockChangePartnerEmails):
        self.env['partner.email.change.wizard'].with_context(
            active_id=self.partner.id
        ).sudo(
            self.user_admin
        ).create({
            'change_contact_email': 'no',
            'change_contracts_emails': 'yes',
            'contract_ids': [(6, 0, [
                self.contract_same_partner.id, self.contract.id
            ])],
            'email_ids': [(6, 0, [
                self.partner_email_b.id, self.partner.id
            ])]
        }).button_change()

        MockChangePartnerEmails.assert_called_once_with(
            ANY,
            self.partner
        )
        MockChangePartnerEmails.return_value.change_contracts_emails.assert_called_once_with(  # noqa
            self.Contract.browse([self.contract_same_partner.id, self.contract.id]),
            self.env["res.partner"].browse([self.partner_email_b.id, self.partner.id]),
            self.expected_activity_args
        )

    @patch(
        'odoo.addons.somconnexio.wizards.partner_email_change.partner_email_change.ChangePartnerEmails',  # noqa
        return_value=Mock(spec=[
            "change_contact_email",
            "change_somoffice_email"
        ])
    )
    def test_change_contact_email(
            self, MockChangePartnerEmails):

        self.env['partner.email.change.wizard'].with_context(
            active_id=self.partner.id
        ).sudo(
            self.user_admin
        ).create({
            'change_contact_email': 'yes',
            'change_contracts_emails': 'no',
            'email_id': self.partner_email_b.id
        }).button_change()

        MockChangePartnerEmails.assert_called_once_with(
            ANY,
            self.partner
        )
        MockChangePartnerEmails.return_value.change_contact_email.assert_called_once_with(  # noqa
            self.partner_email_b,
        )
        MockChangePartnerEmails.return_value.change_somoffice_email.assert_called_once_with(  # noqa
            self.partner_email_b,
        )

    @patch(
        'odoo.addons.somconnexio.wizards.partner_email_change.partner_email_change.ChangePartnerEmails',  # noqa
        return_value=Mock(spec=[
            "change_contact_email",
            "change_somoffice_email"
        ])
    )
    def test_change_contact_email_fail(
            self, MockChangePartnerEmails):
        MockChangePartnerEmails.return_value.change_somoffice_email.side_effect = SomOfficeUserChangeEmailError(self.partner.ref, "Error Text")  # noqa
        wizard = self.env['partner.email.change.wizard'].with_context(
            active_id=self.partner.id
        ).sudo(
            self.user_admin
        ).create({
            'change_contact_email': 'yes',
            'change_contracts_emails': 'no',
            'email_id': self.partner_email_b.id
        })
        self.assertRaises(
            UserError,
            wizard.button_change
        )
