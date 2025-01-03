from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type model"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string='Properties'
    )

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
        'The name of an estate property type should be unique.')
    ]