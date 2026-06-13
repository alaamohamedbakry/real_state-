from odoo import models, fields, api

class PaymentRequestWizard(models.TransientModel):
    _name = 'payment.request.wizard'
    _description = 'Payment Request Wizard'

   
    
    tenant_id = fields.Many2one(related='lease_id.tenant_id', string='Tenant', store=True)
    property_id = fields.Many2one(related='lease_id.property_id', string='Property', store=True)
    lease_id = fields.Many2one('real_estate.lease', string='Lease', required=True, ondelete='cascade')
    
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

    def submit_payment_request(self):
       
        self.ensure_one()
        
       
        payment_request = self.env['lease.payment'].create({
            'property_id': self.property_id.id,
            'lease_id': self.lease_id.id,
            'tenant_id': self.tenant_id.id,
            'amount' : self.amount,
            'payment_date': self.payment_date,
            'due_date' : self.due_date,
            'payment_method': self.payment_method,
            'user_id': self.user_id.id,
            'late_fee': self.late_fee,
            'late_fee_applied': self.late_fee_applied,
            'total_amount': self.total_amount,
            
            'state': 'draft',
        })

    @api.depends('amount','late_fee','late_fee_applied')
    def _compute_total_amount(self):
        
        for rec in self:
            if rec.late_fee_applied:
                rec.total_amount = rec.amount + rec.late_fee
            else:
                rec.total_amount = rec.amount