# Copyright 2022 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product name with attributes",
    "summary": "Product name with attributes",
    "version": "16.0.1.0.0",
    "category": "Inventory",
    "website": "https://github.com/sygel-technology/sy-product-attribute",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base", "product", "sale"],
    "data": [
        "views/sale_order_views.xml",
    ],
}
