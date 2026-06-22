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

    maintenance_ids = fields.One2many('maintenance.request', 'lease_id', string='maintenance')

    # === LEASE TERMS ===
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    next_payment_date = fields.Date()
    monthly_rent = fields.Float(string="Monthly Rent", required=True)
    deposit_paid = fields.Float(string="Deposit Paid")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )
    created_by = fields.Many2one("res.users", string="Created By", index=True)
    last_reminder_sent = fields.Date(string="Last Reminder Sent", readonly=True)

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
    total_rent = fields.Float(
        string="Total Rent", compute="_compute_total_rent", store=True
    )

    def send_reminder_email(self, reminder_type="due_today"):
        """Send payment reminder based on type"""
        template_mapping = {
            "upcoming": "real_estate.email_template_payment_upcoming",
            "due_today": "real_estate.email_template_payment_due",
            "overdue_warning": "real_estate.email_template_payment_overdue",
        }

        template_xml_id = template_mapping.get(reminder_type)
        if not template_xml_id:
            return

        template = self.env.ref(template_xml_id, raise_if_not_found=False)
        if not template:
            return

        for lease in self:
            if not lease.tenant_id.email:
                lease.message_post(body="Could not send reminder: Tenant has no email.")
                continue
            template.send_mail(lease.id, force_send=True)

            reminder_label = reminder_type.replace("_", " ").capitalize()
            lease.message_post(
                body=f"Sent {reminder_label} reminder to {lease.tenant_id.email}"
            )
            lease.last_reminder_sent = fields.Date.today()

    def send_email_to_tenant(self):
        """Send payment reminder based on type"""
        template_xml_id = "real_estate.email_template_send_email_to_tenant"
        if not template_xml_id:
            return

        template = self.env.ref(template_xml_id, raise_if_not_found=False)
        if not template:
            return

        for lease in self:
            if not lease.tenant_id.email:
                lease.message_post(body="Could not send reminder: Tenant has no email.")
                continue
            template.send_mail(lease.id, force_send=True)
            lease.last_reminder_sent = fields.Date.today()

    def _cron_auto_expire_leases(self):
        """Scheduled action - expire leases whose end date has passed"""
        today = fields.Date.today()
        expired_leases = self.search([("end_date", "<", today)])
        for lease in expired_leases:
            lease.write({"state": "expired"})
            lease.send_email_to_tenant()

    def _cron_auto_create_leases_from_state_expired(self):
        """Scheduled action - expire leases whose end date has passed"""
        today = fields.Date.today()
        expired_leases = self.search([("end_date", "<", today), ("state", "=", "expired")])
        for lease in expired_leases:
            lease.create({
                "property_id": lease.property_id.id,
                "tenant_id": lease.tenant_id.id,
                "start_date": lease.start_date,
                "end_date": lease.end_date,
                "deposit_paid": lease.deposit_paid,
                "monthly_rent": lease.monthly_rent,
                "note": lease.note,
                "state": "active",
            })

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
            raise ValidationError("you do not have access")

    def set_expired(self):
        for rec in self:
            rec.write({"state": "expired"})

    def get_property_data(self):
        for rec in self:
            rec.write({
                "note": str(rec.property_id.price)
                + " "
                + rec.tenant_id.name
                + " "
                + str(rec.tenant_id.phone)
            })

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("real_estate.lease")
        return super().create(vals_list)

    def maintenance_request(self):
        for rec in self:
            print("maintenance")

    def action_export_excel(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/real_estate/lease/excel_export/{self.id}',
            'target': 'self',
        }

    def action_export_excel_server_action(self):
        active_ids = self.env.context.get("active_ids",  self.ids)
        return {
            'type': 'ir.actions.act_url',
            'url': f'/real_estate/lease/server_report?lease_ids={active_ids}',
            'target': 'new',
        }

    def action_print_lease_as_pdf(self):
        self.ensure_one()
        return self.env.ref('real_estate.action_report_lease_summary').report_action(self)