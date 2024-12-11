from datetime import date

from mock import patch
from odoo.addons.component.tests.common import ComponentMixin
from odoo.tests.common import SavepointCase

from ..helper_service import (
    contract_fiber_create_data,
    contract_mobile_create_data,
)


class TestContractListener(SavepointCase, ComponentMixin):
    @classmethod
    def setUpClass(cls):
        super(TestContractListener, cls).setUpClass()
        cls.setUpComponent()

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        SavepointCase.setUp(self)
        ComponentMixin.setUp(self)

        self.partner = self.env.ref("somconnexio.res_partner_2_demo")
        self.contract_data = contract_mobile_create_data(self.env, self.partner)
        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

    def _create_ba_contract(self):
        self.ba_contract = self.env["contract.contract"].create(
            contract_fiber_create_data(self.env, self.partner)
        )

    def test_create(self):
        contract = self.env["contract.contract"].create(self.contract_data)

        jobs_domain = [
            ("method_name", "=", "create_subscription"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [contract.id])

    def test_terminate(self):
        contract = self.env["contract.contract"].create(self.contract_data)
        contract.date_start = date.today()

        # Listener would be activated when date_end is set
        contract.date_end = date.today()

        contract.terminate_contract(
            self.browse_ref("somconnexio.reason_other"),
            "Comment",
            date.today(),
            self.browse_ref("somconnexio.user_reason_other"),
        )

        jobs_domain = [
            ("method_name", "=", "terminate_subscription"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [contract.id])

    @patch(
        "odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ChangeTariffExceptionalTicket"  # noqa
    )
    def test_terminate_pack(self, _):
        self._create_ba_contract()
        contract = self.env["contract.contract"].create(self.contract_data)
        contract.parent_pack_contract_id = self.ba_contract.id
        self.ba_contract.date_start = date.today()

        # Listener would be activated when date_end is set
        self.ba_contract.date_end = date.today()

        self.ba_contract.terminate_contract(
            self.browse_ref("somconnexio.reason_other"),
            "Comment",
            date.today(),
            self.browse_ref("somconnexio.user_reason_other"),
        )

        jobs_domain = [
            ("method_name", "=", "terminate_subscription"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [self.ba_contract.id])
        # Call to breack_pack
        self.assertFalse(contract.is_pack)
        self.assertFalse(contract.parent_pack_contract_id)

    def test_terminate_pack_address_change(self):
        self._create_ba_contract()
        contract = self.env["contract.contract"].create(self.contract_data)
        contract.parent_pack_contract_id = self.ba_contract.id
        self.ba_contract.date_start = date.today()

        # Listener would be activated when date_end is set
        self.ba_contract.date_end = date.today()

        self.ba_contract.terminate_contract(
            self.browse_ref("somconnexio.reason_location_change_from_SC_to_SC"),
            "Location change",
            date.today(),
            self.browse_ref("somconnexio.user_reason_other"),
        )

        jobs_domain = [
            ("method_name", "=", "terminate_subscription"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [self.ba_contract.id])
        # Not call to breack_pack
        self.assertTrue(contract.is_pack)
        self.assertEqual(contract.parent_pack_contract_id, self.ba_contract)
