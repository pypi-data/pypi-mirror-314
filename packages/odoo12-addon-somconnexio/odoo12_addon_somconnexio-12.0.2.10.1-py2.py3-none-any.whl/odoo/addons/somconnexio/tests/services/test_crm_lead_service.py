import json

import odoo

from ..common_service import BaseEMCRestCaseAdmin


class CRMLeadServiceRestCase(BaseEMCRestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.partner = self.env.ref("somconnexio.res_partner_1_demo")
        self.url = "/api/crm-lead"
        self.product_mobile = self.env.ref("somconnexio.150Min1GB")
        self.ba_data = {
            "partner_id": self.partner.ref,
            "iban": "ES6621000418401234567891",
            "phone": "700284835",
            "lead_line_ids": [
                {
                    "product_code": (
                        self.browse_ref("somconnexio.Fibra600Mb").default_code
                    ),
                    "mobile_isp_info": {},
                    "broadband_isp_info": {
                        "type": "portability",
                        "delivery_address": {
                            "street": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "service_address": {
                            "street": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B"
                        },
                        "previous_provider": 39,
                        "previous_service": "adsl",
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                }
            ],
        }
        self.mbl_data = {
            "partner_id": self.partner.ref,
            "iban": "ES6621000418401234567891",
            "phone": None,
            "lead_line_ids": [
                {
                    "product_code": self.product_mobile.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                    "broadband_isp_info": {},
                }
            ],
        }

    def test_route_right_create(self):
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            )._api_external_id,
            "iban": "ES6621000418401234567891",
            "phone": None,
            "lead_line_ids": [
                {
                    "product_code": self.product_mobile.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "invoice_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B"
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract"
                    },
                    "broadband_isp_info": {},
                }
            ],
        }

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        (crm_lead,) = self.env["crm.lead"].browse(content["id"])
        self.assertEquals(
            crm_lead.subscription_request_id.id,
            self.browse_ref("easy_my_coop.subscription_request_1_demo").id,
        )
        self.assertEquals(len(crm_lead.lead_line_ids), 1)
        self.assertEquals(crm_lead.lead_line_ids[0].iban, data["iban"])
        self.assertEquals(crm_lead.lead_line_ids[0].mobile_isp_info.phone_number, "123")
        crm_lead_line = crm_lead.lead_line_ids[0]
        self.assertEquals(
            crm_lead_line.product_id.id, self.browse_ref("somconnexio.150Min1GB").id
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.icc_donor,
            "123",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.type,
            "portability",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_full_street,
            "Carrer del Rec 123",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_city,
            "Barcelona",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_zip_code,
            "08000",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_country_id.id,
            self.browse_ref('base.es').id
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_state_id.id,
            self.browse_ref('base.state_es_b').id
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_full_street,
            "Carrer del Rec 123",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_city,
            "Barcelona",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_zip_code,
            "08000",
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_country_id.id,
            self.browse_ref('base.es').id
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.invoice_state_id.id,
            self.browse_ref('base.state_es_b').id
        )
        self.assertFalse(crm_lead.phone)

    def test_route_right_create_with_partner_id(self):
        data = self.mbl_data.copy()
        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead, = self.env["crm.lead"].browse(content["id"])
        self.assertEquals(
            crm_lead.partner_id.ref,
            self.partner.ref
        )

    def test_route_right_create_with_icc(self):
        data = self.mbl_data.copy()
        data["lead_line_ids"][0]["mobile_isp_info"]["icc"] = "123"

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead, = self.env["crm.lead"].browse(content["id"])
        self.assertTrue(crm_lead.lead_line_ids[0].mobile_isp_info.has_sim)

    def test_route_right_create_with_partner_id_without_previous_owner(self):
        data = self.mbl_data.copy()
        for key in ["previous_owner_name", "previous_owner_first_name",
                    "previous_owner_vat_number"]:
            del data["lead_line_ids"][0]["mobile_isp_info"][key]

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead, = self.env["crm.lead"].browse(content["id"])
        self.assertEquals(
            crm_lead.partner_id.ref,
            self.partner.ref
        )

    def test_route_right_create_broadband_portability_without_fix(self):
        response = self.http_post(self.url, data=self.ba_data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead, = self.env["crm.lead"].browse(content["id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertEquals(crm_lead.phone, "700284835")
        self.assertTrue(crm_lead_line.broadband_isp_info.no_previous_phone_number)
        self.assertEquals(crm_lead_line.broadband_isp_info.phone_number, "-")
        self.assertEquals(crm_lead_line.broadband_isp_info.previous_service, "adsl")

    def test_route_right_create_broadband_portability_with_fix(self):
        self.ba_data["lead_line_ids"][0]["broadband_isp_info"][
            "phone_number"
        ] = "98787889"
        response = self.http_post(self.url, data=self.ba_data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead = self.env["crm.lead"].browse(content["id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertTrue(crm_lead_line.broadband_isp_info.keep_phone_number)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_broadband_empty_previous_service(self):
        # Empty previous_service
        self.ba_data.get('lead_line_ids')[0].get(
            'broadband_isp_info')["previous_service"] = ""

        response = self.http_post(self.url, data=self.ba_data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead, = self.env["crm.lead"].browse(content["id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertFalse(crm_lead_line.broadband_isp_info.previous_service)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_broadband_bad_previous_service(self):
        # Update previous_service
        self.ba_data.get('lead_line_ids')[0].get(
            'broadband_isp_info')["previous_service"] = "fake-service"

        response = self.http_post(self.url, data=self.ba_data)

        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "BadRequest")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_subscription_request_id_create(self):
        data = self.mbl_data.copy()
        data.pop("partner_id")
        data["subscription_request_id"] = 666

        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "SubscriptionRequest with id 666 not found")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_mobile_isp_info_create(self):
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            ).id,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": self.product_mobile.default_code,
                    "mobile_isp_info": {},
                    "broadband_isp_info": {},
                }
            ],
        }
        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(
            error_msg,
            "Mobile product SE_SC_REC_MOBILE_T_150_1024 needs a mobile_isp_info",
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_broadband_isp_info_create(self):
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            ).id,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": (
                        self.browse_ref("somconnexio.ADSL20MBSenseFix").default_code
                    ),
                    "mobile_isp_info": {},
                    "broadband_isp_info": {},
                }
            ],
        }
        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(
            error_msg,
            "Broadband product SE_SC_REC_BA_ADSL_SF needs a broadband_isp_info",
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_bad_subcription_and_partner_ids(self):
        data = self.mbl_data.copy()
        data["subscription_request_id"] = (
            self.ref("easy_my_coop.subscription_request_1_demo"),
        )
        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 400)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_wrong_without_iban(self):
        data = self.mbl_data.copy()
        data.pop("iban")

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 400)

    def test_route_right_create_with_partner_id_wo_delivery_address(self):
        data = self.mbl_data.copy()
        data["lead_line_ids"][0]["mobile_isp_info"].pop("delivery_address")

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead, = self.env["crm.lead"].browse(content["id"])
        self.assertEquals(
            crm_lead.partner_id.ref,
            self.partner.ref
        )
        crm_lead_line = crm_lead.lead_line_ids[0]
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_street,
            self.partner.street,
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_city,
            self.partner.city,
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_zip_code,
            self.partner.zip,
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_country_id, self.partner.country_id
        )
        self.assertEquals(
            crm_lead_line.mobile_isp_info.delivery_state_id, self.partner.state_id
        )

    def test_route_right_create_wo_partner_id_wo_delivery_address_w_icc(self):
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            )._api_external_id,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": self.product_mobile.default_code,
                    "mobile_isp_info": {
                        "icc": "123",
                        "type": "new",
                    },
                    "broadband_isp_info": {},
                }
            ],
        }

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        (crm_lead,) = self.env["crm.lead"].browse(content["id"])
        crm_lead_line = crm_lead.lead_line_ids[0]
        self.assertEquals(
            crm_lead_line.mobile_isp_info.icc,
            "123",
        )

    def test_route_right_create_adsl_wo_fix_void_phone_number(self):
        data = {
            "partner_id": self.partner.ref,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": (
                        self.browse_ref("somconnexio.ADSL20MBSenseFix").default_code
                    ),
                    "broadband_isp_info": {
                        "phone_number": "",
                        "type": "new",
                    },
                }
            ],
        }

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        (crm_lead,) = self.env["crm.lead"].browse(content["id"])
        self.assertEquals(crm_lead.lead_line_ids.broadband_isp_info_phone_number, "-")

    def test_route_right_create_adsl_wo_fix_missing_phone_number(self):
        data = {
            "partner_id": self.partner.ref,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": (
                        self.browse_ref("somconnexio.ADSL20MBSenseFix").default_code
                    ),
                    "broadband_isp_info": {
                        "type": "new",
                    },
                }
            ],
        }

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        (crm_lead,) = self.env["crm.lead"].browse(content["id"])
        self.assertEquals(crm_lead.lead_line_ids.broadband_isp_info_phone_number, "-")

    def test_route_right_combination_no_pack_products(self):
        mobile_product = self.browse_ref("somconnexio.150Min1GB")
        pack_fiber_product = self.browse_ref("somconnexio.Fibra100Mb")
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            )._api_external_id,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": mobile_product.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "invoice_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                    "broadband_isp_info": {},
                },
                {
                    "product_code": pack_fiber_product.default_code,
                    "broadband_isp_info": {
                        "type": "portability",
                        "service_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "previous_provider": 51,
                        "delivery_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "phone_number": "937889022",
                    },
                },
            ],
        }
        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        crm_lead = self.env["crm.lead"].browse(content["id"])

        self.assertTrue(
            all(line.iban == data["iban"] for line in crm_lead.lead_line_ids)
        )

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_right_combination_pack_products(self):
        mobile_product = self.browse_ref("somconnexio.TrucadesIllimitades20GBPack")
        pack_fiber_product = self.browse_ref("somconnexio.Fibra100Mb")
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            )._api_external_id,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": mobile_product.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "invoice_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                    "broadband_isp_info": {},
                },
                {
                    "product_code": pack_fiber_product.default_code,
                    "broadband_isp_info": {
                        "type": "portability",
                        "service_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "previous_provider": 51,
                        "delivery_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "phone_number": "937889022",
                    },
                },
            ],
        }
        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)

    def test_route_right_combination_pack_products_different_number(self):
        mobile_product = self.browse_ref("somconnexio.TrucadesIllimitades20GBPack")
        pack_fiber_product = self.browse_ref("somconnexio.Fibra100Mb")
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            )._api_external_id,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": mobile_product.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "invoice_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                    "broadband_isp_info": {},
                },
                {
                    "product_code": pack_fiber_product.default_code,
                    "broadband_isp_info": {
                        "type": "portability",
                        "service_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "previous_provider": 51,
                        "delivery_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "phone_number": "937889022",
                    },
                },
                {
                    "product_code": pack_fiber_product.default_code,
                    "broadband_isp_info": {
                        "type": "portability",
                        "service_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "previous_provider": 51,
                        "delivery_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "phone_number": "937889022",
                    },
                },
            ],
        }
        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)

    def test_route_right_combination_pack_extra_product(self):
        mobile_product = self.browse_ref("somconnexio.TrucadesIllimitades20GBPack")
        mobile_extra_product = self.browse_ref("somconnexio.TrucadesIllimitades20GB")
        pack_fiber_product = self.browse_ref("somconnexio.Fibra100Mb")
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            )._api_external_id,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": mobile_product.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "invoice_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                    "broadband_isp_info": {},
                },
                {
                    "product_code": mobile_extra_product.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "invoice_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                    "broadband_isp_info": {},
                },
                {
                    "product_code": pack_fiber_product.default_code,
                    "broadband_isp_info": {
                        "type": "portability",
                        "service_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "previous_provider": 51,
                        "delivery_address": {
                            "street": "a",
                            "city": "aa",
                            "zip_code": "aaa",
                            "state": "A",
                            "country": "ES",
                        },
                        "phone_number": "937889022",
                    },
                },
            ],
        }
        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)

    def test_route_bad_single_pack_product(self):
        mobile_pack_product = self.browse_ref("somconnexio.TrucadesIllimitades20GBPack")
        data = {
            "subscription_request_id": self.browse_ref(
                "easy_my_coop.subscription_request_1_demo"
            )._api_external_id,
            "iban": "ES6621000418401234567891",
            "lead_line_ids": [
                {
                    "product_code": mobile_pack_product.default_code,
                    "mobile_isp_info": {
                        "icc_donor": "123",
                        "phone_number": "123",
                        "type": "portability",
                        "delivery_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "invoice_address": {
                            "street": "Carrer del Rec",
                            "street2": "123",
                            "zip_code": "08000",
                            "city": "Barcelona",
                            "country": "ES",
                            "state": "B",
                        },
                        "previous_provider": 1,
                        "previous_owner_name": "Newus",
                        "previous_owner_first_name": "Borgo",
                        "previous_owner_vat_number": "29461336S",
                        "previous_contract_type": "contract",
                    },
                    "broadband_isp_info": {},
                }
            ],
        }
        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)

    def test_fiber_linked_to_mobile_offer(self):
        # Create fiber contract reference
        fiber_contract = self.env.ref("somconnexio.contract_fibra_600")

        data = self.mbl_data.copy()
        data["lead_line_ids"][0]["mobile_isp_info"]["fiber_linked_to_mobile_offer"] = \
            fiber_contract.code

        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead, = self.env["crm.lead"].browse(content["id"])
        mobile_isp_info = crm_lead.lead_line_ids[0].mobile_isp_info
        self.assertEquals(mobile_isp_info.linked_fiber_contract_id, fiber_contract)

    def test_mobile_lead_with_shared_bond_id(self):
        shared_bond_id = "AAA"
        data = self.mbl_data.copy()
        data["lead_line_ids"][0]["mobile_isp_info"]["shared_bond_id"] = shared_bond_id

        response = self.http_post(self.url, data=data)
        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        crm_lead = self.env["crm.lead"].browse(content["id"])
        mobile_isp_info = crm_lead.lead_line_ids[0].mobile_isp_info
        self.assertEquals(mobile_isp_info.shared_bond_id, shared_bond_id)

    def test_route_right_create_with_tag_ids(self):
        data = self.mbl_data.copy()
        data["tag_codes"] = ["first_month_free"]

        response = self.http_post(self.url, data=data)

        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertIn("id", content)

        (crm_lead,) = self.env["crm.lead"].browse(content["id"])
        self.assertEquals(crm_lead.tag_ids, self.env["crm.lead.tag"].browse(9))
