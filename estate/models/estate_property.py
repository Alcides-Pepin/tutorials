from odoo import fields, models
from odoo.tools import date_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=date_utils.add(
            fields.Date.today(),
            months=3
            )
        )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')]
        )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[
                ('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('cancelled', 'Cancelled')
            ],
        required=True,
        copy=False,
        default='new'
        )
    property_type_id = fields.Many2one(string="Property Type",
                                       comodel_name="estate.property.type")
    sales_person_id = fields.Many2one(string="Sales Person",
                                      comodel_name="res.users",
                                      default=lambda self: self.env.user)
    buyer_id = fields.Many2one(string="Buyer",
                               comodel_name="res.partner",
                               copy=False)
    tag_ids = fields.Many2many(string="Tags",
                               comodel_name="estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id",
                                string="Offers")
