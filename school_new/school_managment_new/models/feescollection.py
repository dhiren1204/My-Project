# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from datetime import date, datetime


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
