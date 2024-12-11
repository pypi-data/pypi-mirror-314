from odoo import models, fields, api, _


class ContractGroupChange(models.TransientModel):
    _name = 'contract.group.change.wizard'
    _description = 'Contract Group Change'

    contract_id = fields.Many2one('contract.contract', string='Contract', required=True)
    contract_group_id = fields.Many2one('contract.group', string='Contract Group')

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        contract = self.env['contract.contract'].browse(self.env.context['active_id'])
        defaults['contract_id'] = contract.id
        defaults['contract_group_id'] = contract.contract_group_id.id
        return defaults

    def button_change(self):
        original_group = self.contract_id.contract_group_id
        new_group = self.contract_group_id

        self.contract_id.write({'contract_group_id': new_group.id})

        message = _("Contract group changed from {old} to {new}.").format(old=original_group.code, new=new_group.code)  # noqa

        if original_group and not original_group.contract_ids:
            message += _("{} group was deleted because it was empty.").format(original_group.code)  # noqa
            original_group.unlink()

        self.contract_id.message_post(message)
