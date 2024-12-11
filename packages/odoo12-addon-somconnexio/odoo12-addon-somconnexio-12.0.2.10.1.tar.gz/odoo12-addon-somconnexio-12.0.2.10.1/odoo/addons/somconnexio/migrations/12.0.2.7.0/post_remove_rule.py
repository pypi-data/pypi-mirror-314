from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    rule = env.ref("mail_activity_team.mail_activity_rule_my_team")
    rule.unlink()
