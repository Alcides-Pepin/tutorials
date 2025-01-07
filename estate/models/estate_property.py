from odoo import fields, models, api
from odoo.tools import date_utils
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property model'
    _order = "id desc"

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
    property_type_id = fields.Many2one(string='Property Type',
                                        comodel_name='estate.property.type')
    sales_person_id = fields.Many2one(string='Sales Person',
                                        comodel_name='res.users',
                                        default=lambda self: self.env.user)
    buyer_id = fields.Many2one(string='Buyer',
                                comodel_name='res.partner',
                                copy=False)
    tag_ids = fields.Many2many(string='Tags',
                                comodel_name='estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id',
                                string='Offers')

    total_area = fields.Float(string='Total Area',
                                compute='_compute_total_area')

    best_price = fields.Float(string='Best Price',
                                compute='_compute_best_price')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
        'The expected_price of a property should be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
        'The selling_price of a property should be strictly positive.'),
    ]


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        # self.total_area = self.garden_area + self.living_area

        for record in self:
            record.total_area = record.garden_area + record.living_area

    # # mapped() apply a function to every record of a recordset
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.mapped('offer_ids.price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(("You cannot define a cancelled property as sold."))
            else:
                record.state = 'sold'

    def action_cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(("You cannot define a sold property as cancelled."))
            else:
                record.state = 'cancelled'

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            minimum_limit = 0.9 * record.expected_price
            status = float_utils.float_compare(record.selling_price, minimum_limit, precision_digits=2, precision_rounding=None) 
            if status == -1:
                raise ValidationError("The selling price cannot be inferior to 90% of the expected price.")
            
    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise ValidationError("A property can only be deleted if cancelled or new.")