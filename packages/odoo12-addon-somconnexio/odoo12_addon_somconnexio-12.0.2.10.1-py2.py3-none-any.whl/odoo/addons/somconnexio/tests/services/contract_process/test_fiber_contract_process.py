from datetime import date, datetime, timedelta

from mock import Mock, call, patch

from ...helper_service import crm_lead_create
from .base_test_contract_process import BaseContractProcessTestCase


@patch("pyopencell.resources.subscription.Subscription.get")
@patch(
    "odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractCreateService"  # noqa
)
class TestFiberContractProcess(BaseContractProcessTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            "partner_id": self.partner.ref,
            "email": self.partner.email,
            "service_address": self.service_address,
            "service_technology": "Fiber",
            "service_supplier": "Vodafone",
            "vodafone_fiber_contract_service_info": {
                "phone_number": "654123456",
                "vodafone_offer_code": "offer",
                "vodafone_id": "123",
            },
            "fiber_signal_type": "NEBAFTTH",
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref("somconnexio.Fibra100Mb").default_code
                    ),
                    "date_start": "2020-01-01 00:00:00",
                }
            ],
            "iban": self.iban,
            "ticket_number": self.ticket_number,
            "mandate": self.mandate,
        }
        mobile_product = self.browse_ref(
            'somconnexio.TrucadesIllimitades10GB')
        mobile_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'icc': '123'
        })
        contract_line = {
            "name": mobile_product.showed_name,
            "product_id": mobile_product.id,
            "date_start": "2020-01-01 00:00:00",
        }
        self.vals_mobile_contract = {
            'name': 'New Contract Mobile',
            'partner_id': self.partner.id,
            'invoice_partner_id': self.partner.id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_mobile"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_masmovil"
            ),
            'mobile_contract_service_info_id': (
                mobile_contract_service_info.id
            ),
            'contract_line_ids': [(0, 0, contract_line)],
            'mandate_id': self.mandate.id,
        }
        self.mbl_contract_linked_email_template = self.browse_ref(
            'somconnexio.mobile_linked_with_fiber_email_template')
        self.mbl_contract_to_link_email_template = self.browse_ref(
            'somconnexio.mobile_to_link_with_fiber_email_template')
        self.data_xoln = {**self.data}
        del self.data_xoln["vodafone_fiber_contract_service_info"]
        self.data_xoln["service_supplier"] = "XOLN"
        self.data_xoln["xoln_fiber_contract_service_info"] = {
            "phone_number": "962911963",
            "external_id": "123",
            "id_order": "1",
            "project": self.browse_ref("somconnexio.xoln_project_borda").code,
            "router_product_id": self.browse_ref("somconnexio.Fibra100Mb").default_code,
            "router_serial_number": "XXX",
        }
        self.process = self.env["fiber.contract.process"]

    def test_create_fiber(self, *args):
        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"],
        )

    def test_create_fiber_asociatel(self, *args):
        self.data.update(
            {
                "service_supplier": "Asociatel VDF",
            }
        )
        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"]
        )

    def test_create_fiber_wo_vodafone_offer_code(self, *args):
        self.data["vodafone_fiber_contract_service_info"]["vodafone_offer_code"] = ""

        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertTrue(contract)

    def test_create_fiber_xoln(self, *args):
        content = self.process.create(**self.data_xoln)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data_xoln["xoln_fiber_contract_service_info"]["phone_number"],
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.MobileActivationDateService"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.SetFiberContractCodeMobileTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._relate_new_fiber_with_existing_mobile_contracts"  # noqa
    )
    def test_create_fiber_unblock_mobile_ticket(
        self,
        mock_relate_with_mobile,
        SetFiberContractCodeMock,
        UnblockMobilePackTicketMock,
        MobileActivationDateServiceMock,
        *args
    ):

        expected_date = date(2023, 10, 10)
        MobileActivationDateServiceMock.return_value.get_activation_date.return_value = (  # noqa
            expected_date
        )
        MobileActivationDateServiceMock.return_value.get_introduced_date.return_value = (  # noqa
            expected_date
        )
        pack_code = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        ).default_code
        new_ticket_number = "123454321"
        crm_lead = crm_lead_create(self.env, self.partner, "pack", portability=False)
        for line in crm_lead.lead_line_ids:
            if line.product_id.default_code == pack_code:
                line.ticket_number = new_ticket_number
            else:
                line.ticket_number = self.ticket_number

        content = self.process.create(**self.data)

        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"]
        )

        UnblockMobilePackTicketMock.assert_called_once_with(
            new_ticket_number,
            activation_date=str(expected_date),
            introduced_date=str(expected_date),
        )
        UnblockMobilePackTicketMock.return_value.run.assert_called_once_with()

        SetFiberContractCodeMock.assert_called_once_with(
            new_ticket_number,
            fiber_contract_code=contract.code
        )

        mock_relate_with_mobile.assert_called_once_with(
            {
                "id": contract.id,
                "code": contract.code,
                "partner_id": contract.partner_id.id,
                "ticket_number": contract.ticket_number,
                "create_reason": contract.create_reason,
            }
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.SetFiberContractCodeMobileTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._relate_new_fiber_with_existing_mobile_contracts"  # noqa
    )
    def test_create_fiber_unblock_mobile_ticket_without_set_fiber_contract_code(
        self, mock_relate_with_mobile, SetFiberContractCodeMock,
        UnblockMobilePackTicketMock, *args
    ):
        no_pack_product = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GB"
        )
        new_ticket_number = "123454321"
        crm_lead = crm_lead_create(
            self.env,
            self.partner,
            "pack",
            portability=False,
        )
        for line in crm_lead.lead_line_ids:
            if line.is_mobile:
                line.product_id = no_pack_product.id
                line.ticket_number = new_ticket_number
            else:
                line.ticket_number = self.ticket_number

        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"]
        )
        UnblockMobilePackTicketMock.return_value.run.assert_called_once_with()

        SetFiberContractCodeMock.assert_not_called()

        mock_relate_with_mobile.assert_called_once_with(
            {
                "id": contract.id,
                "code": contract.code,
                "partner_id": contract.partner_id.id,
                "ticket_number": contract.ticket_number,
                "create_reason": contract.create_reason,
            }
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.MobileActivationDateService"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.SetFiberContractCodeMobileTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._relate_new_fiber_with_existing_mobile_contracts"  # noqa
    )
    def test_create_fiber_unblock_shared_mobile_tickets(
        self,
        mock_relate_with_mobile,
        SetFiberContractCodeMock,
        UnblockMobilePackTicketMock,
        MobileActivationDateServiceMock,
        *args
    ):
        expected_date = date(2023, 10, 10)
        MobileActivationDateServiceMock.return_value.get_activation_date.return_value = (  # noqa
            expected_date
        )
        MobileActivationDateServiceMock.return_value.get_introduced_date.return_value = (  # noqa
            expected_date
        )
        crm_lead = crm_lead_create(
            self.env,
            self.partner,
            "pack",
            portability=False,
        )
        crm_lead_line = crm_lead.lead_line_ids.filtered("is_mobile").copy()
        crm_lead.write({"crm_lead_lines": [(4, crm_lead_line.id, 0)]})
        shared_product = self.browse_ref(
            "somconnexio.50GBCompartides2mobils"
        )
        first_ticket_number = "123456"
        second_ticket_number = "234567"

        mobile_lines = crm_lead.lead_line_ids.filtered("is_mobile")
        mobile_lines[0].product_id = shared_product.id
        mobile_lines[0].ticket_number = first_ticket_number
        mobile_lines[1].product_id = shared_product.id
        mobile_lines[1].ticket_number = second_ticket_number
        fiber_line = crm_lead.lead_line_ids.filtered("is_fiber")
        fiber_line.ticket_number = self.ticket_number

        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(
            contract.name,
            self.data["vodafone_fiber_contract_service_info"]["phone_number"]
        )

        UnblockMobilePackTicketMock.assert_has_calls(
            [
                call(
                    first_ticket_number,
                    activation_date=str(expected_date),
                    introduced_date=str(expected_date),
                ),
                call(
                    second_ticket_number,
                    activation_date=str(expected_date),
                    introduced_date=str(expected_date),
                ),
            ],
            any_order=True
        )

        SetFiberContractCodeMock.assert_has_calls(
            [
                call(first_ticket_number,
                     fiber_contract_code=contract.code),
                call(second_ticket_number,
                     fiber_contract_code=contract.code),
            ],
            any_order=True
        )

        mock_relate_with_mobile.assert_called_once_with(
            {
                "id": contract.id,
                "code": contract.code,
                "partner_id": contract.partner_id.id,
                "ticket_number": contract.ticket_number,
                "create_reason": contract.create_reason,
            }
        )

    def test_create_fiber_relate_with_mobile_pack(self, *args):
        # Crear un Contrato de mobil
        contract_product = self.env.ref("somconnexio.TrucadesIllimitades20GBPack")
        mobile_contract_service_info = self.env["mobile.service.contract.info"].create(
            {"phone_number": "654987654", "icc": "123"}
        )
        contract_line = {
            "name": contract_product.name,
            "product_id": contract_product.id,
            "date_start": datetime.now() - timedelta(days=12),
        }
        vals_contract = {
            "name": "Test Contract Mobile",
            "code": "12345",
            "partner_id": self.partner.id,
            "invoice_partner_id": self.partner.id,
            "service_technology_id": self.ref("somconnexio.service_technology_mobile"),
            "service_supplier_id": self.ref("somconnexio.service_supplier_masmovil"),
            "mobile_contract_service_info_id": mobile_contract_service_info.id,
            "contract_line_ids": [(0, 0, contract_line)],
            "email_ids": [(6, 0, [self.partner.id])],
        }
        mobile_contract = self.env["contract.contract"].create(vals_contract)

        # Añadir al data el contrato vinculado
        data = self.data.copy()
        data["mobile_pack_contracts"] = mobile_contract.code

        content = self.process.create(**data)
        contract = self.env["contract.contract"].browse(content["id"])

        # Revisar que el contrato de fibra tiene como childs al contrato de mobil
        self.assertEquals(
            mobile_contract,
            contract.children_pack_contract_ids,
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._update_pack_mobile_tickets"  # noqa
    )
    def test_relate_with_mobile_pack_change_address(
        self, mock_update_pack_mobile_tickets, *args
    ):
        """
        Check that with change address process, mobile products are
        linked to new fiber contract
        """

        mbl_contract_1 = self.env['contract.contract'].create(
            self.vals_mobile_contract
        )
        mbl_contract_2 = self.env['contract.contract'].create(
            self.vals_mobile_contract
        )

        self.assertFalse(mbl_contract_1.parent_pack_contract_id)
        self.assertFalse(mbl_contract_2.parent_pack_contract_id)

        self.data["mobile_pack_contracts"] = "{},{}".format(
            mbl_contract_1.code, mbl_contract_2.code)

        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])

        self.assertEquals(
            mbl_contract_1.parent_pack_contract_id, contract
        )
        self.assertEquals(
            mbl_contract_2.parent_pack_contract_id, contract
        )
        mock_update_pack_mobile_tickets.assert_called_once()

    @patch(
        "odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ContractMobileTariffChangeWizard.create",  # noqa
        return_value=Mock(spec=['button_change'])
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._update_pack_mobile_tickets"  # noqa
    )
    @patch('odoo.addons.mail.models.mail_template.MailTemplate.send_mail')
    def test_relate_with_one_existing_mobile_contract(
        self, mock_send_email, mock_update_pack_mobile_tickets,
        mock_change_tariff_create, *args
    ):
        """
        Check if a fiber is created with an existing unpacked mobile
        contract with an appropiate tariff to become pack, a mobile change
        tariff wizard is created
        """
        pack_mobile_product_id = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        ).id

        # Create packable mobile contract
        mbl_contract = self.env['contract.contract'].create(
            self.vals_mobile_contract
        )
        content = self.process.create(**self.data)

        mock_change_tariff_create.assert_called_once_with(
            {
                "summary": "Automatic mobile tariff change",
                "new_tariff_product_id": pack_mobile_product_id,
                "fiber_contract_to_link": content["id"],
                "exceptional_change": True,
                "otrs_checked": True,
                "send_notification": False,
            }
        )
        mock_change_tariff_create.return_value.button_change.assert_called_once_with()  # noqa
        mock_update_pack_mobile_tickets.assert_called_once()
        mock_send_email.assert_called_with(
            mbl_contract.id,
            email_values=None, force_send=False,
            notif_layout=False, raise_exception=False
        )  # TODO: how to check from which mail template is called?

    @patch(
        "odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ContractMobileTariffChangeWizard.create"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._update_pack_mobile_tickets"  # noqa
    )
    @patch('odoo.addons.mail.models.mail_template.MailTemplate.send_mail')
    def test_relate_with_more_than_one_existing_mobile_contract(
        self, mock_send_email, mock_update_pack_mobile_tickets,
        mock_change_tariff_create, *args
    ):
        """
        Check if a fiber is created with more than one unpacked mobile
        contract with an appropiate tariff to become pack, no mobile
        change is done automatically but a mail is send
        """

        # Create 2 packable mobile contract
        self.env['contract.contract'].create(self.vals_mobile_contract)
        self.env['contract.contract'].create(self.vals_mobile_contract)

        self.process.create(**self.data)

        mock_change_tariff_create.assert_not_called()
        mock_update_pack_mobile_tickets.assert_called_once()
        mock_send_email.assert_called_with(
            self.partner.id,
            email_values=None, force_send=False,
            notif_layout=False, raise_exception=False
        )  # TODO: how to check from which mail template is called?

    @patch(
        "odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ContractMobileTariffChangeWizard.create"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._update_pack_mobile_tickets"  # noqa
    )
    @patch('odoo.addons.mail.models.mail_template.MailTemplate.send_mail')
    def test_relate_with_one_non_packable_mobile_contract(
        self, mock_send_email, mock_update_pack_mobile_tickets,
        mock_change_tariff_create, *args
    ):
        """
        Check if a fiber is created without any mobile
        contract with an appropiate tariff to become pack,
        no change is done
        """

        non_pack_mbl_product = self.browse_ref('somconnexio.150Min1GB')
        contract = self.env['contract.contract'].create(self.vals_mobile_contract)
        contract.contract_line_ids[0].product_id = non_pack_mbl_product.id

        self.process.create(**self.data)

        mock_send_email.assert_not_called()
        mock_change_tariff_create.assert_not_called()
        mock_update_pack_mobile_tickets.assert_called_once()

    @patch(
        "odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ContractMobileTariffChangeWizard.button_change"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._update_pack_mobile_tickets"  # noqa
    )
    @patch('odoo.addons.mail.models.mail_template.MailTemplate.send_mail')
    def test_relate_with_one_mobile_contract_having_CRM_with_pack_product(
        self, mock_send_email, mock_update_pack_mobile_tickets,
        mock_change_tariff_create, *args
    ):
        """
        Check if a fiber is created with an existing unpacked mobile
        contract with an appropiate tariff to become pack, if fiber
        CRM also has a mobile pack petition, no change is done
        """

        # Create packable mobile contract
        self.env['contract.contract'].create(self.vals_mobile_contract)

        crm_lead = crm_lead_create(
            self.env,
            self.partner,
            "pack",
            portability=False,
        )
        fiber_lead_line = crm_lead.lead_line_ids.filtered('is_fiber')
        fiber_lead_line.ticket_number = self.ticket_number

        self.process.create(**self.data)

        mock_send_email.assert_not_called()
        mock_change_tariff_create.assert_not_called()
        mock_update_pack_mobile_tickets.assert_called_once()

    @patch(
        "odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ContractMobileTariffChangeWizard.button_change"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._update_pack_mobile_tickets"  # noqa
    )
    @patch('odoo.addons.mail.models.mail_template.MailTemplate.send_mail')
    def test_relate_with_one_mobile_contract_location_change_case(
        self, mock_send_email, mock_update_pack_mobile_tickets,
        mock_change_tariff_create, *args
    ):
        """
        Check that if a location_change fiber is created no mobile contract
        is related with it
        """

        crm_lead = crm_lead_create(
            self.env, self.partner, "pack", portability=False
        )
        fiber_lead_line = crm_lead.lead_line_ids.filtered('is_fiber')
        fiber_lead_line.ticket_number = self.ticket_number
        fiber_lead_line.create_reason = "location_change"

        # Create packable mobile contract
        self.env['contract.contract'].create(self.vals_mobile_contract)

        contract = self.process.create(**self.data)

        mock_send_email.assert_not_called()
        mock_change_tariff_create.assert_not_called()
        mock_update_pack_mobile_tickets.assert_called_once()
        self.assertEquals(contract["create_reason"], "location_change")

    @patch(
        "odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ContractMobileTariffChangeWizard.create",  # noqa
        return_value=Mock(spec=['button_change'])
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess._update_pack_mobile_tickets"  # noqa
    )
    @patch('odoo.addons.mail.models.mail_template.MailTemplate.send_mail')
    def test_relate_with_one_mobile_contract_having_CRM_wo_pack_product(
        self, mock_send_email, mock_update_pack_mobile_tickets,
        mock_change_tariff_create, *args
    ):
        """
        Check if a fiber is created with an existing unpacked mobile
        contract with an appropiate tariff to become pack, if fiber
        CRM does not have a mobile pack petition, a mobile change
        tariff wizard is created with the fiber contract code
        """

        non_pack_mbl_product = self.browse_ref('somconnexio.150Min1GB')
        pack_mobile_product_id = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        ).id

        # Create packable mobile contract
        mbl_contract = self.env["contract.contract"].create(self.vals_mobile_contract)
        crm_lead = crm_lead_create(self.env, self.partner, "pack", portability=False)
        fiber_lead_line = crm_lead.lead_line_ids.filtered("is_fiber")
        fiber_lead_line.ticket_number = self.ticket_number
        mobile_lead_line = crm_lead.lead_line_ids.filtered("is_mobile").filtered(
            "is_from_pack"
        )
        mobile_lead_line.product_id = non_pack_mbl_product.id

        content = self.process.create(**self.data)

        mock_change_tariff_create.assert_called_once_with(
            {
                "summary": "Automatic mobile tariff change",
                "new_tariff_product_id": pack_mobile_product_id,
                "fiber_contract_to_link": content["id"],
                "exceptional_change": True,
                "otrs_checked": True,
                "send_notification": False,
            }
        )
        mock_change_tariff_create.return_value.button_change.assert_called_once_with()  # noqa
        mock_update_pack_mobile_tickets.assert_called_once()

        mock_send_email.assert_called_with(
            mbl_contract.id,
            email_values=None, force_send=False,
            notif_layout=False, raise_exception=False
        )  # TODO: how to check from which mail template is called?
