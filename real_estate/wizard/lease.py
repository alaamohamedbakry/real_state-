from odoo import models, fields, api
from odoo.exceptions import ValidationError



class LeaseRequestWizard(models.TransientModel):
    _name = "lease.request.wizard"
    _description = "Lease Request Wizard"

    lease_id = fields.Many2one("real_estate.lease", string="Lease", required=True)
    property_id = fields.Many2one(
        "real_estate.property", related="lease_id.property_id", readonly=True
    )
    tenant_id = fields.Many2one(
        "real_estate.tenant", related="lease_id.tenant_id", readonly=True
    )
    new_start_date = fields.Date(
        string="Start Date", required=True, default=fields.Date.today
    )
    new_end_date = fields.Date(string="End Date", required=True)
    deposit_paid = fields.Float(string="Deposit Paid",related='lease_id.deposit_paid')
    note = fields.Text("Note")
    monthly_rent = fields.Float(string='Monthly Rent', related='lease_id.monthly_rent')


    def action_review_lease(self):

        self.ensure_one()
        lease_request =  self.lease_id.state = 'expired'

        lease_request = self.env["real_estate.lease"].create(
            {
                'property_id': self.property_id.id,
                'tenant_id': self.tenant_id.id,
                'start_date': self.new_start_date,
                'end_date': self.new_end_date,
                'deposit_paid': self.deposit_paid,
                'monthly_rent':self.monthly_rent,
                'note': self.note,
                'state': 'active'
            }
        )


    @api.constrains('new_start_date')
    def _check_start_date(self):
        for record in self:
            if record.new_start_date < fields.Date.today():
                raise ValidationError("start date cannot be before today")
            
    
