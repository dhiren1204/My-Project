# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class FeesStructure(models.Model):
    _name = 'fees.structure'
    _description = 'Std wise Fees'

    std_id = fields.Many2one('std.std', string="Std")
    fees = fields.Char(string="Fees")
