# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    skypee = fields.Char(string='Skypee')

    @api.model
    def default_get(self, fields):
        # print("========Default Get call above============")
        res = super(HrEmployee, self).default_get(fields)
        res['country_id'] = self.env.user.partner_id.country_id.id
        # print("========Default Get call============")
        return res

    @api.model
    def create(self, vals):
        res = super(HrEmployee, self).create(vals)
        print("self->>>>>>", self)
        print("create function working")
        return res


class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Details about the Student'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}
    _rec_name = 'first_name'
    _order = 'id desc'

    student_sequence = fields.Char(string="Student Order", required=True, copy=False,
                                   readonly=True, default=lambda self: ('New'))
    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True,
                                 string='Related Partner', help='Partner-related data of the user')

    first_name = fields.Char(string='First Name', required=True)
    middle_name = fields.Char(string='Middle Name', track_visibility='always')
    last_name = fields.Char(string='Last Name')
    mother_name = fields.Char(string='Mother Name', copy=True)
    # std = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
    #                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
    #                         ('9', '9'), ('10', '10'), ('11', '11'),
    #                         ('12', '12')], string="Standard")
    std_id = fields.Many2one('std.std', string="Std")
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        default='male', string='Gender')
    dob = fields.Date(string='Date of Birth', copy=False,
                      track_visibility='always')
    hobbies_ids = fields.Many2many('hobbies.hobbies', string="Hobbies")
    address = fields.Text(string='Address')
    country_id = fields.Many2one('res.country', string='Country',
                                 help="Apply only if delivery or invoicing country match.")
    uid = fields.Char(string='UID')
    adharcard_no = fields.Char(string='AdharCard No')
    image = fields.Binary(string='Image')
    rte = fields.Boolean(
        string='RTE')
    ph = fields.Boolean(string='Physical Handicap')
    uid = fields.Char(string='UID')
    mo = fields.Char(string='Mobile No')
    total_marks = fields.Float(string='Total Marks')
    department = fields.Selection([('primary', 'Primary'),
                                   ('secondary', 'Secondary'),
                                   ('highersecondary', 'HigherSecondary')],
                                  string='Department', onchange='_set_department')
    about_some = fields.Html(string='Something About Student')
    school_id = fields.Many2one('school.school', string="School Name")
    medium = fields.Char(string="Medium", onchange='_set_medium_principal')
    principal = fields.Char(
        string="Principal", onchange='_set_medium_principal')
    state = fields.Selection([('oraltest', 'OralTest'),
                              ('writtentest', 'Written Test'),
                              ('conform', 'Conform'), ('cancle', 'Cancle')],
                             string="Status", default="oraltest")
    hr_employee_name = fields.Many2one(
        'hr.employee', string="Hr Employee Name ")
    student_doc = fields.Many2many('ir.attachment', string="Student Document")
    avtive = fields.Boolean("Active", default=True)

    _sql_constraints = [
        ('firstname_middlename_check', 'check(first_name != middle_name)',
         'The First name and middle name are not same !'),
    ]
    # # This code working on compute field
    # api.depends('std')

    # def _set_department(self):
    #     for rec in self:
    #         if rec.std:
    #             if rec.std not in ('9', '10', '11', '12'):
    #                 rec.department = 'primary'
    #             elif rec.std in ('9', '10'):
    #                 rec.department = 'secondary'
    #             else:
    #                 rec.department = 'highersecondary'

    @api.model
    def default_get(self, fields):
        res = super(StudentStudent, self).default_get(fields)
        print("========Default Get call============")
        print("Self User->>>>>>>>>>>>>", self.env.user)
        print("SelfContext->>>>>>>>>>>", self._context)
        # print("country->>>>>>>>>>", self.country_id.id)
        res['country_id'] = self.env.user.partner_id.country_id.id
        res['school_id'] = 1
        res['about_some'] = 'Here Write the Student Unique Creativity'
        return res
    #  This code is woking on onchange

    @api.onchange('std')
    def _set_department(self):
        for rec in self:
            if rec.std:
                if rec.std not in ('9', '10', '11', '12'):
                    rec.department = 'primary'
                elif rec.std in ('9', '10'):
                    rec.department = 'secondary'
                else:
                    rec.department = 'highersecondary'

    @api.onchange('school_id')
    def _set_medium_principal(self):
        self.medium = self.school_id.sch_type
        self.principal = self.school_id.sch_principal

    @api.constrains('adharcard_no')
    def _check_adharcardno(self):
        for rec in self:
            if len(rec.adharcard_no) != 12:
                raise ValidationError(
                    ('Adharcard No must be Enter in 12 Digit'))

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = '[' + str(rec.id) + ']' + ' ' + \
                str(rec.first_name) + '  ' + str(rec.last_name)
            res.append((rec.id, name))
        return res

    @api.multi
    def set_to_oraltest(self):

        for rec in self:
            rec.write({'state': 'oraltest', })
            print("dhiren")
        return True

    @api.multi
    def set_to_writtentest(self):

        for rec in self:
            rec.write({'state': 'writtentest'})
            return True

    # @api.model
    # def create(self, vals):
    #     res = super(StudentStudent, self).create(vals)
    #     print("Result->>>>>>>>", res['first_name'])
    #     print("Result->>>>>>>>", res.first_name)
    #     res1 = self.env['res.partner'].create({'name': res['first_name']})
    #     print("Result->>>>>>>>", res1)
    #     return res1

    @api.model
    def create(self, vals):
        if vals.get('student_sequence', ('New')) == ('New'):
            vals['student_sequence'] = self.env['ir.sequence'].next_by_code(
                'student.student.sequence') or ('New')

        res = super(StudentStudent, self).create(vals)
        # partner_vals = {'name': vals.get('first_name')}
        # self.env['res.partner'].create(partner_vals)
        # print("Result->>>>>>>>>>>>>>>>>", res)
        return res

    @api.multi
    def write(self, vals):
        result = super(StudentStudent, self).write(vals)
        # print("Write Function Working")
        # print("result->>>>>>>>>>>>>>>>>", result)
        # print("values->>>>>>>>>>>>>>>>", vals)
        # print("Self->>>>>>>>>>>>>>>>", self)
        return result

    @api.multi
    def unlink(self):
        for res in self:
            if res.state in ('conform'):
                raise UserError(('You Can Not Delete Confirm Record'))
        result = super(StudentStudent, self).unlink()
        # print("Delete Function Working")
        # print("self->>>>>>>>>>", self)
        # print("Result->>>>>>>>>>>>", result)
        return result

    # @api.multi
    # def copy(self, default={'last_name': "Parmar"}):
    #     for res in self:
    #         if res.state in ('conform', 'cancel'):
    #             raise UserError(
    #                 'You can not copy data in confirm and cancle state')
    #     print("============copy call===========")
    #     print("default->>>>>>>>>>", default)
    #     result = super(StudentStudent, self).copy(default=default)
    #     print("Copy Function is Working")
    #     # print("self->>>>>>>>>>", self)
    #     # print("default->>>>>>>>>>", default)
    #     # Print("Result->>>>>>>>>>>>>", result)
    #     return result

    @api.multi
    def copy(self, default=None):
        for res in self:
            if res.state in ('conform', 'cancel'):
                raise UserError(
                    'You can not copy data in confirm and cancle state')
        print("============copy call===========")
        result = super(StudentStudent, self).copy(default=default)
        # print("context->>>>>>>>>>>>>>", self._context)
        print("Copy Function is Working")
        print("self->>>>>>>>>>", self)
        print("default->>>>>>>>>>", default)
        print("Result->>>>>>>>>>>>>", result)
        return result

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None):
    #     # print("===========search========")
    #     result = super(StudentStudent, self).search(
    #         [('address', '=', 'Ahmedabad')])
    #     # print("self->>>>>>>>>>", self)
    #     # print("args->>>>>>>>>>", args)
    #     # print("offset->>>>>>>>>>", offset)
    #     # print("limit->>>>>>>>>>", limit)
    #     print("result->>>>>>>", result)
    #     return result

    @api.multi
    def check_address(self):
        for res in self:
            if res.address:
                print("")
                result = self.env['student.student'].search(
                    [('address', '=', 'Ahmedabad')])
                print("Result->>>>>>>>>", result)
        return result
