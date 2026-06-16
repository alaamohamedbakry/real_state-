from odoo import models, fields, api
from odoo.exceptions import ValidationError
class Sale_order(models.Model):
    _inherit="sale.order"

    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('commercial', 'Commercial'),
    ], string='Property Type', required=True)    



    def action_cancel(self):
      res = super(Sale_order,self).action_cancel()
      for rec in self:
        rec.write({'property_type':'house'})
      return res
