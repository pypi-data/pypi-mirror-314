import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute(
        "UPDATE ir_model_data SET name='20GB', module='somconnexio' "
        "WHERE res_id = "
        "(SELECT id FROM product_attribute_value WHERE name='20 GB') "
        "AND model='product.attribute.value';"
    )
    cr.execute(
        "UPDATE ir_model_data SET name='TrucadesIllimitades20GB', "
        "module='somconnexio' WHERE res_id = "
        "(SELECT id FROM product_product WHERE custom_name='Ilimitadas 20 GB') "
        "AND model='product.product';"
    )
