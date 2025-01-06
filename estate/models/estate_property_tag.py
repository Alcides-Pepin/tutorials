from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag model"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
        'The name of an estate property tag should be unique.')
    ]