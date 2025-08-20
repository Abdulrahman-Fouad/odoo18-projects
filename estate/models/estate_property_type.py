from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property type'

    name = fields.Char(required=True)


    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'This Type already exists!!')
    ]