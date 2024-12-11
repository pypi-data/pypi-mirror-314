from odoo import SUPERUSER_ID, api

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    MailActivty = env["mail.activity"]
    MailActivtyType = env["mail.activity.type"]
    target_activities_types = [
        "Tarrif Change", "One Shot", "Roaming", "Sim Change", "Contract Data Change",
        "Mobile Incident", "Out Portability", "Consume Limit", "Fiber Vdf Incident",
        "ADSL Incident", "Massive Mobile Incident", "Mobile Provisioning Incident",
        "Ubication Change and Fiber MM Leave", "SC Service Claim", "Supplier Claim",
        "Mobile Provisioning Incident", "Router Send/Return"
        ]

    activity_types = MailActivtyType.search(
        [('name', 'in', target_activities_types)])
    activity_type_ids = [activity.id for activity in activity_types]
    activities = MailActivty.search(
        [
            ('activity_type_id', 'in', activity_type_ids),
            ('active', '=', True),
            ('done', '=', False),
        ]
    )
    for activity in activities:
        if activity.user_id:
            activity.write({
                "user_id": env.ref('base.user_admin').id
            })
