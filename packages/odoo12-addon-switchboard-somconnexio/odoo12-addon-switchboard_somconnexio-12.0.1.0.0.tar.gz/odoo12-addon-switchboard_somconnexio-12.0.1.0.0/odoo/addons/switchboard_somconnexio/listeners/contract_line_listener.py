from odoo.addons.component.core import Component

# 5 mins in seconds to delay the jobs
ETA = 300


class ContractLineListener(Component):
    _inherit = "contract.line.listener"
    _apply_on = ["contract.line"]

    def on_record_create(self, record, fields=None):
        super(ContractLineListener, self).on_record_create(record, fields)
        switchboard_categ_id = self.env.ref(
            "switchboard_somconnexio.switchboard_category"
        )

        if record.product_id.categ_id == switchboard_categ_id:
            self.env["contract.contract"].with_delay(eta=ETA).add_service(
                record.contract_id.id, record
            )
