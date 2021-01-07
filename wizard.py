
from odoo import models, fields, api

# wizard records are nt meant to be persistent; automatically deleted from the database after a certain time
# do not require access rights, users have all permissions on wizad record
# regular record cant refer to wizard records through many2one fields
class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_session(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session',
        string="Sessions", required=True, default=_default_session)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    def subscribe(self):
        for session in self.session_ids:
            # bitwise-OR
            session.attendee_ids |= self.attendee_ids
        return {}