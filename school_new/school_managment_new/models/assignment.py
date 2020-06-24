# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import xlsxwriter


class AssignmentType(models.Model):
    _name = 'assignment.type'
    _description = "Assignment Type Details"

    name = fields.Char(string="Name")
    assignment_code = fields.Char(string="Code")


class AssignmentDetails(models.Model):
    _name = 'assignment.details'
    _description = "Assignment Details"

    name = fields.Char(string="Assignment Name")
    std_id = fields.Many2one('std.std', string="Std")
    sub_id = fields.Many2one('subject.subject', string="Subject")
    assignmenttype_id = fields.Many2one(
        'assignment.type', string="Assignment Type")
    teacher_id = fields.Many2one('teacher.teacher', string="Faculty")
    issued_date = fields.Datetime(
        string="Issued Date", default=datetime.today())
    submission_date = fields.Datetime(string="Submission Date")
    assignment_marks = fields.Float(string="Marks")
    description = fields.Html(string="Description")

    @api.onchange('std_id')
    def _set_stdwise_subject(self):
        for record in self:
            # result = self.env['std.std'].search(
            #     [('std', '=', record.std_id.id)])
            # subject_line = result.line_ids
            # print("Subject Line->>>>>.", subject_line)

            result = record.std_id.line_ids.mapped('sub_id')
            print("result->>>>>>>>>>", result)
            # subject_list = result.mapped('sub_id')
            # print("Subject ID->>>>>>>>>", subject_list)
            return {'domain': {'sub_id': [('id', 'in', result.ids)]}}
