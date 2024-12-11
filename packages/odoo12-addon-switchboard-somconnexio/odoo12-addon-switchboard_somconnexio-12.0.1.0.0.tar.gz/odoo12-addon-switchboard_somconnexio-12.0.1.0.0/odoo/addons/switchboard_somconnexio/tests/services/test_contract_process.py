from mock import patch
from odoo.exceptions import UserError
from odoo.addons.somconnexio.tests.services.contract_process.base_test_contract_process import (  # noqa
    BaseContractProcessTestCase,
)


@patch("pyopencell.resources.subscription.Subscription.get")
@patch(
    "odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractCreateService"  # noqa
)
class TestSwitchboardContractProcess(BaseContractProcessTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            "partner_id": self.partner.ref,
            "email": self.partner.email,
            "service_address": self.service_address,
            "service_technology": "Switchboard",
            "service_supplier": "Enreach Contact",
            "switchboard_contract_service_info": {
                "phone_number": "97272829",
                "phone_number_2": "97272830",
                "mobile_phone_number": "66687827",
                "icc": "82828288282",
                "extension": "8382",
                "agent_name": "agent1",
                "agent_email": "agent1",
                "MAC_CPE_SIP": "00:00:00:00:00:00",
                "SIP_channel_name": "agent1",
                "SIP_channel_password": "1234",
            },
            "contract_lines": [
                {
                    "product_code": (
                        self.browse_ref(
                            "switchboard_somconnexio.AgentCentraletaVirtualApp500"
                        ).default_code
                    ),
                    "date_start": "2024-08-27 00:00:00",
                }
            ],
            "iban": self.iban,
            "ticket_number": self.ticket_number,
        }
        self.process = self.env["sb.contract.process"]

    def test_contract_create(self, *args):
        content = self.process.create(**self.data)
        contract = self.env["contract.contract"].browse(content["id"])
        self.assertIn(
            self.browse_ref("switchboard_somconnexio.AgentCentraletaVirtualApp500"),
            [c.product_id for c in contract.contract_line_ids],
        )
        sb_info = contract.switchboard_service_contract_info_id
        sb_info_original_data = self.data["switchboard_contract_service_info"]

        self.assertEquals(sb_info.phone_number, sb_info_original_data["phone_number"])
        self.assertEquals(
            sb_info.phone_number_2, sb_info_original_data["phone_number_2"]
        )
        self.assertEquals(
            sb_info.mobile_phone_number, sb_info_original_data["mobile_phone_number"]
        )
        self.assertEquals(sb_info.icc, sb_info_original_data["icc"])
        self.assertEquals(sb_info.extension, sb_info_original_data["extension"])
        self.assertEquals(sb_info.agent_name, sb_info_original_data["agent_name"])
        self.assertEquals(sb_info.agent_email, sb_info_original_data["agent_email"])
        self.assertEquals(sb_info.MAC_CPE_SIP, sb_info_original_data["MAC_CPE_SIP"])
        self.assertEquals(
            sb_info.SIP_channel_name, sb_info_original_data["SIP_channel_name"]
        )
        self.assertEquals(
            sb_info.SIP_channel_password, sb_info_original_data["SIP_channel_password"]
        )

    def test_contract_create_missing_sb_contract_info(self, *args):
        self.data.pop("switchboard_contract_service_info")
        self.assertRaisesRegex(
            UserError,
            "Switchboard needs switchboard_contract_service_info",
            self.process.create,
            **self.data
        )

    def test_contract_create_missing_service_supplier(self, *args):
        self.data["service_supplier"] = "Other"
        self.assertRaisesRegex(
            UserError,
            "Switchboard needs Enreach Contact supplier",
            self.process.create,
            **self.data
        )
