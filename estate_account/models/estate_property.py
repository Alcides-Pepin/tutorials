from odoo import api, models
from odoo.exceptions import UserError
from odoo import Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell_property(self):
        super().action_sell_property()
        
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        if not journal:
            raise UserError(('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        # Créer la facture
        self.env['account.move'].create({
            'name': 'Test',
            'partner_id': self.buyer_id.id,  # Le client
            'move_type': 'out_invoice',  # Type de facture (facture client)
            'journal_id': journal.id,
            'line_ids': [
                Command.create({
                    'name': f'Property : {self.name}',
                    'quantity': 1.0,
                    'price_unit': self.selling_price,
                }),
                Command.create({
                    'name': f'Fees',
                    'quantity': 1.0,
                    'price_unit': self.selling_price * 0.06 + 100,
                })
            ]
        })
