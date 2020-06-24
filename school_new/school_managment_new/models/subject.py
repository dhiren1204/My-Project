# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class SubjectSubject(models.Model):
    _name = 'subject.subject'
    _description = "Details of Subject"
    _rec_name = "subject"

    subject = fields.Char(string="Subject Name")
    max_mark = fields.Float(string="Maximum Marks")
