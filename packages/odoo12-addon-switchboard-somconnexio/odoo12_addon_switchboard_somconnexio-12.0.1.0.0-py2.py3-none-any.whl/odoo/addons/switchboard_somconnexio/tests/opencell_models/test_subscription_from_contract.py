from odoo.addons.somconnexio.tests.opencell_models.test_subscription_from_contract import (  # noqa
    SubscriptionFromContractTestCase,
)


class SubscriptionFromContractTestCase(SubscriptionFromContractTestCase):
    def test_switchboard_subscription_construct_ok(self):
        self.contract.service_contract_type = "switchboard"
        self.contract.service_partner_id = None

        subscription_from_contract = self.env["subscription.from.contract"].build(
            self.contract, self.crm_account_code
        )

        self._common_assert(subscription_from_contract, "OF_SC_TEMPLATE_CV")
        self.assertEqual(subscription_from_contract["customFields"], {})
