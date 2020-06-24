from odoo import models, fields, api
import xlsxwriter
import os
import base64
import tempfile
from xlsxwriter.utility import xl_rowcol_to_cell
r = 0


class MarksMarks(models.TransientModel):
    _name = 'marks.marks'
    _description = 'Marks Wizard'

    mark_guj = fields.Float(string="Gujarati")
    mark_sci = fields.Float(string="Science")

    @api.multi
    def create_total_marks(self):
        for rec in self:
            print("======Method Call============")
            context = rec._context
            print("IDDD->>>>>>>>>", context)
            get_active_id = context.get('active_id')
            print("Active id->>>>>>>>>>>>>>>", get_active_id)
            record_set = rec.env['student.student'].browse(get_active_id)
            # record_set = rec.browse(get_active_id)
            print("========Record set->>>>>>", record_set)
            total = self.mark_guj + self.mark_sci
            record_set.write({'total_marks': total})
            # record_set.total_marks = 10
            # print("==>Result", res)
            # return True

    def create_exel_report(self):
        student_id = self.env['student.student'].search([])
        print("Student id->>>>>>>>", student_id)

        print("==========Call the Excel Function=========")
        attch_obj = self.env['ir.attachment']
        file_path = tempfile.NamedTemporaryFile().name
        workbook = xlsxwriter.Workbook(file_path + '.xlsx')
        worksheet = workbook.add_worksheet('Sheet 1')
        header = workbook.add_format({'font_size': 11,
                                      'font_name': 'Calibri',
                                      'align': 'center',
                                      'text_wrap': True,
                                      'bold': True})
        header.set_bg_color("#b0e9c0")
        header.set_font_color("green")
        header.set_align('center')
        header.set_align('vcenter')

        # workbook = xlsxwriter.Workbook('write_data.xlsx')
        # worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'First Name', header)
        worksheet.write('B1', 'Middle Name', header)
        worksheet.write('C1', 'Last Name', header)
        worksheet.write('D1', 'Mother Name', header)
        worksheet.write('E1', 'Std', header)
        for rec in student_id:
            worksheet.write('A2', rec.first_name)
            worksheet.write('B2', rec.middle_name)
            # worksheet.write('C2', rec.last_name)
            worksheet.write('D2', rec.mother_name)
            # worksheet.write('E2', rec.std_id)
            worksheet.write('F2', rec.dob)
        workbook.close()

        buf = base64.encodestring(open(file_path + '.xlsx', 'rb').read())
        try:
            if buf:
                os.remove(file_path + '.xlsx')
        except OSError:
            pass

        # attach_ids = attch_obj.search([('res_model', '=',
        #                                 'inventory.list.product_qty.wizard')])
        # if attach_ids:
        #     try:
        #         attach_ids.unlink()
        #     except:
        #         pass
        doc_id = attch_obj.create({'name': '%s.xlsx' % ('Student Information'),
                                   'datas': buf,
                                   # 'res_model': 'inventory.list.product_qty.'
                                   # 'wizard',
                                   'datas_fname': '%s.xlsx' % (
                                   'Student Information'),
                                   })
        return {'type': 'ir.actions.act_url',
                'url': 'web/content/%s?download=true' % (doc_id.id),
                'target': 'current',
                }
