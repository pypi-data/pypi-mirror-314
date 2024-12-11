from odoo.addons.component.core import Component
from datetime import datetime, timedelta

# 5 mins in seconds to delay the jobs
ETA = 300


class Contract(Component):
    _name = 'contract.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['contract.contract']

    def on_record_create(self, record, fields=None):
        self.env['contract.contract'].with_delay().create_subscription(
            record.id
        )

    def on_record_write(self, record, fields=None):
        if 'is_terminated' in fields and record.is_terminated:
            eta = ETA
            if record.date_end > datetime.today().date():
                end_datetime = datetime.combine(record.date_end, datetime.min.time()) \
                    + timedelta(seconds=ETA)
                eta = end_datetime - datetime.today()

            self.env['contract.contract'].with_delay(
                eta=eta
            ).terminate_subscription(
                record.id
            )
            if (
                record.is_pack
                and record.terminate_reason_id.id not in [
                    self.env.ref("somconnexio.reason_location_change_from_SC_to_SC").id,
                    self.env.ref("somconnexio.reason_holder_change_pack").id,
                ]
            ):
                record.break_packs()
