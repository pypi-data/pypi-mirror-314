from odoo import models


class AccountMove(models.Model):
    _inherit = ['mail.thread', 'account.move']
    _name = 'account.move'
