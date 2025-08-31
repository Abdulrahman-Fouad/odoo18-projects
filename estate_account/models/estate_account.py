from odoo import fields, models, api


class EstateAccount(models.Model):
    _name = 'estate.account'
    _description = 'Estate Account'

    name = fields.Char()
