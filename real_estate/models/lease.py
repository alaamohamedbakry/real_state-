from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Lease(models.Model):
    _name = "real_estate.lease"
    _description = "Property Lease Agreement"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "start_date desc"

    # === CORE FIELDS ===
    name = fields.Char(
        string="Lease Reference", required=True, readonly=True, default="New"
    )
    note = fields.Text("Note")

    # === RELATIONSHIPS (Many2one) ===
    property_id = fields.Many2one(
        "real_estate.property",
        string="Property",
        required=True,
        ondelete="cascade",  # If property deleted, delete lease too
        index=True,
    )
    tenant_id = fields.Many2one(
        "real_estate.tenant",
        string="Tenant",
        required=True,
        ondelete="cascade",
        index=True,
    )

    # === LEASE TERMS ===
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    monthly_rent = fields.Float(string="Monthly Rent", required=True)
    deposit_paid = fields.Float(string="Deposit Paid")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )
    created_by = fields.Many2one("res.users", string="Created By", index=True)

    # === STATUS ===
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("at_risk", "At Risk"),
            ("expired", "Expired"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
    )

    # === COMPUTED FIELDS ===

    duration_months = fields.Integer(
        string="Duration (months)", compute="_compute_duration", store=True
    )
    # is_active = fields.Boolean(string = "Currency Active" , compute = '_compute_is_active')
    total_rent = fields.Float(
        string="Total Rent", compute="_compute_total_rent", store=True
    )

    def set_active(self):
        for rec in self:

            rec.write({"state": "active"})

    def set_draft(self):
        for rec in self:

            rec.write({"state": "draft"})

    def set_at_risk(self):
        if self.env.user.has_group("real_estate.group_property_manager"):
            for rec in self:
                rec.write({"state": "at_risk"})
        else:
            raise ValidationError("you don not have  access")

    def set_expired(self):
        for rec in self:

            rec.write({"state": "expired"})

    def get_property_data(self):

        for rec in self:
            rec.write(
                {
                    "note": str(rec.property_id.price)
                    + " "
                    + rec.tenant_id.name
                    + " "
                    + str(rec.tenant_id.phone)
                }
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "real_estate.lease"
                )

            return super().create(vals_list)

    def maintenance_request(self):
        for rec in self:
            print("maintenance")

    # #=== Computed Methods ===
    # @api.depends('start_date','end_date')
    # #=== calculate duration in months ===

    # def _compute_duration(self):

    #   for record in self:

    #     if record.start_date and record.end_date:
    #       delta = record.end_date - record.start_date
    #       record.duration_months = int(delta.days/30)

    #     else:
    #       record.duration_months = 0

    # @api.depends('start_date','end_date')
    # def _compute_is_active(self):
    #   today = fields.Date.today()
    #   # === Check lease is  currently active ===
    #   for record in self:
    #     if  record.start_date and record.end_date:
    #       record.is_active = record.start_date <= today <= record.end_date
    #       record.state = 'active'
    #     else:
    #       record.is_active = False

    # @api.depends('start_date','note')

    # def _compute_note(self):
    #    today = fields.Date.today()

    #    for record in self:
    #      if record.start_date:
    #         update =   record.start_date - today
    #         record.write({'note':update})
    #      else:
    #        record.note = False

    # @api.depends('duration_months','monthly_rent')

    # def _compute_total_rent(self):
    #   for rec in self:
    #     rec.total_rent = rec.monthly_rent * rec.duration_months

    # @api.constrains('start_date','end_date')

    # def date_validation(self):
    #   for dat in self:
    #     if dat.end_date < dat.start_date:
    #       raise ValidationError("the start date must be before end date")

    # @api.onchange('start_date', 'end_date')
    # def auto_date_correction(self):
    #   for rec in self:
    #     if rec.start_date and rec.end_date:
    #         if rec.end_date <= rec.start_date:
    #             rec.end_date = rec.start_date + timedelta(days=1)

    # @api.constrains('deposit_paid','monthly_rent')
    # def deposit_validate(self):
    #   for rec in self:
    #     if rec.deposit_paid <= 0:
    #       raise ValidationError("the deposit must be bigger than 0")
    #     if rec.deposit_paid != rec.monthly_rent:
    #       raise ValidationError("the deposit must be equal month rent")

    # @api.constrains('property_id')
    # def name_validation(self):
    #   for lead in self:
    #     if lead.property_id:

    #      valdiate = self.env['crm.lead'].search([
    #     ('name','=',lead.property_id.name)
    #     ])

    #      if valdiate:
    #        raise ValidationError(f"There is already a CRM Lead with the name '{lead.property_id.name}'")

    # @api.constrains('property_id')

    # def property_validation(self):
    #   if self.property_id and not self.property_id.available:
    #     raise ValidationError("Property id not available")

    # @api.constrains('property_id', 'tenant_id')
    # def check_tenant_validate(self):
    #  for lease in self:
    #     checking = self.search([
    #         ('property_id', '=', lease.property_id.id),
    #         ('tenant_id', '=', lease.tenant_id.id),
    #         ('id', '!=', lease.id),
    #     ])

    #     if checking:
    #         raise ValidationError(
    #             "This tenant already has a lease for this property."
    #         )
    # @api.constrains('tenant_id')
    # def check_tenant_phone(self):
    #    for rec in self:
    #      if not rec.tenant_id.phone:
    #        raise ValidationError("the tenant phone does not exist")

    # @api.constrains('property_id', 'start_date', 'end_date')
    # def _check_overlapping_leases(self):
    #     for lease in self:
    #         # Search for OTHER leases on the SAME property
    #         overlapping = self.search([
    #             ('property_id', '=', lease.property_id.id),
    #             ('id', '!=', lease.id),  # Exclude the current lease
    #             ('state', 'in', ['draft', 'active']),  # Only check active/draft leases
    #             ('start_date', '<=', lease.end_date),
    #             ('end_date', '>=', lease.start_date),
    #         ])
    #         print("overlapping:", overlapping)
    #         if overlapping:
    #             raise ValidationError(
    #                 f"Property '{lease.property_id.name}' is already leased from "
    #                 f"{overlapping[0].start_date} to {overlapping[0].end_date}. "
    #                 f"id is: {overlapping[0].id}"
    #                 f"Cannot create overlapping lease."
    #             )

    # @api.onchange('tenant_id')
    # def _onchange_property(self):
    #   properties = self.env['real_estate.property'].search([
    #       ('available', '=', True)
    #      ])

    #   return {
    #     'domain': {
    #         'property_id': [('id', 'in', properties.ids)]
    #     }
    #   }

    # def write(self,vals):
    #  if self.state not in 'draft':
    #    raise ValidationError("you can not change in this stage")
