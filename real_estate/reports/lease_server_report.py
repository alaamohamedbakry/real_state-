import io
import xlsxwriter
from odoo import http
from odoo.http import request, content_disposition
from ast import literal_eval

class RealEstateController(http.Controller):

    @http.route('/real_estate/lease/server_report', type='http', auth='user', methods=['GET', 'POST'], csrf=False)
    def lease_server_report(self, lease_ids, **kwargs):
        try:
            lease_obj = request.env['real_estate.lease'].sudo().browse(literal_eval(lease_ids))
        except Exception as e:
            return request.not_found()
        
        if not lease_obj or not lease_obj.exists():
            return request.not_found()
        
        # إنشاء ملف الإكسيل في الذاكرة
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Lease Details')
        
        header_format = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        title_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'left'})
        label_format = workbook.add_format({'bold': True, 'bg_color': '#F2F2F2', 'border': 1})
        data_format = workbook.add_format({'border': 1})
        currency_format = workbook.add_format({'num_format': '$#,##0.00', 'border': 1})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1})
        
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:E', 20)
        
        row = 0
        report_title = lease_obj[0].name if len(lease_obj) == 1 else "Multiple Leases Summary"
        worksheet.write(row, 0, f'Lease Report: {report_title}', title_format)
        row += 2
        
        for lease in lease_obj:
            worksheet.write(row, 0, f'LEASE: {lease.name or "New"}', header_format)
            worksheet.merge_range(row, 1, row, 4, '', header_format)
            row += 1
            
            lease_data = [
                ('Lease Name', lease.name or ''),
                ('Property Type', lease.property_id.name if lease.property_id else ''),
                ('Tenant', lease.tenant_id.name if lease.tenant_id else ''),
                ('Start Date', lease.start_date or ''),
                ('End Date', lease.end_date or ''),
                ('Monthly Rent', lease.monthly_rent or 0.0),
            ]
            
            for label, value in lease_data:
                worksheet.write(row, 0, label, label_format)
                if label == 'Monthly Rent':
                    worksheet.write(row, 1, value, currency_format)
                elif label in ['Start Date', 'End Date'] and value:
                    worksheet.write(row, 1, str(value), date_format)
                else:
                    worksheet.write(row, 1, str(value), data_format)
                row += 1
            
            row += 1 
            
            if lease.maintenance_ids:
                worksheet.write(row, 0, 'MAINTENANCE HISTORY', header_format)
                worksheet.merge_range(row, 1, row, 3, '', header_format)
                row += 1
                
                headers = ['Request Name', 'Description', 'Execution Date']
                for col, header in enumerate(headers):
                    worksheet.write(row, col, header, header_format)
                row += 1
                
                for maint in lease.maintenance_ids:
                    worksheet.write(row, 0, maint.name or '', data_format)
                    worksheet.write(row, 1, maint.description or '', data_format)
                    maint_date = getattr(maint, 'date_execution', '') or ''
                    worksheet.write(row, 2, str(maint_date), data_format)
                    row += 1
            
            row += 2  # مسافة فاصلة بين كل عقد والآخر في التقرير
        
        workbook.close()
        output.seek(0)
        
        filename = f'Lease_Server_Report.xlsx'
        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', content_disposition(filename))
            ]
        )