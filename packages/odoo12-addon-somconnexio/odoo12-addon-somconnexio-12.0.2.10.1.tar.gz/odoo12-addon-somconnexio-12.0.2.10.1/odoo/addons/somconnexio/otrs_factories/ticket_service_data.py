from odoo import models
from ..otrs_factories.mobile_data_from_crm_lead_line import MobileDataFromCRMLeadLine
from ..otrs_factories.fiber_data_from_crm_lead_line import FiberDataFromCRMLeadLine
from ..otrs_factories.adsl_data_from_crm_lead_line import ADSLDataFromCRMLeadLine
from ..otrs_factories.router_4G_data_from_crm_lead_line import (
    Router4GDataFromCRMLeadLine,
)


class TicketServiceData(models.AbstractModel):
    _name = "ticket.service.data"
    _register = True
    _description = """
        Service build service data from crm lead line
        according to their technology
    """

    def build(self, crm_lead_line):
        if crm_lead_line.is_mobile:
            service_data = MobileDataFromCRMLeadLine(crm_lead_line)
        elif crm_lead_line.is_fiber:
            service_data = FiberDataFromCRMLeadLine(crm_lead_line)
        elif crm_lead_line.is_adsl:
            service_data = ADSLDataFromCRMLeadLine(crm_lead_line)
        elif crm_lead_line.is_4G:
            service_data = Router4GDataFromCRMLeadLine(crm_lead_line)

        return service_data.build()
