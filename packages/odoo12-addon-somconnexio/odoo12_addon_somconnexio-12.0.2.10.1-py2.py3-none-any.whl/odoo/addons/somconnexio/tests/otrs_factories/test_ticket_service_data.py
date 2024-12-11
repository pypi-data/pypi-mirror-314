from unittest.mock import patch
from ..sc_test_case import SCTestCase
from ..helper_service import crm_lead_create


class TestTicketServiceData(SCTestCase):
    def setUp(self):
        self.TicketServiceData = self.env["ticket.service.data"]
        self.partner_id = self.env.ref("somconnexio.res_partner_2_demo")
        self.expected_data = object()
        return super().setUp()

    @patch(
        "odoo.addons.somconnexio.otrs_factories.mobile_data_from_crm_lead_line.MobileDataFromCRMLeadLine.build"  # noqa
    )
    def test_build_mobile(self, mock_build):
        mock_build.return_value = self.expected_data

        crm_lead = crm_lead_create(
            self.env,
            self.partner_id,
            "mobile",
        )
        crm_lead_line = crm_lead.lead_line_ids[0]
        service_data = self.TicketServiceData.build(crm_lead_line)

        mock_build.assert_called_once_with()
        self.assertEqual(service_data, self.expected_data)

    @patch(
        "odoo.addons.somconnexio.otrs_factories.fiber_data_from_crm_lead_line.FiberDataFromCRMLeadLine.build"  # noqa
    )
    def test_build_fiber(self, mock_build):
        mock_build.return_value = self.expected_data

        crm_lead = crm_lead_create(
            self.env,
            self.partner_id,
            "fiber",
        )
        crm_lead_line = crm_lead.lead_line_ids[0]
        service_data = self.TicketServiceData.build(crm_lead_line)

        mock_build.assert_called_once_with()
        self.assertEqual(service_data, self.expected_data)

    @patch(
        "odoo.addons.somconnexio.otrs_factories.adsl_data_from_crm_lead_line.ADSLDataFromCRMLeadLine.build"  # noqa
    )
    def test_build_adsl(self, mock_build):
        mock_build.return_value = self.expected_data

        crm_lead = crm_lead_create(
            self.env,
            self.partner_id,
            "adsl",
        )
        crm_lead_line = crm_lead.lead_line_ids[0]
        service_data = self.TicketServiceData.build(crm_lead_line)

        mock_build.assert_called_once_with()
        self.assertEqual(service_data, self.expected_data)

    @patch(
        "odoo.addons.somconnexio.otrs_factories.router_4G_data_from_crm_lead_line.Router4GDataFromCRMLeadLine.build"  # noqa
    )
    def test_build_adsl(self, mock_build):
        mock_build.return_value = self.expected_data

        crm_lead = crm_lead_create(
            self.env,
            self.partner_id,
            "4G",
        )
        crm_lead_line = crm_lead.lead_line_ids[0]
        service_data = self.TicketServiceData.build(crm_lead_line)

        mock_build.assert_called_once_with()
        self.assertEqual(service_data, self.expected_data)
