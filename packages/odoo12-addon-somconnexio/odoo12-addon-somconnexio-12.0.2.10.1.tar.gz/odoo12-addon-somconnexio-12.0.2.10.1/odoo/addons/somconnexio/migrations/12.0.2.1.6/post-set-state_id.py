import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def _update_state_id_from_zip(partner, env):
    city_zip = env["res.city.zip"].search([("name", "=", partner.zip)])
    if not city_zip:
        _logger.warning(
            "No city found searching by the zip code of partner {}".format(partner.id)
        )
        return
    if len(city_zip) > 1:
        _logger.warning(
            "More than one city found searching by the zip code of partner {}".format(
                partner.id
            )
        )
        state_id = city_zip[0].city_id.state_id.id
    else:
        state_id = city_zip.city_id.state_id.id
    partner.write({"state_id": state_id})


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Migrar partners sin state pillando el state de city_zip
    _logger.info(
        "Fix partners without state getting the state from Geonames imported zips."
    )
    partner_to_update_address = env["res.partner"].search(
        [
            ("zip", "!=", None),
            ("state_id", "=", None),
        ]
    )
    for p in partner_to_update_address:
        _update_state_id_from_zip(p, env)
