import json
import odoo

from ..common_service import BaseEMCRestCaseAdmin


class TestProductCatalogController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()
        self.url = "/api/product-catalog"
        self.code = "21IVA"
        self.url_with_code = "{}?code={}".format(self.url, self.code)
        self.demo_pricelist = self.browse_ref("somconnexio.pricelist_21_IVA")

        # Mobile product
        self.mbl_product = self.browse_ref('somconnexio.150Min1GB')
        self.mbl_product.product_tmpl_id.catalog_attribute_id = (
            self.browse_ref('somconnexio.150Min')
        )
        self.mbl_product.product_tmpl_id.catalog_attribute_id.catalog_name = (
            "150"
        )
        self.mbl_product.attribute_value_ids.catalog_name = '1024'
        self.mbl_product.public = True
        self.expected_mobile_product_info = {
            "code": self.mbl_product.default_code,
            "name": self.mbl_product.showed_name,
            "price": self.mbl_product.with_context(
                pricelist=self.demo_pricelist.id).price,
            "category": "mobile",
            "minutes": 150,
            "data": 1024,
            "bandwidth": None,
            "available_for": [
                "member",
                "coop_agreement",
                "sponsored",
            ],
        }

        # Fiber product
        self.fiber_product = self.browse_ref('somconnexio.Fibra600Mb')
        self.fiber_product.attribute_value_ids.catalog_name = '600'
        self.fiber_product.public = True
        self.expected_fiber_product_info = {
            "code": self.fiber_product.default_code,
            "name": self.fiber_product.showed_name,
            "price": self.fiber_product.with_context(
                pricelist=self.demo_pricelist.id).price,
            "category": "fiber",
            "minutes": None,
            "data": None,
            "bandwidth": 600,
            "available_for": [
                "member",
            ],
            "has_landline_phone": True,
        }

        # ADSL product
        self.adsl_product = self.browse_ref('somconnexio.ADSL20MBSenseFix')
        # The 20 Mb product attribute value already exists in prod DB
        adsl_attribute_value = self.env["product.attribute.value"].create({
            "name": "20 Mb",
            "attribute_id": self.browse_ref('somconnexio.Bandwidth').id,
            "catalog_name": '20'
        })
        self.adsl_product.product_tmpl_id.catalog_attribute_id = (
            adsl_attribute_value.id
        )
        self.adsl_product.public = True
        self.expected_adsl_product_info = {
            "code": self.adsl_product.default_code,
            "name": self.adsl_product.showed_name,
            "price": self.adsl_product.with_context(
                pricelist=self.demo_pricelist.id).price,
            "category": "adsl",
            "minutes": None,
            "data": None,
            "bandwidth": 20,
            "available_for": [
                "member",
                "coop_agreement",
            ],
            "has_landline_phone": False,
        }

    def _get_service_products(self):
        service_product_templates = self.env["product.template"].search([
            ("categ_id", 'in', [
                self.env.ref('somconnexio.mobile_service').id,
                self.env.ref('somconnexio.broadband_adsl_service').id,
                self.env.ref('somconnexio.broadband_fiber_service').id,
                ])
        ])
        service_products = self.env["product.product"].search([
            ("product_tmpl_id", 'in', [tmpl.id for tmpl in service_product_templates]),
            ("public", '=', True),
        ])
        return service_products

    def test_route(self):
        response = self.http_get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.reason, "OK")

    def test_price_list_count(self):
        response = self.http_get(self.url)
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content["pricelists"]), 2)

    def test_price_list_content(self):
        response = self.http_get(self.url_with_code)
        content = json.loads(response.content.decode("utf-8"))

        obtained_pricelist = content.get("pricelists")[0].get('products')
        service_products = self._get_service_products()

        self.assertEqual(
            len(service_products),
            len(obtained_pricelist)
        )
        self.assertIn(self.expected_mobile_product_info, obtained_pricelist)
        self.assertIn(self.expected_fiber_product_info, obtained_pricelist)
        self.assertIn(self.expected_adsl_product_info, obtained_pricelist)

    def test_search_by_code(self):
        code = "new-fake-code"
        self.env["product.pricelist"].create({
            "code": code,
            "name": "test pricelist",
            "currency_id": 1
        })

        response = self.http_get("{}?code={}".format(self.url, code))
        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelists = content.get("pricelists")
        self.assertEqual(len(obtained_pricelists), 1)
        self.assertEqual(obtained_pricelists[0].get("code"), code)

    def test_search_by_category(self):
        mobile_products_templ_ids = self.env["product.template"].search([
            ("categ_id", '=', self.env.ref('somconnexio.mobile_service').id)
        ])
        mobile_products = self.env["product.product"].search([
            ("product_tmpl_id", 'in', [tmpl.id for tmpl in mobile_products_templ_ids]),
            ("public", '=', True)
        ])

        response = self.http_get("{}&categ=mobile".format(self.url_with_code))
        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelists = content.get("pricelists")
        obtained_mobile_catalog = obtained_pricelists[0].get("products")
        self.assertEqual(len(obtained_pricelists), 1)
        self.assertEqual(len(obtained_mobile_catalog), len(mobile_products))
        self.assertEqual(obtained_mobile_catalog[0]["category"], "mobile")

    def test_search_by_4G_category(self):
        router_4G_product = self.env.ref('somconnexio.Router4G')
        router_4G_product.attribute_value_ids.catalog_name = '1000000'
        router_4G_product.write({'public': True})

        response = self.http_get("{}?categ=4G".format(self.url))
        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelists = content.get("pricelists")
        obtained_4G_catalog = obtained_pricelists[0].get("products")
        self.assertEqual(len(obtained_4G_catalog), 1)
        self.assertEqual(obtained_4G_catalog[0]["category"], "4G")
        self.assertEqual(obtained_4G_catalog[0]["code"],
                         router_4G_product.default_code)
        self.assertEqual(obtained_4G_catalog[0]["data"],
                         int(router_4G_product.attribute_value_ids.catalog_name))

    def test_search_catalan(self):
        response = self.http_get(self.url, headers={'Accept-Language': 'ca_ES'})
        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelist = content.get("pricelists")[0].get('products')
        service_products = self._get_service_products()

        self.assertEqual(
            len(service_products),
            len(obtained_pricelist)
        )
        self.assertIn(self.expected_mobile_product_info, obtained_pricelist)
        self.assertIn(self.expected_fiber_product_info, obtained_pricelist)
        self.assertIn(self.expected_adsl_product_info, obtained_pricelist)

    def test_search_filtering_by_products_availables_from_product(self):
        fiber100sensefix_product = self.browse_ref('somconnexio.SenseFixFibra100Mb')
        fiber100sensefix_product.attribute_value_ids.catalog_name = '100'
        fiber100sensefix_product.public = True
        expected_fiber_product_info = {
            "code": fiber100sensefix_product.default_code,
            "name": fiber100sensefix_product.showed_name,
            "price": fiber100sensefix_product.with_context(
                pricelist=self.demo_pricelist.id).price,
            "category": "fiber",
            "minutes": None,
            "data": None,
            "bandwidth": 100,
            "available_for": [
                "member",
            ],
            "has_landline_phone": False,
        }
        fiber100_product = self.browse_ref('somconnexio.Fibra100Mb')

        response = self.http_get("{}?product_code={}".format(
            self.url,
            fiber100_product.default_code)
        )

        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelist = content.get("pricelists")[0].get('products')

        self.assertIn(expected_fiber_product_info, obtained_pricelist)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_search_raise_error_incompatible_code_product_code(self):
        response = self.http_get("{}?product_code={}&categ={}".format(
            self.url,
            "PRODUCT_CODE",
            "CATEG",
            )
        )
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(
            error_msg,
            "'categ' must not be present with 'product_code'",
        )

    def test_price_list_content_pack(self):
        pack_product = self.browse_ref('somconnexio.PackFibra100MbIL20GB')
        component_fiber_product = self.browse_ref('somconnexio.Fibra100Mb')
        component_mobile_product = self.browse_ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        )
        expected_pack_component_fiber_info = {
            "code": component_fiber_product.default_code,
            "name": component_fiber_product.showed_name,
            "price": component_fiber_product.with_context(
                pricelist=self.demo_pricelist.id
            ).price,
            "category": "fiber",
            "minutes": None,
            "data": None,
            "bandwidth": 100,
            "has_landline_phone": True,
        }
        expected_pack_component_mobile_info = {
            "code": component_mobile_product.default_code,
            "name": component_mobile_product.showed_name,
            "price": component_mobile_product.with_context(
                pricelist=self.demo_pricelist.id
            ).price,
            "category": "mobile",
            "minutes": 99999,
            "data": 20480,
            "bandwidth": None,
        }
        expected_pack_product_info = {
            "code": pack_product.default_code,
            "name": pack_product.showed_name,
            "price": pack_product.with_context(pricelist=self.demo_pricelist.id).price,
            "category": "bonified_mobile",
            "mobiles_in_pack": 1,
            "fiber_bandwidth": 100,
            "has_land_line": True,
            "available_for": [
                "member",
            ],
        }
        pack_product.public = True
        response = self.http_get(self.url)
        content = json.loads(response.content.decode("utf-8"))
        pricelist = content.get("pricelists")[0]
        self.assertTrue('packs' in pricelist)
        pack = [
            pack
            for pack in pricelist['packs']
            if pack['code'] == expected_pack_product_info['code']
        ]
        self.assertTrue(pack)
        pack = pack[0]
        self.assertIn('products', pack)
        products = pack['products']
        del (pack['products'])
        self.assertEqual(expected_pack_product_info, pack)
        self.assertIn(
            expected_pack_component_mobile_info,
            products
        )
        self.assertIn(
            expected_pack_component_fiber_info,
            products
        )
        self.assertEqual(
            len(products),
            2
        )
        mobile_pack_product_EiE = self.browse_ref(
            "somconnexio.TrucadesIllimitades50GBPackEiE"
        )
        self.assertNotIn(
            mobile_pack_product_EiE.default_code,
            [product["code"] for product in products],
        )

    def test_price_list_offer_attribute(self):
        product_with_offer = self.browse_ref('somconnexio.TrucadesIllimitades20GB')
        offer_product = self.browse_ref('somconnexio.TrucadesIllimitades20GBPack')
        product_with_offer.public = True
        response = self.http_get(self.url)
        content = json.loads(response.content.decode("utf-8"))
        expected_mobile_product_info = {
            "code": product_with_offer.default_code,
            "name": product_with_offer.showed_name,
            "price": product_with_offer.with_context(
                pricelist=self.demo_pricelist.id
            ).price,
            "category": "mobile",
            "minutes": 99999,
            "data": 20480,
            "bandwidth": None,
            "available_for": [
                "member",
                "coop_agreement",
                "sponsored",
            ],
            "offer": {
                "code": offer_product.default_code,
                "price": offer_product.with_context(
                    pricelist=self.demo_pricelist.id
                ).price,
                "name": offer_product.showed_name
            }
        }
        obtained_pricelist = content.get("pricelists")[0].get('products')
        self.assertTrue(expected_mobile_product_info in obtained_pricelist)

    def test_contract_as_new_service(self):
        self.fiber_product.contract_as_new_service = False

        response = self.http_get(self.url)
        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelist = content.get("pricelists")[0].get('products')
        service_products = self._get_service_products()

        self.assertEqual(
            len(service_products)-1,
            len(obtained_pricelist)
        )
        self.assertTrue(self.mbl_product.contract_as_new_service)
        self.assertIn(self.expected_mobile_product_info, obtained_pricelist)
        self.assertTrue(self.adsl_product.contract_as_new_service)
        self.assertIn(self.expected_adsl_product_info, obtained_pricelist)
        self.assertFalse(self.fiber_product.contract_as_new_service)
        self.assertNotIn(self.expected_fiber_product_info, obtained_pricelist)

    def test_price_list_content_shared_bond(self):
        compartides_pack_product = self.browse_ref(
            "somconnexio.CompartidesFibra1Gb3mobils"
        )
        component_fiber_product = self.browse_ref("somconnexio.Fibra1Gb")
        component_mobile_product = self.browse_ref("somconnexio.50GBCompartides3mobils")
        expected_pack_component_fiber_info = {
            "code": component_fiber_product.default_code,
            "name": component_fiber_product.showed_name,
            "price": component_fiber_product.with_context(
                pricelist=self.demo_pricelist.id
            ).price,
            "category": "fiber",
            "minutes": None,
            "data": None,
            "bandwidth": 1024,
            "has_landline_phone": True,
        }
        expected_pack_component_mobile_info = {
            "code": component_mobile_product.default_code,
            "name": component_mobile_product.showed_name,
            "price": component_mobile_product.with_context(
                pricelist=self.demo_pricelist.id
            ).price,
            "category": "mobile",
            "minutes": 99999,
            "data": 51200,
            "bandwidth": None,
        }
        expected_compartides_pack_product_info = {
            "code": compartides_pack_product.default_code,
            "name": compartides_pack_product.showed_name,
            "price": compartides_pack_product.with_context(
                pricelist=self.demo_pricelist.id
            ).price,
            "category": "mobile_shared_data",
            "mobiles_in_pack": 3,
            "fiber_bandwidth": 1024,
            "has_land_line": True,
            "available_for": [
                "member",
            ],
        }
        compartides_pack_product.public = True
        response = self.http_get(self.url)
        content = json.loads(response.content.decode("utf-8"))
        pricelist = content.get("pricelists")[0]
        self.assertTrue("packs" in pricelist)
        pack = [
            pack
            for pack in pricelist["packs"]
            if pack["code"] == expected_compartides_pack_product_info["code"]
        ]
        self.assertTrue(pack)

        pack = pack[0]
        self.assertIn("products", pack)

        products = pack["products"]
        del pack["products"]
        self.assertEqual(expected_compartides_pack_product_info, pack)
        self.assertIn(expected_pack_component_mobile_info, products)
        self.assertIn(expected_pack_component_fiber_info, products)
        self.assertEqual(len(products), 4)

    def test_exclude_company_products(self):
        fiber_company_product = self.browse_ref("somconnexio.Fibra600MbEiE")

        response = self.http_get("{}&categ=fiber".format(self.url_with_code))
        content = json.loads(response.content.decode("utf-8"))
        obtained_pricelists = content.get("pricelists")
        obtained_fiber_catalog = obtained_pricelists[0].get("products")

        self.assertNotIn(
            fiber_company_product.default_code,
            [fiber_product["code"] for fiber_product in obtained_fiber_catalog],
        )
