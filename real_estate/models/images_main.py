from odoo import models, fields, api

class Images_Maintenance(models.Model):
    _name = 'request.images'
    _description = 'Images Maintenance Request'


    name = fields.Char(string='Name')
    
    image = fields.Binary()
    
    request_id = fields.Many2one(
        'maintenance.request',
        string='Maintenance Request',
        ondelete='cascade'
    )