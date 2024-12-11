from odoo import api, fields, models, _


class Product(models.Model):
    _inherit = ['mail.thread', 'product.product']
    _name = 'product.product'

    _sql_constraints = [
        ('default_code_uniq', 'unique (default_code)',
         'The product code must be unique !'
         ),
    ]

    public = fields.Boolean(
        string='Public',
        help='This field selects if the products that we expose in the catalog API.',
        default=False)

    custom_name = fields.Char(
        string='Custom name',
        translate=True,)

    showed_name = fields.Char(
        string="Name",
        compute="_compute_showed_name",
        inverse="_inverse_showed_name",
        translate=True,
        store=True,)

    without_fix = fields.Boolean("Product without fix number", default=False)
    contract_as_new_service = fields.Boolean("Contract as new service", default=True)

    has_custom_products_to_change_tariff = fields.Boolean(
        help="""
        This flag allows select a list of products to allow change tariff from
        this product.
        If this flag is not selected, all the products from the same category
        will be available in change tariff process.
        """
    )

    products_available_change_tariff = fields.Many2many(
        'product.product', 'product_product_change_tariff_rel',
        'main_product_id', 'product_id',
        string="Available Products to Change Tariff"
    )

    product_is_pack_exclusive = fields.Boolean(
        compute='_compute_is_pack_exclusive',
        default=False,
        store=True,
    )

    has_sharing_data_bond = fields.Boolean(
        string='Is sharing mobile data?',
        default=False
    )

    @api.model
    def name_search(
        self, name, args=None, operator='ilike', limit=100, name_get_uid=None
    ):

        if name:
            if args:
                new_args = [
                    '&', '|',
                    ('showed_name', operator, name), ('default_code', operator, name)
                ] + args
            else:
                new_args = [
                    '|',
                    ('showed_name', operator, name), ('default_code', operator, name)
                ]
            records = self.env['product.product'].search(new_args, limit=limit)
            return models.lazy_name_get(records)
        else:
            return super()._name_search(
                name=name, args=args, operator=operator,
                limit=limit, name_get_uid=name_get_uid
            )

    @api.depends('attribute_value_ids')
    def _compute_is_pack_exclusive(self):
        pack_attr = self.env.ref("somconnexio.IsInPack", raise_if_not_found=False)
        if not pack_attr:
            return

        for product in self:
            product.product_is_pack_exclusive = bool(
                pack_attr in product.attribute_value_ids
            )

    # TAKE IN MIND: We can overwrite this method from product_product for now,
    # but in the future we might need some additional features/conditions from
    # the original one:
    # https://github.com/odoo/odoo/blob/12.0/addons/product/models/product.py#L424
    @api.multi
    def name_get(self):
        data = []
        for product in self:
            data.append((product.id, product.showed_name))
        return data

    @api.depends('custom_name', 'name')
    def _compute_showed_name(self):
        for product in self:
            product.showed_name = product.custom_name or product.name

    def _inverse_showed_name(self):
        for product in self:
            product.custom_name = product.showed_name

    def get_catalog_name(self, attribute_name):
        catalog_name = False
        for attribute_value in self.attribute_value_ids:
            if attribute_value.attribute_id.name == attribute_name:
                catalog_name = attribute_value.catalog_name
        if not catalog_name:
            product_tmpl_catalog_attr = self.product_tmpl_id.catalog_attribute_id
            if product_tmpl_catalog_attr.attribute_id.name == attribute_name:
                catalog_name = self.product_tmpl_id.catalog_attribute_id.catalog_name
        return catalog_name

    def without_lang(self):
        ctx = self.env.context.copy()
        if 'lang' in ctx:
            del ctx['lang']
        return self.with_context(ctx)

    def write(self, vals):
        for product in self:
            for key, value in vals.items():
                msg = _("Field '{}' edited from '{}' to '{}'")
                product.message_post(msg.format(key, getattr(product, key), value))
        super().write(vals)
        return True

    def get_offer(self):
        """
        Return the same product but the one with offer.
        Ex. If we execute this method for Unilimited 20GB
        it return Unilimited 20GB Pack
        """

        if (
            self.has_sharing_data_bond
            or self.env.ref("somconnexio.CompanyExclusive") in self.attribute_value_ids
        ):
            # Company exclusive and sharing data tariff
            # products are already an offer
            return

        attr_to_exclude = (
            self.env.ref("somconnexio.IsNotInPack")
            | self.env.ref("somconnexio.CompanyExclusive")
            | self.env.ref("somconnexio.Sharing2Mobiles")
            | self.env.ref("somconnexio.Sharing3Mobiles")
        )
        attr_to_include = self.env.ref("somconnexio.IsInPack")

        return self.get_variant_with_attributes(attr_to_exclude, attr_to_include)

    def get_variant_with_attributes(self, attr_to_exclude=False, attr_to_include=False):
        """
        Return the product that has the same attribute combination excluding
        some attributes and including others.
        """
        attr_combination = self.attribute_value_ids

        if attr_to_include:
            attr_combination += attr_to_include
        if attr_to_exclude:
            attr_combination -= attr_to_exclude

        product_domain = [
            ("attribute_value_ids", "=", att.id) for att in attr_combination
        ]
        product_domain.extend(
            [
                ("attribute_value_ids", "not in", attr_to_exclude.ids),
                ("product_tmpl_id", "=", self.product_tmpl_id.id),
                ("id", "!=", self.id),
            ]
        )
        return self.env["product.product"].search(
            product_domain,
            limit=1,
        )
