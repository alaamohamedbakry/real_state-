from odoo import models, fields, api


class PaymentTenant(models.TransientModel):
    _name = 'payment.tenant.wizard'
    _description = 'Payment Tenant Wizard'


    lease_id = fields.Many2one('real_estate.lease', string="Lease")
    tenant_id = fields.Many2one('real_estate.tenant', string="Tenant")


    def change_tenant(self):
        
        self.ensure_one()
        self.lease_id.write({'tenant_id':self.tenant_id.id})

        