from ..helper_service import crm_lead_create
from ..sc_test_case import SCTestCase


class TestCRMLeadsGenerateSIMDeliveryWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner_id = self.browse_ref("somconnexio.res_partner_2_demo")
        self.pack_crm_lead = crm_lead_create(
            self.env, self.partner_id, "pack", portability=True
        )

    def test_wizard_OK(self):

        self.pack_crm_lead.action_set_remesa()

        wizard = self.env['crm.lead.generate.sim.delivery.wizard'].with_context(
            active_ids=[self.pack_crm_lead.id]
        ).create({})
        wizard.button_generate_delivery()

        self.assertEquals(
            self.pack_crm_lead.stage_id, self.browse_ref("somconnexio.stage_lead8")
        )
