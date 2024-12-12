# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSearchCatAttrLine(models.AbstractModel):
    _name = "product.search.cat.attr.line"
    _description = "Product Search Category Attribute"

    search_id = fields.Many2one(
        comodel_name="product.search.cat.attr",
        string="Search",
        ondelete="cascade",
    )
    attribute_id = fields.Many2one(
        comodel_name="product.attribute", string="Attribute", readonly=True
    )
    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        domain="[('attribute_id', '=', attribute_id)]",
    )
