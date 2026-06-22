from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import re


class Tenant(models.Model):
    _name = "real_estate.tenant"
    _description = "Real Estate Tenant"
    _order = "name asc"

    # === CORE FIELDS ===
    name = fields.Char(string=" Name", required=True)
    email = fields.Char(string="Email", required=True, index=True)
    phone = fields.Char(string="Phone Number")
    mobile = fields.Char(string="Mobile Number")
    city = fields.Char(string="City")
    user_id = fields.Many2one("res.users", string="Related User", index=True)

    # === DATES ===
    date_joined = fields.Date(
        string="Date Joined", default=fields.Date.today, readonly=True
    )
    date_of_birth = fields.Date(string="Date of Birth")

    # === ADDITIONAL INFO ===
    notes = fields.Text(string="Notes")
    active = fields.Boolean(string="Active", default=True)
    property_type = fields.Selection(
        [
            ("apartment", "Apartment"),
            ("house", "House"),
            ("villa", "Villa"),
            ("commercial", "Commercial"),
        ],
        string="Property Type",
        required=True,
    )

    lease_ids = fields.One2many("real_estate.lease", "tenant_id", string="Leases1")

    created_from_api = fields.Boolean(default=False, readonly=True)

    # def write(self, vals):
    #        if not self.env.user.has_group('real_estate.group_tenant_manager'):
    #         raise ValidationError("you do not have access")
    #        return  super().write(vals)

    # def write(self, values):

    #     if self.env.user.id != self.user_id.id and not self.env.user.has_group(
    #         "real_estate.group_tenant_manager"
    #     ):
    #         raise ValidationError("you do not have access")
    #     return super().write(values)

    def unlink(self):
        if not self.env.user.has_group("real_estate.group_tenant_manager") and self.created_from_api:
         
         raise ValidationError("you can not delete that")
        return super().unlink()
    
    def copy(self, default=None):
        if not self.env.user.has_group("real_estate.group_tenant_manager"):
            raise ValidationError("you can not duplicate it")
        
        return self.copy(default)

