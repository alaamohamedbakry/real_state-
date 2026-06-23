# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': "Real Estate Workflow",
    'description': """
Long description of module's purpose
    """,

    'author': "Alaa mohamed",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','sale'],

    # always loaded
    'data': [
       'security/property_security.xml',
       'security/maintenance_security.xml',
       'security/ir.model.access.csv',
        'data/name_sequence.xml',
        'data/mail_template_data.xml',
        'data/demo.xml',
        'views/menu.xml',
        'wizard/maintenance.xml',
        'wizard/lease.xml',
        'wizard/payment_request.xml',
        'wizard/payment_tenant.xml',
        'views/crm_lead_view.xml',
        'views/sale_order_view.xml',
        'views/lease_payment.xml',
        'views/property_views.xml',
        'views/tenant_views.xml',
        'views/lease_views.xml',
        'views/maintenance_views.xml',
        'views/portal_templates.xml',
        'views/views.xml',
        'views/templates.xml',
        'reports/lease_report_templates.xml',
        'reports/property_report_templates.xml',

        
        
        

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
   
}

