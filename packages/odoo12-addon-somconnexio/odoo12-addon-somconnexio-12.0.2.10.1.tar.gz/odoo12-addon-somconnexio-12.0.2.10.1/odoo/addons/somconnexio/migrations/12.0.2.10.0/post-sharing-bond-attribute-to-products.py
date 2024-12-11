from odoo import SUPERUSER_ID, api

_products_to_update = {
    "Sharing2Mobiles": [
        "50GBCompartides2mobils",
        "50GBCompartides2mobilsEiE",
        "150GBCompartides2mobilsEiE",
    ],
    "Sharing3Mobiles": [
        "50GBCompartides3mobils",
        "50GBCompartides3mobilsEiE",
        "150GBCompartides3mobilsEiE",
    ],
}


def migrate(cr, _):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for attr_ref, product_xml_ids in _products_to_update.items():
        attribute = env.ref(f"somconnexio.{attr_ref}")
        for xml_id in product_xml_ids:
            product = env.ref(f"somconnexio.{xml_id}")
            product.write({"attribute_value_ids": [(4, attribute.id)]})
