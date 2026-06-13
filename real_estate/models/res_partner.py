from odoo import models, fields, api

class Contact(models.Model):
    _inherit = "res.partner"

    Agency = fields.Char(string='Agency Type')
    license_number =  fields.Char('license Number')
    