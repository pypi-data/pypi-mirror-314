from mock import patch

from ...sc_test_case import SCTestCase


class TestContractProcess(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.process = self.env["contract.contract.process"]
        self.expected_contract = object

    @patch(
        "odoo.addons.somconnexio.services.contract_process.mobile.MobileContractProcess.create"  # noqa
    )
    def test_create_mobile_contract(self, mock_mobile_contract_process_create):
        mock_mobile_contract_process_create.return_value = self.expected_contract
        data = {
            "service_technology": "Mobile",
        }
        contract = self.process.create(**data)

        self.assertEquals(contract, self.expected_contract)
        mock_mobile_contract_process_create.assert_called_once_with(**data)

    @patch(
        "odoo.addons.somconnexio.services.contract_process.adsl.ADSLContractProcess.create"  # noqa
    )
    def test_create_adsl_contract(self, mock_adsl_contract_process_create):
        mock_adsl_contract_process_create.return_value = self.expected_contract
        data = {
            "service_technology": "ADSL",
        }
        contract = self.process.create(**data)

        self.assertEquals(contract, self.expected_contract)
        mock_adsl_contract_process_create.assert_called_once_with(**data)

    @patch(
        "odoo.addons.somconnexio.services.contract_process.fiber.FiberContractProcess.create"  # noqa
    )
    def test_create_fiber_contract(self, mock_fiber_contract_process_create):
        mock_fiber_contract_process_create.return_value = self.expected_contract
        data = {
            "service_technology": "Fiber",
        }
        contract = self.process.create(**data)

        self.assertEquals(contract, self.expected_contract)
        mock_fiber_contract_process_create.assert_called_once_with(**data)

    @patch(
        "odoo.addons.somconnexio.services.contract_process.router4g.Router4GContractProcess.create"  # noqa
    )
    def test_create_router4g_contract(self, mock_router4g_contract_process_create):
        mock_router4g_contract_process_create.return_value = self.expected_contract
        data = {
            "service_technology": "4G",
        }
        contract = self.process.create(**data)

        self.assertEquals(contract, self.expected_contract)
        mock_router4g_contract_process_create.assert_called_once_with(**data)
