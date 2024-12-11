import logging
import os
import re

from itertools import combinations

from socket import error as SocketError
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout as TimeOut

from correos_preregistro.errors import (
    InvalidApiResponse,
    MissingData,
    UnknownApiResponse,
)
from correos_seguimiento.services.shipment import (
    InvalidApiResponse as InvalidApiResponseSeguimiento,
)
from correos_seguimiento.services.shipment import (
    InvalidCredentials,
    InvalidEndpoint,
    TrackingShipment,
    UndefinedCredentials,
)
from correos_seguimiento.errors import (
    UnknownApiResponse as UnknownApiResponseSeguimiento,
)
from odoo import _, api, fields, models
from odoo.addons.queue_job.job import job
from odoo.exceptions import MissingError, ValidationError
from otrs_somconnexio.client import OTRSClient
from otrs_somconnexio.exceptions import TicketNotReadyToBeUpdatedWithSIMReceivedData
from otrs_somconnexio.services.set_SIM_recieved_mobile_ticket import (
    SetSIMRecievedMobileTicket,
)
from otrs_somconnexio.services.set_SIM_returned_mobile_ticket import (
    SetSIMReturnedMobileTicket,
)

from ..helpers.job_retry_utils import retry_on_error
from ..helpers.bank_utils import BankUtils
from ..correos_services.shipment import DELIVERY_ARGS, CorreosShipment
from ..services.mobile_activation_date_service import MobileActivationDateService

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"
    subscription_request_id = fields.Many2one(
        "subscription.request", "Subscription Request"
    )

    skip_duplicated_phone_validation = fields.Boolean(
        string="Skip duplicated phone validation",
    )

    partner_category_id = fields.Many2many(
        "res.partner.category",
        string="Tags",
        related="partner_id.category_id",
    )
    create_date = fields.Datetime("Creation Date")

    mobile_lead_line_ids = fields.One2many(
        "crm.lead.line",
        string="Mobile lead lines",
        compute="_compute_mobile_lead_line_ids",
    )

    broadband_lead_line_ids = fields.One2many(
        "crm.lead.line",
        string="BA lead lines",
        compute="_compute_broadband_lead_line_ids",
    )

    has_mobile_lead_lines = fields.Boolean(
        compute="_compute_has_mobile_lead_lines", store=True
    )
    has_broadband_lead_lines = fields.Boolean(
        compute="_compute_has_broadband_lead_lines", store=True
    )
    broadband_wo_fix_lead_line_ids = fields.One2many(
        "crm.lead.line",
        string="BA without fix lead lines",
        compute="_compute_broadband_wo_fix_lead_line_ids",
    )
    broadband_w_fix_lead_line_ids = fields.One2many(
        "crm.lead.line",
        string="BA with fix lead lines",
        compute="_compute_broadband_w_fix_lead_line_ids",
    )
    phones_from_lead = fields.Char(compute="_compute_phones_from_lead", store=True)
    sims_to_deliver = fields.Selection(
        [("none", "None"), ("one", "One"), ("multiple", "multiple")],
        compute="_compute_sims_to_deliver",
        store=True,
    )
    correos_tracking_code = fields.Char(string="Correos Tracking Code")
    sim_delivery_in_course = fields.Boolean()
    email_sent = fields.Boolean()
    is_broadband_isp_info_type_location_change = fields.Boolean(
        compute="_compute_is_broadband_isp_info_type_location_change"
    )

    def _ensure_crm_lead_iban_belongs_to_partner(self, crm_lead):
        partner_iban_list = crm_lead.partner_id.bank_ids.mapped("sanitized_acc_number")
        crm_lead_iban_list = crm_lead.lead_line_ids.mapped("iban")

        # IBANS present in CRM Lead Lines but not found with their partner
        missing_ibans = [
            iban
            for iban in crm_lead_iban_list
            if iban and iban not in partner_iban_list
        ]
        for iban in missing_ibans:
            self.env["res.partner.bank"].create(
                {
                    "acc_type": "iban",
                    "acc_number": iban,
                    "partner_id": crm_lead.partner_id.id,
                }
            )

    def action_set_won(self):
        for crm_lead in self:
            crm_lead.validate_won()
            crm_lead.validate_icc()
            if crm_lead.lead_line_ids.mapped("iban"):
                self._ensure_crm_lead_iban_belongs_to_partner(crm_lead)
        super(CrmLead, self).action_set_won()

    def validate_won(self):
        if self.stage_id not in [
            self.env.ref("crm.stage_lead3"),
            self.env.ref("somconnexio.stage_lead6"),
        ]:
            raise ValidationError(
                _("The crm lead must be in remesa or delivery generated stage.")
            )

    def validate_icc(self):
        for line in self.lead_line_ids.filtered("is_mobile"):
            if not line.mobile_isp_info.icc:
                raise ValidationError(
                    _("The ICC value of all mobile lines is not filled")
                )
            icc_prefix = self.env["ir.config_parameter"].get_param(
                "somconnexio.icc_start_sequence"
            )
            if (
                not line.mobile_isp_info.icc.startswith(icc_prefix)
                or len(line.mobile_isp_info.icc) != 19
            ):
                raise ValidationError(
                    _(
                        "The value of ICC is not right: it must contain "
                        "19 digits and starts with {}"
                    ).format(icc_prefix)
                )

    @api.depends("lead_line_ids")
    def _compute_mobile_lead_line_ids(self):
        for crm in self:
            crm.mobile_lead_line_ids = crm.lead_line_ids.filtered(lambda p: p.is_mobile)

    @api.depends("mobile_lead_line_ids")
    def _compute_has_mobile_lead_lines(self):
        for crm in self:
            crm.has_mobile_lead_lines = bool(crm.mobile_lead_line_ids)

    @api.depends("lead_line_ids")
    def _compute_broadband_lead_line_ids(self):
        for crm in self:
            crm.broadband_lead_line_ids = crm.lead_line_ids.filtered(
                lambda p: p.is_4G or p.is_adsl or p.is_fiber
            )

    @api.depends("broadband_lead_line_ids")
    def _compute_has_broadband_lead_lines(self):
        for crm in self:
            crm.has_broadband_lead_lines = bool(crm.broadband_lead_line_ids)

    @api.depends("broadband_lead_line_ids")
    def _compute_broadband_wo_fix_lead_line_ids(self):
        for record in self:
            record.broadband_wo_fix_lead_line_ids = (
                record.broadband_lead_line_ids.filtered(
                    lambda l: (l.product_id.without_fix)
                )
            )

    @api.depends("broadband_lead_line_ids")
    def _compute_broadband_w_fix_lead_line_ids(self):
        for record in self:
            record.broadband_w_fix_lead_line_ids = (
                record.broadband_lead_line_ids.filtered(
                    lambda l: (not l.is_mobile and not l.product_id.without_fix)
                )
            )

    @api.depends("lead_line_ids")
    def _compute_phones_from_lead(self):
        for crm in self:
            mbl_phones = crm.mobile_lead_line_ids.mapped("mobile_isp_info_phone_number")
            ba_phones = crm.broadband_lead_line_ids.filtered(
                lambda l: (
                    l.broadband_isp_info_phone_number
                    and l.broadband_isp_info_phone_number != "-"
                )
            ).mapped("broadband_isp_info_phone_number")

            crm.phones_from_lead = mbl_phones + ba_phones

    @api.depends("lead_line_ids", "lead_line_ids.mobile_isp_info_has_sim",
                 "lead_line_ids.active")
    def _compute_sims_to_deliver(self):
        for crm in self:
            mobile_lines_without_sims = crm.lead_line_ids.filtered(
                lambda line: (
                    line.is_mobile and not line.mobile_isp_info_has_sim and line.active)
            )
            if not mobile_lines_without_sims:
                crm.sims_to_deliver = "none"
            elif len(mobile_lines_without_sims) == 1:
                crm.sims_to_deliver = "one"
            else:
                crm.sims_to_deliver = "multiple"

    def _get_email_from_partner_or_SR(self, vals):
        if vals.get("partner_id"):
            contact_id = vals.get("partner_id")
            model = self.env["res.partner"]
        else:
            contact_id = vals.get("subscription_request_id")
            model = self.env["subscription.request"]
        return model.browse(contact_id).email

    @api.model
    def create(self, vals):
        if not vals.get("email_from"):
            vals["email_from"] = self._get_email_from_partner_or_SR(vals)
        if not vals.get("team_id"):
            vals["team_id"] = self.env.ref("somconnexio.residential").id
        leads = super(CrmLead, self).create(vals)
        return leads

    def action_set_paused(self):
        paused_stage_id = self.env.ref("crm.stage_lead2").id
        for crm_lead in self:
            crm_lead.write({"stage_id": paused_stage_id})

    def action_set_remesa(self):
        remesa_stage_id = self.env.ref("crm.stage_lead3").id
        for crm_lead in self:
            crm_lead.validate_remesa()
            crm_lead.write({"stage_id": remesa_stage_id})

    def action_set_cancelled(self):
        cancelled_stage_id = self.env.ref("somconnexio.stage_lead5").id
        for crm_lead in self:
            crm_lead.write({"stage_id": cancelled_stage_id, "probability": 0})

    def action_set_delivery_generated(self):
        for crm_lead in self:
            crm_lead.sim_delivery_in_course = True
            crm_lead.write({"stage_id": self.env.ref("somconnexio.stage_lead8").id})

    def action_send_email(self):
        for crm_lead in self:
            template = crm_lead.with_context(
                lang=crm_lead.partner_id.lang
            )._get_crm_lead_creation_email_template()

            template.sudo().send_mail(crm_lead.id)
            crm_lead.email_sent = True

    def validate_remesa(self):
        self.ensure_one()
        # Check if related SR is validated
        if not self.partner_id:
            raise ValidationError(
                _(
                    "Error in {}: The subscription request related must be validated."
                ).format(self.id)
            )
        for iban in self.lead_line_ids.mapped("iban"):
            BankUtils.validate_iban(iban, self.env)
        # Validate phone number
        self._validate_phone_number()

        if self.stage_id not in [
            self.env.ref("crm.stage_lead1"),
            self.env.ref("somconnexio.stage_lead7"),
        ]:
            raise ValidationError(_("The crm lead must be in new stage."))

    def validate_leads_to_generate_SIM_delivery(self):
        self.ensure_one()
        if self.stage_id not in [
            self.env.ref("crm.stage_lead3"),
            self.env.ref("somconnexio.stage_lead8"),
        ]:
            raise ValidationError(
                _("The crm lead with id {} must be in remesa stage.").format(self.id)
            )

        if self.sims_to_deliver == "none":
            raise ValidationError(
                _("The crm lead with id {} does not need SIM delivery.").format(self.id)
            )

    def _phones_already_used(self, line):
        # Avoid phone duplicity validation with address change leads
        if line.create_reason == "location_change":
            self.skip_duplicated_phone_validation = True

        if self.skip_duplicated_phone_validation:
            return False

        phone = False
        if line.mobile_isp_info:
            phone = line.mobile_isp_info.phone_number
        else:
            phone = line.broadband_isp_info.phone_number
        if not phone or phone == "-":
            return False
        contracts = self.env["contract.contract"].search(
            [
                ("is_terminated", "=", False),
                "|",
                "|",
                "|",
                ("mobile_contract_service_info_id.phone_number", "=", phone),
                ("vodafone_fiber_service_contract_info_id.phone_number", "=", phone),
                ("mm_fiber_service_contract_info_id.phone_number", "=", phone),
                ("adsl_service_contract_info_id.phone_number", "=", phone),
            ]
        )
        won_stage_id = self.env.ref("crm.stage_lead4").id
        remesa_stage_id = self.env.ref("crm.stage_lead3").id
        new_stage_id = self.env.ref("crm.stage_lead1").id
        order_lines = self.env["crm.lead.line"].search([
            "|",
            ("lead_id.stage_id", "=", won_stage_id),
            ("lead_id.stage_id", "=", remesa_stage_id),
            "|",
            ("mobile_isp_info.phone_number", "=", phone),
            ("broadband_isp_info.phone_number", "=", phone),
        ])
        if contracts or order_lines:
            raise ValidationError(
                _("Error in {}: Contract or validated CRMLead with the same phone already exists.").format(self.id)  # noqa
            )
        new_lines = self.env["crm.lead.line"].search([
            ("lead_id.stage_id", "=", new_stage_id),
            "|",
            ("mobile_isp_info.phone_number", "=", phone),
            ("broadband_isp_info.phone_number", "=", phone),
        ])
        if len(new_lines) > 1:
            raise ValidationError(
                _("Error in {}: Duplicated phone number in CRMLead petitions.").format(self.id)  # noqa
            )

    def _phone_number_portability_format_validation(self, line):
        if line.mobile_isp_info_type == 'portability' or line.broadband_isp_info_type == 'portability':  # noqa
            phone = line.mobile_isp_info_phone_number or line.broadband_isp_info_phone_number  # noqa
            if not phone:
                raise ValidationError(
                    _('Phone number is required in a portability')
                )
            pattern = None
            if line.mobile_isp_info:
                pattern = re.compile(r"^(6|7)?[0-9]{8}$")
                message = _('Mobile phone number has to be a 9 digit number starting with 6 or 7')  # noqa
            elif not line.check_phone_number:
                pattern = re.compile(r"^(8|9)?[0-9]{8}$|^-$")
                message = _(
                    'Landline phone number has to be a dash "-" or a 9 digit number starting with 8 or 9'  # noqa
                )

            isValid = pattern.match(phone) if pattern else True
            if not isValid:
                raise ValidationError(message)

    def _validate_phone_number(self):
        self.ensure_one()
        for line in self.lead_line_ids:
            self._phone_number_portability_format_validation(line)
            self._phones_already_used(line)

    @api.multi
    def action_set_new(self):
        for lead in self:
            new_stage_id = self.env.ref("crm.stage_lead1")
            lead.write({"stage_id": new_stage_id.id})

    @api.multi
    def action_restore(self):
        for lead in self:
            lead.toggle_active()
            new_stage_id = self.env.ref("crm.stage_lead1")
            lead.write({"stage_id": new_stage_id.id})

    @job
    def link_pack_tickets(self):
        fiber_ticket = None
        fiber_ticket_number = ""
        OTRS_client = OTRSClient()
        mobile_ticket_numbers = {
            line.id: line.ticket_number for line in self.lead_line_ids if line.is_mobile
        }
        mobile_tickets = {
            mobile_ticket_number: OTRS_client.get_ticket_by_number(mobile_ticket_number)
            for mobile_ticket_number in mobile_ticket_numbers.values()
            if mobile_ticket_number
        }
        for line in [line for line in self.lead_line_ids if line.ticket_number]:
            if line.is_fiber:
                fiber_ticket_number = line.ticket_number
                fiber_ticket = OTRS_client.get_ticket_by_number(fiber_ticket_number)

        if not all(mobile_ticket_numbers.values()) or not fiber_ticket_number:
            raise MissingError(
                _(
                    "Either mobile or fiber ticket numbers where not found among "
                    "the lines of this pack CRMLead"
                )
            )
        if not all(mobile_tickets.values()):
            raise MissingError(
                _("Mobile tickets not found in OTRS with ticket_numbers {}").format(
                    ",".join(
                        number
                        for number in mobile_tickets
                        if not mobile_tickets[number]
                    )
                )
            )
        elif not fiber_ticket:
            raise MissingError(
                _("Fiber ticket not found in OTRS with ticket_number {}").format(
                    fiber_ticket_number
                )
            )
        for mobile_ticket in mobile_tickets.values():
            OTRS_client.link_tickets(
                fiber_ticket.tid, mobile_ticket.tid, link_type="ParentChild"
            )

    @job
    def link_sharing_data_mobile_tickets(self):
        OTRS_client = OTRSClient()

        # Either 2 or 3 lines
        sharing_data_mobile_lines = self.mobile_lead_line_ids.filtered(
            lambda l: (l.product_id.has_sharing_data_bond)
        )
        if len(sharing_data_mobile_lines) not in [2, 3]:
            raise ValidationError(
                _("We cannot share bonds with <2 or >3 mobiles")
            )

        sharing_data_mobile_tickets = [
            OTRS_client.get_ticket_by_number(line.ticket_number)
            for line in sharing_data_mobile_lines
        ]
        tickets_paired = combinations(sharing_data_mobile_tickets, 2)
        for pair_combination in tickets_paired:
            paired_tickets = list(pair_combination)
            OTRS_client.link_tickets(
                paired_tickets[0].tid, paired_tickets[1].tid,
                link_type="Normal"
            )

    @retry_on_error(
        retries=20,
        delay=300,
        errors=[InvalidEndpoint, ConnectionError, SocketError, TimeOut],
    )
    @job(default_channel="root.tracking_correos")
    def track_correos_delivery(self):
        # TODO: Move this method to a separated service to interact with Correos.
        try:
            delivery = TrackingShipment(
                os.environ['CORREOS_USER'],
                os.environ['CORREOS_PASSWORD'],
                self.correos_tracking_code
            ).build()

            if delivery.is_returned():
                self.message_post(
                    _(
                        "Return Process\nThe tracking code {tracking_code} is no loger valid"  # noqa
                    ).format(tracking_code=self.correos_tracking_code)
                )
                for line in self.lead_line_ids:
                    if not line.is_mobile or line.mobile_isp_info_has_sim:
                        continue
                    SetSIMReturnedMobileTicket(line.ticket_number).run()
                self.sim_delivery_in_course = False
                self.correos_tracking_code = False
            elif delivery.is_delivered():
                for line in self.lead_line_ids:
                    if not line.is_mobile or line.mobile_isp_info_has_sim:
                        continue
                    date_service = MobileActivationDateService(
                        self.env,
                        line.is_portability(),
                    )
                    SetSIMRecievedMobileTicket(
                        line.ticket_number,
                        date_service.get_activation_date(),
                        date_service.get_introduced_date(),
                    ).run()
                self.sim_delivery_in_course = False
            else:
                if delivery.is_relabeled():
                    old_tracking_code = self.correos_tracking_code
                    self.correos_tracking_code = delivery.get_relabeled_shipment_code()

                    self.message_post(
                        _(
                            "The shipment code was relabeled from: {old} to {new}"
                        ).format(old=old_tracking_code, new=self.correos_tracking_code)
                    )

        except IndexError:
            raise IndexError(_("IndexError while retrieving relabeled shipment code"))
        except KeyError:
            raise KeyError(_("KeyError while retrieving relabeled shipment code"))
        except UndefinedCredentials:
            raise UndefinedCredentials(_('Credentials for Correos API are not defined'))
        except InvalidCredentials:
            raise InvalidCredentials(_('Credentials for Correos API are not valid'))
        except InvalidEndpoint:
            raise InvalidEndpoint(_('Endpoint is wrong or is down'))
        except ConnectionError:
            raise ConnectionError(_('Connection with Correos API failed'))
        except SocketError:
            raise SocketError(_('Connection with Correos API failed'))
        except UnknownApiResponseSeguimiento:
            raise UnknownApiResponseSeguimiento(
                _("The JSON shows a data format that can't be parsed")
            )
        except InvalidApiResponseSeguimiento:
            raise InvalidApiResponseSeguimiento(_('Returned data is not JSON valid'))
        except TicketNotReadyToBeUpdatedWithSIMReceivedData:
            pass

    @api.model
    def cron_track_correos_delivery(self):
        domain = [
            ('stage_id', '=', self.env.ref("crm.stage_lead4").id),
            ('sims_to_deliver', '!=', 'none'),
            ('sim_delivery_in_course', '=', True)
        ]
        crm_leads = self.search(domain)
        for lead in crm_leads:
            lead.with_delay(max_retries=3).track_correos_delivery()

    @job
    def create_shipment(self, delivery_args=None):
        delivery_OK_stage_id = self.env.ref("somconnexio.stage_lead6").id
        delivery_KO_stage_id = self.env.ref("somconnexio.stage_lead7").id
        self.validate_leads_to_generate_SIM_delivery()
        try:
            self._create_shipment(delivery_args)
            self.write({"stage_id": delivery_OK_stage_id})
        except (MissingData, UnknownApiResponse, InvalidApiResponse) as e:
            self.write({"stage_id": delivery_KO_stage_id})
            if isinstance(e, MissingData):
                message = _(
                    "Error sending the delivery to Correos with the next field: {}"  # noqa
                ).format(e.field)
            else:
                message = _(
                    "Error sending the delivery to Correos. Contact with Sistemas team. Error: {}"  # noqa
                ).format(e.message)
            self.message_post(message)

    def _create_shipment(self, delivery_args):
        """Create a Correos shipment and save the PDF label and the
        shipment_code in the CRMLead."""
        shipment = CorreosShipment().create(self, delivery_args)
        self.write(
            {
                "correos_tracking_code": shipment.shipment_code,
                "sims_delivery_in_course": True,
            }
        )
        name = "shipment_{}".format(shipment.shipment_code)
        self.env["ir.attachment"].create(
            {
                "name": name,
                "type": "binary",
                "datas": shipment.label_file,
                "datas_fname": name + ".pdf",
                "store_fname": name,
                "res_model": "crm.lead",
                "res_id": self.id,
                "mimetype": "application/x-pdf",
            }
        )

    def action_generate_express_delivery(self):
        for crm_lead in self:
            crm_lead.with_delay().create_shipment(DELIVERY_ARGS["express"])

    def _get_crm_lead_creation_email_template(self):
        return self.env.ref("somconnexio.crm_lead_creation_manual_email_template")

    @api.depends("broadband_lead_line_ids")
    def _compute_is_broadband_isp_info_type_location_change(self):
        for record in self:
            record.is_broadband_isp_info_type_location_change = any(
                line.broadband_isp_info.type == "location_change"
                for line in record.lead_line_ids
                if line.broadband_isp_info
            )


class Tag(models.Model):
    _inherit = "crm.lead.tag"
    code = fields.Char("Code")
