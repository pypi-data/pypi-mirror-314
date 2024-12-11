from ..sc_test_case import SCTestCase


class ContratLineTest(SCTestCase):
    def test_is_mobile_tariff(self):
        cl_data = {
            "name": "Test",
            "product_id": "",
            "contract_id": 1,
            "date_start": "2023-01-01",
        }

        # Broadband product
        cl_data["product_id"] = self.env.ref("somconnexio.ADSL20MBSenseFix").id
        ba_cl = self.env["contract.line"].create(cl_data)
        self.assertFalse(ba_cl.is_mobile_tariff_service)

        # Mobile one shot product
        cl_data["product_id"] = self.env.ref("somconnexio.DadesAddicionals1GB").id
        mbl_one_shot_cl = self.env["contract.line"].create(cl_data)
        self.assertFalse(mbl_one_shot_cl.is_mobile_tariff_service)

        # Mobile additional service product
        cl_data["product_id"] = self.env.ref("somconnexio.EnviamentSIM").id
        mbl_sim_cl = self.env["contract.line"].create(cl_data)
        self.assertFalse(mbl_sim_cl.is_mobile_tariff_service)

        # Mobile service product
        cl_data["product_id"] = self.env.ref("somconnexio.TrucadesIllimitades150GB").id
        mbl_service_cl = self.env["contract.line"].create(cl_data)
        self.assertTrue(mbl_service_cl.is_mobile_tariff_service)
