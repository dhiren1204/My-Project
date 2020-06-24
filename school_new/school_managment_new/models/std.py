# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import date, datetime


class StdStd(models.Model):
    _name = 'std.std'
    _description = 'Student Standard'
    _rec_name = "std"

    std = fields.Char(string="Std")
    line_ids = fields.One2many('stdsubject.line', 'stddsubject_line_id')

    @api.multi
    @api.constrains('line_ids')
    def _check_unique_subject(self):
        for subject in self:
            exist_subject_list = []
            for eachline in subject.line_ids:
                if eachline.sub_id.id in exist_subject_list:
                    raise ValidationError(('Subject should be one per line.'))
                exist_subject_list.append(eachline.sub_id.id)

    @api.constrains('line_ids')
    def _check_negative_maximummarks(self):
        for maxmarks in self:
            for eachline in maxmarks.line_ids:
                if eachline.max_marks < 0:
                    raise ValidationError(('Please Enter Proper Marks'))


class StdSubjectLine(models.Model):
    _name = 'stdsubject.line'
    _description = 'Std Details Line'

    sub_id = fields.Many2one('subject.subject', String="Subject")
    max_marks = fields.Float(string="Maximum Mark")
    stddsubject_line_id = fields.Many2one('std.std')
