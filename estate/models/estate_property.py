from dateutil import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,
                                    default=lambda self: fields.Date.today() + relativedelta.relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], required=True, copy=False, default='new', string='Status', readonly=True)

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)

    tag_ids = fields.Many2many('estate.property.tag')

    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Property expected price must be a positive value!'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Property selling price must be a positive value!'),

    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else False
        self.garden_orientation = 'north' if self.garden else False

    def cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise UserError("Sold Properties cannot be cancelled")

    def sell_property(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise UserError("Cancelled Properties cannot be sold")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            else:
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                    raise ValidationError("The selling price must be at least 90% of the expected price! "
                                          "You must reduce the expected price if you want to accept this offer")
