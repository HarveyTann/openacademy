from odoo import models, fields
from odoo.addons import decimal_precision as dp

class DecimalPoints(models.Model):

    _inherit = "openacademy.course"
    # digits - 6 before the . 5 decimal points
    # price = fields.Float(string="Course Price", digits=(6,5))

    #dp.get_precision
    price = fields.Float(String="Course Price", digits=dp.get_precision('Course Price'), default=0.0)