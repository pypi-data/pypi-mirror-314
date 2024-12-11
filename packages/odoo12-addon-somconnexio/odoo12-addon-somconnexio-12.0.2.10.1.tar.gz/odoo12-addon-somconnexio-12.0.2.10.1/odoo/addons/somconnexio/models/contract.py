from datetime import date
from otrs_somconnexio.services.search_tickets_service import SearchTicketsService
from otrs_somconnexio.services.activate_change_tarriff_mobile_tickets import (
    ActivateChangeTariffMobileTickets,
)
from otrs_somconnexio.otrs_models.configurations.changes.change_tariff import (
    ChangeTariffSharedBondTicketConfiguration,
    ChangeTariffTicketConfiguration,
)
from odoo import _, api, fields, models
from odoo.addons.queue_job.job import job
from odoo.exceptions import UserError, ValidationError

from ..opencell_services.crm_account_hierarchy_create_service import (
    CRMAccountHierarchyFromContractCreateService,
)
from ..opencell_services.crm_account_hierarchy_update_service import (
    CRMAccountHierarchyFromContractUpdateService,
)
from ..opencell_services.subscription_service import SubscriptionService
from .opencell_configuration import OpenCellConfiguration


class Contract(models.Model):
    _inherit = 'contract.contract'

    def _get_default_journal(self):
        return self.env.ref('somconnexio.consumption_invoices_journal')

    def name_get(self):
        res = []
        for contract in self:
            if contract.is_broadband:
                address = (
                    contract.service_partner_id
                    if contract.service_partner_id
                    else contract.partner_id
                )
                name = "{} - {}, {}, {}, {}".format(
                    contract.name,
                    address.full_street,
                    address.city,
                    address.zip,
                    address.state_id.name,
                )
                res.append((contract.id, name))
            else:
                res.append((contract.id, contract.name))
        return res

    name = fields.Char(compute='_compute_name', store=True, readonly=True)
    service_technology_id = fields.Many2one(
        'service.technology',
        'Service Technology',
        required=True,
    )
    service_supplier_id = fields.Many2one(
        'service.supplier',
        'Service Supplier',
        required=True,
    )

    service_partner_id = fields.Many2one(
        'res.partner',
        'Service Contact',
    )
    is_broadband = fields.Boolean(
        compute="_compute_is_broadband",
    )
    service_contract_type = fields.Char(
        compute="_compute_contract_type",
    )
    email_ids = fields.Many2many(
        'res.partner',
        string='Emails',
    )
    available_email_ids = fields.Many2many(
        "res.partner", string="Available Emails", compute="_compute_available_email_ids"
    )

    crm_lead_line_id = fields.Many2one(
        'crm.lead.line',
        string="Crm Lead Line"
    )
    mobile_contract_service_info_id = fields.Many2one(
        'mobile.service.contract.info',
        domain=[('id', '=', 0)],
        string='Service Contract Info'
    )
    vodafone_fiber_service_contract_info_id = fields.Many2one(
        'vodafone.fiber.service.contract.info',
        domain=[('id', '=', 0)],
        string="Service Contract Info"
    )
    mm_fiber_service_contract_info_id = fields.Many2one(
        'mm.fiber.service.contract.info',
        domain=[('id', '=', 0)],
        string='Service Contract Info'
    )
    orange_fiber_service_contract_info_id = fields.Many2one(
        'orange.fiber.service.contract.info',
        domain=[('id', '=', 0)],
        string='Service Contract Info'
    )
    router_4G_service_contract_info_id = fields.Many2one(
        "router.4g.service.contract.info",
        domain=[("id", "=", 0)],
        string="Service Contract Info",
    )
    xoln_fiber_service_contract_info_id = fields.Many2one(
        'xoln.fiber.service.contract.info',
        domain=[('id', '=', 0)],
        string='Service Contract Info'
    )
    adsl_service_contract_info_id = fields.Many2one(
        'adsl.service.contract.info',
        domain=[('id', '=', 0)],
        string='Service Contract Info'
    )
    current_tariff_contract_line = fields.Many2one(
        'contract.line',
        compute='_compute_current_tariff_contract_line',
        store=True
    )
    tariff_contract_line = fields.Many2one(
        'contract.line',
        compute='_compute_tariff_contract_line',
    )
    current_tariff_product = fields.Many2one(
        'product.product',
        related='current_tariff_contract_line.product_id',
        string="Current Tariff",
        store=True
    )
    current_tariff_start_date = fields.Date(
        string="Current Tariff Start Date",
        related='current_tariff_contract_line.date_start',
        store=True
    )
    tariff_product = fields.Many2one(
        'product.product',
        related='tariff_contract_line.product_id',
        string="Current Tariff"
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        default=_get_default_journal,
    )

    date_start = fields.Date(
        compute='_compute_date_start', string='Date Start', store=True
    )
    phone_number = fields.Char(
        compute='_compute_phone_number', string='Service Phone Number', store=True
    )
    icc = fields.Char(
        "ICC", compute="_compute_icc", inverse="_inverse_set_icc", store=True
    )
    ppp_user = fields.Char(
        'PPP User', related='adsl_service_contract_info_id.ppp_user'
    )
    ppp_password = fields.Char(
        'PPP Password', related='adsl_service_contract_info_id.ppp_password'
    )
    endpoint_user = fields.Char(
        'Endpoint User', related='adsl_service_contract_info_id.endpoint_user'
    )
    endpoint_password = fields.Char(
        'Endpoint Password', related='adsl_service_contract_info_id.endpoint_password'
    )
    vodafone_id = fields.Char(
        'Vodafone ID',
        compute='_compute_vodafone_id',
        store=True,
    )
    vodafone_offer_code = fields.Char(
        'Vodafone Offer Code',
        compute='_compute_vodafone_offer_code',
    )
    mm_id = fields.Char(
        'MásMóvil ID',
        related='mm_fiber_service_contract_info_id.mm_id'
    )
    suma_id = fields.Char(
        'Suma ID',
        related='orange_fiber_service_contract_info_id.suma_id'
    )
    external_id = fields.Char(
        'External ID',
        related='xoln_fiber_service_contract_info_id.external_id'
    )
    project_id = fields.Many2one(
        "xoln.project",
        related="xoln_fiber_service_contract_info_id.project_id",
        string="Project",
    )
    id_order = fields.Char(
        'Order ID XOLN',
        related='xoln_fiber_service_contract_info_id.id_order'
    )
    administrative_number = fields.Char(
        'Administrative Number',
        related='adsl_service_contract_info_id.administrative_number'
    )
    order_id = fields.Char(
        'Order ID ADSL',
        related='adsl_service_contract_info_id.id_order'
    )

    router_product_id = fields.Many2one(
        'product.product', 'Router Model',
        compute='_compute_router_product_id',
    )
    router_lot_id = fields.Many2one(
        'stock.production.lot', 'S/N / MAC Address',
        compute='_compute_router_lot_id',
    )
    partner_priority = fields.Text(
        'Partner priority',
        related='partner_id.priority_id.description'
    )
    mail_activity_count = fields.Integer(
        compute='_compute_mail_activity_count',
        string='Activity Count'
    )
    ticket_number = fields.Char(string='Ticket Number')

    create_reason = fields.Selection([('portability', _('Portability')),
                                      ('new', _('New')),
                                      ('location_change', _('Location Change')),
                                      ('holder_change', _('Holder Change'))],
                                     string='Contract Creation Reason',
                                     related='crm_lead_line_id.create_reason',
                                     store=True)

    terminate_user_reason_id = fields.Many2one(
        'contract.terminate.user.reason',
        string="Termination User Reason",
        ondelete="restrict",
        readonly=True,
        copy=False,
        track_visibility="onchange",
    )

    category_id = fields.Many2many(
        'res.partner.category',
        string='Tags',
        related="partner_id.category_id",
    )

    res_partner_user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        related='partner_id.user_id'
    )

    previous_id = fields.Char(
        compute="_compute_previous_id",
        inverse="_inverse_set_previous_id",
        string="Previous Id",
        readonly=False,
    )

    fiber_signal_type_id = fields.Many2one(
        'fiber.signal.type',
        string="Fiber Signal Type",
    )

    service_partner_street = fields.Char(
        related='service_partner_id.street'
    )
    service_partner_zip = fields.Char(
        related='service_partner_id.zip'
    )
    service_partner_city = fields.Char(
        related='service_partner_id.city'
    )
    service_partner_state = fields.Many2one(
        related='service_partner_id.state_id'
    )
    lang = fields.Selection(
        related='partner_id.lang',
        store=True
    )

    is_fiber = fields.Boolean(
        compute='_compute_is_fiber',
    )
    is_mobile = fields.Boolean(
        compute='_compute_is_mobile',
    )
    is_pack = fields.Boolean(
        compute='_compute_is_pack',
        string="Is pack",
    )

    parent_pack_contract_id = fields.Many2one(
        'contract.contract',
        string="Parent Pack Contract",
    )
    number_contracts_in_pack = fields.Integer(
        compute='_compute_number_contract_in_pack',
        string="Number of pack contracts",
    )
    children_pack_contract_ids = fields.One2many(
        comodel_name='contract.contract',
        inverse_name='parent_pack_contract_id',
        string="Mobile contracts of pack",
    )
    sharing_bond_contract_ids = fields.Many2many(
        comodel_name='contract.contract',
        relation="sharing_data_contracts",
        column1="id",
        column2="contract_id",
        string="Shared Bond Mobile Contracts",
        compute='_compute_sharing_bond_contract_ids',
        store=True,
    )
    shared_bond_id = fields.Char(
        'Shared bond ID',
        related='mobile_contract_service_info_id.shared_bond_id',
    )

    # Hide fields from odoo custom filter by inheriting function fields_get()
    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes)
        res.pop('tariff_product', None)
        return res

    @api.depends("service_technology_id")
    def _compute_is_mobile(self):
        mobile_tech = self.env.ref('somconnexio.service_technology_mobile')
        for contract in self:
            contract.is_mobile = contract.service_technology_id == mobile_tech

    @api.depends("service_technology_id")
    def _compute_is_fiber(self):
        fiber_tech = self.env.ref('somconnexio.service_technology_fiber')
        for contract in self:
            contract.is_fiber = contract.service_technology_id == fiber_tech

    @api.depends("number_contracts_in_pack")
    def _compute_is_pack(self):
        for contract in self:
            contract.is_pack = bool(contract.number_contracts_in_pack)

    @api.depends("children_pack_contract_ids", "parent_pack_contract_id",
                 "sharing_bond_contract_ids")
    def _compute_number_contract_in_pack(self):
        for contract in self:
            pack_contract_ids = []
            if contract.parent_pack_contract_id:
                pack_contract_ids.append(contract.parent_pack_contract_id.id)
            if contract.children_pack_contract_ids:
                pack_contract_ids.extend(contract.children_pack_contract_ids.ids)
            if contract.sharing_bond_contract_ids:
                pack_contract_ids.extend(contract.sharing_bond_contract_ids.ids)

            if contract.id not in pack_contract_ids:
                pack_contract_ids.append(contract.id)

            contract.number_contracts_in_pack = (
                len(pack_contract_ids) if len(pack_contract_ids) > 1 else 0
            )

    @api.depends("shared_bond_id")
    def _compute_sharing_bond_contract_ids(self):
        """
        We use direct SQL commits here to ensure that Many2Many relation of
        sharing_bond_contract_ids is stored in DB following both directions
        ex:
            id, contract_id
             X,           Y
             Y,           X

        It will also be recomputed every time we edit the shared_bond_id
        """

        for contract in self:
            if type(contract.id) == models.NewId:
                # TODO: When editing contract model, a NewId class is created,
                # which should not trigger this compute method
                continue

            # DELETE from DB table sharing_data_contracts all instances with contract.id
            self.env.cr.execute(
                "DELETE FROM sharing_data_contracts WHERE id = %s or contract_id = %s",
                (contract.id, contract.id)
            )
            if contract.shared_bond_id:
                contracts_with_shared_bond = (
                    self.env["contract.contract"].search([
                        ("partner_id", "=", contract.partner_id.id),
                        ("is_terminated", "=", False),
                        (
                            "service_technology_id",
                            "=",
                            self.env.ref("somconnexio.service_technology_mobile").id,
                        ),
                        ("shared_bond_id", "=", contract.shared_bond_id),
                    ])
                )

                # Assign matching contracts according to their "shared_bond_id"
                contract.sharing_bond_contract_ids = [
                    (6, 0, contracts_with_shared_bond.ids)
                ]

                # INSERT to DB table sharing_data_contracts missing relation
                sharing_contracts_with = contracts_with_shared_bond - self
                for sharing_contract_id in sharing_contracts_with.ids:
                    self.env.cr.execute(
                        "INSERT INTO sharing_data_contracts VALUES (%s, %s)",
                        (sharing_contract_id, contract.id)
                    )

    def _compute_mail_activity_count(self):
        for contract in self:
            count = self.env['mail.activity'].search_count([
                ('res_id', '=', contract.id),
                ('res_model', '=', 'contract.contract')
            ])
            contract.mail_activity_count = count

    @api.depends(
        'vodafone_fiber_service_contract_info_id.vodafone_id',
        'router_4G_service_contract_info_id.vodafone_id'
    )
    def _compute_vodafone_id(self):
        for contract in self:
            contract.vodafone_id = (
                contract.vodafone_fiber_service_contract_info_id.vodafone_id or  # noqa
                contract.router_4G_service_contract_info_id.vodafone_id          # noqa
            )

    @api.depends(
        'vodafone_fiber_service_contract_info_id.vodafone_offer_code',
        'router_4G_service_contract_info_id.vodafone_offer_code'
    )
    def _compute_vodafone_offer_code(self):
        for contract in self:
            contract.vodafone_offer_code = (
                contract.vodafone_fiber_service_contract_info_id.vodafone_offer_code or  # noqa
                contract.router_4G_service_contract_info_id.vodafone_offer_code          # noqa
            )

    @api.depends(
        "service_contract_type",
        "mobile_contract_service_info_id.phone_number",
        "adsl_service_contract_info_id.phone_number",
        "mm_fiber_service_contract_info_id.phone_number",
        "vodafone_fiber_service_contract_info_id.phone_number",
        "orange_fiber_service_contract_info_id.phone_number",
        "router_4G_service_contract_info_id.phone_number",
    )
    def _compute_phone_number(self):
        for contract in self:
            contract_type = contract.service_contract_type
            if contract_type == 'mobile':
                contract.phone_number = (
                    contract.mobile_contract_service_info_id.phone_number
                )
            elif contract_type == 'adsl':
                contract.phone_number = (
                    contract.adsl_service_contract_info_id.phone_number
                )
            elif contract_type in ["asociatel", "vodafone"]:
                contract.phone_number = (
                    contract.vodafone_fiber_service_contract_info_id.phone_number
                )
            elif contract_type == 'masmovil':
                contract.phone_number = (
                    contract.mm_fiber_service_contract_info_id.phone_number
                )
            elif contract_type == 'xoln':
                contract.phone_number = (
                    contract.xoln_fiber_service_contract_info_id.phone_number
                )
            elif contract_type == 'router4G':
                contract.phone_number = (
                    contract.router_4G_service_contract_info_id.phone_number
                )
            elif contract_type == 'orange':
                contract.phone_number = (
                    contract.orange_fiber_service_contract_info_id.phone_number
                )

    @api.depends(
        'service_contract_type',
        'xoln_fiber_service_contract_info_id.router_product_id',
        'adsl_service_contract_info_id.router_product_id',
    )
    def _compute_router_product_id(self):
        for contract in self:
            contract_type = contract.service_contract_type
            if contract_type == 'adsl':
                contract.router_product_id = (
                    contract.adsl_service_contract_info_id.router_product_id
                )
            elif contract_type == 'xoln':
                contract.router_product_id = (
                    contract.xoln_fiber_service_contract_info_id.router_product_id
                )
            else:
                contract.router_product_id = False

    @api.depends(
        'service_contract_type',
        'xoln_fiber_service_contract_info_id.router_lot_id',
        'adsl_service_contract_info_id.router_lot_id',
    )
    def _compute_router_lot_id(self):
        for contract in self:
            contract_type = contract.service_contract_type
            if contract_type == 'adsl':
                contract.router_lot_id = (
                    contract.adsl_service_contract_info_id.router_lot_id
                )
            elif contract_type == 'xoln':
                contract.router_lot_id = (
                    contract.xoln_fiber_service_contract_info_id.router_lot_id
                )
            else:
                contract.router_product_id = False

    def _get_crm_lead_line_id(self, values):
        # TODO Rise error if exists more than one crm_lead_line
        # with the same ticket_number
        if values.get('crm_lead_line_id'):
            return values['crm_lead_line_id']
        ticket_number = values.get('ticket_number')
        if not ticket_number:
            return
        return self.env['crm.lead.line'].search([
            ('ticket_number', '=', ticket_number)
        ], limit=1).id

    @api.depends(
        'service_contract_type',
        'adsl_service_contract_info_id.previous_id',
        'mm_fiber_service_contract_info_id.previous_id',
        'router_4G_service_contract_info_id.previous_id',
        'vodafone_fiber_service_contract_info_id.previous_id',
        'xoln_fiber_service_contract_info_id.previous_id',
        'orange_fiber_service_contract_info_id.previous_id'
    )
    def _compute_previous_id(self):
        for record in self:
            contract_type = record.service_contract_type
            if contract_type == 'adsl':
                record.previous_id = (
                    record.adsl_service_contract_info_id.previous_id
                )
            elif contract_type == 'masmovil':
                record.previous_id = (
                    record.mm_fiber_service_contract_info_id.previous_id
                )
            elif contract_type in ["asociatel", "vodafone"]:
                record.previous_id = (
                    record.vodafone_fiber_service_contract_info_id.previous_id
                )
            elif contract_type == 'xoln':
                record.previous_id = (
                    record.xoln_fiber_service_contract_info_id.previous_id
                )
            elif contract_type == 'router4G':
                record.previous_id = (
                    record.router_4G_service_contract_info_id.previous_id
                )
            elif contract_type == 'orange':
                record.previous_id = (
                    record.orange_fiber_service_contract_info_id.previous_id
                )

    def _inverse_set_previous_id(self):
        for record in self:
            contract_type = record.service_contract_type
            if contract_type == 'adsl':
                record.adsl_service_contract_info_id.previous_id = (
                    record.previous_id
                )
            elif contract_type == 'masmovil':
                record.mm_fiber_service_contract_info_id.previous_id = (
                    record.previous_id
                )
            elif contract_type in ["asociatel", "vodafone"]:
                record.vodafone_fiber_service_contract_info_id.previous_id = (
                    record.previous_id
                )
            elif contract_type == 'xoln':
                record.xoln_fiber_service_contract_info_id.previous_id = (
                    record.previous_id
                )
            elif contract_type == 'router4G':
                record.router_4G_service_contract_info_id.previous_id = (
                    record.previous_id
                )
            elif contract_type == 'orange':
                record.orange_fiber_service_contract_info_id.previous_id = (
                    record.previous_id
                )

    @api.depends(
        'mobile_contract_service_info_id.icc',
        'router_4G_service_contract_info_id.icc'
    )
    def _compute_icc(self):
        for record in self:
            contract_type = record.service_contract_type
            if contract_type == 'mobile':
                record.icc = (
                    record.mobile_contract_service_info_id.icc
                )
            elif contract_type == 'router4G':
                record.icc = (
                    record.router_4G_service_contract_info_id.icc
                )

    def _inverse_set_icc(self):
        for record in self:
            contract_type = record.service_contract_type
            if contract_type == 'mobile':
                record.mobile_contract_service_info_id.icc = (
                    record.icc
                )
            elif contract_type == 'router4G':
                record.router_4G_service_contract_info_id.icc = (
                    record.icc
                )

    @api.depends('phone_number')
    def _compute_name(self):
        for contract in self:
            contract.name = contract.phone_number

            if not contract.name and contract.service_contract_type == "router4G":
                contract.name = contract.router_4G_service_contract_info_id.name

    @api.onchange('service_supplier_id')
    def onchange_service_supplier_id(self):
        coaxial = self.env.ref('somconnexio.coaxial_fiber_signal')
        ftth = self.env.ref('somconnexio.FTTH_fiber_signal')
        neba_ftth = self.env.ref('somconnexio.FTTH_neba_fiber_signal')
        indirect = self.env.ref('somconnexio.indirect_fiber_signal')

        if self.service_supplier_id == self.env.ref(
            "somconnexio.service_supplier_vodafone"
        ):
            allowed_types = [coaxial.id, ftth.id, neba_ftth.id]
        elif self.service_supplier_id == self.env.ref(
            "somconnexio.service_supplier_asociatel_vdf"
        ):
            allowed_types = [ftth.id, neba_ftth.id]
        elif self.service_supplier_id == self.env.ref(
            "somconnexio.service_supplier_masmovil"
        ):
            allowed_types = [ftth.id, indirect.id]
        elif self.service_supplier_id == self.env.ref(
            "somconnexio.service_supplier_orange"
        ):
            allowed_types = [ftth.id, indirect.id]
        else:
            return

        return {'domain': {'fiber_signal_type_id': [('id', 'in', allowed_types)]}}

    @api.constrains('service_technology_id', 'service_supplier_id')
    def validate_contract_service_info(self):
        if self.is_mobile and not self.mobile_contract_service_info_id:
            raise ValidationError(_(
                'Mobile Contract Service Info is required'
                'for technology Mobile'
            ))
        if self.service_technology_id == self.env.ref(
            'somconnexio.service_technology_adsl'
        ) and not self.adsl_service_contract_info_id:
            raise ValidationError(_(
                'ADSL Contract Service Info is required'
                'for technology ADSL'
            ))
        if self.service_technology_id == self.env.ref(
            'somconnexio.service_technology_4G'
        ) and not self.router_4G_service_contract_info_id:
            raise ValidationError(_(
                'Router 4G Contract Service Info is required '
                'for technology Router 4G'
            ))

        if self.is_fiber:
            if self.service_supplier_id == self.env.ref(
                'somconnexio.service_supplier_masmovil'
            ) and not self.mm_fiber_service_contract_info_id:
                raise ValidationError(_(
                    'MásMóvil Fiber Contract Service Info is required'
                    'for technology Fiber and supplier MásMóvil'
                ))

            if (
                self.service_supplier_id
                in [
                    self.env.ref("somconnexio.service_supplier_vodafone"),
                    self.env.ref("somconnexio.service_supplier_asociatel_vdf"),
                ]
                and not self.vodafone_fiber_service_contract_info_id
            ):
                raise ValidationError(
                    _(
                        "Vodafone Fiber Contract Service Info is required"
                        "for technology Fiber and supplier Vodafone/Asociatel"
                    )
                )
            if (
                self.service_supplier_id
                == self.env.ref("somconnexio.service_supplier_xoln")
                and not self.xoln_fiber_service_contract_info_id
            ):
                raise ValidationError(
                    _(
                        "XOLN Fiber Contract Service Info is required"
                        "for technology Fiber and supplier XOLN"
                    )
                )
            if (
                self.service_supplier_id
                == self.env.ref("somconnexio.service_supplier_orange")
                and not self.orange_fiber_service_contract_info_id
            ):
                raise ValidationError(
                    _(
                        "Orange Fiber Contract Service Info is required"
                        "for technology Fiber and supplier Orange"
                    )
                )

    @api.multi
    @api.depends("partner_id")
    def _compute_available_email_ids(self):
        for contract in self:
            if contract.partner_id:
                contract.available_email_ids = [
                    (6, 0, contract.partner_id.get_available_email_ids())
                ]

    @api.depends('service_technology_id')
    def _compute_is_broadband(self):
        for record in self:
            adsl = self.env.ref('somconnexio.service_technology_adsl')
            fiber = self.env.ref('somconnexio.service_technology_fiber')
            router4G = self.env.ref('somconnexio.service_technology_4G')
            record.is_broadband = (
                adsl.id == record.service_technology_id.id
                or
                fiber.id == record.service_technology_id.id
                or
                router4G.id == record.service_technology_id.id
            )

    @api.depends('service_technology_id', 'service_supplier_id')
    def _compute_contract_type(self):
        adsl = self.env.ref("somconnexio.service_technology_adsl")
        router4G = self.env.ref("somconnexio.service_technology_4G")
        vodafone = self.env.ref("somconnexio.service_supplier_vodafone")
        asociatel = self.env.ref("somconnexio.service_supplier_asociatel_vdf")
        masmovil = self.env.ref("somconnexio.service_supplier_masmovil")
        orange = self.env.ref("somconnexio.service_supplier_orange")
        xoln = self.env.ref("somconnexio.service_supplier_xoln")
        for record in self:
            if record.is_mobile:
                record.service_contract_type = 'mobile'
            elif record.service_technology_id == adsl:
                record.service_contract_type = 'adsl'
            elif record.service_technology_id == router4G:
                record.service_contract_type = 'router4G'
            elif record.is_fiber:
                if record.service_supplier_id == vodafone:
                    record.service_contract_type = 'vodafone'
                elif record.service_supplier_id == asociatel:
                    record.service_contract_type = "asociatel"
                elif record.service_supplier_id == masmovil:
                    record.service_contract_type = 'masmovil'
                elif record.service_supplier_id == xoln:
                    record.service_contract_type = 'xoln'
                elif record.service_supplier_id == orange:
                    record.service_contract_type = 'orange'

    def _tariff_contract_line(self, field, current):
        for contract in self:
            service_product_category = (
                self.service_technology_id.service_product_category_id
            )

            for line in contract.contract_line_ids:
                if line.product_id.categ_id == service_product_category and (
                    contract._is_contract_line_active(line) or not current
                ):
                    setattr(contract, field, line)
                    break

    @api.model
    def cron_compute_current_tariff_contract_line(self):
        domain = [
            '|',
            ('date_end', '>', date.today().strftime('%Y-%m-%d')),
            ('date_end', '=', False)
        ]
        contracts = self.search(domain)
        for contract in contracts:
            contract._compute_current_tariff_contract_line()

    @api.model
    def cron_execute_OTRS_tariff_change_tickets(self):
        """
        Get all Change Tariff tickets from OTRS and trigger them to be sent to MM
        """
        service = SearchTicketsService(ChangeTariffTicketConfiguration)
        change_tariff_tickets = service.search()
        sb_service = SearchTicketsService(ChangeTariffSharedBondTicketConfiguration)
        shared_bond_tickets = sb_service.search(df_dct={"creadorAbonament": "1"})
        for ticket in change_tariff_tickets + shared_bond_tickets:
            ActivateChangeTariffMobileTickets(ticket.number).run()

    @api.depends('service_technology_id', 'contract_line_ids')
    def _compute_current_tariff_contract_line(self):
        self._tariff_contract_line('current_tariff_contract_line', current=True)

    @api.depends('service_technology_id', 'contract_line_ids')
    def _compute_tariff_contract_line(self):
        self._tariff_contract_line('tariff_contract_line', current=False)

    def _is_contract_line_active(self, line):
        if (
            (line.date_end and line.date_start <= date.today() <= line.date_end)
            or (not line.date_end and line.date_start <= date.today())
        ):
            return True
        else:
            return False

    @api.constrains('partner_id', 'service_partner_id')
    def _check_service_partner_id(self):
        self.ensure_one()
        if not self.service_partner_id:
            return True
        elif self.service_partner_id == self.partner_id:
            return True
        elif self.service_partner_id.parent_id != self.partner_id:
            raise ValidationError(
                _('Service contact must be a child of %s') % (
                    self.partner_id.name
                )
            )
        elif self.service_partner_id.type != "service":
            raise ValidationError(
                _('Service contact %s must be service type') % (
                    self.service_partner_id.name
                )
            )

    @api.constrains('partner_id', 'invoice_partner_id')
    def _check_invoice_partner_id(self):
        self.ensure_one()
        if not self.invoice_partner_id or self.invoice_partner_id == self.partner_id:
            return True
        if self.invoice_partner_id.parent_id != self.partner_id:
            raise ValidationError(
                _('Invoicing contact must be a child of %s') % (
                    self.partner_id.name
                )
            )
        if self.invoice_partner_id.type not in ['invoice', 'representative']:
            raise ValidationError(
                _('Invoicing contact %s must be either representative or invoice type')
                % (self.invoice_partner_id.name)
            )

    @api.constrains('service_technology_id', 'service_supplier_id')
    def _check_service_technology_service_supplier(self):
        self.ensure_one()
        available_relations = (
            self.env['service.technology.service.supplier'].search([
                ('service_technology_id', '=', self.service_technology_id.id)
            ])
        )
        available_service_suppliers = [
            s.service_supplier_id.id for s in available_relations
        ]
        if self.service_supplier_id.id not in available_service_suppliers:
            raise ValidationError(
                _('Service supplier %s is not allowed by service technology %s')
                % (
                    self.service_supplier_id.name,
                    self.service_technology_id.name
                )
            )

    @api.constrains('service_technology_id', 'service_supplier_id', 'contract_line_ids')
    def _check_service_category_products(self):
        self.ensure_one()
        available_relations = self.env['product.category.technology.supplier'].search([
            ('service_technology_id', '=', self.service_technology_id.id),
            ('service_supplier_id', '=', self.service_supplier_id.id)
        ])
        available_categories = [c.product_category_id.id for c in available_relations]
        available_products_categ = self.env['product.template'].search([
            ('categ_id', 'in', available_categories)
        ])

        for line in self.contract_line_ids:
            if line.product_id.product_tmpl_id not in available_products_categ:
                raise ValidationError(
                    _('Product %s is not allowed by contract with \
                            technology %s and supplier %s') % (
                        line.product_id.name,
                        self.service_technology_id.name,
                        self.service_supplier_id.name
                    )
                )

    @api.constrains('partner_id', 'contract_line_ids')
    def _check_coop_agreement(self):
        self.ensure_one()
        if self.partner_id.coop_agreement:
            for line in self.contract_line_ids:
                line_prod_tmpl_id = line.product_id.product_tmpl_id
                agreement = self.partner_id.coop_agreement_id
                if line_prod_tmpl_id not in agreement.products:
                    raise ValidationError(
                        _('Product %s is not allowed by agreement %s') % (
                            line.product_id.name, agreement.code
                        )
                    )

    @api.model
    def create(self, values):
        values['crm_lead_line_id'] = self._get_crm_lead_line_id(values)
        values['code'] = self._get_code(values)
        values["service_supplier_id"] = self._get_service_supplier_id(values)
        res = super(Contract, self).create(values)
        res.contract_group_id = self._get_contract_group_id(res)
        return res

    def _get_code(self, values):
        code = values.get("code")
        return (
            code if code else self.env.ref("somconnexio.sequence_contract").next_by_id()
        )

    def _get_service_supplier_id(self, values):
        if "service_technology_id" not in values or "service_supplier_id" in values:
            return values["service_supplier_id"]
        service_tech_id = values["service_technology_id"]
        if service_tech_id == self.env.ref("somconnexio.service_technology_mobile").id:
            return self.env.ref("somconnexio.service_supplier_masmovil").id
        if service_tech_id == self.env.ref("somconnexio.service_technology_adsl").id:
            return self.env.ref("somconnexio.service_supplier_jazztel").id

    def _get_contract_group_id(self, contract):
        """
        Return the first group that match with mandate and email
        If any group match with mandate and email, create a new one.
        """
        if contract.contract_group_id:
            return contract.contract_group_id

        partner = contract.partner_id
        if partner.special_contract_group:
            return self.env.ref("somconnexio.to_review_contract_group").id
        groups = (
            self.env["contract.group"].sudo().search([("partner_id", "=", partner.id)])
        )
        for group in groups:
            contract_group = group.contract_ids[0]
            if (
                contract_group.mandate_id == contract.mandate_id
                and contract_group.email_ids.mapped("id")
                == contract.email_ids.mapped("id")
            ):
                return group.id
        return (
            self.env["contract.group"]
            .create(
                {
                    "partner_id": partner.id,
                    "code": "",  # TODO: Calculate a code with a sequence?
                }
            )
            .id
        )

    @api.one
    @api.constrains('partner_id', 'email_ids')
    def _validate_emails(self):
        available_email_ids = self.available_email_ids
        for email_id in self.email_ids:
            if email_id not in available_email_ids:
                raise ValidationError(_('Email(s) not valid'))

    @api.depends('contract_line_ids.date_start')
    def _compute_date_start(self):
        for contract in self:
            contract.date_start = False
            date_start = contract.contract_line_ids.mapped('date_start')
            if date_start and all(date_start):
                contract.date_start = min(date_start)

    # The following two methods are overwritten instead of using super
    # in order to produce a single register note.

    @api.multi
    def terminate_contract(
        self, terminate_reason_id, terminate_comment,
        terminate_date, terminate_user_reason_id
    ):
        self.ensure_one()
        if not self.env.user.has_group("contract.can_terminate_contract"):
            raise UserError(_('You are not allowed to terminate contracts.'))
        if terminate_date < self.date_start:
            raise UserError(_("A contract can't be terminated before it started"))
        self.contract_line_ids.filtered("is_stop_allowed").stop(terminate_date)
        if not all(self.contract_line_ids.mapped("date_end")):
            raise UserError(
                _(
                    "Please set an end-date to all of its "
                    "contract lines manually and try again"
                )
            )
        self.write(
            {
                "is_terminated": True,
                "terminate_reason_id": terminate_reason_id.id,
                "terminate_user_reason_id": terminate_user_reason_id.id,
                "terminate_comment": terminate_comment,
                "terminate_date": terminate_date,
            }
        )
        return True

    @api.multi
    def action_cancel_contract_termination(self):
        self.ensure_one()
        self.write({
            'is_terminated': False,
            'terminate_reason_id': False,
            'terminate_user_reason_id': False,
            'terminate_comment': False,
            'terminate_date': False,
        })

    @job
    def create_subscription(self, _id, force=False):
        contract = self.browse(_id)
        CRMAccountHierarchyFromContractCreateService(
            contract,
            OpenCellConfiguration(self.env),
            self.env,
        ).run(force=force)

    @job
    def terminate_subscription(self, _id):
        contract = self.browse(_id)
        SubscriptionService(contract).terminate()

    @job
    def update_subscription(self, contracts, updated_field):
        CRMAccountHierarchyFromContractUpdateService(
            contracts, updated_field).run()

    @job
    def update_subscription_force(self, contracts, updated_field):
        CRMAccountHierarchyFromContractUpdateService(
            contracts, updated_field, force=True).run()

    @job
    def add_one_shot(self, _id, product_default_code):
        contract = self.browse(_id)
        SubscriptionService(contract).create_one_shot(product_default_code)

    @job
    def add_service(self, _id, contract_line):
        contract = self.browse(_id)
        SubscriptionService(contract).create_service(contract_line)

    @job
    def terminate_service(self, _id, contract_line):
        contract = self.browse(_id)
        SubscriptionService(contract).terminate_service(
            contract_line.product_id, contract_line.date_end)

    @job
    def create_contract(self, **params):
        self.env["contract.contract.process"].create(**params)

    def break_packs(self):
        if self.is_fiber:
            # Remove the parent from the children
            for contract in self.children_pack_contract_ids:
                contract.parent_pack_contract_id = False
                new_product = self.env.ref("somconnexio.TrucadesIllimitades5GB")
                contract._create_change_tariff_ticket(
                    new_product, start_date=self.terminate_date
                )
        if self.is_mobile:
            # Remove the parent from the children
            self.parent_pack_contract_id = False
            if self.shared_bond_id:
                self.quit_sharing_bond_and_update_sharing_mobiles_tariffs()

    def quit_sharing_bond_and_update_sharing_mobiles_tariffs(self):
        """
        Remove itself from sharing data with others and update the mobile
        tariffs of those that used to share data with it accordingly
        """

        self._compute_sharing_bond_contract_ids()

        sharing_data_contracts = self.sharing_bond_contract_ids - self
        self.mobile_contract_service_info_id.shared_bond_id = False
        current_product = sharing_data_contracts[0].current_tariff_product

        # Change from 3 mobiles sharing data to 2 of them:
        if len(sharing_data_contracts) == 2:
            new_product = current_product.get_variant_with_attributes(
                attr_to_exclude=self.env.ref("somconnexio.Sharing3Mobiles"),
                attr_to_include=self.env.ref("somconnexio.Sharing2Mobiles"),
            )
            for contract in sharing_data_contracts:
                contract._change_tariff_only_in_ODOO(new_product, self.terminate_date)

        # Change from 2 mobiles sharing data to single pack product:
        elif len(sharing_data_contracts) == 1:
            # Single mobile pack product correspondance can not be computed by getting
            # variants, since the Data attributes do not mach, so it is hardcoded here
            break_sharing_bond_product_match = {
                self.env.ref("somconnexio.50GBCompartides2mobils"): self.env.ref(
                    "somconnexio.TrucadesIllimitades20GBPack"
                ),
                self.env.ref("somconnexio.50GBCompartides2mobilsEiE"): self.env.ref(
                    "somconnexio.TrucadesIllimitades50GBPackEiE"
                ),
                self.env.ref("somconnexio.150GBCompartides2mobilsEiE"): self.env.ref(
                    "somconnexio.TrucadesIllimitades50GBPackEiE"
                ),
            }
            new_product = break_sharing_bond_product_match.get(current_product)

            contract = sharing_data_contracts[0]
            contract.mobile_contract_service_info_id.shared_bond_id = False
            contract._create_change_tariff_ticket(
                new_product,
                fiber_contract_id=contract.parent_pack_contract_id.id,
                start_date=self.terminate_date
            )

    def update_sharing_mobiles_tariffs_after_joining_shared_bond(
            self, start_date=None):
        """When a third contract joins a shared bond shared by two mobile contracts,
        update their tariffs to 3 mobiles sharing, if they still have the 2 mobiles
        sharing tariff"""

        sharing_product_3 = self.current_tariff_product
        sharing_product_2 = sharing_product_3.get_variant_with_attributes(
            attr_to_exclude=self.env.ref("somconnexio.Sharing3Mobiles"),
            attr_to_include=self.env.ref("somconnexio.Sharing2Mobiles"),
        )
        sharing_contracts = self.sharing_bond_contract_ids - self

        if len(sharing_contracts) >= 3:
            raise UserError(_("No more than 3 mobiles can share data together"))
        elif (
            len(sharing_contracts) == 2 and
            all(
                contract.current_tariff_product == sharing_product_2
                for contract in sharing_contracts
            )
        ):
            for sharing_contract in sharing_contracts:
                sharing_contract._change_tariff_only_in_ODOO(
                    sharing_product_3,
                    start_date=start_date
                )

    def _create_change_tariff_ticket(
        self, new_product, fiber_contract_id=False, start_date=None
    ):
        """Create CRMLead for the mobile with another product"""
        self.ensure_one()

        wizard = self.env['contract.mobile.tariff.change.wizard'].with_context(  # noqa
            active_id=self.id
        ).sudo().create(
            {
                "new_tariff_product_id": new_product.id,
                "exceptional_change": True,
                "otrs_checked": True,
                "send_notification": False,
                "fiber_contract_to_link": fiber_contract_id,
                "start_date": start_date,
            }
        )
        wizard.button_change()

    def _change_tariff_only_in_ODOO(self, new_product, start_date=None):
        """Change tariff in ODOO contract"""
        self.ensure_one()

        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.id
        ).sudo().create(
            {
                "start_date": start_date or date.today(),
                "new_tariff_product_id": new_product.id,
                "summary": "{} {}".format(
                    "Canvi de tarifa a",
                    new_product.showed_name
                ),
            }
        )
        wizard.button_change()

    @api.constrains("active")
    def _constrains_active(self):
        self.ensure_one()
        if not self.active and not self.env.user.has_group("base.group_system"):

            raise UserError(_("You cannot archive contacts"))
