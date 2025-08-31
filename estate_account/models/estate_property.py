from odoo import fields, models, api
from odoo.cli import Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sell_property(self):
        invoice_vals = [{
            "partner_id": self.buyer_id.id,
            "move_type": 'out_invoice',
            "invoice_line_ids": [
                (0, 0, {
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),

                (0, 0, {
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100
                })
            ]
        }]

        self.env['account.move'].create(invoice_vals)
        return super().sell_property()
