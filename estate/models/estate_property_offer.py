from dateutil import relativedelta

from odoo import fields, models, api
from odoo.fields import Datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    name = fields.Char()
    price = fields.Float()
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refused','Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date().today()
            record.date_deadline = create_date + relativedelta.relativedelta(days= record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = record.create_date.date() if record.create_date else fields.Date().today()
                record.validity = (record.date_deadline - record.create_date.date()).days