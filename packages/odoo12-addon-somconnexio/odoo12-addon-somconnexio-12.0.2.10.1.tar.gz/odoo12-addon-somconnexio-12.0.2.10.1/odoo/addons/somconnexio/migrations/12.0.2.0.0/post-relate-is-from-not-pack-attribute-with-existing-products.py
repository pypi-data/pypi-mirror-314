from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    not_in_pack_attrib_value = env["ir.model.data"].search(
        [("name", "=", "IsNotInPack")]
    )
    product_list = [
        "SE_SC_REC_MOBILE_T_UNL_0",
        "SE_SC_REC_MOBILE_T_UNL_500",
        "SE_SC_REC_MOBILE_T_UNL_1024",
        "SE_SC_REC_MOBILE_T_UNL_2048",
        "SE_SC_REC_MOBILE_T_UNL_5120",
        "SE_SC_REC_MOBILE_T_UNL_10240",
        "SE_SC_REC_MOBILE_T_UNL_20552",
        "SE_SC_REC_MOBILE_T_UNL_30720",
        "SE_SC_REC_MOBILE_T_UNL_51200",
    ]
    products = env["product.product"].search(
        [
            ("default_code", "in", product_list),
        ]
    )
    products.write({"attribute_value_ids": [(4, not_in_pack_attrib_value.res_id, 0)]})
