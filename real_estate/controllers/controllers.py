from odoo import http
from odoo.http import request
from werkzeug.urls import url_quote
from odoo.addons.portal.controllers.portal import CustomerPortal


class RealEstatePortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(RealEstatePortal, self)._prepare_portal_layout_values()
        # tenant = request.env['real_estate.tenant'].sudo().search([
        #     ('user_id', '=', request.env.user.id),
        # ], limit=1)
        properties = (
            request.env["real_estate.property"]
            .sudo()
            .search(
                [
                    ("agent_id", "=", request.env.user.id),
                ]
            )
        )
        payments = (
            request.env["lease.payment"]
            .sudo()
            .search([("tenant_id.user_id", "=", request.env.user.id)])
        )
        # lease_count = 0
        # if tenant:
        #     lease_count = request.env['real_estate.lease'].sudo().search_count([
        #         ('tenant_id', '=', tenant.id)
        #     ])
        properties_count = (
            request.env["real_estate.property"]
            .sudo()
            .search_count([("agent_id", "=", request.env.user.id)])
        )
        values.update(
            {
                # 'lease_count': lease_count,
                # 'tenant': tenant,
                "properties": properties,
                "properties_count": properties_count,
                "payments": payments,
            }
        )
        return values

    @http.route(
        ["/my/leases", "/my/leases/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_leases(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        tenant = values.get("tenant")
        if not tenant:
            values.update(
                {
                    "leases": request.env["real_estate.lease"].sudo().browse(),
                }
            )
            return request.render("real_estate.portal_my_leases", values)

        leases = (
            request.env["real_estate.lease"]
            .sudo()
            .search([("tenant_id", "=", tenant.id)], order="start_date desc")
        )
        values.update(
            {
                "leases": leases,
            }
        )
        return request.render("real_estate.portal_my_leases", values)

    @http.route(
        ["/my/properties", "/my/properties/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_properties(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        properties = values.get("properties")
        if not properties:
            values.update(
                {
                    "properties": request.env["real_estate.property"].sudo().browse(),
                }
            )
            return request.render("real_estate.portal_my_properties", values)

        properties = (
            request.env["real_estate.property"]
            .sudo()
            .search([("agent_id", "=", request.env.user.id)])
        )
        values.update(
            {
                "properties": properties,
            }
        )
        return request.render("real_estate.portal_my_properties", values)

    @http.route(
        ["/my/payments", "/my/payments/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_payments(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        payments = values.get("payments")
        if not payments:
            values.update(
                {
                    "payments": request.env["lease.payment"].sudo().browse(),
                }
            )
            return request.render("real_estate.portal_my_payments", values)

        payments = (
            request.env["lease.payment"]
            .sudo()
            .search([("tenant_id.user_id", "=", request.env.user.id)])
        )
        values.update(
            {
                "payments": payments,
            }
        )
        return request.render("real_estate.portal_my_payments", values)

    @http.route(['/my/property/<int:property_id>'], type='http',auth='user', website=True) 
    def show_properties_details(self, property_id):

      property_details = request.env['real_estate.property'].sudo().browse(property_id)

      if not property_details.exists():
        return request.not_found()

      lease = request.env['real_estate.lease'].sudo().search([
        ('property_id', '=', property_details.id),
        ('tenant_id.user_id', '=', request.env.user.id)
      ], limit=1)

      if not lease:
        return request.not_found()

      return request.render('real_estate.property_details_template', {
         'property': property_details, 
         'lease': lease 
         })