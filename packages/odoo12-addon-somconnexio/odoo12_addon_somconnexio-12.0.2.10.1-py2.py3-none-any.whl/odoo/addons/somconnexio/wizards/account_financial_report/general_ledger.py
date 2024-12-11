from odoo import models, fields, api


class GeneralLedgerWizard(models.TransientModel):
    _inherit = 'general.ledger.report.wizard'
    general_expenses = fields.Boolean()

    @api.onchange('general_expenses', 'account_type_ids')
    def _onchange_account_type_ids(self):
        general_expenses_accounts = [
            62300001, 62300002, 62300010, 62300005, 62300006, 62100000,
            62900000, 62800000, 64900000, 62300000, 62900010, 62600000,
            62500000, 62700000, 62700001, 69100000, 62800002, 62800001,
            62300003, 62300004, 62300007, 62300008, 62900003, 62900002,
            62400000, 62900001, 60200040, 60200000, 63100000, 60200020,
            60200030, 67800001, 62300009, 62300011
        ]
        if self.account_type_ids:
            if self.general_expenses:
                self.account_ids = self.env['account.account'].search([
                    ('company_id', '=', self.company_id.id),
                    ('user_type_id', 'in', self.account_type_ids.ids),
                    ('code', 'in', general_expenses_accounts),
                ])
            else:
                self.account_ids = self.env['account.account'].search([
                    ('company_id', '=', self.company_id.id),
                    ('user_type_id', 'in', self.account_type_ids.ids)
                ])
        else:
            if self.general_expenses:
                self.account_ids = self.env['account.account'].search([
                    ('company_id', '=', self.company_id.id),
                    ('code', 'in', general_expenses_accounts),
                ])
            else:
                self.account_ids = None
