from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    model = env['crm.lead.line']
    env.add_todo(model._fields['is_from_pack'], model.search([]))
    model.recompute()
