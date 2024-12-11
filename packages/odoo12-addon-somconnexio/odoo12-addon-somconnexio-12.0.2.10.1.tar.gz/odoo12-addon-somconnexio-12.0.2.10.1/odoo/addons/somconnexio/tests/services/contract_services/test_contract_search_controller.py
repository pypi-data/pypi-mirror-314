import json
import odoo
from ...common_service import BaseEMCRestCaseAdmin


class TestContractSearchController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()
        self.url = "/api/contract"
        self.partner = self.browse_ref("somconnexio.res_partner_1_demo")
        self.mobile_contract = self.env.ref("somconnexio.contract_mobile_il_20")
        self.shared_bond_mobile_contract = self.env.ref(
            "somconnexio.contract_mobile_il_50_shared_1_of_2"
        )
        self.pack_mobile_contract = self.env.ref(
            "somconnexio.contract_mobile_il_20_pack"
        )
        self.broadband_contract = self.env.ref("somconnexio.contract_adsl")
        self.adsl_without_fix = self.env.ref("somconnexio.contract_adsl_without_fix")
        self.fiber_contract = self.env.ref("somconnexio.contract_fibra_600")
        self.fourth_g_contract = self.env.ref("somconnexio.contract_4G")

    @odoo.tools.mute_logger("odoo.addons.auth_api_key.models.ir_http")
    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_without_auth(self):
        response = self.http_get_without_auth()

        self.assertEquals(response.status_code, 403)
        self.assertEquals(response.reason, "FORBIDDEN")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_unknown_parameter(self):
        url = "{}?{}={}".format(self.url, "unknown_parameter", "2828")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_multiple_parameters(self):
        url = "{}?{}={}&{}={}".format(self.url, "code", "111111",
                                      "partner_vat", "ES1828028")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_subscription_type_single_parameter(self):
        url = "{}?{}={}".format(self.url, "subscription_type", "mobile")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_subscription_type_unallowed_value(self):
        url = "{}?{}={}&{}={}".format(
            self.url,
            "customer_ref",
            "1",
            "subscription_type",
            "some",
        )
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_code_not_found(self):
        url = "{}?{}={}".format(self.url, "code", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_vat_not_found(self):
        url = "{}?{}={}".format(self.url, "partner_vat", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_phone_number_not_found(self):
        url = "{}?{}={}".format(self.url, "phone_number", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    def test_route_contract_search_code_ok(self):
        url = "{}?{}={}".format(self.url, "code", self.mobile_contract.code)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.mobile_contract.id)

    def test_route_contract_search_phone_number_ok(self, *args):
        url = "{}?{}={}".format(
            self.url, "phone_number", self.mobile_contract.phone_number
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(len(result["contracts"]), 1)
        self.assertEquals(result["contracts"][0]["id"], self.mobile_contract.id)

    def test_route_contract_search_partner_code_ok(self):
        url = "{}?{}={}".format(
            self.url, "customer_ref", self.mobile_contract.partner_id.ref
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn(self.mobile_contract.id, [c["id"] for c in result["contracts"]])

    def test_route_contract_search_partner_code_multi_filter(self):
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "customer_ref",
            self.fiber_contract.partner_id.ref,
            "phone_number",
            "93951",
            "subscription_type",
            "broadband",
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn(self.fiber_contract.id, [c["id"] for c in result["contracts"]])

    def test_route_contract_search_partner_vat_multiple_ok(self, *args):
        num_contracts = len(
            self.env["contract.contract"].search(
                [("partner_id", "=", self.partner.id)],
                limit=10,
            )
        )
        url = "{}?{}={}".format(self.url, "partner_vat", self.partner.vat)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", result)
        self.assertEquals(len(result["contracts"]), num_contracts)

    def test_route_contract_search_partner_pagination(self, *args):
        num_contracts = self.env["contract.contract"].search_count(
            [("partner_id", "=", self.partner.id)]
        )
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "limit", 1
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", result)
        self.assertEquals(len(result['contracts']), 1)
        self.assertIn("paging", result)
        self.assertIn("limit", result["paging"])
        self.assertEquals(result["paging"]["limit"], 1)
        self.assertIn("offset", result["paging"])
        self.assertEquals(result["paging"]["offset"], 0)
        self.assertIn("totalNumberOfRecords", result["paging"])
        self.assertEquals(result["paging"]["totalNumberOfRecords"], num_contracts)

    def test_route_contract_search_partner_pagination_with_offset(self, *args):
        num_contracts = self.env["contract.contract"].search_count(
            [("partner_id", "=", self.partner.id)]
        )
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "limit", 1, "offset", 1
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", result)
        self.assertEquals(len(result["contracts"]), 1)
        self.assertIn("paging", result)
        self.assertIn("offset", result["paging"])
        self.assertEquals(result["paging"]["offset"], 1)
        self.assertIn("limit", result["paging"])
        self.assertEquals(result["paging"]["limit"], 1)
        self.assertIn("totalNumberOfRecords", result["paging"])
        self.assertEquals(result["paging"]["totalNumberOfRecords"], num_contracts)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_pagination_bad_limit(self, *args):
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "limit", 'XXX'
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Limit must be numeric")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_pagination_bad_offset(self, *args):
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "limit", '1', "offset", 'XXX'
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Offset must be numeric")

    def test_route_contract_search_partner_sort_by(self, *args):
        expected_contracts_sorted = (
            self.env["contract.contract"]
            .search(
                [("partner_id", "=", self.partner.id)],
                limit=10,
                order="name",
            )
            .mapped("code")
        )

        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortBy", "name"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        codes = [c["code"] for c in result["contracts"]]
        self.assertEquals(codes, expected_contracts_sorted)
        self.assertIn("paging", result)
        self.assertIn("sortBy", result['paging'])
        self.assertEquals(result['paging']['sortBy'], 'name')

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_bad_sort_by(self, *args):
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortBy", "XXX"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Invalid field to sortBy")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_sort_order(self, *args):
        expected_contracts_sorted = (
            self.env["contract.contract"]
            .search(
                [("partner_id", "=", self.partner.id)],
                limit=10,
                order="name desc",
            )
            .mapped("code")
        )

        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortBy", "name", "sortOrder", "DESCENDENT"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        codes = [c["code"] for c in result["contracts"]]
        self.assertEquals(codes, expected_contracts_sorted)
        self.assertIn("paging", result)
        self.assertIn("sortBy", result['paging'])
        self.assertEquals(result['paging']['sortBy'], 'name')
        self.assertIn("sortOrder", result['paging'])
        self.assertEquals(result['paging']['sortOrder'], 'DESCENDENT')

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_bad_sort_order(self, *args):
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortBy", "name",
            "sortOrder", "XXX"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "sortOrder must be ASCENDING or DESCENDING")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_pagination_offset_without_limit(self, *args):
        num_contracts = self.env["contract.contract"].search_count(
            [("partner_id", "=", self.partner.id)],
        )
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "offset", '1'
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", result)
        self.assertEquals(len(result["contracts"]), 10)
        self.assertIn("paging", result)
        self.assertIn("offset", result["paging"])
        self.assertEquals(result["paging"]["offset"], 1)
        self.assertIn("totalNumberOfRecords", result["paging"])
        self.assertEquals(result["paging"]["totalNumberOfRecords"], num_contracts)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_pagination_sort_order_without_by(self, *args):  # noqa
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortOrder", "DESCENDENT"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    def test_route_contract_search_to_dict(self):
        result = self.env["contract.service"]._to_dict(self.fiber_contract)

        self.assertEquals(result["id"], self.fiber_contract.id)
        self.assertEquals(result["code"], self.fiber_contract.code)
        self.assertEquals(
            result["customer_firstname"], self.fiber_contract.partner_id.firstname
        )
        self.assertEquals(
            result["customer_lastname"], self.fiber_contract.partner_id.lastname
        )
        self.assertEquals(result["customer_ref"], self.fiber_contract.partner_id.ref)
        self.assertEquals(result["customer_vat"], self.fiber_contract.partner_id.vat)
        self.assertEquals(result["phone_number"], self.fiber_contract.phone_number)
        self.assertEquals(
            result["current_tariff_product"],
            self.fiber_contract.current_tariff_product.code,
        )
        self.assertEquals(result["ticket_number"], self.fiber_contract.ticket_number)
        self.assertEquals(
            result["technology"], self.fiber_contract.service_technology_id.name
        )
        self.assertEquals(
            result["supplier"], self.fiber_contract.service_supplier_id.name
        )
        self.assertEquals(result["lang"], self.fiber_contract.lang)
        self.assertEquals(
            result["iban"],
            self.fiber_contract.mandate_id.partner_bank_id.sanitized_acc_number,
        )
        self.assertEquals(result["is_terminated"], self.fiber_contract.is_terminated)
        self.assertEquals(result["date_start"], self.fiber_contract.date_start)
        self.assertEquals(result["date_end"], self.fiber_contract.date_end)
        fiber_signal = (
            self.fiber_contract.fiber_signal_type_id
            and self.fiber_contract.fiber_signal_type_id.code
            or False
        )
        self.assertEquals(result["fiber_signal"], fiber_signal)
        self.assertEquals(result["data"], 0)
        self.assertEquals(result["minutes"], 0)
        self.assertEquals(result["bandwidth"], 600)
        self.assertEquals(result["available_operations"], ["ChangeContractHolder"])

    def test_route_contract_search_to_dict_subscription_type_mobile(self):
        self.url = "{}?{}={}".format(self.url, "code", self.mobile_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.mobile_contract.id)
        self.assertEquals(result["contracts"][0]["subscription_type"], "mobile")

    def test_route_contract_search_to_dict_subscription_type_broadband(self):
        self.url = "{}?{}={}".format(self.url, "code", self.broadband_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.broadband_contract.id)
        self.assertEquals(result["contracts"][0]["subscription_type"], "broadband")

    def test_route_contract_search_to_dict_address(self):
        self.url = "{}?{}={}".format(self.url, "code", self.mobile_contract.code)
        response = self.http_get(self.url)
        result = json.loads(response.content.decode("utf-8"))
        self.assertEquals(
            result["contracts"][0]["address"]["street"], self.partner.street
        )
        self.assertEquals(result["contracts"][0]["address"]["city"], self.partner.city)
        self.assertEquals(
            result["contracts"][0]["address"]["zip_code"], self.partner.zip
        )

    def test_route_contract_search_to_dict_subscription_technology_mobile(self):
        self.url = "{}?{}={}".format(self.url, "code", self.mobile_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.mobile_contract.id)
        self.assertEquals(result["contracts"][0]["subscription_technology"], "mobile")

    def test_route_contract_search_to_dict_subscription_technology_adsl(self):
        self.url = "{}?{}={}".format(self.url, "code", self.broadband_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.broadband_contract.id)
        self.assertEquals(result["contracts"][0]["subscription_technology"], "adsl")

    def test_route_contract_search_to_dict_subscription_technology_fiber(self):
        self.url = "{}?{}={}".format(self.url, "code", self.fiber_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.fiber_contract.id)
        self.assertEquals(result["contracts"][0]["subscription_technology"], "fiber")

    def test_route_contract_search_to_dict_available_operations_change_tariff_fiber_out_landline(  # noqa
        self,
    ):
        fiber_fix = self.browse_ref("somconnexio.Fibra100Mb")
        fiber_fix.without_fix = False
        self.fiber_contract.contract_line_ids.update({
            "product_id": fiber_fix.id
        })
        self.url = "{}?{}={}".format(self.url, "code", self.fiber_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.fiber_contract.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ["ChangeTariffFiberOutLandline", "ChangeContractHolder"],
        )

    def test_route_contract_adsl_search_to_dict_available_operations_change_tariff_fiber_landline(  # noqa
        self,
    ):
        self.url = "{}?{}={}".format(self.url, "code", self.broadband_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.broadband_contract.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ["ChangeContractHolder", "ChangeTariffFiberLandline"],
        )

    def test_route_contract_adsl_search_to_dict_available_operations_change_tariff_fiber_out_landline(  # noqa
        self,
    ):
        self.url = "{}?{}={}".format(self.url, "code", self.adsl_without_fix.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertEquals(result["contracts"][0]["id"], self.adsl_without_fix.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ["ChangeContractHolder", "ChangeTariffFiberOutLandline"],
        )

    def test_route_contract_search_to_dict_available_operations_change_tariff_mobile(  # noqa
        self,
    ):
        self.url = "{}?{}={}".format(self.url, "code", self.mobile_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.mobile_contract.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ['ChangeTariffMobile', 'AddOneShotMobile', 'ChangeContractHolder'],
        )

    def test_route_contract_search_to_dict_available_operations_router_4g(  # noqa
        self,
    ):
        self.url = "{}?{}={}".format(self.url, "code", self.fourth_g_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertEquals(result["contracts"][0]["id"], self.fourth_g_contract.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ["ChangeContractHolder"],
        )

    def test_route_contract_search_to_dict_available_operations_t_conserva(self):
        # TODO remove after migration : /12.0.2.5.11/post-set-tconserva-categid.py
        self.env.ref("somconnexio.TarifaConserva_product_template").write(
            {"categ_id": self.env.ref("somconnexio.mobile_service").id}
        )

        mobile_contract_conserva = self.env.ref("somconnexio.contract_mobile_t_conserva")  # noqa
        # TODO remove after migration : /12.0.2.5.11/post-set-tconserva
        mobile_contract_conserva._compute_current_tariff_contract_line()

        self.url = "{}?{}={}".format(self.url, "code", mobile_contract_conserva.code)
        response = self.http_get(self.url)

        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], mobile_contract_conserva.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ["ChangeTariffMobile", "ChangeContractHolder"],
        )

    def test_route_contract_search_to_dict_mobile_pack(  # noqa
        self,
    ):
        self.url = "{}?{}={}".format(self.url, "code", self.pack_mobile_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        contract = result["contracts"][0]
        self.assertEquals(contract["id"], self.pack_mobile_contract.id)
        self.assertEquals(
            contract["available_operations"],
            ['ChangeTariffMobile', 'AddOneShotMobile'],
        )
        self.assertEquals(
            contract["parent_contract"],
            self.pack_mobile_contract.parent_pack_contract_id.code,
        )
        self.assertFalse(contract["has_landline_phone"])
        self.assertEquals(contract["data"], 20480)
        self.assertEquals(contract["minutes"], 99999)

    def test_route_contract_search_to_dict_mobile_shared_bond(  # noqa
        self,
    ):
        self.url = "{}?{}={}".format(
            self.url, "code", self.shared_bond_mobile_contract.code
        )
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        contract = result["contracts"][0]
        self.assertEquals(contract["id"], self.shared_bond_mobile_contract.id)
        self.assertEquals(
            contract["available_operations"],
            ["AddOneShotMobile"],
        )
        self.assertEquals(
            contract["parent_contract"],
            self.shared_bond_mobile_contract.parent_pack_contract_id.code,
        )
        self.assertEquals(
            contract["shared_bond_id"],
            self.shared_bond_mobile_contract.shared_bond_id,
        )
        self.assertEquals(
            contract["price"],
            self.shared_bond_mobile_contract.current_tariff_product.with_context(
                pricelist=self.ref("somconnexio.pricelist_21_IVA")
            ).price,
        )
        self.assertFalse(contract["has_landline_phone"])
        self.assertEquals(contract["data"], 51200)
        self.assertEquals(contract["minutes"], 99999)

    def test_route_contract_search_to_dict_broadband_with_landline(  # noqa
        self,
    ):
        response = self.http_get(
            "{}?code={}".format(self.url, self.fiber_contract.code)
        )
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        contract = result["contracts"][0]

        self.assertTrue(contract["has_landline_phone"])
        self.assertEquals(contract["bandwidth"], 600)

    def test_route_contract_search_to_dict_description_translation(  # noqa
        self,
    ):
        response = self.http_get(
            "{}?code={}".format(self.url, self.broadband_contract.code)
        )
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        ca_contract = result["contracts"][0]

        self.broadband_contract.partner_id.lang = "es_ES"

        response = self.http_get(
            "{}?code={}".format(self.url, self.broadband_contract.code)
        )
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        es_contract = result["contracts"][0]

        # TODO: Review translations
        self.assertEqual(ca_contract["description"], "ADSL 100 min a fijo o móvil")
        self.assertEqual(es_contract["description"], "ADSL 100 min a fijo o móvil")

    def test_route_contract_partner_company(self,):
        url = "{}?{}={}".format(
            self.url, "customer_ref", self.adsl_without_fix.partner_id.ref
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertEquals(result["contracts"][0]["id"], self.adsl_without_fix.id)
        self.assertEquals(result["contracts"][0]["customer_firstname"], "")
