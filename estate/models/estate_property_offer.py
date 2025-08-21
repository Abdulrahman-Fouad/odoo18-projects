from dateutil import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = 'price desc'

    name = fields.Char()
    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', stored=True)

    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'Property offer price must be a positive value!')
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + relativedelta.relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = record.create_date.date() if record.create_date else fields.Date.today()
                record.validity = (record.date_deadline - create_date).days

    def offer_accept(self):
        for record in self:
            record_property = record.property_id
            offers_states = record_property.offer_ids.mapped('status')
            if 'accepted' in offers_states and record.status != 'accepted':
                raise UserError('Only one offer can be accepted for the property!')
            else:
                record.status = 'accepted'
                record_property.selling_price = record.price
                record_property.buyer_id = record.partner_id
                record_property.state = 'offer_accepted'

    def offer_refuse(self):
        for record in self:
            record.status = 'refused'