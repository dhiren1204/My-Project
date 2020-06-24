# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import xlsxwriter


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


class HobbiesHobbies(models.Model):
    _name = 'hobbies.hobbies'
    _description = "Details of Hobbies"

    name = fields.Char(string="Hobbies")


class SubjectSubject(models.Model):
    _name = 'subject.subject'
    _description = "Details of Subject"
    _rec_name = "subject"

    subject = fields.Char(string="Subject Name")
    max_mark = fields.Float(string="Maximum Marks")


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


class SchoolSchool(models.Model):
    _name = 'school.school'
    _description = 'School Basic Details'
    _rec_name = 'sch_name'
    _sql_constraints = [
        ('email_uniq', 'unique (sch_email)', 'The Email Must be unique !'),
    ]

    sch_name = fields.Char(string="School Name")
    sch_address = fields.Char(string="School Address")
    sch_email = fields.Char(string="Email")
    sch_Ph = fields.Char(string="Phone")
    sch_website = fields.Char(string="Website")
    sch_type = fields.Char(string="School Type")
    sch_principal = fields.Char(string="Principal Name")

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        # print('========call name search============')
        result = super(SchoolSchool, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        # print("self->>>>>>>>>>>>>>", self)
        # print("name->>>>>>>>>>>>>>>>", name)
        # print("args->>>>>>>>>>>>>>>", args)
        # print("Operator->>>>>>>>>>>>>>", operator)
        # print("Limit->>>>>>>>>>>>>>>>", limit)
        # print("Search Function is Working", result)
        return result


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


class FeesStructure(models.Model):
    _name = 'fees.structure'
    _description = 'Std wise Fees'

    std_id = fields.Many2one('std.std', string="Std")
    fees = fields.Char(string="Fees")


class FeesCollection(models.Model):
    _name = 'fees.collection'
    _description = 'Fees Collection OF Student'
    _rec_name = "student_id"
    student_id = fields.Many2one('student.student', string="Student Name")
    std = fields.Char(string="Std", onchange='_set_std_fees')
    student_fees = fields.Float(string="Fees")
    sale_count = fields.Integer(
        string="Sale Count", compute='sale_order_count')

    def sale_order_count(self):
        count = self.env['sale.order'].search_count(
            [('partner_id', '=', self.id)])
        self.sale_count = count

    @api.onchange('student_id')
    def _set_std_fees(self):
        self.std = self.student_id.std_id.id
        print('==========std==========', self.std)
        result = self.env['fees.structure'].search([('std_id', '=', self.std)])
        print("result->>>>>>>>>>", result)
        feesssss = self.student_fees = result.fees
        print("Fessssss->>>>>>", feesssss)

    @api.multi
    def create_sale_order(self):
        vals = {
            'partner_id': self.env.user.partner_id.id
        }
        res = self.env['sale.order'].create(vals)
        vals_order_line = {'product_id': self.env.ref
                           ('school_managment_new.library_fees').id,
                           'product_uom_qty': 2,
                           'name': "Fees",
                           'customer_lead': 0,
                           'price_unit': self.student_fees,
                           'order_id': res.id
                           }
        res1 = self.env['sale.order.line'].create(vals_order_line)
        # res.order_line = res1
        print("res->>>>>>>>>>>>>>", res)
        print("res1", res1)
        # return res
        return True

    # above code and this code work same but here is in
    # single create method using to create sale order as well as order_line

    # @api.multi
    # def create_sale_order(self):
    #     res = self.env['sale.order'].create(
    #         {'partner_id': self.env.user.partner_id.id,
    #          'order_line': [(0, 0, {'product_id': self.env.ref
    #                                 ('school_managment_new.school_fees').id,
    #                                 'product_uom_qty': 1,
    #                                 'name': "Fees",
    #                                 'customer_lead': 0,
    #                                 'price_unit': self.student_fees
    #                                 })]})

    #     print("res->>>>>>>>>>>>>>", res)

    @api.multi
    def sale_order_open(self):
        vals = {
            'name': ('SaleOrder'),
            'domain': [('partner_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'sale.order',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        print("Vals ->>>>>>>>", vals)
        return vals


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


class AssignmentType(models.Model):
    _name = 'assignment.type'
    _description = "Assignment Type Details"

    name = fields.Char(string="Name")
    assignment_code = fields.Char(string="Code")


class AssignmentDetails(models.Model):
    _name = 'assignment.details'
    _description = "Assignment Details"

    name = fields.Char(string="Assignment Name")k
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
