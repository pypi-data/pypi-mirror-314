from openupgradelib import openupgrade

_xml_ids_mapping = [
    (
        "CH_SC_OSO_SHARED_10GB_ADDICIONAL",
        "DadesAddicionals10GBCompartides",
    ),
    (
        "CH_SC_OSO_SHARED_20GB_ADDICIONAL",
        "DadesAddicionals20GBCompartides",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    model = "product.product"
    for default_code, new_xml_id in _xml_ids_mapping:
        product = env[model].search([("default_code", "=", default_code)])
        openupgrade.add_xmlid(env.cr, "somconnexio", new_xml_id, model, product.id)
