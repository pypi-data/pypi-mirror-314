from datetime import date, datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import MissingError, ValidationError
from otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket import (
    ChangeTariffExceptionalTicket,
    ChangeTariffTicket,
)
from otrs_somconnexio.otrs_models.ticket_types.change_tariff_ticket_shared_bonds import (  # noqa
    ChangeTariffTicketSharedBond,
)

from ...helpers.date import date_to_str, first_day_next_month


class AvailableFibers(models.TransientModel):
    # Why is a TransientModel?
    # Is a hackish solution for a cache problem.
    # We need a cache to store the information received from OTRS to avoid to call OTRS
    # API every time the wizard is loaded.
    # The default Odoo wizard load process execute many times the same methods without a
    # common context between them.
    # Using a TransientModel the vacumm remove automaticaly the old records.
    # osv_memory_count_limit: Force a limit on the maximum number of records kept in the
    # virtual osv_memory tables. The default is False, which means no count-based limit.
    # _transient_max_count = lazy_classproperty(
    #    lambda _: config.get("osv_memory_count_limit")
    # )
    # osv_memory_age_limit: Force a limit on the maximum age of records kept in the
    # virtual osv_memory tables. This is a decimal value expressed in hours,
    # and the default is 1 hour.
    # _transient_max_hours = lazy_classproperty(
    #     lambda _: config.get("osv_memory_age_limit")
    # )
    _name = "contract.mobile.tariff.change.wizard.available.fibers"

    partner_ref = fields.Char()
    fiber_contracts_ids = fields.Char()


class ContractMobileTariffChangeWizard(models.TransientModel):
    _name = 'contract.mobile.tariff.change.wizard'

    contract_id = fields.Many2one('contract.contract')
    partner_id = fields.Many2one(
        'res.partner',
        related='contract_id.partner_id'
    )
    start_date = fields.Date('Start Date')
    note = fields.Char()
    current_tariff_contract_line = fields.Many2one(
        'contract.line',
        related='contract_id.current_tariff_contract_line',
    )
    current_tariff_product = fields.Many2one(
        'product.product',
        related='current_tariff_contract_line.product_id',
        string="Current Tariff"
    )
    new_tariff_product_id = fields.Many2one(
        'product.product',
        string='New tariff',
    )
    exceptional_change = fields.Boolean(default=False)
    send_notification = fields.Boolean(
        string='Send notification', default=False
    )
    otrs_checked = fields.Boolean(
        string='I have checked OTRS and no other tariff change is pending',
        default=False,
    )
    mobile_products = fields.Many2many(
        "product.product",
        compute="_compute_mobile_products",
    )
    available_products = fields.Many2many(
        "product.product",
    )
    location = fields.Char(
        related='contract_id.phone_number'
    )
    mobile_contracts_to_share_data = fields.Many2many(
        comodel_name="contract.contract",
        inverse_name="id",
        string="With which mobile contracts should it share data with?",
    )
    available_fiber_contracts = fields.Many2many(
        comodel_name='contract.contract',
        inverse_name="id",
        relation="available_fiber_contracts_change_mobile_tariff_wizard_table"
    )
    fiber_contract_to_link = fields.Many2one(
        'contract.contract',
        string='To which fiber contract should be linked?',
    )
    mobile_contracts_wo_sharing_bond = fields.Many2many(
        'contract.contract',
        compute='_compute_mobile_contracts_wo_sharing_bond',
    )
    pack_options = fields.Selection(
        selection=lambda self: self._get_pack_options(),
        string='Fiber linked options',
    )
    shared_bond_id_to_join = fields.Selection(
        selection=lambda self: self._get_shared_bond_id_to_join(),
        string='Shared bond id to join option',
    )
    phones_from_new_shared_bond = fields.Many2many(
        "contract.contract",
    )
    is_shared_bond_full = fields.Boolean(
        compute="_compute_is_shared_bond_full",
    )
    phone_to_exchange = fields.Many2one(
        "contract.contract", string="Mobile contract to exchange from bond"
    )
    new_tariff_product_id_exchanged_phone = fields.Many2one(
        "product.product",
        string="New tariff for exchanged phone",
    )

    will_force_other_mobiles_to_quit_pack = fields.Boolean(
        compute="_compute_will_force_other_mobiles_to_quit_pack"
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['contract_id'] = self.env.context['active_id']
        return defaults

    def _get_shared_bond_id_to_join(self):

        c_id = self.env.context.get('active_id')
        if not c_id:
            return

        contract_id = self.env["contract.contract"].browse(c_id)

        mobile_contracts_w_sharing_bond = self.env["contract.contract"].search(
            [
                ("id", "!=", contract_id.id),
                ("partner_id", "=", contract_id.partner_id.id),
                ("service_technology_id", "=", self.env.ref(
                    "somconnexio.service_technology_mobile").id,
                 ),
                ("is_terminated", "=", False),
                ("shared_bond_id", "!=", False),
            ]
        )

        shared_bond_dict = {}
        shared_bond_id_list = []

        for contract in mobile_contracts_w_sharing_bond:
            # Group contracts by code
            if contract.shared_bond_id in shared_bond_dict:
                shared_bond_dict[contract.shared_bond_id].append(contract)
            else:
                shared_bond_dict[contract.shared_bond_id] = [contract]

        # Gather phone numbers for contracts sharing the same shared_bond_id
        for shared_bond_id, contracts in shared_bond_dict.items():
            shared_bond_id_list.append(
                (
                    shared_bond_id,
                    '{}: {}'.format(shared_bond_id, ', '.join(
                        [contract.phone_number for contract in contracts]
                    ))
                )
            )

        return shared_bond_id_list

    def _get_pack_options(self):

        c_id = self.env.context.get('active_id')
        contract_id = self.env["contract.contract"].browse(c_id)

        pack_options = []

        if not contract_id or contract_id.shared_bond_id or self.pack_options:
            return pack_options

        fiber_contracts_wo_sharing_data_mobiles = False
        mobile_contracts_wo_sharing_bond = False

        mobile_contracts = self.env["contract.contract"].search(
            [
                ("id", "!=", contract_id.id),
                ("partner_id", "=", contract_id.partner_id.id),
                ("service_technology_id", "=", self.env.ref(
                    "somconnexio.service_technology_mobile").id,
                 ),
                ("is_terminated", "=", False),
            ]
        )

        if mobile_contracts:
            mobile_contracts_w_sharing_bond = mobile_contracts.filtered(
                lambda c: c.shared_bond_id
            )

            if mobile_contracts_w_sharing_bond:
                pack_options.append(
                    ('existing_shared_bond', _('Add line to existing shared bond')),
                )

            mobile_contracts_wo_sharing_bond = mobile_contracts.filtered(
                lambda c: not c.shared_bond_id
            )

        fiber_contracts_to_pack = self._get_fiber_contracts_to_pack(
            contract_id.partner_id.ref
        )

        if fiber_contracts_to_pack:
            fiber_contracts_unlinked = (
                fiber_contracts_to_pack.filtered(
                    lambda c: not c.children_pack_contract_ids
                )
            )
            if fiber_contracts_unlinked:
                pack_options.append(
                    ('pinya_mobile_tariff', _('Pack with fiber')),
                )

            fiber_contracts_wo_sharing_data_mobiles = (
                fiber_contracts_to_pack.filtered(
                    lambda c: not c.children_pack_contract_ids
                    or len(c.children_pack_contract_ids) == 1
                )
            )

        if (
            fiber_contracts_wo_sharing_data_mobiles and
            mobile_contracts_wo_sharing_bond
        ):
            pack_options.append(
                ('new_shared_bond', _('Create new shared bond')),
            )

        return pack_options

    @api.depends("contract_id")
    def _compute_mobile_contracts_wo_sharing_bond(self):
        if not self.contract_id:
            return
        self.mobile_contracts_wo_sharing_bond = self.env["contract.contract"].search(
            [
                ("id", "!=", self.contract_id.id),
                ("partner_id", "=", self.partner_id.id),
                ("service_technology_id", "=", self.env.ref(
                    "somconnexio.service_technology_mobile").id,
                 ),
                ("shared_bond_id", "=", False),
                ("is_terminated", "=", False),
            ]
        )

    @api.depends("contract_id")
    def _compute_mobile_products(self):
        mbl_product_templates = self.env["product.template"].search(
            [
                ("categ_id", "=", self.env.ref("somconnexio.mobile_service").id),
            ]
        )
        self.mobile_products = self.env["product.product"].search(
            [
                ("product_tmpl_id", "in", mbl_product_templates.ids),
            ]
        )

    @api.onchange("pack_options")
    def _compute_available_products(self):
        attr_to_exclude = self.env["product.attribute.value"]
        attr_to_include = self.env["product.attribute.value"]

        if (
            not self.contract_id.partner_id.is_company
        ):  # Do not show company exclusive products
            attr_to_exclude |= self.env.ref("somconnexio.CompanyExclusive")
        if not self.pack_options:  # Do not show mobile products from offer packs
            attr_to_exclude |= self.env.ref("somconnexio.IsInPack")
        else:
            attr_to_include |= self.env.ref("somconnexio.IsInPack")
            sharing_bond = bool(self.pack_options != "pinya_mobile_tariff")

        product_search_domain = [
            ("id", "in", self.mobile_products.ids),
        ]
        if attr_to_exclude:
            product_search_domain.append(
                ("attribute_value_ids", "not in", attr_to_exclude.ids)
            )
        if attr_to_include:
            product_search_domain.extend(
                [
                    ("attribute_value_ids", "in", attr_to_include.ids),
                    ("has_sharing_data_bond", "=", sharing_bond),
                ]
            )
        self.available_products = self.env["product.product"].search(
            product_search_domain
        )

    @api.depends("contract_id")
    def _compute_will_force_other_mobiles_to_quit_pack(self):
        self.will_force_other_mobiles_to_quit_pack = (
            len(self.contract_id.sharing_bond_contract_ids) == 2
        )

    @api.depends("phones_from_new_shared_bond")
    def _compute_is_shared_bond_full(self):
        if not self.phones_from_new_shared_bond:
            return
        self.is_shared_bond_full = bool(len(self.phones_from_new_shared_bond) == 3)

    @api.onchange('shared_bond_id_to_join')
    def onchange_shared_bond_id_to_join(self):
        if not self.shared_bond_id_to_join:
            return

        mobile_contracts_to_join = self.env["contract.contract"].search(
            [
                ("partner_id", "=", self.partner_id.id),
                ("service_technology_id", "=", self.env.ref(
                    "somconnexio.service_technology_mobile").id,
                 ),
                ("is_terminated", "=", False),
                ("shared_bond_id", "=", self.shared_bond_id_to_join),
            ]
        )
        self.fiber_contract_to_link = (
            mobile_contracts_to_join[0].parent_pack_contract_id
        )
        self.phones_from_new_shared_bond = mobile_contracts_to_join

    @api.onchange('mobile_contracts_to_share_data')
    def onchange_mobile_contracts_to_share_data(self):
        if len(self.mobile_contracts_to_share_data) > 3:
            raise ValidationError(_(
                "Maximum 3 mobile contracts to build a shared data bond"
            ))

    @api.onchange('fiber_contract_to_link')
    def onchange_fiber_contract_to_link(self):
        if not self.fiber_contract_to_link:
            return

        # If chosen fiber is linked with mobile, that mobile contract should share data
        if (
            self.fiber_contract_to_link.children_pack_contract_ids and
            self.pack_options == "new_shared_bond"
        ):
            mobile_pack = self.fiber_contract_to_link.children_pack_contract_ids[0]
            self.mobile_contracts_to_share_data = [(4, mobile_pack.id)]

    @api.onchange('pack_options')
    def onchange_pack_options(self):
        if self.pack_options == "pinya_mobile_tariff":
            fiber_contracts_to_pack = self._get_fiber_contracts_to_pack(
                self.contract_id.partner_id.ref
            )
            self.available_fiber_contracts = fiber_contracts_to_pack.filtered(
                lambda c: not c.children_pack_contract_ids
            )
        elif self.pack_options == "new_shared_bond":
            self.mobile_contracts_to_share_data = [(6, _, [self.contract_id.id])]
            fiber_contracts_to_pack = self._get_fiber_contracts_to_pack(
                self.contract_id.partner_id.ref
            )
            self.available_fiber_contracts = (
                fiber_contracts_to_pack.filtered(
                    lambda c: not c.children_pack_contract_ids
                    or len(c.children_pack_contract_ids) == 1
                )
            )

    def _get_fiber_contracts_to_pack(self, partner_ref):
        """
        Check fiber contracts available to link with mobile contracts
        """

        fibers = self.env[
            "contract.mobile.tariff.change.wizard.available.fibers"
        ].search(
            [
                ("partner_ref", "=", partner_ref),
            ]
        )
        old_date = datetime.now() - timedelta(minutes=5)
        old_register = fibers and fibers.write_date <= old_date

        if not fibers or old_register:
            try:
                fiber_contracts_dct = self.env[
                    "contract.service"
                ].get_fiber_contracts_to_pack(
                    partner_ref=partner_ref, mobiles_sharing_data="true"
                )
                fiber_contracts_ids = [c["id"] for c in fiber_contracts_dct]
            except MissingError:
                return
            fiber_contracts_id_list = " ".join([str(id) for id in fiber_contracts_ids])
            if not fibers:
                self.env[
                    "contract.mobile.tariff.change.wizard.available.fibers"
                ].create(
                    [
                        {
                            "partner_ref": partner_ref,
                            "fiber_contracts_ids": fiber_contracts_id_list,
                        }
                    ]
                )
            elif old_register:
                fibers.write(
                    {
                        "fiber_contracts_ids": fiber_contracts_id_list,
                    }
                )
        else:
            fiber_contracts_ids = [
                int(n) for n in fibers.fiber_contracts_ids.split(" ")
            ]

        return self.env["contract.contract"].search([("id", "in", fiber_contracts_ids)])

    def button_change(self):
        self.ensure_one()

        if not self.otrs_checked:
            raise ValidationError(_(
                "You must check if any previous tariff change is found in OTRS"
            ))

        if self.exceptional_change:
            if not self.start_date:
                self.start_date = date.today()
            Ticket = ChangeTariffExceptionalTicket
        else:
            if not self.start_date:
                self.start_date = first_day_next_month()
            Ticket = ChangeTariffTicket

        fields_dict = {
            "phone_number": self.contract_id.phone_number,
            "new_product_code": self.new_tariff_product_id.default_code,
            "current_product_code": self.current_tariff_product.default_code,
            "subscription_email": self.contract_id.email_ids[0].email,
            "effective_date": date_to_str(self.start_date),
            "language": self.partner_id.lang,
            "fiber_linked": (
                self.fiber_contract_to_link.code
                if self.fiber_contract_to_link else False
            ),
            "send_notification": self.send_notification,
        }

        if self.pack_options == 'existing_shared_bond':
            fields_dict["shared_bond_id"] = self.shared_bond_id_to_join

        elif self.pack_options == 'new_shared_bond':
            if self.exceptional_change:
                raise ValidationError(_(
                    "A new shared bond creation cannot be an exceptional change"
                ))
            elif len(self.mobile_contracts_to_share_data) < 2:
                raise ValidationError(_(
                    "Another mobile is required to create a shared data bond"
                ))
            Ticket = ChangeTariffTicketSharedBond
            fields_dict["contracts"] = [
                {
                    "phone_number": contract.phone_number,
                    "current_product_code": contract.current_tariff_product.code,
                    "subscription_email": contract.email_ids[0].email,
                } for contract in self.mobile_contracts_to_share_data
            ]

        Ticket(self.partner_id.vat, self.partner_id.ref, fields_dict).create()

        message = _("OTRS change tariff ticket created. Tariff to be changed from '{}' to '{}' with start_date: {}")  # noqa
        self.contract_id.message_post(
            message.format(
                self.current_tariff_product.showed_name,
                self.new_tariff_product_id.showed_name,
                self.start_date,
            )
        )
        self._create_activity()

        if self.phone_to_exchange:
            self.phone_to_exchange._create_change_tariff_ticket(
                self.new_tariff_product_id_exchanged_phone, start_date=self.start_date
            )

        return True

    def _create_activity(self):
        self.env['mail.activity'].create(
            {
                'summary': " ".join(
                    [_('Tariff change'), self.new_tariff_product_id.showed_name]
                ),
                'res_id': self.contract_id.id,
                'res_model_id': self.env.ref('contract.model_contract_contract').id,
                'user_id': self.env.user.id,
                'activity_type_id': self.env.ref('somconnexio.mail_activity_type_tariff_change').id,  # noqa
                'done': True,
                'date_done': date.today(),
                'date_deadline': date.today(),
                'location': self.contract_id.phone_number,
                'note': self.note,
            }
        )
