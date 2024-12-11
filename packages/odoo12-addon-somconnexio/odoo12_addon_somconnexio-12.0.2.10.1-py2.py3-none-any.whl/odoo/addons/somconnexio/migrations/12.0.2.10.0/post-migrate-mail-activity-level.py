import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, _):
    env = api.Environment(cr, SUPERUSER_ID, {})
    levels = ["N1", "N2"]

    # Use level field instead of team_id in mail.activity
    for level in levels:
        _logger.info("Searching mail activity team by level {}.".format(level))
        team = env["mail.activity.team"].search([("name", "=", level)])

        if not team:
            continue

        mail_activities = env["mail.activity"].search([("team_id", "=", team.id)])

        _logger.info("Substituing mail activity team for level {}.".format(level))

        for mail_activity in mail_activities:
            mail_activity.write(
                {
                    "level": level,
                    "team_id": False,
                }
            )

        _logger.info("Mail activity team {} deleted.".format(level))

        team.unlink()
