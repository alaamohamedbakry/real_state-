from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError

class Property(models.Model):
    _name = 'real_estate.property'
    _description = 'Real Estate Property'
    _order = 'name asc'
    
    # === CORE FIELDS ===
    name = fields.Char(string='Property Name', required=True, index=True)
    description = fields.Text(string='Description')
    agent_id = fields.Many2one('res.users', string='Agent', default=lambda self: self.env.user, index=True)
    
    # === FINANCIAL FIELDS ===
    price = fields.Float(string='Monthly Rent', required=True)
