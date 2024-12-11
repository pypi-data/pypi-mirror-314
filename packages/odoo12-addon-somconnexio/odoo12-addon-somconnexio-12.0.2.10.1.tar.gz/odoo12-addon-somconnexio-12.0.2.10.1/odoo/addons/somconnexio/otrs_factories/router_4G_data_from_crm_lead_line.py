from otrs_somconnexio.otrs_models.router_4G_data import Router4GData

from .broadband_data_from_crm_lead_line import BroadbandDataFromCRMLeadLine


class Router4GDataFromCRMLeadLine(BroadbandDataFromCRMLeadLine):

    def build(self):
        router_4G_data = super().build()
        router_4G_data.update({
            "technology": router_4G_data.get("technology") or "4G"
        })
        return Router4GData(**router_4G_data)
