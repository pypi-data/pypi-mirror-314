# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductSearchCatAttr(models.AbstractModel):
    _name = "product.search.cat.attr"
    _description = "Product Search Category Attribute"

    RELOAD_VIEW = ""

    applied_category = fields.Many2one(
        comodel_name="product.category",
        compute="_compute_applied_category",
        help="Category for which products are currently searched.",
    )
    category_id = fields.Many2one(
        comodel_name="product.category",
        string="Category",
        help="Click on 'Apply Category' button to refresh the "
        "attributes that apply to the products in this category.",
    )
    applied_category_ids = fields.Many2many(
        comodel_name="product.search.cat.attr.category",
        string="Categories",
        relation="product_search_cat_attr_category_rel",
        column1="search_id",
        column2="category_id",
        readonly=True,
        help="Applied category path.",
    )
    attribute_line_ids = fields.One2many(
        comodel_name="product.search.cat.attr.line",
        string="Attribute Lines",
        inverse_name="search_id",
    )

    def _get_products_by_category(self):
        self.ensure_one()
        products = False
        category_to_search = self.applied_category
        if category_to_search:
            products = self.env["product.product"].search(
                [("categ_id", "child_of", category_to_search.id)]
            )
        return products

    def _add_attribute_line_ids(self):
        for sel in self:
            sel.attribute_line_ids.unlink()
            attributes = []
            attr_lines_create = []
            products = sel._get_products_by_category()
            if products:
                attributes = products.mapped("attribute_line_ids").mapped(
                    "attribute_id"
                )
            for attribute in attributes:
                attr_lines_create.append(
                    {"search_id": sel.id, "attribute_id": attribute.id}
                )
            if attr_lines_create:
                self.env[self.attribute_line_ids._name].create(attr_lines_create)

    def reload_view(self):
        self.ensure_one()
        view_id = self.env.ref(self.RELOAD_VIEW)
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": self._name,
            "target": "new",
            "view_id": view_id.id,
            "res_id": self.id,
        }

    def apply_category(self):
        self.ensure_one()
        new_cat_line = self.env["product.search.cat.attr.category"].create(
            {
                "sequence": self.applied_category_ids[-1].sequence + 1
                if self.applied_category_ids
                else 1,
                "category_id": self.category_id.id,
            }
        )
        self.write(
            {"applied_category_ids": [(4, new_cat_line.id)], "category_id": False}
        )
        self._add_attribute_line_ids()
        return self.reload_view()

    def delete_category(self):
        self.ensure_one()
        self.applied_category_ids.unlink()
        self.attribute_line_ids.unlink()
        self.applied_category_ids.category_id = False
        self.applied_category = False
        return self.reload_view()

    def _search_products(self):
        self.ensure_one()
        category = self.applied_category
        products = self.env["product.product"].search(
            [("categ_id", "child_of", category.id)]
        )
        for attr in self.attribute_line_ids.filtered("attribute_value_ids"):
            attr_products = self.env["product.product"]
            for attr_val in attr.attribute_value_ids:
                attr_products += products.filtered(
                    lambda a, attr_val=attr_val: a.product_template_variant_value_ids
                    and attr_val.id
                    in a.product_template_variant_value_ids.mapped(
                        "product_attribute_value_id"
                    ).ids
                )
            products = attr_products
        return products

    def search_products(self):
        raise NotImplementedError()

    @api.depends("applied_category_ids")
    def _compute_applied_category(self):
        for sel in self:
            applied_category = False
            if sel.applied_category_ids:
                applied_category = sel.applied_category_ids[-1].category_id.id
            sel.applied_category = applied_category
