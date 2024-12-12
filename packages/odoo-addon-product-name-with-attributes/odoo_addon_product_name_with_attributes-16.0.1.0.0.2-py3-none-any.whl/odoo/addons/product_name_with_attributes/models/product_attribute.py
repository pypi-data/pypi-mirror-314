# Copyright 2022 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    def _get_combination_name(self):
        ptavs = self._without_no_variant_attributes().with_prefetch(self._prefetch_ids)
        return ", ".join(
            [(ptav.attribute_id.name + ": " + ptav.name) for ptav in ptavs]
        )
