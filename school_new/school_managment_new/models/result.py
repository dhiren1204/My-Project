# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import xlsxwriter


class ResultResult(models.Model):
    _name = 'result.result'
    _description = 'Student Result Details'
    _rec_name = 'student_id'

    student_id = fields.Many2one('student.student', string="Student Name")
    student_std_id = fields.Many2one('std.std', string="Std")
    mark_line_ids = fields.One2many('result.line', 'result_line_id')
    total_marks = fields.Float(
        string="Total Maximum Marks", compute='_cal_total')
    total_received_marks = fields.Float(
        string="Total Received Marks", compute='_cal_total')
    percentage = fields.Float(string="Percentage", compute='_cal_total')

    @api.onchange('student_id')
    def _set_std(self):
        self.student_std_id = self.student_id.std_id.id

    def auto_fill_subject(self):
        print("Auto fill Function Call")
        std = self.student_std_id
        print("Std->>>>>>>>>>>>", std)
        self.mark_line_ids = False
        a = []
        for line in std.line_ids:
            a.append((0, 0, {'sub_id': line.sub_id.id,
                             'max_marks': line.max_marks,
                             }))
        self.mark_line_ids = a

    # @api.onchange('student_std_id')
    # def _set_stdwisesubject_line(self):
    #     std = self.student_std_id
    #     print("Std->>>>>>>>>>>>", std)
    #     self.mark_line_ids = False
    #     a = []
    #     for line in std.line_ids:
    #         a.append((0, 0, {'sub_id': line.sub_id.id,
    #                          'max_marks': line.max_marks,
    #                          }))
    #     self.mark_line_ids = a
        # print("A->>>>>>>>>>>>>>>>>>>>>", a)

    @api.depends('mark_line_ids')
    def _cal_total(self):
        # using simple code
        for rec in self:
            total_marks = 0
            total_received_marks = 0

            for each_line in rec.mark_line_ids:
                total_marks += each_line.max_marks
                total_received_marks += each_line.rec_marks
            rec.total_marks = total_marks
            rec.total_received_marks = total_received_marks
            if total_marks != 0:
                rec.percentage = (total_received_marks * 100) / total_marks

        # using in Line Code
        # self.total_marks = sum(
        #     each_line.max_marks for each_line in self.mark_line_ids)
        # self.total_received_marks = sum(
        #     each_line.rec_marks for each_line in self.mark_line_ids)
        # self.percentage = (self.total_received_marks *
        #                    100) / self.total_marks
    @api.multi
    def create_result(self):
        return self.env.ref('school_managment_new.student_result').report_action(self)


class ResultLine(models.Model):
    _name = 'result.line'
    _description = "Result Line Details"

    sub_id = fields.Many2one('subject.subject', string="Subject")
    max_marks = fields.Float(string="Maximum Mark")
    rec_marks = fields.Float(string="Received Mark")
    result_line_id = fields.Many2one('result.result')

    @api.multi
    @api.constrains('rec_marks')
    def _check_receivedmarks(self):
        for rec in self:
            if rec.rec_marks > rec.max_marks:
                raise ValidationError(
                    ('Please Enter Valid Marks'))
