# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions

class Course(models.Model):
    # IMPORTANT. required and defines name for the model
    _name = 'openacademy.course'
    _description = 'OpenAcademy Courses'

    # Defines what the model can store and where
    # Common Attributes - fields can be configured, by passing config attributes as parameters 
    # Simple fields - atomic values stored directly in the model's table and 'relational' fields linking records 
    # Reserved fields - fields managed by the system and shouldnt write to it, can be read 
    # Special fields - requires a name field on al models for display and search behaviours. field can be overridden by setting _rec_name
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    # Relational fields - links records
    # Many2one - simple link to other object
    responsible_id = fields.Many2one('res.users', ondelete='set null', string='Responsible', index=True)

    # self.cr, self.uid, self.pool = request.cr, request.uid, request.registry
    # user = self.pool["res.users"].browse(self.cr, self.uid, self.uid)
    # company_id = user.company_id.id
    # company_id = fields.Many2one('res.company', string='Company',  required=True, default=lambda self: self.env['res.company']._company_default_get('account.invoice'))


    # One2many - virtual relo, inverse of Many2one, behaves as a container of records
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sesions")

    # re implement copy method whihc allows duplicate of course object
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count([('name', '=like', u"Copy of {}%".format(self.name))])

        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    # sql constraints
    _sql_constraints = [
        ('name_description_check','CHECK(name != description)',"The title of the course should not be the description"),

        ('name_unique','UNIQUE(name)',"The course title must be unique"),
    ]

class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'OpenAcademy Session'

    name = fields.Char(required=True)
    # Default values
    start_date = fields.Date(default=fields.Date.today)
    # digits=(6,2) specifies precision of a float number: 6 is total, 2 is number after comma
    duration = fields.Float(digits=(6,2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
    color = fields.Integer()

    # Domains on relational fields - list evaluated server-side and can't refer to dynamic values
    # when selecting instructor for a session, (partners with instructor set True) should be visible
    # instructor_id = fields.Many2one('res.parnter', string='Ínstructor', domain=[('instructor', '=', True)])
    
    # Complex Doomains
    instructor_id = fields.Many2one('res.partner', string='Instructor', domain=['|',('instructor', '=', True), ('category_id.name', 'ilike', 'Teacher')])

    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string='Course', required=True)

    # Many2many - bidirectiona; multiple relo, behaves as a container
    attendee_ids = fields.Many2many('res.partner', string="Attendees") # built-in model res.patner

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')

    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    # percentage of taken seat
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if r.attendee_ids and r.seats:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
            else:
                r.taken_seats = 0
               

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.not_date = r.start_date
            # add duration to start_date
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end-date):
                continue
            # compute the difference
            r.duration = (r.end_date - r.start_date).days + 1

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    # explicit onchange warm invalid values
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "increase seats or remove excess attendees",
                },
            }

    # constraint that checks that the instructor is not present in the attendees of own session
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A sessions's instructor can't be an attendee")


# class openacademy(models.Model): 
#     _name = 'openacademy.openacademy'
#     _description = 'openacademy.openacademy'
    
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


