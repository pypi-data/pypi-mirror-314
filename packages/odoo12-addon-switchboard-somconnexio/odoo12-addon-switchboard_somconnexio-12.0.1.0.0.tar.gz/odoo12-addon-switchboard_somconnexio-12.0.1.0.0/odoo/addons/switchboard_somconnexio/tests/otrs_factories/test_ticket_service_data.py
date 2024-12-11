from unittest.mock import patch
from ..helper_service import crm_lead_create

from odoo.addons.somconnexio.tests.otrs_factories.test_ticket_service_data import (
    TestTicketServiceData as BaseTestTicketServiceData,
)


class TestTicketServiceData(BaseTestTicketServiceData):
    @patch(
        "odoo.addons.switchboard_somconnexio.otrs_factories.switchboard_data_from_crm_lead_line.SwitchboardDataFromCRMLeadLine.build"  # noqa
    )
    def test_build_switchboard(self, mock_build):
        mock_build.return_value = self.expected_data

        crm_lead = crm_lead_create(
            self.env,
            self.partner_id,
            "switchboard",
        )
        crm_lead_line = crm_lead.lead_line_ids[0]
        service_data = self.TicketServiceData.build(crm_lead_line)

        mock_build.assert_called_once_with()
        self.assertEqual(service_data, self.expected_data)
