# Copyright 2022 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Product(models.Model):
    _inherit = "product.product"

    product_template_variant_value_ids = fields.Many2many(
        domain=[("attribute_line_id.value_count", ">", 0)]
    )
