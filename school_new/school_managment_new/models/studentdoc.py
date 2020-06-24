# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import date, datetime


class StudentDoc(models.TransientModel):
    _name = 'student.doc'
    _description = 'student Document Name'

    name = fields.Char(string="Document Name")


class StudentdocLine(models.TransientModel):
    _name = 'studentdoc.line'
    _description = 'Student Document Details'

    documentname_id = fields.Many2one('student.doc', string="Document Name")
    document = fields.Binary(string='Document')
    student_document_id = fields.Many2one('document.upload')
