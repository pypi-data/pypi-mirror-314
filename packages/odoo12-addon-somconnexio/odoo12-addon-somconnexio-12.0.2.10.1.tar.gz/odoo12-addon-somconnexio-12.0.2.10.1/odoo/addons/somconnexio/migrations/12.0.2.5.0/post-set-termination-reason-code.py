import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    _logger.info("Setting code for terminate reason contract.")
    codes = {
        "somconnexio.reason_exit_portability": "TR001",
        "somconnexio.reason_line_sign_out": "TR002",
        "somconnexio.reason_holder_change": "TR003",
        "somconnexio.reason_change_to_fiber_and_landline": "TR004",
        "somconnexio.reason_change_to_fiber_without_landline": "TR005",
        "somconnexio.reason_location_change_from_SC_to_SC": "TR006",
        "somconnexio.reason_change_to_4G_SC": "TR007",
        "somconnexio.reason_other": "TR008",
        "somconnexio.reason_location_change": "TR009",
        "somconnexio.reason_tech_change": "TR010",
        "somconnexio.reason_unknown": "TR011",
        "somconnexio.reason_change_adsl_to_fiber": "TR012",
        "somconnexio.reason_move_to_home_with_connexion": "TR013",
        "somconnexio.reason_termination": "TR014",
        "somconnexio.reason_change_to_4G_other_provider": "TR015",
    }

    for key, value in codes.items():
        env.ref(key).write({"code": value})

    _logger.info("Setting code for terminate user reason contract.")

    user_codes = {
        "somconnexio.user_reason_price": "TUR001",
        "somconnexio.user_reason_incident": "TUR002",
        "somconnexio.user_reason_service_claim": "TUR003",
        "somconnexio.user_reason_sc_claim": "TUR004",
        "somconnexio.user_reason_no_coverage_at_new_home": "TUR005",
        "somconnexio.user_reason_no_fiber_need": "TUR006",
        "somconnexio.user_reason_move_to_home_with_connexion": "TUR007",
        "somconnexio.user_reason_non_payment": "TUR008",
        "somconnexio.user_reason_unknown": "TUR009",
        "somconnexio.user_reason_other": "TUR010",
        "somconnexio.user_reason_not_applicable": "TUR011",
    }

    for key, value in user_codes.items():
        env.ref(key).write({"code": value})
