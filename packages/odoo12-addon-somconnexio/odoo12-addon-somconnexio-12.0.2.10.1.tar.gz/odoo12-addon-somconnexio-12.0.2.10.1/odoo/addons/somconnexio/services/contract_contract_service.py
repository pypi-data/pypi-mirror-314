from odoo import models, _
from odoo.addons.base_rest.http import wrapJsonException
from odoo.exceptions import MissingError
from otrs_somconnexio.otrs_models.configurations.changes.change_tariff import (
    ChangeTariffSharedBondTicketConfiguration,
    ChangeTariffTicketConfiguration,
)
from otrs_somconnexio.services.search_tickets_service import SearchTicketsService
from datetime import datetime
from werkzeug.exceptions import BadRequest

from .res_partner_service import AddressService


class ContractService(models.AbstractModel):
    _name = "contract.service"
    _register = True
    _description = """
        Service to manage contracts
    """

    def search(self, **params):
        code = params.get("code")
        phone_number = params.get("phone_number")
        partner_vat = params.get("partner_vat")
        limit = params.get("limit", 10)
        offset = params.get("offset", 0)
        sortBy = params.get("sortBy", "")
        sortOrder = params.get("sortOrder", "")
        customer_ref = params.get("customer_ref", "")
        if limit:
            if isinstance(limit, int) or isinstance(limit, str) and limit.isdigit():
                limit = int(limit)
            else:
                raise wrapJsonException(
                    BadRequest("Limit must be numeric"),
                    include_description=True,
                )
        if offset:
            if isinstance(offset, int) or isinstance(offset, str) and offset.isdigit():
                offset = int(offset)
            else:
                raise wrapJsonException(
                    BadRequest("Offset must be numeric"),
                    include_description=True,
                )
        if sortBy:
            if sortBy not in self.env["contract.contract"].fields_get():
                raise wrapJsonException(
                    BadRequest("Invalid field to sortBy"), include_description=True
                )
        if sortOrder:
            if sortOrder == "ASCENDENT":
                pass
            elif sortOrder == "DESCENDENT":
                sortOrder = " DESC"
            else:
                raise wrapJsonException(
                    BadRequest("sortOrder must be ASCENDING or DESCENDING"),
                    include_description=True,
                )
        if code:
            domain = [("code", "=", code)]
            search_params = ["code"]
        elif customer_ref:
            domain = [("partner_id.ref", "=", customer_ref)]
            search_params = ["customer_ref"]
            self._add_customer_domain_filters(domain, params, search_params)
        elif phone_number:
            domain = [("phone_number", "=", phone_number)]
            search_params = ["phone_number"]
        elif partner_vat:
            domain = [
                ("partner_id.vat", "=", partner_vat),
                ("partner_id.parent_id", "=", False),
            ]
            search_params = ["partner_vat"]
        domain += [("is_terminated", "=", False)]
        contracts = (
            self.env["contract.contract"]
            .sudo()
            .search(domain, limit=limit, offset=offset, order=sortBy + sortOrder)
        )
        if not contracts:
            raise MissingError(
                _(
                    "No contract with {} could be found".format(
                        " - ".join(
                            [
                                ": ".join([search_param, params.get(search_param)])
                                for search_param in search_params
                            ]
                        )
                    )
                )
            )

        ret = {"contracts": [self._to_dict(contract) for contract in contracts]}
        if limit or offset or sortBy:
            ret["paging"] = {
                "limit": limit,
                "offset": offset,
                "totalNumberOfRecords": self.env["contract.contract"]
                .sudo()
                .search_count(domain),
            }
            if sortBy:
                ret["paging"].update(
                    {
                        "sortBy": sortBy,
                        "sortOrder": "DESCENDENT"
                        if sortOrder == " DESC"
                        else "ASCENDENT",
                    }
                )
        return ret

    def create(self, **params):
        self.env["contract.contract"].with_delay().create_contract(**params)
        return {"result": "OK"}

    def count(self):
        domain_contracts = [('is_terminated', '=', False)]
        domain_members = [
            ('parent_id', '=', False), ('customer', '=', True),
            '|', ('member', '=', True), ('coop_candidate', '=', True)
        ]
        number = self.env["contract.contract"].sudo().search_count(domain_contracts)
        result = {"contracts": number}
        number = self.env['res.partner'].sudo().search_count(domain_members)
        result['members'] = number
        return result

    def get_fiber_contracts_to_pack(self, **params):
        """
        Returns all contracts from the requested that match these
        conditions:
        - Own by requested partner (ref)
        - Supplier MM
        - Technology fiber
        - Not in pack (if not mobiles_sharing_data)
        """

        partner_ref = params.get('partner_ref')

        partner = self.env['res.partner'].sudo().search([
            ('parent_id', '=', False),
            ('ref', '=', partner_ref)
        ])

        if not partner:
            raise MissingError(
                "Partner with ref {} not found".format(
                    partner_ref)
                )

        contracts = (
            self.env["contract.contract"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", partner.id),
                    ("is_terminated", "=", False),
                    (
                        "service_technology_id",
                        "=",
                        self.env.ref("somconnexio.service_technology_fiber").id,
                    ),
                ]
            )
        )
        if params.get('mobiles_sharing_data') == 'true':
            contracts = contracts.filtered(
                lambda c: len(c.children_pack_contract_ids) == 1
                or not c.children_pack_contract_ids
            )
        else:
            contracts = contracts.filtered(
                lambda c: not c.children_pack_contract_ids
            )

        contracts = self._filter_out_fibers_used_in_OTRS_tickets(contracts)
        contracts = self._filter_out_fibers_used_in_ODOO_lead_lines(contracts)

        if not contracts:
            raise MissingError(
                _("No fiber contracts available to pack found with this user")
            )

        result = [self._to_dict(contract) for contract in contracts]

        return result

    def _to_dict(self, contract):
        contract.ensure_one()

        fiber_signal = contract.fiber_signal_type_id and \
            contract.fiber_signal_type_id.code or False

        return {
            "id": contract.id,
            "code": contract.code,
            "email": contract.partner_id.email or "",
            "customer_firstname": contract.partner_id.firstname or "",
            "customer_lastname": contract.partner_id.lastname or "",
            "customer_ref": contract.partner_id.ref or "",
            "customer_vat": contract.partner_id.vat or "",
            "phone_number": contract.phone_number,
            "current_tariff_product": contract.current_tariff_product.default_code,
            "description": contract.current_tariff_product.with_context(
                lang=contract.lang
            ).showed_name,
            "ticket_number": contract.ticket_number,
            "technology": contract.service_technology_id.name,
            "supplier": contract.service_supplier_id.name,
            "lang": contract.lang,
            "iban": contract.mandate_id.partner_bank_id.sanitized_acc_number,
            "is_terminated": contract.is_terminated,
            "date_start": contract.date_start,
            "date_end": contract.date_end,
            "fiber_signal": fiber_signal,
            "subscription_type": (
                "mobile" if contract.service_contract_type == "mobile" else "broadband"
            ),
            "address": AddressService(self.env, contract.service_partner_id).__dict__,
            "subscription_technology": (
                contract.service_contract_type
                if contract.service_contract_type in ("adsl", "mobile", "router4G")
                else "fiber"
            ),
            "available_operations": self._get_available_operations(contract),
            "parent_contract": contract.parent_pack_contract_id.code
            if contract.parent_pack_contract_id
            else "",
            "shared_bond_id": contract.shared_bond_id,
            "price": self._product_price(contract.current_tariff_product),
            "has_landline_phone": not bool(contract.current_tariff_product.without_fix)
            if contract.service_contract_type != "mobile"
            else False,
            "bandwidth": self._get_bandwidth(contract),
            "data": self._get_data(contract),
            "minutes": self._get_minutes(contract),
        }

    def _get_bandwidth(self, contract):
        return int(
            contract.current_tariff_product.without_lang().get_catalog_name("Bandwidth")
            or 0
        )

    def _get_minutes(self, contract):
        if contract.service_contract_type == "mobile":
            min = contract.current_tariff_product.without_lang().get_catalog_name("Min")
            return 99999 if min == "UNL" else int(min)
        return 0

    def _get_data(self, contract):
        return int(
            contract.current_tariff_product.without_lang().get_catalog_name("Data") or 0
        )

    def _get_available_operations(self, contract):
        """
        Resolve available operations to contract detail in somoffice
        """
        return (
            self._get_mobile_available_operations(contract)
            if contract.service_contract_type == "mobile"
            else self._get_broadband_available_operations(contract)
        )

    def _get_mobile_available_operations(self, contract):
        if contract.shared_bond_id:
            # mobile is sharing data
            return ["AddOneShotMobile"]
        else:
            mobile_available_operations = ["ChangeTariffMobile"]
            # check is contract with T-Conserva
            if (
                not contract.current_tariff_product.id
                == self.env.ref("somconnexio.TarifaConserva").id
            ):
                mobile_available_operations.append("AddOneShotMobile")
            # check bonified mobile with assocciated fiber
            if not contract.parent_pack_contract_id:
                mobile_available_operations.append("ChangeContractHolder")
            return mobile_available_operations

    def _get_broadband_available_operations(self, contract):
        if contract.service_contract_type == "router4G":
            return ["ChangeContractHolder"]
        elif contract.service_contract_type == "adsl":
            adsl_available_operations = ["ChangeContractHolder"]
            if contract.current_tariff_product.without_fix:
                adsl_available_operations.append("ChangeTariffFiberOutLandline")
            else:
                adsl_available_operations.append("ChangeTariffFiberLandline")
            return adsl_available_operations
        else:
            fiber_available_operations = []
            # Fiber
            if (
                not contract.current_tariff_product.without_fix
                and self._get_bandwidth(contract) <= 300
            ):
                # Fiber 100/300 without landline
                fiber_available_operations.append("ChangeTariffFiberOutLandline")
            if not contract.number_contracts_in_pack:
                # Fiber without mobiles associated
                fiber_available_operations.append("ChangeContractHolder")
            return fiber_available_operations

    def _filter_out_fibers_used_in_OTRS_tickets(self, contracts):
        """
        From a list of fiber contracts, search if any of their codes are
        already referenced in OTRS new mobile change tariff tickets
        (DF OdooContractRefRelacionat).
        If so, that fiber contract is about to be linked to a mobile offer,
        and shouldn't be available for others.
        Returns the original contract list excluding, if found,
        those referenced in OTRS.
        """

        if not contracts:
            return []

        partner = contracts[0].partner_id
        service = SearchTicketsService(
            [
                ChangeTariffTicketConfiguration,
                ChangeTariffSharedBondTicketConfiguration,
            ]
        )
        df_dct = {"OdooContractRefRelacionat": [c.code for c in contracts]}
        tickets_found = service.search(partner.ref, df_dct=df_dct)

        fiber_contracts_used_otrs = []
        for ticket in tickets_found:
            code = ticket.fiber_contract_code
            fiber_contracts_used_otrs.append(code)

        return contracts.filtered(lambda c: c.code not in fiber_contracts_used_otrs)

    def _filter_out_fibers_used_in_ODOO_lead_lines(self, contracts):
        """
        From a list of fiber contracts, search if any of them is
        already referenced in a mobile provisioning crm lead line
        (field `linked_fiber_contract_id`).
        If so, that fiber contract is about to be linked to a mobile
        offer, and shouldn't be available for others.
        Returns the original contract list excluding, if found,
        those linked in mobile lead lines.
        """

        if not contracts:
            return []

        stages_to_discard = [
            self.env.ref('crm.stage_lead4').id,
            self.env.ref('somconnexio.stage_lead5').id,
        ]
        partner_id = contracts[0].partner_id.id
        mbl_lead_lines = self.env["crm.lead.line"].search([
            ('partner_id', '=', partner_id),
            ('mobile_isp_info', '!=', False),
            ('stage_id', 'not in', stages_to_discard)
        ])

        already_linked_contracts = mbl_lead_lines.mapped(
            'mobile_isp_info').mapped('linked_fiber_contract_id')

        return contracts - already_linked_contracts

    def _product_price(self, product):
        pricelist_id = self.env["product.pricelist"].search([("code", "=", "21IVA")])
        return product.with_context(pricelist=pricelist_id.id).price

    def terminate(self, **params):
        contract_code = params["code"]
        terminate_reason_code = params["terminate_reason"]
        terminate_comment = params.get("terminate_comment")
        terminate_date = datetime.strptime(params["terminate_date"], "%Y-%m-%d").date()
        terminate_user_reason_code = params["terminate_user_reason"]

        contract = self.env["contract.contract"].search([("code", "=", contract_code)])
        terminate_reason = self.env["contract.terminate.reason"].search(
            [("code", "=", terminate_reason_code)]
        )
        terminate_user_reason = self.env["contract.terminate.user.reason"].search(
            [("code", "=", terminate_user_reason_code)]
        )

        if not contract:
            raise MissingError(
                _("Contract with code {} not found.".format(contract_code))
            )
        if not terminate_reason:
            raise MissingError(
                _(
                    "Terminate reason with code {} not found.".format(
                        terminate_reason_code
                    )
                )
            )
        if not terminate_user_reason:
            raise MissingError(
                _(
                    "Terminate user reason with code {} not found.".format(
                        terminate_user_reason_code
                    )
                )
            )

        contract.sudo().terminate_contract(
            terminate_reason, terminate_comment, terminate_date, terminate_user_reason
        )
        return {"result": "OK"}

    def get_terminate_reasons(self):
        terminate_reasons = self.env["contract.terminate.reason"].search([])
        user_terminate_reasons = self.env["contract.terminate.user.reason"].search([])

        return {
            "terminate_reasons": [
                {"code": reason.code, "name": reason.name}
                for reason in terminate_reasons
            ],
            "terminate_user_reasons": [
                {"code": reason.code, "name": reason.name}
                for reason in user_terminate_reasons
            ],
        }

    def _add_customer_domain_filters(self, domain, params, search_params):
        phone_number = params.get("phone_number")
        subscription_type = params.get("subscription_type")

        if phone_number:
            domain += [("phone_number", "ilike", phone_number)]
            search_params += ["phone_number"]
        if subscription_type:
            domain += [
                (
                    "service_technology_id",
                    "=" if subscription_type == "mobile" else "!=",
                    self.env.ref("somconnexio.service_technology_mobile").id,
                )
            ]
            search_params += ["subscription_type"]
