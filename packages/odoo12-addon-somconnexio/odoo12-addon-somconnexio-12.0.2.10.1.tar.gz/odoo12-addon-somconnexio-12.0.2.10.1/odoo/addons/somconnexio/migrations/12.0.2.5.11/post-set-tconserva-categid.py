import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    _logger.info("Setting mobile to categ id for t-conserva product template.")
    env.ref("somconnexio.TarifaConserva_product_template").write(
        {"categ_id": env.ref("somconnexio.mobile_service").id}
    )
