# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Search Category Attribute",
    "summary": "Base module for category/attribute products searching",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/sygel-technology/sy-product-attribute",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_search_category_attribute_views.xml",
    ],
}
