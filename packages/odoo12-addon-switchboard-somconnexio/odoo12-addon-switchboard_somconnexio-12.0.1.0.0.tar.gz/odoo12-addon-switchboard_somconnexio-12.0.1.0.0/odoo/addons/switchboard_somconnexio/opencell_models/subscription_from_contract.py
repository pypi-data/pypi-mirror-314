from odoo import models


class SubscriptionFromContract(models.AbstractModel):
    _inherit = "subscription.from.contract"
    registration = True

    def _offerTemplate(self, contract):
        if contract.service_contract_type == "switchboard":
            return "OF_SC_TEMPLATE_CV"
        else:
            return super()._offerTemplate(contract)
