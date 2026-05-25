from odoo import models, fields


class HmsDoctors(models.Model):
    _name = 'hms.doctors'
    _description = 'HMS doctors'

    first_name = fields.Char(string='first name', required=True)
    last_name = fields.Char(string='last name', required=True)
    image = fields.Image(string='image')
