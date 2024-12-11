from odoo import fields
from odoo.addons.component.tests.common import ComponentMixin
from odoo.tests.common import SavepointCase


class TestContractLineListener(SavepointCase, ComponentMixin):
    @classmethod
    def setUpClass(cls):
        super(TestContractLineListener, cls).setUpClass()
        cls.setUpComponent()

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        SavepointCase.setUp(self)
        ComponentMixin.setUp(self)
        self.switchboard_service = self.browse_ref(
            "switchboard_somconnexio.AgentCentraletaVirtualApp500"
        )
        self.switchboard_contract = self.env.ref(
            "switchboard_somconnexio.contract_switchboard_app_500"
        )

    def test_create_line_with_switchboard_service(self):
        cl = self.env["contract.line"].create(
            {
                "name": self.switchboard_service.name,
                "contract_id": self.switchboard_contract.id,
                "product_id": self.switchboard_service.id,
                "date_start": fields.Date.today(),
            }
        )

        jobs_domain = [
            ("method_name", "=", "add_service"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [self.switchboard_contract.id, cl])
