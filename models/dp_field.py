from odoo import models, fields

class DecimalPoints(models.Model):

    _inherit = "openacademy.course"
    # digits - 6 before the . 5 decimal points
    price = fields.Float(string="Course price", digits=(6,5))