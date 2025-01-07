from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type model"
    _order = "sequence, name asc"

    sequence = fields.Integer('Sequence', default=1)
    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties'
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers'
    )

    offer_count = fields.Integer(
        compute='_compute_offer_count',
        string='Offer Count'
    )

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
        'The name of an estate property type should be unique.')
    ]

    @api.depends('offer_count')
    def _compute_offer_count(self):
        for record in self:
            # record.offer_count = len(record.offer_ids.filtered(lambda offer: offer.property_type_id == record.id))
            record.offer_count = len(record.offer_ids)
