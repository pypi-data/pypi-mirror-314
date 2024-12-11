import json
import odoo

from ..common_service import BaseEMCRestCaseAdmin
from ..helper_service import subscription_request_create_data


class TestResPartnerController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()

        self.partner = self.browse_ref("somconnexio.res_partner_1_demo")
        self.url = "/api/partner"
        self.sponsees_url = self.url + '/sponsees'

    @odoo.tools.mute_logger("odoo.addons.auth_api_key.models.ir_http")
    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_raise_error_without_auth(self):
        response = self.http_get_without_auth()

        self.assertEquals(response.status_code, 403)
        self.assertEquals(response.reason, "FORBIDDEN")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_get_without_ref(self):
        response = self.http_get(self.url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_get_not_found(self):
        response = self.http_get(
            "{}/{}".format(self.url, 123)
        )

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    def test_route_get(self):
        response = self.http_get(
            "{}/{}".format(self.url, int(self.partner.ref))
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content["id"], self.partner.id)
        self.assertEqual(content["name"], self.partner.name)
        self.assertEqual(content["ref"], self.partner.ref)
        self.assertEqual(content["addresses"][0]["street"],
                         self.partner.street)
        self.assertEqual(
            content["cooperator_register_number"],
            self.partner.cooperator_register_number
        )
        self.assertEqual(
            content["cooperator_end_date"],
            ""
        )
        self.assertEqual(
            content['sponsorship_code'], self.partner.sponsorship_hash
        )
        self.assertEqual(
            content['sponsorship_code'], self.partner.sponsorship_hash
        )
        self.assertEqual(content['sponsees_number'], 1)
        self.assertEqual(
            content['sponsees_max'],
            self.partner.company_id.max_sponsees_number
        )
        self.assertEqual(content['sponsor_ref'], "")

    def test_sponsees_route_get_without_sponsees(self):

        partner = self.browse_ref("somconnexio.res_partner_2_demo")
        self.assertFalse(partner.sponsee_ids)

        response = self.http_get(
            "{}?ref={}".format(self.sponsees_url, int(partner.ref))
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertFalse(content['sponsorship_code'])
        self.assertEqual(content['sponsees_number'], 0)
        self.assertEqual(
            content['sponsees_max'], partner.company_id.max_sponsees_number
        )
        self.assertFalse(content['sponsees'])

    def test_sponsees_route_get_with_SR_as_sponsor(self):

        SR_sponsee = self.browse_ref("somconnexio.sc_subscription_request_2_demo")
        self.assertEquals(SR_sponsee.sponsor_id, self.partner)
        self.assertTrue(self.partner.sponsee_ids.inactive_sponsored)

        response = self.http_get(
            "{}?ref={}".format(self.sponsees_url, int(self.partner.ref))
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content['sponsorship_code'], self.partner.sponsorship_hash)
        self.assertEqual(content['sponsees_number'], 1)
        self.assertEqual(
            content['sponsees_max'], self.partner.company_id.max_sponsees_number
        )
        self.assertEqual(content['sponsees'], [SR_sponsee.name])

    def test_sponsees_route_get_with_active_provisioning(self):
        partner = self.browse_ref('somconnexio.res_sponsored_partner_1_demo')
        self.assertTrue(partner.inactive_sponsored)
        self.assertFalse(partner.has_lead_in_provisioning)

        # Remove sponsor from a SR
        SR_sponsee = self.browse_ref("somconnexio.sc_subscription_request_2_demo")
        self.assertEquals(SR_sponsee.sponsor_id, partner.sponsor_id)
        SR_sponsee.write({"sponsor_id": self.ref("somconnexio.res_partner_2_demo")})
        self.assertNotEquals(SR_sponsee.sponsor_id, partner.sponsor_id)

        crm_lead_id = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': partner.id,
            }]
        )[0].id
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'phone_number': '666666666',
            'type': 'new',
        })
        broadband_adsl_product_tmpl_args = {
            'name': 'ADSL 20Mb',
            'type': 'service',
            'categ_id': self.ref('somconnexio.broadband_adsl_service')
        }
        product_adsl_broadband_tmpl = self.env['product.template'].create(
            broadband_adsl_product_tmpl_args
        )
        product_broadband_adsl = product_adsl_broadband_tmpl.product_variant_id

        crm_lead_line_args = {
            'lead_id': crm_lead_id,
            'broadband_isp_info': broadband_isp_info.id,
            'product_id': product_broadband_adsl.id,
            'name': '666666666',
        }
        self.env['crm.lead.line'].create(
            [crm_lead_line_args]
        )
        self.assertTrue(partner.has_lead_in_provisioning)

        response = self.http_get(
            "{}?ref={}".format(self.sponsees_url, int(partner.sponsor_id.ref))
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content['sponsorship_code'],
                         partner.sponsor_id.sponsorship_hash)
        self.assertEqual(content['sponsees_number'], 1)
        self.assertIn(partner.name, content['sponsees'])

    def test_route_sponsees_get_with_active_sponsees(self):

        partner = self.browse_ref('somconnexio.res_sponsored_partner_1_demo')
        self.assertTrue(partner.inactive_sponsored)

        self.Contract = self.env['contract.contract']
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        service_partner = self.env['res.partner'].create({
            'parent_id': partner.id,
            'name': 'Service partner',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner.id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner.id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))
        self.assertFalse(partner.inactive_sponsored)

        response = self.http_get(
            "{}?ref={}".format(self.sponsees_url, int(partner.sponsor_id.ref))
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content['sponsees_number'], 2)
        self.assertEqual(len(content['sponsees']), 2)
        self.assertIn(partner.name, content['sponsees'])

    def test_route_get_with_active_sponsees(self):

        self.Contract = self.env['contract.contract']
        self.product_1 = self.env.ref('product.product_product_1')
        self.router_product = self.env['product.product'].search(
            [
                ("default_code", "=", "NCDS224WTV"),
            ]
        )
        self.router_lot = self.env['stock.production.lot'].create({
            'product_id': self.router_product.id,
            'name': '123',
            'router_mac_address': '12:BB:CC:DD:EE:90'
        })
        self.mobile_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'icc': '123'
        })
        self.adsl_contract_service_info = self.env[
            'adsl.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'administrative_number': '123',
            'router_product_id': self.router_product.id,
            'router_lot_id': self.router_lot.id,
            'ppp_user': 'ringo',
            'ppp_password': 'rango',
            'endpoint_user': 'user',
            'endpoint_password': 'password'
        })
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.browse_ref('somconnexio.res_sponsored_partner_1_demo')
        self.service_partner = self.env['res.partner'].create({
            'parent_id': self.partner.id,
            'name': 'Service partner',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': self.partner.id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': self.partner.id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))
        sponsor = self.browse_ref("somconnexio.res_partner_1_demo")
        response = self.http_get(
            "{}/{}".format(self.url, int(sponsor.ref))
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content['sponsees_number'], 2)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_search_not_found(self):
        response = self.http_get(
            "{}?vat={}".format(self.url, "66758531L")
        )

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    def test_route_search(self):
        response = self.http_get(
            "{}?vat={}".format(self.url, self.partner.vat)
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content["id"], self.partner.id)
        self.assertEqual(content["name"], self.partner.name)
        self.assertEqual(content["ref"], self.partner.ref)
        self.assertEqual(
            content["cooperator_register_number"],
            self.partner.cooperator_register_number
        )
        self.assertEqual(
            content["cooperator_end_date"],
            ""
        )
        self.assertFalse(content["coop_candidate"])
        self.assertTrue(content["member"])

    def test_route_search_normalize_vat(self):
        bad_formatted_vat = "  {}---. ".format(self.partner.vat)
        response = self.http_get(
            "{}?vat={}".format(self.url, bad_formatted_vat)
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content["id"], self.partner.id)

    def test_filter_duplicate_addresses(self):
        address_dict = {
            'type': 'service',
            'parent_id': self.partner.id,
            'street': 'test',
            'street2': 'test',
            'zip': '08123',
            'city': 'city',
            'state_id': self.ref('base.state_es_b'),
            'country_id': self.ref('base.es'),
            'name': 'test',
        }
        address_dict['street'] = 'Test'
        self.env['res.partner'].create(address_dict)
        address_dict['street'] = '  Test '
        self.env['res.partner'].create(address_dict)

        response = self.http_get(
            "{}/{}".format(self.url, int(self.partner.ref))
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(content["id"], self.partner.id)
        self.assertEqual(len(content["addresses"]), 2)

    def test_route_search_banned_actions(self):
        partner = self.browse_ref("somconnexio.res_partner_1_demo")

        response = self.http_get(
            "{}/{}".format(self.url, int(partner.ref))
        )
        content = json.loads(response.content.decode("utf-8"))

        self.assertFalse(partner.banned_action_tags)
        self.assertEqual(content["banned_actions"], [])

        action_new_service = self.browse_ref('somconnexio.new_services_action')
        action_one_shot = self.browse_ref('somconnexio.mobile_one_shot_action')
        partner.write(
            {'banned_action_tags': [(6, 0, [action_new_service.id,
                                            action_one_shot.id])]}
        )

        self.assertIn(action_new_service, partner.banned_action_tags)
        self.assertIn(action_one_shot, partner.banned_action_tags)
        self.assertEquals(len(partner.banned_action_tags), 2)

        response = self.http_get(
            "{}/{}".format(self.url, int(partner.ref))
        )
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(
            content["banned_actions"],
            [action_new_service.code, action_one_shot.code]
        )

    def test_can_sponsor_ok(self):
        route = "{url}?vat={vat}&sponsor_code={sponsor_code}".format(
            url=self.url + "/check_sponsor",
            vat=self.partner.vat,
            sponsor_code=self.partner.sponsorship_hash,
        )
        content = self.http_get_content(route)

        self.assertEqual(content["result"], "allowed")
        self.assertEqual(content["message"], "ok")

    def test_can_sponsor_ok_code_insensitive(self):
        route = "{url}?vat={vat}&sponsor_code={sponsor_code}".format(
            url=self.url + "/check_sponsor",
            vat=self.partner.vat,
            sponsor_code=self.partner.sponsorship_hash.lower(),
        )
        content = self.http_get_content(route)

        self.assertEqual(content["result"], "allowed")
        self.assertEqual(content["message"], "ok")

    def test_can_sponsor_ko_code_incomplete(self):
        route = "{url}?vat={vat}&sponsor_code={sponsor_code}".format(
            url=self.url + "/check_sponsor",
            vat=self.partner.vat,
            sponsor_code=self.partner.sponsorship_hash[:-1],
        )
        content = self.http_get_content(route)

        self.assertEqual(content["result"], "not_allowed")
        self.assertEqual(content["message"], "invalid code or vat number")

    def test_can_sponsor_ko_maximum_exceeded(self):
        while (self.partner.active_sponsees_number
               < self.partner.company_id.max_sponsees_number):
            sr_vals = subscription_request_create_data(self)
            sr_vals.update({'sponsor_id': self.partner.id})
            self.assertTrue(self.env['subscription.request'].create(sr_vals))

        route = "{url}?vat={vat}&sponsor_code={sponsor_code}".format(
            url=self.url + "/check_sponsor",
            vat=self.partner.vat,
            sponsor_code=self.partner.sponsorship_hash,
        )
        content = self.http_get_content(route)

        self.assertEqual(content["result"], "not_allowed")
        self.assertEqual(content["message"], "maximum number of sponsees exceeded")

    def test_can_sponsor_ko_invalid_code_or_vat(self):
        route = "{url}?vat={vat}&sponsor_code={sponsor_code}".format(
            url=self.url + "/check_sponsor",
            vat="WRONG VAT",
            sponsor_code="WRONG SPONSOR CODE"
        )
        content = self.http_get_content(route)

        self.assertEqual(content["result"], "not_allowed")
        self.assertEqual(content["message"], "invalid code or vat number")

    def test_route_get_inactive_sponsored(self):

        partner = self.browse_ref('somconnexio.res_sponsored_partner_1_demo')

        response = self.http_get(
            "{}/{}".format(self.url, int(partner.ref))
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")
        content = json.loads(response.content.decode("utf-8"))
        self.assertTrue(content["inactive_sponsored"])
        self.assertEqual(content["sponsor_ref"], partner.sponsor_id.ref)

        self.Contract = self.env['contract.contract']
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        service_partner = self.env['res.partner'].create({
            'parent_id': partner.id,
            'name': 'Service partner',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner.id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner.id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': partner.bank_ids.id
        }
        self.assertTrue(self.env['contract.contract'].create(vals_contract))

        response = self.http_get(
            "{}/{}".format(self.url, int(partner.ref))
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")
        content = json.loads(response.content.decode("utf-8"))
        self.assertFalse(content["inactive_sponsored"])
