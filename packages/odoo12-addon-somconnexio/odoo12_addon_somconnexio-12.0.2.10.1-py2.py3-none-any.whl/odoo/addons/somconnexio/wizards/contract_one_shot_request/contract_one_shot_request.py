from datetime import datetime, date

from odoo import models, fields, api, _
from odoo.addons.queue_job.job import job

from otrs_somconnexio.otrs_models.ticket_types.add_data_ticket import AddDataTicket
from ...services.contract_one_shot_process import ContractOneShotProcess
from ...helpers.date import last_day_of_month_of_given_date


class ContractOneShotRequestWizard(models.TransientModel):
    _name = 'contract.one.shot.request.wizard'
    contract_id = fields.Many2one('contract.contract')
    summary = fields.Char(required=True)
    done = fields.Boolean(required=True)
    location = fields.Char()
    note = fields.Char()
    start_date = fields.Date("Start Date", required=True)

    available_products = fields.Many2many(
        "product.product", compute="_compute_available_products"
    )
    one_shot_product_id = fields.Many2one(
        'product.product',
        string='One Shot products',
    )
    activity_type = fields.Many2one('mail.activity.type')

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['contract_id'] = self.env.context['active_id']
        defaults['start_date'] = datetime.strftime(date.today(), "%Y-%m-%d")
        return defaults

    @api.depends("contract_id")
    def _compute_available_products(self):
        if not self.contract_id:
            return False

        if self.contract_id.is_mobile:
            category = self.env.ref("somconnexio.mobile_oneshot_service")
        elif self.contract_id.service_technology_id == self.env.ref(
            "somconnexio.service_technology_adsl"
        ):
            category = self.env.ref("somconnexio.broadband_oneshot_adsl_service")
        else:
            category = self.env.ref("somconnexio.broadband_oneshot_service")

        product_tmpl = self.env["product.template"].search(
            [
                ("categ_id", "=", category.id),
            ]
        )
        products = self.env["product.product"].search(
            [
                ("product_tmpl_id", "in", product_tmpl.ids),
                ("active", "=", True),
            ]
        )

        if self.contract_id.is_mobile:
            products = self._filter_mobile_products(products)

        self.available_products = products

    def _filter_mobile_products(self, products):
        """
        Filter the products to show only the additional sharing data products
        for mobile sharing data contracts, and hide them for mobile contracts
        without sharing data.
        """
        additional_data_products = products.filtered(
            lambda product: product.product_tmpl_id
            == self.env.ref("somconnexio.DadesAddicionals500MB_product_template")
        )
        other_products = products - additional_data_products

        if self.contract_id.shared_bond_id:
            additional_data_products = additional_data_products.filtered(
                lambda product: product.has_sharing_data_bond
            )
        else:
            additional_data_products = additional_data_products.filtered(
                lambda product: not product.has_sharing_data_bond
            )

        return additional_data_products + other_products

    @api.onchange("one_shot_product_id")
    def onchange_one_shot_product_id(self):
        router_list = [
            self.env.ref('somconnexio.EnviamentRouter_product_template'),
            self.env.ref('somconnexio.RecollidaRouter_product_template')
        ]
        one_shot_list = [
            self.env.ref("somconnexio.SMSMassius500SMS_product_template"),
            self.env.ref("somconnexio.DadesAddicionals1GBSenseCost_product_template"),
            self.env.ref("somconnexio.DadesAddicionals500MB_product_template"),
        ]

        if self.one_shot_product_id.product_tmpl_id in one_shot_list:
            self.done = True
            self.activity_type = self.env.ref('somconnexio.mail_activity_type_one_shot')
        elif self.one_shot_product_id.product_tmpl_id in router_list:
            self.done = True
            self.activity_type = self.env.ref('somconnexio.mail_activity_type_router_send_or_return')  # noqa
        else:
            self.done = False
            self.activity_type = self.env.ref('somconnexio.mail_activity_type_sim_change')  # noqa

    def button_add(self):
        self.ensure_one()

        if self.one_shot_product_id.product_tmpl_id == self.env.ref(
            "somconnexio.DadesAddicionals500MB_product_template"
        ):
            self.create_otrs_ticket()
        else:
            self.add_one_shot_to_contract()

        return True

    def add_one_shot_to_contract(self):
        one_shot_contract_line = {
            "name": self.one_shot_product_id.name,
            "product_id": self.one_shot_product_id.id,
            "date_start": self.start_date,
            "date_end": last_day_of_month_of_given_date(self.start_date),
        }

        self.contract_id.write(
            {'contract_line_ids': [(0, 0, one_shot_contract_line)]}
        )

        message = _("One shot product '{}' added on '{}'")
        self.contract_id.message_post(
            message.format(
                self.one_shot_product_id.showed_name,
                self.start_date,
            )
        )

        self._create_activity()

    def create_otrs_ticket(self):
        fields_dict = {
            "phone_number": self.contract_id.phone_number,
            "new_product_code": self.one_shot_product_id.default_code,
            "subscription_email": self.contract_id.email_ids[0].email,
            "language": self.contract_id.partner_id.lang,
        }

        AddDataTicket(
            self.contract_id.partner_id.vat,
            self.contract_id.partner_id.ref,
            fields_dict,
        ).create()

        message = _("OTRS add data ticket created. Added additional data bond: '{}'")
        self.contract_id.message_post(
            message.format(self.one_shot_product_id.showed_name)
        )

        self._create_activity()

    def _create_activity(self):
        self.env['mail.activity'].create({
            'summary': self.summary,
            'res_id': self.contract_id.id,
            'res_model_id': self.env.ref('contract.model_contract_contract').id,
            'user_id': self.env.user.id,
            'activity_type_id': self.activity_type.id,
            'done': self.done,
            'date_done': date.today(),
            'date_deadline': date.today(),
            'location': self.location,
            'note': self.note,
        })

    @job
    def run_from_api(self, **params):
        service = ContractOneShotProcess(self.env)
        service.run_from_api(**params)
