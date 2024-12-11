from odoo import SUPERUSER_ID, api

# Dict with products to fix. Format:
# Key: default_code
# Value: externalId
products_to_fix = {
    "SE_SC_REC_BA_F_300_SF": "SenseFixFibra300Mb",
    "SE_SC_REC_BA_F_300": "Fibra300Mb",
    "SE_SC_REC_MOBILE_T_UNL_102400": "TrucadesIllimitades100GB",
    "SE_SC_REC_MOBILE_T_UNL_153600": "TrucadesIllimitades150GB",
}

# Dict with attributes to fix. Format:
# Key: attribute_id (externalId)
# Value: Dicts
#    Key: name
#    Value: externalId
attributes_to_fix = {
    "Data": {
        "100 GB": "100GB",
        "150 GB": "150GB",
    },
    "Bandwidth": {
        "300 Mb": "300Mb",
    },
}


def create_or_update_model_data(ModelData, model, name, res_id):
    model_data = ModelData.search([("model", "=", model), ("res_id", "=", res_id)])
    if model_data:
        model_data.write(
            {
                "module": "somconnexio",
                "name": name,
            }
        )
    else:
        ModelData.create(
            {
                "model": model,
                "module": "somconnexio",
                "name": name,
                "res_id": res_id,
            }
        )


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    ModelData = env["ir.model.data"]
    # Products
    products = env["product.product"].search(
        [("default_code", "in", list(products_to_fix.keys()))]
    )
    for product in products:
        create_or_update_model_data(
            ModelData,
            "product.product",
            products_to_fix[product.default_code],
            product.id,
        )
    # Attribute Values
    for attribute_type in attributes_to_fix.keys():
        attribute_values = env["product.attribute.value"].search(
            [
                (
                    "attribute_id",
                    "=",
                    env.ref("somconnexio.{}".format(attribute_type)).id,
                ),
                ("name", "in", list(attributes_to_fix[attribute_type].keys())),
            ]
        )
        for attribute in attribute_values:
            create_or_update_model_data(
                ModelData,
                "product.attribute.value",
                attributes_to_fix[attribute_type][attribute.name],
                attribute.id,
            )
