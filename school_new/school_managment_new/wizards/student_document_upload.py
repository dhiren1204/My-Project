import base64
from odoo import models, fields, api


class StudentDocumentUpload(models.TransientModel):
    _name = 'document.upload'
    _description = 'Document Uplaod Wizard'

    document_id = fields.One2many('studentdoc.line', 'student_document_id')

    @api.multi
    def student_document_upload(self):
        for rec in self:
            context = self._context.get('active_id')
            student_id = self.env['student.student'].browse(context)
            print("Activeid->>>>>>>", context)
            datas = base64.b64decode(rec.document_id.document)
            attachment_vals = {
                'name': rec.document_id.documentname_id.name,
                'datas': datas,
                'datas_fname': rec.document_id.documentname_id.name + '.pdf',
                'res_model': 'student.student',
                'res_id': context,
            }
            # attachment_id = self.env['ir.attachment'].sudo().create(
            #     attachment_vals)

            # student_id.write({'student_doc': attachment_id})
            student_id.student_doc = [(0, 0, attachment_vals)]
