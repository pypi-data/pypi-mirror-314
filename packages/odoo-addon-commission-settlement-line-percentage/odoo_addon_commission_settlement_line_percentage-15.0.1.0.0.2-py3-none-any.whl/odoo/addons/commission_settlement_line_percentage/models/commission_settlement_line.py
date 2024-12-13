# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CommissionSettlementLine(models.Model):
    _inherit = "commission.settlement.line"

    percentage = fields.Float(
        name="Percentage",
        compute="_compute_percentage",
        digits=(3, 1),
        store=True,
    )

    def _compute_percentage(self):
        for rec in self:
            rec.percentage = (
                rec.settled_amount / rec.invoice_line_id.price_subtotal * 100
                if rec.invoice_line_id.price_subtotal
                else 0
            )
