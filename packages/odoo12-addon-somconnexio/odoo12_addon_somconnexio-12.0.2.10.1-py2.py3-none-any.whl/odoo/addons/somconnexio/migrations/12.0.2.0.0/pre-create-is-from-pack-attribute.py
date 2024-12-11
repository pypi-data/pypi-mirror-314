from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    imd_attr = env['ir.model.data'].search([
        ('name', '=', 'InPack')
    ])
    imd_attr_value = env['ir.model.data'].search([
        ('name', '=', 'IsInPack')
    ])
    if not imd_attr:
        attr = env['product.attribute'].create({
            'name': "Is it in Pack?",
            'create_variant': 'always',
            'type': 'radio'
        })
        # When a new template is created, it also creates one new product.product
        env['ir.model.data'].create({
            'model': 'product.attribute',
            'module': 'somconnexio',
            'name': 'InPack',
            'res_id': attr.id,
        })
    if not imd_attr_value:
        attr_id = env.ref('somconnexio.InPack').id
        attr_value = env['product.attribute.value'].create({
            'name': "Forma part d'un pack",
            'attribute_id': attr_id
        })
        # When a new template is created, it also creates one new product.product
        env['ir.model.data'].create({
            'model': 'product.attribute.value',
            'module': 'somconnexio',
            'name': 'IsInPack',
            'res_id': attr_value.id,
        })
