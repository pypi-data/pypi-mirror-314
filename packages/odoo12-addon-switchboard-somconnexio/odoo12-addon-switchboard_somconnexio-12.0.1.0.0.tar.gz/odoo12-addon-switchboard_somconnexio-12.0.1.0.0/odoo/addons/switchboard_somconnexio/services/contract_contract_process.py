from odoo import models


class ContractContractProcess(models.AbstractModel):
    _inherit = "contract.contract.process"
    _register = True
    _description = """
      ContractContractProcess --> ContractProcessFactory

      Refactor to separate the methods of contracts in classes with type as scope.
      We create the MobileContractProcess, ADSLContractProcess, FiberContractProcess,
      Router4GContractProcess and SBContractProcess classes.

        BaseContractProcess
               |
               |
        -----------------------------------------------------
        |                         |                         |
    MobileContractProcess         |                 SBContractProcess
                          BAContractProcess
                                  |
                -------------------------------------
                |                 |                 |
        ADSLContractProcess       |     Router4GContractProcess
                                  |
                           FiberContractProcess
    """

    # pylint: disable=W8106
    def create(self, **params):
        service_technology = params["service_technology"]
        if service_technology == "Switchboard":
            Contract = self.env["sb.contract.process"]
            return Contract.create(**params)
        else:
            return super().create(**params)
