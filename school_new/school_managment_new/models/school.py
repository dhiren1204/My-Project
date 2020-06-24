
from odoo import api, fields, models
from datetime import date, datetime


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
