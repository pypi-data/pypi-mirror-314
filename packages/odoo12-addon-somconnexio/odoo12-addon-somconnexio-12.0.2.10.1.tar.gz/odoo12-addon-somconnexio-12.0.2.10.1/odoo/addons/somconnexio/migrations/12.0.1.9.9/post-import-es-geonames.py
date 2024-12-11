from odoo import SUPERUSER_ID, api

import logging

_logger = logging.getLogger(__name__)


def _update_address_from_zip(partner, env):
    city_zip = env["res.city.zip"].search([
        ('name', '=', partner.zip)
    ])
    if not city_zip:
        _logger.warning("No city found searching by the zip code of partner {}".format(partner.id))  # noqa
        return
    if len(city_zip) > 1:
        _logger.warning("More than one city found searching by the zip code of partner {}".format(partner.id))  # noqa
        partner.write({
            'state_id': city_zip[0].city_id.state_id.id,
        })
    else:
        partner.write({
            'state_id': city_zip.city_id.state_id.id,
            'city': city_zip.city_id.name,
        })


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Partner = env["res.partner"]

    # Import the Toponyms of Spain
    _logger.info("Import ES Geoname cities and zip codes.")
    env["config.es.toponyms"].execute()

    # Migrar partners zip de 4 digitos y state Barcelona y añadir un 0 delante del ZIP
    _logger.info("Fix partners with 4 digits zip and state Barcelona.")
    barcelona = env.ref("base.state_es_b")
    partner_to_update_zip = Partner.search([
        ('state_id', '=', barcelona.id),
        ('zip', '!=', None),
    ]).filtered(lambda p: len(p.zip) == 4)
    for p in partner_to_update_zip:
        p.write({
            'zip': "0{}".format(p.zip),
        })

    # Migrar partners sin state/city pillando el state/city de city_zip
    _logger.info("Fix partners without state or city getting the state/city from Geonames imported zips.")  # noqa
    partner_to_update_address = Partner.search([
        ('zip', '!=', None),
        '|',
        ('state_id', '=', None),
        ('city', '=', None),
    ])
    for p in partner_to_update_address:
        _update_address_from_zip(p, env)
