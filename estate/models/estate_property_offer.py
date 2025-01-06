from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer model'
    _order = "price desc"

    price = fields.Float(
        string='Price',
    )
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
                ('accepted', 'Accepted'),
                ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one(
        string='Buyer',
        comodel_name='res.partner',
        required=True
    )
    property_id = fields.Many2one(
        string='Property',
        comodel_name='estate.property',
        required=True
    )
    validity = fields.Integer(
        string='Validity',
        default=7)

    date_deadline = fields.Date(
        string='Date Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
        'The price of a property offer should be strictly positive.')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        # print("Méthode compute appelée")
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date().today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        # print("Méthode inverse appelée")
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
                record.validity = (record.date_deadline - create_date).days
            else:
                record.validity = (record.date_deadline - fields.Date().today()).days

    def action_accept_offer(self):
        if self.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
            raise UserError(("Another offer has already been accepted."))
        else:
            self.status = 'accepted'
            self.property_id.state = 'offer_accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id

    def action_refuse_offer(self):
        self.status = 'refused'
        self.property_id.selling_price = False
        self.property_id.buyer_id = False
