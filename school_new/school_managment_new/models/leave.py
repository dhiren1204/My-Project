# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import date, datetime


class LeaveLeave(models.Model):
    _name = 'leave.leave'
    _description = "Leave Details"

    name = fields.Char(string="Leave")


class LeaveConformLine(models.Model):
    _name = 'leaveconform.line'
    _description = "Leave Conformation Details"

    leave_id = fields.Many2one('leave.leave', string="Leave Name")
    days = fields.Char(string="No of Days")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(String="To date")
    leave_conform_id = fields.Many2one('teacher.leave')


class TeacherLeave(models.Model):
    _name = 'teacher.leave'
    _description = 'Teachers Leave Details'
    _rec_name = 'teacher_id'

    teacher_id = fields.Many2one('teacher.teacher', string="Teacher Name")
    date = fields.Date(string="Date")
    line_ids = fields.One2many('leaveconform.line', 'leave_conform_id')
