import json
import odoo
from faker import Faker
from mock import patch
from odoo.addons.somconnexio.tests.common_service import (
    BaseEMCRestCaseAdmin,
)

HOST = "127.0.0.1"
PORT = odoo.tools.config["http_port"]


@patch("pyopencell.resources.subscription.Subscription.get")
@patch(
    "odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractCreateService"  # noqa
)
class TestContractController(BaseEMCRestCaseAdmin):
    def setUp(self):
        super().setUp()
        self.partner = self.env.ref("somconnexio.res_partner_2_demo")
        self.fake = Faker("es-ES")
        self.mandate = self.env.ref("somconnexio.demo_mandate_partner_2_demo")
        self.sb_product = self.env.ref(
            "switchboard_somconnexio.CentraletaVirtualSIMBasic"
        )

    def http_public_post(self, url, data, headers=None):
        if url.startswith("/"):
            url = "http://{}:{}{}".format(HOST, PORT, url)
        return self.session.post(url, json=data)

    def test_route_right_create(self, *args):
        url = "/public-api/contract"
        data = {
            "partner_id": self.partner.ref,
            "service_supplier": "Enreach Contact",
            "service_technology": "Switchboard",
            "ticket_number": "2024112900000015",
            "email": self.partner.email,
            "iban": self.mandate.partner_bank_id.acc_number,
            "switchboard_contract_service_info": {
                "SIP_channel_name": self.fake.name(),
                "extension": str(self.fake.random_int(1, 99)),
                "SIP_channel_password": self.fake.password(),
                "phone_number": self.fake.phone_number(),
                "mobile_phone_number": self.fake.phone_number(),
                "MAC_CPE_SIP": self.fake.mac_address(),
                "agent_email": self.fake.email(),
                "agent_name": self.fake.name(),
                "icc": "8934048319120034815",
            },
            "contract_lines": [
                {
                    "product_code": self.sb_product.default_code,
                    "date_start": "2024-11-01 00:00:00",
                },
                {"product_code": "CH_SC_OSO_SIM", "date_start": "2024-11-01 00:00:00"},
            ],
        }
        response = self.http_public_post(url, data=data)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertEquals(decoded_response, {"result": "OK"})

        content = self.env["contract.contract.process"].create(**data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertEquals(contract.partner_id, self.partner)
        self.assertEquals(
            contract.service_technology_id,
            self.env.ref("switchboard_somconnexio.service_technology_switchboard"),
        )
        self.assertEquals(
            contract.service_supplier_id,
            self.env.ref("switchboard_somconnexio.service_supplier_enreach"),
        )
        self.assertTrue(contract.switchboard_service_contract_info_id)
        self.assertEquals(
            contract.switchboard_service_contract_info_id.icc,
            data["switchboard_contract_service_info"]["icc"],
        )
        self.assertEquals(
            contract.switchboard_service_contract_info_id.phone_number,
            data["switchboard_contract_service_info"]["phone_number"],
        )
        self.assertEquals(
            contract.switchboard_mobile,
            data["switchboard_contract_service_info"]["mobile_phone_number"],
        )
        self.assertEquals(contract.mandate_id, self.mandate)
        self.assertEquals(contract.ticket_number, data["ticket_number"])
