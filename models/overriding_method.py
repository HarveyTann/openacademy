# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Overriding_method(models.Model):
    _inherit = "account.move"

    lookHere = fields.Char(string='Test action_post')

    # this function extend the account.move action_post function
    def action_post(self):
        self.lookHere = "This function extends"
        return super(Overriding_method, self).action_post()

    # this function overides the account.move action_post function
    # def action_post(self):
    #     self.lookHere = "This function replace"
