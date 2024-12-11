from ..helper_service import crm_lead_create
from ..sc_test_case import SCComponentTestCase


class TestCRMLeadListener(SCComponentTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCRMLeadListener, cls).setUpClass()
        # disable tracking test suite wise
        cls.env = cls.env(context=dict(
            cls.env.context,
            tracking_disable=True,
            test_queue_job_no_delay=False,
        ))

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner_id = self.browse_ref('somconnexio.res_partner_2_demo')

        self.mobile_crm_lead = crm_lead_create(self.env, self.partner_id, "mobile",
                                               portability=True)
        self.mobile_crm_lead.action_set_remesa()

    def test_create_ticket(self):
        queue_jobs_before = self.env['queue.job'].search_count([])

        self.mobile_crm_lead.action_set_won()

        queue_jobs_after = self.env['queue.job'].search_count([])

        self.assertEqual(queue_jobs_before, queue_jobs_after-1)

        jobs_domain = [
            ("method_name", "=", "create_ticket"),
            ("model_name", "=", "crm.lead.line"),
        ]
        queued_job = self.env['queue.job'].search(jobs_domain)

        self.assertTrue(queued_job)

    def test_link_pack_tickets(self):
        queue_jobs_before = self.env['queue.job'].search_count([])

        self.mobile_crm_lead.lead_line_ids.is_from_pack = True
        self.mobile_crm_lead.action_set_won()

        queue_jobs_after = self.env['queue.job'].search_count([])

        self.assertEqual(queue_jobs_before, queue_jobs_after - 1)

        queue_jobs_before = queue_jobs_after

        crm_lead_to_link = crm_lead_create(
            self.env,
            self.partner_id,
            "pack",
        )
        crm_lead_to_link.action_set_remesa()
        crm_lead_to_link.action_set_won()

        queue_jobs_after = self.env["queue.job"].search_count([])
        jobs_domain = [
            ("method_name", "=", "link_pack_tickets"),
            ("model_name", "=", "crm.lead"),
        ]
        queued_job = self.env['queue.job'].search(jobs_domain)

        self.assertEqual(queue_jobs_before, queue_jobs_after - 3)
        self.assertTrue(queued_job)

    def link_sharing_data_mobile_tickets(self):
        queue_jobs_before = self.env['queue.job'].search_count([])

        self.mobile_crm_lead.lead_line_ids.product_id = self.env.ref(
            "somconnexio.50GBCompartides2mobils"
        )
        self.mobile_crm_lead.action_set_won()

        queue_jobs_after = self.env['queue.job'].search_count([])

        jobs_domain = [
            ("method_name", "=", "link_sharing_data_mobile_tickets"),
            ("model_name", "=", "crm.lead"),
        ]
        queued_job = self.env['queue.job'].search(jobs_domain)

        self.assertEqual(queue_jobs_before, queue_jobs_after - 2)
        self.assertTrue(queued_job)

    def test_create_shipment(self):
        queue_jobs_before = self.env["queue.job"].search_count([])

        self.mobile_crm_lead.action_set_delivery_generated()

        queue_jobs_after = self.env["queue.job"].search_count([])

        self.assertEqual(queue_jobs_before, queue_jobs_after - 1)

        jobs_domain = [
            ("method_name", "=", "create_shipment"),
            ("model_name", "=", "crm.lead"),
        ]
        queued_job = self.env["queue.job"].search(jobs_domain)

        self.assertTrue(queued_job)
