from odoo import fields, models, api

class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate.property',
        'sales_person_id',
        string="Properties",
        domain=[('active', '=', True)]
    )