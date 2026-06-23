from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError


class Property(models.Model):
    _name = "real_estate.property"
    _description = "Real Estate Property"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name asc"

    # === CORE FIELDS ===
    name = fields.Char(string="Property Name", required=True, index=True)
    description = fields.Text(string="Description")
    agent_id = fields.Many2one(
        "res.users", string="Agent", default=lambda self: self.env.user, index=True
    )
    image_property = fields.Image("Image Property", max_width=1970, max_height=1970)
    total_amount = fields.Float(string="Total Amount")

    # === FINANCIAL FIELDS ===
    price = fields.Float(string="Monthly Rent", required=True)
    deposit_required = fields.Float(string="Sequrity Deposit")
    created_date = fields.Date(
        string="Created Date", default=fields.Date.today, readonly=True
    )

    # ===  Property Details ===

    bed_rooms = fields.Integer("Bedrooms")
    bath_rooms = fields.Integer("Bathrooms")
    floor = fields.Integer("Floor")
    address = fields.Char(string="Address")
    city = fields.Char(string="City")
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
    available = fields.Boolean("Available", default=True, index=True)
    created_from_api = fields.Boolean(default=False, readonly=True)

    lease_ids = fields.One2many("real_estate.lease", "property_id", string="Leases")

    lead_id = fields.Many2one("crm.lead", string="lead_id")
    lease_count = fields.Integer(compute="_compute_lease_count")

    def notify_agent_if_state_available(self):
        """Send payment reminder based on type"""
        template_xml_id = "real_estate.email_template_send_notify"
        if not template_xml_id:
            return

        template = self.env.ref(template_xml_id, raise_if_not_found=False)
        if not template:
            return

        for property in self:
            if not property.agent_id.email:
                property.message_post(
                    body="Could not send reminder: Agent has no email."
                )
                continue
            if not property.available:
                property.message_post(
                    body="Could not send reminder:Property is Not Available."
                )
            #     continue
            # Send the email
            template.send_mail(property.id, force_send=True)

    def mark_as_available(self):
        """mark property as available"""
        for rec in self:
            rec.write({"available": True, "price": 0})

    def mark_as_unavailable(self):
        """mark property as unavailable"""
        for rec in self:
            rec.write({"available": False})

    def make_default_price(self):
        for rec in self:
            rec.write({"price": 3000})

    def add_price(self):
        for rec in self:
            if rec.available == False:
                rec.write({"price": rec.price + 1000})

    def get_available_properties(self):
        #  avilable_pro = self.search([('available','=',True)])
        #  for pro in avilable_pro :
        #      print(pro.name)
        avilable_property = self.env["crm.lead"].search(
            [("expected_revenue", ">", 1000)]
        )
        print(avilable_property.mapped("name"))

    def action_export_excel(self):
        return {
            "type": "ir.actions.act_url",
            "url": f"/real_estate/property/excel_export/{self.id}",
            "target": "self",
        }

    def action_print_property_summary(self):
        self.ensure_one()
        return self.env.ref("real_estate.action_report_property_summary").report_action(
            self
        )

    def action_view_leases(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id(
            "real_estate.action_lease"
        )

        if len(self.lease_ids) > 1:
            action["domain"] = [("id", "in", self.lease_ids.ids)]

        elif len(self.lease_ids) == 1:
            action["views"] = [
                (self.env.ref("real_estate.real_estate_view_form").id, "form")
            ]
            action["res_id"] = self.lease_ids.id

        else:
            action = {"type": "ir.actions.act_window_close"}

        return action

    # def write(self, values):

    #     if not self.env.user.has_group('real_estate.group_property_manager'):
    #         raise ValidationError("you do not have access")
    #     values['available'] = True
    #     result = super(Property, self).write(values)

    #     return result

    # def get_data_for_desc(self):
    #    avilable_property = self.env['crm.lead'].search(['|',
    #        ('expected_revenue','>',1000),
    #        ('email_from','!=',False)
    #        ])
    #    res = (avilable_property.mapped('name'))

    #    self.write({'description':res})

    # def get_won_for_desc(self):
    #    won_available = self.env['crm.lead'].search([
    #        ('stage_id.id','=',4)
    #     ])
    #    res = (won_available.mapped('name'))

    #    self.write({'description':res})

    def get_customer_data(self):
        customer_data = self.env["crm.lead"].search([("partner_id.email", "!=", False)])

        self.write({"description": customer_data.mapped("user_id.name")})

    def _compute_lease_count(self):
        for rec in self:
            rec.lease_count = self.env["real_estate.lease"].search_count(
                [("property_id", "=", rec.id)]
            )
