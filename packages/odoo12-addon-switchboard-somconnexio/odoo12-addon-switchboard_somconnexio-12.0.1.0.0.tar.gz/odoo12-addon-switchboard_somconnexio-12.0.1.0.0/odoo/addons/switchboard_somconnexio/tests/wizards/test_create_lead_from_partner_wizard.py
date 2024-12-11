from mock import patch

from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase
from odoo.exceptions import MissingError


@patch(
    "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
)
class TestCreateLeadfromPartnerWizard(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner = self.browse_ref("somconnexio.res_partner_2_demo")
        self.email = self.env["res.partner"].create(
            {
                "parent_id": self.partner.id,
                "email": "new_email@test.com",
                "type": "contract-email",
            }
        )
        self.sb_categ = self.env.ref("switchboard_somconnexio.switchboard_category")

    def test_create_switchboard_lead(self, mock_get_fiber_contracts_to_pack):
        mock_get_fiber_contracts_to_pack.side_effect = MissingError("")

        business_team = self.env.ref("somconnexio.business")

        wizard = (
            self.env["partner.create.lead.wizard"]
            .with_context(active_id=self.partner.id)
            .create(
                {
                    "opportunity": "test SB portability",
                    "bank_id": self.partner.bank_ids.id,
                    "email_id": self.email.id,
                    "phone_contact": "882828282",
                    "product_id": self.ref(
                        "switchboard_somconnexio.AgentCentraletaVirtualAppUNL"
                    ),
                    "product_categ_id": self.sb_categ.id,
                    "team_id": business_team.id,
                    "type": "portability",
                    "icc": "88288202",
                    "extension": "1234",
                    "landline": "972972972",
                    "landline_2": "972972973",
                    "agent_name": "Agent Name",
                    "agent_email": "sb@somconnexio.coop",
                }
            )
        )

        product_templs = self.env["product.template"].search(
            [("categ_id", "=", self.sb_categ.id)]
        )
        expected_domain = [
            ("product_tmpl_id", "in", product_templs.ids),
            ("pack_ok", "=", False),
            (
                "attribute_value_ids",
                "!=",
                self.env.ref("somconnexio.IsInPack").id,
            ),
        ]
        self.assertEquals(
            wizard.available_products,
            self.env["product.product"].search(expected_domain),
        )

        crm_lead_action = wizard.create_lead()
        crm_lead = self.env["crm.lead"].browse(crm_lead_action["res_id"])
        crm_lead_line = crm_lead.lead_line_ids[0]

        self.assertEquals(
            crm_lead_action.get("xml_id"),
            "somconnexio.crm_case_form_view_pack",
        )

        self.assertEquals(crm_lead.name, "test SB portability")
        self.assertEquals(crm_lead.partner_id, self.partner)
        self.assertEquals(crm_lead.email_from, self.email.email)
        self.assertEquals(crm_lead_line.product_id, wizard.product_id)
        self.assertEquals(crm_lead_line.switchboard_isp_info.type, "portability")
        self.assertEquals(crm_lead_line.switchboard_isp_info.icc, wizard.icc)
        self.assertEquals(
            crm_lead_line.switchboard_isp_info.phone_number, wizard.landline
        )
        self.assertEquals(
            crm_lead_line.switchboard_isp_info.phone_number_2, wizard.landline_2
        )
        self.assertEquals(
            crm_lead_line.switchboard_isp_info.extension, wizard.extension
        )
