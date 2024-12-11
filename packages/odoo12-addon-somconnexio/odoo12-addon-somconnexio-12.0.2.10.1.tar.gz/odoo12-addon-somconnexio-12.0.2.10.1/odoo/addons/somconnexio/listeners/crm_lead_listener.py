from odoo.addons.component.core import Component

# 5 mins in seconds to delay the jobs
ETA = 300


class CrmLeadListener(Component):
    _name = 'crm.lead.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['crm.lead']

    def on_record_write(self, record, fields=None):

        if "stage_id" in fields:
            self._stage_changed(record)

    def _stage_changed(self, record):
        if record.stage_id.id == self.env.ref("crm.stage_lead4").id:  # Stage Won
            for line in record.lead_line_ids:
                line.with_delay().create_ticket()
            if record.has_mobile_lead_lines and record.has_broadband_lead_lines:
                record.with_delay(eta=ETA).link_pack_tickets()
            if record.mobile_lead_line_ids.filtered(
                lambda l: (l.product_id.has_sharing_data_bond)
            ):
                record.with_delay(eta=ETA+100).link_sharing_data_mobile_tickets()
        elif (
            record.stage_id.id == self.env.ref("somconnexio.stage_lead8").id
        ):  # Stage Generating delivery
            record.with_delay().create_shipment()
