
# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import xlsxwriter


class TeacherTeacher(models.Model):
    _name = 'teacher.teacher'
    _description = "Details Of Teacher"

    name = fields.Char(String="Teacher Name")
    dob = fields.Date(string="Date of Birth")
    age = fields.Char(string="Age", compute='_cal_age')
    salary = fields.Char(string="Salary")
    subject_id = fields.Many2many('subject.subject', string="Teaching Subject")
    Main_subject_id = fields.Many2one('subject.subject', string="Main Subject")
    experience = fields.Char(string="Experience")
    student_id = fields.Char(string="Student Name")

    @api.depends('dob')
    def _cal_age(self):
        for rec in self:
            if rec.dob:
                years = relativedelta(date.today(), rec.dob).years
                months = relativedelta(date.today(), rec.dob).months
                day = relativedelta(date.today(), rec.dob).days

                rec.age = str(int(years)) + ' Year/s ' + \
                    str(int(months)) + ' Month/s ' + str(day) + ' Day/s'

    def create_exel_report(self):
        print("==========Call the Excel Function=========")
        workbook = xlsxwriter.Workbook('write_data.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 1234)     # Writes an int
        worksheet.write(1, 0, 1234.56)  # Writes a float
        worksheet.write(2, 0, 'Hello')  # Writes a string
        worksheet.write(3, 0, None)     # Writes None
        worksheet.write(4, 0, True)     # Writes a bool

        workbook.close()


# def generate_xlsx_report(self, workbook)


# worksheet = workbook.add_worksheet('Sheet 1')
# header1 = workbook.add_format(
#     {'bold': True, 'font_name': 'Times New Roman',
#      'size': 14, 'align': 'center',
#      'font': 'height 180',
#      }
# )
# header1.set_fg_color('#808080')
