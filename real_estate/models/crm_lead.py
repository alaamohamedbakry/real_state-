from odoo import models, fields, api
from odoo.exceptions import ValidationError
class CrmLead(models.Model):
    _inherit="crm.lead"
    tenant_created = fields.Boolean('tenant_created')
    created_from_api = fields.Boolean(default=False)

    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('commercial', 'Commercial'),
    ], string='Property Type', required=True)    

    def toggle_active(self):
        res = super(CrmLead, self).toggle_active()
        for rec in self:
            rec.write({'description': 'restored'})
        return res    
    

    def create_tenant(self):
     for lead in self:
        
        self.env['real_estate.tenant'].create({
            'name': lead.name,
            'email': lead.email_from,
            'property_type':lead.property_type
        })

        lead.tenant_created = True



    def _cron_auto_create_tenant(self):
     leads = self.search([('email_from','!=',False),('property_type','!=',False),('tenant_created','!=',True)])
     leads.create_tenant()
        
       


            

   
 