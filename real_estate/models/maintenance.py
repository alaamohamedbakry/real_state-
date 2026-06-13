from odoo import models, fields, api

class MaintenanceRequest(models.Model):
    _name = 'maintenance.request'
    _description = 'Property Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    
    name = fields.Char(string='REFNO',default='MAIN',required=True, readonly=True)
    property_id = fields.Many2one(related='lease_id.property_id', store=True)
    lease_id = fields.Many2one('real_estate.lease')
    tenant_id = fields.Many2one(related='lease_id.tenant_id', store=True)
    images_ids = fields.One2many('request.images', 'request_id', string='images')

    
    issue_type = fields.Selection([
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('air_condition', 'Air Condition'),
        ('appliance', 'Appliance'),
        ('other', 'Other')
    ], required=True)
    description = fields.Text(required=True, tracking=True)
    urgency = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency')
    ], default='medium', required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)
    
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    scheduled_date = fields.Date(tracking=True)
    completion_date = fields.Date()
    actual_cost = fields.Float(tracking=True)
    preferred_date = fields.Date(string='Preferred Maintenance Date')
    tenant_phone = fields.Char(string='Tenant Contact Phone')


    
    @api.model_create_multi
    def create(self, vals_list):
     for vals in vals_list:
        if vals.get('name', 'MAIN') == 'MAIN':
            vals['name'] = self.env['ir.sequence'].next_by_code('real_estate.maintenance')

        return super().create(vals_list)
     

