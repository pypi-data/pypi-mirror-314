from odoo import models


class ContractService(models.AbstractModel):
    _inherit = "contract.service"
    _register = True

    def _to_dict(self, contract):
        data = super()._to_dict(contract)
        if contract.service_contract_type == "switchboard":
            data["subscription_type"] = contract.service_contract_type
        return data

    def _get_available_operations(self, contract):
        operations = super()._get_available_operations(contract)
        if contract.service_contract_type == "switchboard":
            operations = []
        return operations
