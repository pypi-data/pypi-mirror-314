# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ProductSearchCatAttrCategory(models.TransientModel):
    _name = "product.search.cat.attr.category"
    _description = "Product Search Cat Attr Category"
    _order = "sequence"

    sequence = fields.Integer()
    category_id = fields.Many2one(comodel_name="product.category", string="Category")
