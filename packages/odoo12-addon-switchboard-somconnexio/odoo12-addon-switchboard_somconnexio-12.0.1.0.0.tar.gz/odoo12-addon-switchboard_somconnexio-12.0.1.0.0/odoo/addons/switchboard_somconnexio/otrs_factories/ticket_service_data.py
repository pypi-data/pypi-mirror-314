from odoo import models
from ..otrs_factories.switchboard_data_from_crm_lead_line import (
    SwitchboardDataFromCRMLeadLine,
)


class TicketServiceData(models.AbstractModel):
    _inherit = "ticket.service.data"
    register = True

    def build(self, crm_lead_line):
        if crm_lead_line.is_switchboard:
            service_data = SwitchboardDataFromCRMLeadLine(crm_lead_line)
            return service_data.build()
        else:
            return super().build(crm_lead_line)
