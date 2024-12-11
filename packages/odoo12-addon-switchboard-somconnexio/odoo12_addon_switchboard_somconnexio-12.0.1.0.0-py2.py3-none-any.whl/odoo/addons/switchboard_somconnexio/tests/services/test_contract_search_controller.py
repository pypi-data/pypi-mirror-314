import json
from odoo.addons.somconnexio.tests.common_service import (
    BaseEMCRestCaseAdmin,
)


class TestContractSearchController(BaseEMCRestCaseAdmin):
    def test_route_contract_search_to_dict_switchboard(self):
        base_url = "/api/contract"
        sb_contract = self.env.ref(
            "switchboard_somconnexio.contract_switchboard_app_500"
        )
        url = "{}?{}={}".format(base_url, "code", sb_contract.code)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        contract = result["contracts"][0]
        self.assertEquals(contract["id"], sb_contract.id)
        self.assertEquals(contract["subscription_type"], "switchboard")
        self.assertEquals(
            contract["available_operations"],
            [],
        )
