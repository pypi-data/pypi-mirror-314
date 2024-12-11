from odoo import models
from .opencell_types.custom_field import CustomField


class SubscriptionFromContract(models.AbstractModel):
    _name = "subscription.from.contract"
    _description = "Subscription From Contract"
    registration = True

    def _offerTemplate(self, contract):
        """
        Returns offer template code for current contract's service type.

        :return: offer template code (string)
        """

        if contract.service_contract_type == "mobile":
            return "OF_SC_TEMPLATE_MOB"
        else:
            return "OF_SC_TEMPLATE_BA"

    def _customFields(self, contract):
        if not contract.service_partner_id:
            return {}
        address = contract.service_partner_id
        fields = [
            ("CF_OF_SC_SUB_SERVICE_ADDRESS", address.full_street),
            ("CF_OF_SC_SUB_SERVICE_CP", address.zip),
            ("CF_OF_SC_SUB_SERVICE_CITY", address.city),
            ("CF_OF_SC_SUB_SERVICE_SUBDIVISION", address.state_id.name),
        ]
        return {
            "customField": [
                CustomField(name, value).to_dict() for name, value in fields
            ]
        }

    def build(self, contract, userAccount):
        """
        Returns subscription dictionary for current contract.

        :param contract: contract record
        :return: subscription dictionary
        """
        return {
            "code": contract.code,
            "description": contract.phone_number,
            "userAccount": userAccount,
            "offerTemplate": self._offerTemplate(contract),
            "subscriptionDate": contract.date_start.strftime("%Y-%m-%d"),
            "customFields": self._customFields(contract),
        }
