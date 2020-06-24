# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class HobbiesHobbies(models.Model):
    _name = 'hobbies.hobbies'
    _description = "Details of Hobbies"

    name = fields.Char(string="Hobbies")
