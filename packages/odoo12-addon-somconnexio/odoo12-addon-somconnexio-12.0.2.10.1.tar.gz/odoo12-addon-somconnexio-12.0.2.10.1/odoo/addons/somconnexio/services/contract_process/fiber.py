import logging

from odoo.exceptions import UserError
from odoo import models
from otrs_somconnexio.services.set_fiber_contract_code_mobile_ticket import (
    SetFiberContractCodeMobileTicket,
)
from otrs_somconnexio.services.unblock_mobile_pack_ticket import UnblockMobilePackTicket

from ..mobile_activation_date_service import MobileActivationDateService

_logger = logging.getLogger(__name__)


class FiberContractProcess(models.AbstractModel):
    _name = "fiber.contract.process"
    _inherit = "ba.contract.process"
    _register = True
    _description = """
        Fiber Contract creation
    """

    @staticmethod
    def validate_service_technology_deps(params):
        errors = []
        if "service_address" not in params:
            errors.append('Fiber needs "service_address"')
        fiber_suppliers = [
            "Asociatel VDF",
            "Vodafone",
            "Orange",
            "MásMóvil",
            "XOLN",
        ]
        if params["service_supplier"] not in fiber_suppliers:
            errors.append("Fiber needs {} suppliers".format(", ".join(fiber_suppliers)))
        else:
            if params["service_supplier"] in ["Asociatel VDF", "Vodafone"]:
                if "vodafone_fiber_contract_service_info" not in params:
                    errors.append(
                        "Vodafone Fiber needs vodafone_fiber_contract_service_info"
                    )
                if params.get("fiber_signal_type") == "fibraIndirecta":
                    errors.append(
                        'Fiber signal "Fibra Indirecta" needs MásMóvil supplier'
                    )
            elif params["service_supplier"] == "MásMóvil":
                if "mm_fiber_contract_service_info" not in params:
                    errors.append("MásMóvil Fiber needs mm_fiber_contract_service_info")
                if params.get("fiber_signal_type") in ("fibraCoaxial", "NEBAFTTH"):
                    errors.append(
                        'Fiber signal "{}" needs Vodafone supplier'.format(
                            params["fiber_signal_type"]
                        )
                    )
            elif params["service_supplier"] == "XOLN":
                if "xoln_fiber_contract_service_info" not in params:
                    errors.append("XOLN Fiber needs mm_fiber_contract_service_info")
            elif params["service_supplier"] == "Orange":
                if "orange_fiber_contract_service_info" not in params:
                    errors.append(
                        "Orange Fiber needs orange_fiber_contract_service_info"
                    )
        if errors:
            raise UserError("\n".join(errors))

    def _create_vodafone_fiber_contract_service_info(self, params):
        if not params:
            return False
        return (
            self.env["vodafone.fiber.service.contract.info"]
            .sudo()
            .create(
                {
                    "phone_number": params["phone_number"],
                    "vodafone_id": params["vodafone_id"],
                    "vodafone_offer_code": params["vodafone_offer_code"],
                }
            )
        )

    def _create_mm_fiber_contract_service_info(self, params):
        if not params:
            return False
        return (
            self.env["mm.fiber.service.contract.info"]
            .sudo()
            .create(
                {
                    "phone_number": params["phone_number"],
                    "mm_id": params["mm_id"],
                }
            )
        )

    def _create_orange_fiber_contract_service_info(self, params):
        if not params:
            return False
        return (
            self.env["orange.fiber.service.contract.info"]
            .sudo()
            .create(
                {
                    "suma_id": params["suma_id"],
                }
            )
        )

    def _create_xoln_fiber_contract_service_info(self, params):
        if not params:
            return False
        if "router_mac_address" in params and params["router_mac_address"] != "-":
            router_mac_address = params["router_mac_address"]
        else:
            router_mac_address = False
        router_product = self._get_router_product_id(params["router_product_id"])
        router_lot_id = self._create_router_lot_id(
            params["router_serial_number"],
            router_mac_address,
            router_product,
        )
        project_id = self._get_project_xoln_id_by_code(params["project"])

        return (
            self.env["xoln.fiber.service.contract.info"]
            .sudo()
            .create(
                {
                    "phone_number": params["phone_number"],
                    "external_id": params["external_id"],
                    "id_order": params["id_order"],
                    "project_id": project_id,
                    "router_product_id": router_product.id,
                    "router_lot_id": router_lot_id.id,
                }
            )
        )

    def create(self, **params):
        contract_dict = super().create(**params)
        # Update mobile tiquets
        self._update_pack_mobile_tickets(contract_dict)

        if params.get("mobile_pack_contracts"):
            self._relate_with_CU_former_mobile_contracts(
                contract_dict["id"], params.get("mobile_pack_contracts")
            )
        else:
            self._relate_new_fiber_with_existing_mobile_contracts(
                contract_dict
            )
        return contract_dict

    def _relate_with_CU_former_mobile_contracts(self, _id, mobile_pack_contracts):
        """
        When we create a contract from an address change petition (CU),
        we need to relate the mobile contracts linked with the
        former fiber contract with the new one
        """
        if mobile_pack_contracts:
            mobile_contracts = (
                self.env["contract.contract"]
                .sudo()
                .search([("code", "in", mobile_pack_contracts.split(","))])
            )
            for contract in mobile_contracts:
                contract.parent_pack_contract_id = _id

    def _relate_new_fiber_with_existing_mobile_contracts(
            self, contract_dict):
        """
        Link new fiber to an existing mobile contract, except:
          - New fiber contract comes from location_change
          - Within the fiber CRMLead there is a mobile with
            pack product (the fiber contract is needed to be
            packed with that mobile).
          - No existing mobile contract is found with appropiate
            mobile tariffs to be packed.
        """

        # Check that fiber contract does not come from a location change
        if contract_dict["create_reason"] == "location_change":
            return

        # Check if fiber CRMLead has mobile with pack product
        crm_lead_line = self.env["crm.lead.line"].sudo().search(
            [("ticket_number", "=", contract_dict["ticket_number"])]
        )
        mobile_lines = crm_lead_line.lead_id.lead_line_ids.filtered(
            "is_mobile").filtered("is_from_pack")
        if mobile_lines:
            return

        # Check existing mobile contracts
        mobile_tech_id = self.env.ref(
            "somconnexio.service_technology_mobile"
        ).id
        mobile_products_appropiate_to_pack = [
            self.env.ref("somconnexio.TrucadesIllimitades5GB").id,
            self.env.ref("somconnexio.TrucadesIllimitades10GB").id,
            self.env.ref("somconnexio.TrucadesIllimitades12GB").id,
            self.env.ref("somconnexio.TrucadesIllimitades20GB").id
        ]
        mobile_contracts = (
            self.env["contract.contract"]
            .sudo()
            .search([
                ("partner_id", "=", contract_dict["partner_id"]),
                ("service_technology_id", "=", mobile_tech_id),
                ("date_end", "=", False),
                ("parent_pack_contract_id", "=", False),
                ("current_tariff_product", "in", mobile_products_appropiate_to_pack)  # noqa
            ])
        )

        if not mobile_contracts:
            return

        if len(mobile_contracts) == 1:
            mbl_contract = mobile_contracts[0]
            fiber_contract = self.env["contract.contract"].sudo().search([
                ("code", "=", contract_dict["code"]),
                ("service_technology_id", "=", self.env.ref("somconnexio.service_technology_fiber").id),  # noqa
            ])

            # Create OTRS ticket for mobile tariff change
            pack_mobile_product_id = self.env.ref(
                "somconnexio.TrucadesIllimitades20GBPack"
            ).id
            wizard = self.env['contract.mobile.tariff.change.wizard'].with_context(  # noqa
                active_id=mbl_contract.id
            ).sudo().create({
                "summary": "Automatic mobile tariff change",
                "new_tariff_product_id": pack_mobile_product_id,
                "fiber_contract_to_link": fiber_contract.id,
                "exceptional_change": True,
                "otrs_checked": True,
                "send_notification": False,
            })
            wizard.button_change()

            # Send mail
            template = self.env.ref(
                'somconnexio.mobile_linked_with_fiber_email_template')
            template.sudo().send_mail(mbl_contract.id)

        else:
            # Send mail
            template = self.env.ref(
                'somconnexio.mobile_to_link_with_fiber_email_template')
            template.sudo().send_mail(contract_dict["partner_id"])

    def _update_pack_mobile_tickets(self, contract_dict):
        crm_lead_line = self.env["crm.lead.line"].sudo().search(
            [("ticket_number", "=", contract_dict["ticket_number"])]
        )
        mobile_lines = crm_lead_line.lead_id.lead_line_ids.filtered("is_mobile")
        if not mobile_lines:
            return True

        dates_service = MobileActivationDateService(
            self.env, crm_lead_line.is_portability()
        )
        introduced_date = dates_service.get_introduced_date()
        activation_date = dates_service.get_activation_date()

        for line in mobile_lines:
            UnblockMobilePackTicket(
                line.ticket_number,
                activation_date=str(activation_date),
                introduced_date=str(introduced_date),
            ).run()

        mobile_pack_lines = mobile_lines.filtered("is_from_pack")

        for line in mobile_pack_lines:
            SetFiberContractCodeMobileTicket(
                line.ticket_number,
                fiber_contract_code=contract_dict["code"],
            ).run()
