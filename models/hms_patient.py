from odoo import models, fields


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS patient'
    first_name = fields.Char(string='first name')
    last_name = fields.Char(string='last name')
    birth_date = fields.Datetime(string='BOD')
    history = fields.Html(string='medical history')
    cr_ratio = fields.Float(string='cr ratio')
    blood_type = fields.Selection(
        selection=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        string='blood type',
    )
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='patient image')
    address = fields.Text(string='address')
