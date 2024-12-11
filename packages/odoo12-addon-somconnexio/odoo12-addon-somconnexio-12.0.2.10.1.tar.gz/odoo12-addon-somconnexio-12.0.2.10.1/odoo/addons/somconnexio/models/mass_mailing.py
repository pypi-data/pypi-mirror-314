from odoo import models, fields, api, _
from odoo.addons.mass_mailing.models.mass_mailing import MASS_MAILING_BUSINESS_MODELS
from odoo.exceptions import ValidationError
MASS_MAILING_BUSINESS_MODELS = MASS_MAILING_BUSINESS_MODELS.copy()
MASS_MAILING_BUSINESS_MODELS.append('contract.contract')


@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


class MassMailing(models.Model):
    _inherit = 'mail.mass_mailing'
    mailing_model_id = fields.Many2one(
        domain=[('model', 'in', MASS_MAILING_BUSINESS_MODELS)]
    )
    lang = fields.Selection(
        _lang_get, string='Language', default=lambda self: self.env.lang
    )
    indispensable_email = fields.Boolean()

    @api.multi
    def put_in_queue(self):
        self.validate_opt_out()
        self.validate_lang()
        return super().put_in_queue()

    @api.multi
    def action_schedule_date(self):
        self.validate_opt_out()
        self.validate_lang()
        return super().action_schedule_date()

    @api.multi
    def action_test_mailing(self):
        self.validate_opt_out()
        self.validate_lang()
        return super().action_test_mailing()

    @api.multi
    def validate_lang(self):
        self.ensure_one()
        partners = [
            contact.partner_id
            for contact_list in self.contact_list_ids
            for contact in contact_list.contact_ids
        ]
        wrong_lang_partner = next(
            (
                partner
                for partner in partners
                if partner.lang != self.lang
            ), self.env['res.partner'].browse()
        )
        if self.lang and wrong_lang_partner:
            raise ValidationError(
                _('Lang for partner {} is {} not {}').format(
                    wrong_lang_partner.name, wrong_lang_partner.lang, self.lang
                )
            )

    @api.multi
    def validate_opt_out(self):
        self.ensure_one()
        if not self.indispensable_email:
            partners = [
                contact.partner_id
                for contact_list in self.contact_list_ids
                for contact in contact_list.contact_ids
            ]
            wrong_opt_out_partner = next(
                (
                    partner
                    for partner in partners
                    if partner.only_indispensable_emails
                ), self.env['res.partner'].browse()
            )
            if wrong_opt_out_partner:
                raise ValidationError(
                    _('Partner {} has set only_indispensable_emails').format(
                        wrong_opt_out_partner.name
                    )
                )
