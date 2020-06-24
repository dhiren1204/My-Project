from odoo import models, fields, api


class CreateAdobeStudent(models.TransientModel):
    _name = 'create.adobestudent'
    _description = 'Adobe Student Wizard'
    student_id = fields.Many2one('student.student', string="Student Name")

    @api.multi
    def create_adobe_student(self):
        print("=======Method Call============")
        context = self._context
        print("IDDD->>>>>>>>>", context)
        active_id = context.get('active_ids')
        print("Active id->>>>>>>>", active_id)
        recordset = self.env['teacher.teacher'].browse(active_id)
        print("Record set->>>>>>>>>>>>>", recordset)
        # recordset.student_id = 10
        recordset.write({'student_id': self.student_id.first_name})
