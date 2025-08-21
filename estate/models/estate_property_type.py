from itertools import count

from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'This Type already exists!!')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            if record.offer_ids:
                record.offer_count = len(record.offer_ids)

    def print_offer_count(self):
        print(self.offer_count)