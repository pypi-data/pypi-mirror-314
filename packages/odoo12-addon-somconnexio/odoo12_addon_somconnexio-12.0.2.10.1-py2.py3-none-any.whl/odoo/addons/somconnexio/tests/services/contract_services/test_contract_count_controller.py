import json
from ...common_service import BaseEMCRestCaseAdmin
from ...helper_service import (
    contract_fiber_create_data,
    subscription_request_create_data,
)


class TestContractCountController(BaseEMCRestCaseAdmin):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Contract = self.env["contract.contract"]
        self.Partner = self.env["res.partner"]
        partner = self.browse_ref("somconnexio.res_partner_2_demo")
        self.vals_contract = contract_fiber_create_data(self.env, partner)
        self.vals_subscription = subscription_request_create_data(self)
        self.vals_subscription["state"] = "done"

    def test_route_count_one_contract_active(self, *args):
        url = "/public-api/contract-count"
        count_contract = self.env["contract.contract"].search_count([])
        self.Contract.create(self.vals_contract)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", decoded_response)
        self.assertEquals(decoded_response["contracts"], count_contract + 1)

    def test_route_doesnt_count_one_contract_terminated(self, *args):
        url = "/public-api/contract-count"
        count_contract = self.env["contract.contract"].search_count([])
        self.vals_contract["is_terminated"] = True
        self.Contract.create(self.vals_contract)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", decoded_response)
        self.assertEquals(decoded_response["contracts"], count_contract)

    def test_route_count_one_member(self, *args):
        url = "/public-api/contract-count"
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        count_members = decoded_response["members"]
        self.Partner.create(
            {
                "name": "test member",
                "member": True,
                "coop_candidate": False,
                "customer": True,
            }
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        self.assertEquals(decoded_response["members"] - count_members, 1)

    def test_route_count_one_coop_candidate(self, *args):
        url = "/public-api/contract-count"
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        count_members = decoded_response["members"]
        partner = self.Partner.create(
            {"name": "test member", "coop_candidate": True, "customer": True}
        )
        self.vals_subscription["partner_id"] = partner.id
        self.env["subscription.request"].create(self.vals_subscription)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        self.assertEquals(decoded_response["members"] - count_members, 1)

    def test_route_doesnt_count_one_partner_not_member(self, *args):
        url = "/public-api/contract-count"
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        count_members = decoded_response["members"]
        self.Partner.create(
            {
                "name": "test member",
                "member": False,
                "coop_candidate": False,
                "customer": True,
            }
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn("members", decoded_response)
        self.assertEquals(decoded_response["members"] - count_members, 0)
