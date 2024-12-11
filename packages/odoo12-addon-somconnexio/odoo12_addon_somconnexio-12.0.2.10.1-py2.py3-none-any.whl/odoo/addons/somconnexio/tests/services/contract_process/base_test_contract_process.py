from faker import Faker

from ...sc_test_case import SCTestCase


class BaseContractProcessTestCase(SCTestCase):
    def setUp(self):
        super().setUp()
        self.partner = self.browse_ref("somconnexio.res_partner_2_demo")

        self.iban = self.partner.bank_ids[0].acc_number
        self.mandate = self.browse_ref("somconnexio.demo_mandate_partner_2_demo")

        fake = Faker("es-ES")

        self.service_address = {
            "street": fake.street_address() + " " + fake.secondary_address(),
            "zip_code": fake.postcode(),
            "city": fake.city(),
            "state": self.browse_ref("base.state_es_m").code,
            "country": self.browse_ref("base.es").code,
        }

        self.ticket_number = "1234"
