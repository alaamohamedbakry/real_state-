import io
import xlsxwriter
from odoo import http
from odoo.http import request, content_disposition

class RealEstateController(http.Controller):
    
    @http.route('/real_estate/lease/excel_export/<int:lease_id>', type='http', auth='user')
    def property_excel_export(self, lease_id, **kwargs):
        """
        Export single property details to Excel
        """
        lease_obj = request.env['real_estate.lease'].browse(lease_id)
        
        if not lease_obj.exists():
            return request.not_found()
        
        # Create Excel file in memory
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Add worksheet
        worksheet = workbook.add_worksheet('Lease Details')
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': "#012A70",
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'left'
        })
        
        label_format = workbook.add_format({
            'bold': True,
            'bg_color': '#F2F2F2',
            'border': 1
        })
        
        data_format = workbook.add_format({
            'border': 1
        })
        
        currency_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'border': 1
        })
        
        date_format = workbook.add_format({
            'num_format': 'yyyy-mm-dd',
            'border': 1
        })
        
        # Set column widths
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:E', 15)
        
        # Title
        row = 0
        col = 0
        worksheet.merge_range(0,0,0,1,  f'Lease Report: {lease_obj.name}', title_format)
        row += 2
        
        # Basic Information Section
        worksheet.merge_range(row, 0, row, 1, 'BASIC INFORMATION', header_format)
        row += 1
        
        lease_data = [
            ('Property Name', lease_obj.property_id.name),
            ('Tenant Name',lease_obj.tenant_id.name ),
         
          
        ]
        
        for label, value in lease_data:
            worksheet.write(row, 0, label, label_format)
            # if isinstance(value, (int, float)) and not isinstance(value, bool):
            worksheet.write(row, 1, value, data_format)
            # else:
            #     worksheet.write(row, 1, str(value) if value else '', data_format)
            row += 1
        
        row += 1
        
        # Pricing Section
        worksheet.merge_range(row, 0, row, 1, 'Dates & Time', header_format)
        row += 1
        
        worksheet.write(row, 0, 'Start Date', label_format)
        worksheet.write(row, 1, lease_obj.start_date, date_format)
        row += 1
        
        worksheet.write(row, 0, 'End Date', label_format)
        worksheet.write(row, 1, lease_obj.end_date, date_format)
        row += 1

       
        
        row += 2
        
        # Leases Table
        if lease_obj.maintenance_ids:
            worksheet.merge_range(row, 0, row, 2, 'Maintenance HISTORY', header_format)
            row += 1
            
            # Table headers
            headers = ['issue_type', 'urgency', 'assigned_to']
            for col, header in enumerate(headers):
                worksheet.write(row, col, header, header_format)
            row += 1
            
            # Table data
            for maintenance in lease_obj.maintenance_ids:
                worksheet.write(row, 0, maintenance.issue_type, data_format)
                worksheet.write(row, 1, maintenance.urgency, data_format)
                worksheet.write(row, 2,maintenance.assigned_to.name, data_format)
              
                row += 1
        
        # Close workbook
        workbook.close()
        
        # Prepare response
        output.seek(0)
        filename = f'lease_{lease_obj.name.replace(" ", "_")}.xlsx'
        
        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', content_disposition(filename))
            ]
        )