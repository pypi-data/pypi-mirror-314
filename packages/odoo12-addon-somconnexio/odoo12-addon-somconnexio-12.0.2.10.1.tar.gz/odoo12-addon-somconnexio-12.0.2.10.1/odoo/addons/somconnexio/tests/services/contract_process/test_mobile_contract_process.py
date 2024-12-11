from mock import patch
from odoo.exceptions import UserError

from ...helper_service import crm_lead_create
from .base_test_contract_process import BaseContractProcessTestCase


@patch("pyopencell.resources.subscription.Subscription.get")
@patch(
    "odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractCreateService"  # noqa
)
class TestMobileContractProcess(BaseContractProcessTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            "partner_id": self.partner.ref,
            "email": self.partner.email,
            "service_technology": "Mobile",
            "service_supplier": "MásMóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
            },
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref("somconnexio.150Min1GB").default_code
                    ),
                    "date_start": "2020-01-01 00:00:00",
                }
            ],
            "iban": self.iban,
            "ticket_number": self.ticket_number,
        }
        self.pack_code = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        ).default_code
        self.mobile_ticket_number = "123454321"
        self.fiber_ticket_number = "543212345"

        self.fiber_contract_data = {
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
            "ticket_number": self.fiber_ticket_number,
        }
        other_partner = self.browse_ref("somconnexio.res_partner_1_demo")
        sharing_product = self.browse_ref("somconnexio.50GBCompartides2mobils")
        self.sharing_mobile_data = {
            "partner_id": other_partner.ref,
            "email": other_partner.email,
            "service_technology": "Mobile",
            "service_supplier": "MásMóvil",
            "mobile_contract_service_info": {
                "phone_number": "654321123",
                "icc": "123456",
                "shared_bond_id": "",
            },
            "contract_lines": [
                {
                    "product_code": sharing_product.default_code,
                    "date_start": "2020-01-01 00:00:00",
                }
            ],
            "iban": other_partner.bank_ids[0].acc_number,
            "ticket_number": self.ticket_number,
        }
        self.process = self.env["mobile.contract.process"]

    def test_contract_create(self, *args):
        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertIn(
            self.browse_ref("somconnexio.150Min1GB"),
            [c.product_id for c in contract.contract_line_ids],
        )

    def test_contract_create_with_shared_data(self, *args):
        shared_bond_id = "AAAA"

        mobile_content = self.data.copy()
        mobile_content["mobile_contract_service_info"].update(
            {"shared_bond_id": shared_bond_id}
        )

        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEqual(
            contract.mobile_contract_service_info_id.shared_bond_id, shared_bond_id
        )

    # TODO -> Remove this when OTRS stops sending an empty dict
    def test_contract_create_with_empty_shared_data(self, *args):
        shared_bond_id = {}

        mobile_content = self.data.copy()
        mobile_content["mobile_contract_service_info"].update(
            {"shared_bond_id": shared_bond_id}
        )

        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertFalse(
            contract.mobile_contract_service_info_id.shared_bond_id,
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.SetFiberContractCodeMobileTicket"  # noqa
    )
    def test_create_mobile_pack_contract_link_parent_contract(
        self, *args
    ):
        crm_lead = crm_lead_create(
            self.env,
            self.partner,
            "pack",
            portability=False,
        )
        for line in crm_lead.lead_line_ids:
            if line.product_id.default_code == self.pack_code:
                line.ticket_number = self.mobile_ticket_number
            else:
                line.ticket_number = self.fiber_ticket_number

        fiber_content = self.env["fiber.contract.process"].create(
            **self.fiber_contract_data
        )
        fiber_contract = self.env["contract.contract"].browse(fiber_content["id"])
        mobile_content = self.data
        mobile_content.update(
            {
                "ticket_number": self.mobile_ticket_number,
                "contract_lines": [
                    {
                        "product_code": self.pack_code,
                        "date_start": "2020-01-01 00:00:00",
                    }
                ],
            }
        )
        mobile_content = self.process.create(**self.data)
        mobile_contract = self.env["contract.contract"].browse(mobile_content["id"])
        self.assertEqual(
            mobile_contract.parent_pack_contract_id,
            fiber_contract,
        )
        self.assertEqual(mobile_contract.number_contracts_in_pack, 2)
        self.assertTrue(mobile_contract.is_pack)

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.SetFiberContractCodeMobileTicket"  # noqa
    )
    def test_create_mobile_pack_contract_link_with_contract_line(
        self, *args
    ):
        crm_lead = crm_lead_create(
            self.env,
            self.partner,
            "pack",
            portability=False,
        )
        for line in crm_lead.lead_line_ids:
            if line.product_id.default_code == self.pack_code:
                line.ticket_number = self.mobile_ticket_number
            else:
                line.ticket_number = self.fiber_ticket_number

        fiber_content = self.env["fiber.contract.process"].create(
            **self.fiber_contract_data
        )
        fiber_contract = self.env["contract.contract"].browse(fiber_content["id"])
        mobile_content = self.data

        # Substitute a "contract_lines" list for a "contract_line" dict
        mobile_content.update(
            {
                "ticket_number": self.mobile_ticket_number,
                "contract_line": {
                    "product_code": self.pack_code,
                    "date_start": "2020-01-01 00:00:00",
                },
            }
        )
        mobile_content.pop("contract_lines")

        mobile_content = self.process.create(**self.data)
        mobile_contract = self.env["contract.contract"].browse(mobile_content["id"])
        self.assertEqual(
            mobile_contract.parent_pack_contract_id,
            fiber_contract,
        )
        self.assertEqual(mobile_contract.number_contracts_in_pack, 2)
        self.assertTrue(mobile_contract.is_pack)

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    def test_raise_error_if_not_found_parent_pack_contract(
        self, *args
    ):
        crm_lead = crm_lead_create(
            self.env,
            self.partner,
            "pack",
            portability=False,
        )
        for line in crm_lead.lead_line_ids:
            if line.product_id.default_code == self.pack_code:
                line.ticket_number = self.mobile_ticket_number
            else:
                line.ticket_number = self.fiber_ticket_number
        mobile_content = self.data
        mobile_content.update(
            {
                "ticket_number": self.mobile_ticket_number,
                "contract_lines": [
                    {
                        "product_code": self.pack_code,
                        "date_start": "2020-01-01 00:00:00",
                    }
                ],
            }
        )
        self.assertRaisesRegex(
            UserError,
            "Fiber contract of CRMLead ID = {}, ticket = {} not found".format(
                crm_lead.id,
                self.fiber_ticket_number,
            ),
            self.process.create,
            **mobile_content
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    def test_create_mobile_pack_contract_link_known_fiber_contract(self, *args):
        self.fiber_contract_data.update({"ticket_number": "867846"})
        fiber_content = self.env["fiber.contract.process"].create(
            **self.fiber_contract_data
        )
        fiber_contract = self.env["contract.contract"].browse(fiber_content["id"])

        mobile_content = self.data
        mobile_content.update(
            {
                "ticket_number": "34215134",
                "contract_lines": [
                    {
                        "product_code": self.pack_code,
                        "date_start": "2020-01-01 00:00:00",
                    }
                ],
                "parent_pack_contract_id": fiber_contract.code,
            }
        )
        mobile_content = self.process.create(**self.data)
        mobile_contract = self.env["contract.contract"].browse(mobile_content["id"])
        self.assertEqual(
            mobile_contract.parent_pack_contract_id,
            fiber_contract,
        )
        self.assertEqual(mobile_contract.number_contracts_in_pack, 2)
        self.assertTrue(mobile_contract.is_pack)

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.UnblockMobilePackTicket"  # noqa
    )
    def test_raise_error_if_not_found_parent_pack_contract_with_code(
        self, *args
    ):
        parent_contract_code = "272281"
        mobile_content = self.data
        mobile_content.update(
            {
                "ticket_number": "",
                "contract_lines": [
                    {
                        "product_code": self.pack_code,
                        "date_start": "2020-01-01 00:00:00",
                    }
                ],
                "parent_pack_contract_id": parent_contract_code,
            }
        )
        self.assertRaisesRegex(
            UserError,
            "Fiber contract with ref = {} not found".format(
                parent_contract_code,
            ),
            self.process.create,
            **mobile_content
        )

    @patch(
        "odoo.addons.somconnexio.models.contract.Contract._change_tariff_only_in_ODOO"
    )
    def test_create_mobile_sharing_bond_1_to_2(self, mock_change_tariff_odoo, *args):
        """
        No sharing data contract can stay without beeing linked to
        another, but every contract is created independently from the API,
        so always one will be first.
        """

        sharing_data_product_2 = self.browse_ref('somconnexio.50GBCompartides2mobils')
        sharing_contract = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_1_of_2'
        )
        shared_bond_id = "AAAAABBBB"

        # Change its shared bond to unlink it from the other contract sharing data with
        sharing_contract.mobile_contract_service_info_id.shared_bond_id = shared_bond_id

        self.assertEquals(len(sharing_contract.sharing_bond_contract_ids), 1)

        # Change new contract owner to match old sharing contract owner
        self.sharing_mobile_data["mobile_contract_service_info"][
            "shared_bond_id"
        ] = shared_bond_id

        content = self.process.create(**self.sharing_mobile_data)
        contract = self.env["contract.contract"].browse(content["id"])

        # No tariff change applied to first contract
        mock_change_tariff_odoo.assert_not_called()

        self.assertEqual(contract.shared_bond_id, sharing_contract.shared_bond_id)
        self.assertEquals(len(sharing_contract.sharing_bond_contract_ids), 2)
        self.assertIn(
            contract,
            sharing_contract.sharing_bond_contract_ids,
        )
        self.assertEquals(
            contract.current_tariff_product,
            sharing_data_product_2
        )

    def test_create_mobile_sharing_bond_2_to_3(self, *args):

        sharing_contract = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_1_of_2')
        sharing_data_product_2 = self.browse_ref('somconnexio.50GBCompartides2mobils')
        sharing_data_product_3 = self.browse_ref('somconnexio.50GBCompartides3mobils')

        shared_bond_id = sharing_contract.shared_bond_id
        self.sharing_mobile_data["mobile_contract_service_info"][
            "shared_bond_id"
        ] = shared_bond_id
        self.sharing_mobile_data["contract_lines"][0][
            "product_code"
        ] = sharing_data_product_3.default_code
        self.assertEquals(len(sharing_contract.sharing_bond_contract_ids), 2)
        self.assertEquals(
            sharing_contract.current_tariff_product, sharing_data_product_2
        )
        content = self.process.create(**self.sharing_mobile_data)
        contract = self.env["contract.contract"].browse(content["id"])

        self.assertEqual(contract.shared_bond_id, shared_bond_id)

        self.assertEquals(len(sharing_contract.sharing_bond_contract_ids), 3)
        self.assertIn(
            contract,
            sharing_contract.sharing_bond_contract_ids,
        )
        self.assertEquals(
            sharing_contract.current_tariff_product,
            sharing_data_product_3
        )

    @patch("odoo.addons.somconnexio.models.contract.Contract._change_tariff_only_in_ODOO")  # noqa
    def test_create_mobile_sharing_bond_3_sequential(
            self, mock_change_tariff_ODOO, *args):

        shared_bond_id = "A83028"
        sharing_3_mobiles_data = self.sharing_mobile_data.copy()
        sharing_data_product_3 = self.browse_ref('somconnexio.50GBCompartides3mobils')

        sharing_3_mobiles_data.update(
            {
                "mobile_contract_service_info": {
                    "phone_number": "654321123",
                    "icc": "123456",
                    "shared_bond_id": shared_bond_id,
                },
                "contract_lines": [
                    {
                        "product_code": sharing_data_product_3.default_code,
                        "date_start": "2023-01-01 00:00:00",
                    }
                ],
            }
        )

        content = self.process.create(**sharing_3_mobiles_data)
        first_contract = self.env["contract.contract"].browse(content["id"])

        self.assertEquals(len(first_contract.sharing_bond_contract_ids), 1)
        self.assertEquals(first_contract.current_tariff_product, sharing_data_product_3)

        sharing_3_mobiles_data["mobile_contract_service_info"].update(
            {
                "phone_number": "654321124",
                "icc": "123457",
            }
        )
        sharing_3_mobiles_data["ticket_number"] = "22828290929282"
        content = self.process.create(**sharing_3_mobiles_data)
        second_contract = self.env["contract.contract"].browse(content["id"])

        self.assertEquals(len(second_contract.sharing_bond_contract_ids), 2)
        self.assertEquals(
            second_contract.current_tariff_product, sharing_data_product_3
        )

        sharing_3_mobiles_data["mobile_contract_service_info"].update(
            {
                "phone_number": "654321125",
                "icc": "123458",
            }
        )
        sharing_3_mobiles_data["ticket_number"] = "22828290929283"
        content = self.process.create(**sharing_3_mobiles_data)
        third_contract = self.env["contract.contract"].browse(content["id"])

        self.assertEquals(len(third_contract.sharing_bond_contract_ids), 3)
        self.assertEquals(third_contract.current_tariff_product, sharing_data_product_3)

        mock_change_tariff_ODOO.assert_not_called()

    def test_create_mobile_sharing_bond_3_to_4(self, *args):

        sharing_contract = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_1_of_3'
        )
        sharing_data_product_3 = self.browse_ref('somconnexio.50GBCompartides3mobils')

        shared_bond_id = sharing_contract.shared_bond_id
        self.sharing_mobile_data["mobile_contract_service_info"]["shared_bond_id"] = (
            shared_bond_id
        )
        self.sharing_mobile_data["contract_lines"][0]["product_code"] = (
            sharing_data_product_3.default_code
        )

        self.assertEquals(len(sharing_contract.sharing_bond_contract_ids), 3)
        self.assertEquals(
            sharing_contract.current_tariff_product, sharing_data_product_3
        )

        self.assertRaisesRegex(
            UserError,
            "No more than 3 mobiles can share data together",
            self.process.create,
            **self.sharing_mobile_data
        )
