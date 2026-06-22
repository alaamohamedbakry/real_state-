from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class LeasePayment(models.Model):
    _name = 'lease.payment'
    _description = 'Lease Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'due_date desc, id desc'
    
    name = fields.Char(string='Payment Reference', required=True, copy=False, readonly=True, default='New')
    lease_id = fields.Many2one('real_estate.lease', string='Lease', required=True, ondelete='cascade')
    tenant_id = fields.Many2one(related='lease_id.tenant_id', string='Tenant', store=True)
    property_id = fields.Many2one(related='lease_id.property_id', string='Property', store=True)
    
    due_date = fields.Date(string='Due Date', required=True, tracking=True)
    amount = fields.Float(string='Amount Due', required=True, tracking=True)
    late_fee = fields.Float(string='Late Fee', tracking=True)
    late_fee_applied = fields.Boolean(string='Late Fee Applied', default=False)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    user_id = fields.Many2one('res.users',string="Created by",default= lambda self: self.env.user.id)
    
    payment_date = fields.Date(string='Payment Date', tracking=True)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('other', 'Other')
    ], string='Payment Method')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('reconciled', 'Reconciled')
    ], default='draft', required=True, tracking=True)
    
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
        
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('lease.payment') or "New"   
                
        return super().create(vals_list)   

    def confirm_payment(self):
        for rec in self:
            if not rec.payment_date:
                raise UserError("You must set a payment date before confirming the payment.")
                     
            rec.state = 'paid'         

    
    @api.depends('amount','late_fee','late_fee_applied')
    def _compute_total_amount(self):
        
        for rec in self:
            if rec.late_fee_applied:
                rec.total_amount = rec.amount + rec.late_fee
            else:
                rec.total_amount = rec.amount