from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS patient'

    first_name = fields.Char(string='first name', required=True)
    last_name = fields.Char(string='last name', required=True)
    birth_date = fields.Date(string='BOD')
    age = fields.Integer(string='age', compute='_compute_age', store=True)
    address = fields.Text(string='address')
    # unique email
    email = fields.Char(string='email')
    _sql_constraints = [
        ('unique_email', 'unique(email)', 'Email must be unique!')
    ]
    image = fields.Image(string='patient image')

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
    cr_ratio = fields.Float(string='cr ratio')
    history = fields.Html(string='medical history')

    # rel with department
    department_id = fields.Many2one(
        'hms.department',
        string='department',
        domain="[('is_opened', '=', True)]",  # no closed dept
    )
    # dept capacity
    department_capacity = fields.Integer(
        related='department_id.capacity',
        string='department capacity',
        readonly=True,
    )
    doctor_ids = fields.Many2many('hms.doctors', string='doctors')
    state = fields.Selection(
        selection=[
            ('undetermined', 'Undetermined'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('serious', 'Serious'),
        ],
        string='state',
        default='undetermined',
    )
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='log history')

    # compute age
    @api.depends('birth_date')
    def _compute_age(self):
        from datetime import date
        today = date.today()
        for rec in self:
            if rec.birth_date:
                b = rec.birth_date
                rec.age = today.year - b.year - ((today.month, today.day) < (b.month, b.day))
            else:
                rec.age = 0

    # age lower 30
    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR auto-checked',
                    'message': 'Age is below 30 — PCR has been automatically checked.',
                }
            }

    # state change log
    @api.onchange('state')
    def _onchange_state(self):
        if self.state:
            self.log_ids = [(0, 0, {
                'created_by': self.env.user.id,
                'date': fields.Datetime.now(),
                'description': f'State changed to {dict(self._fields["state"].selection).get(self.state)}',
            })]

    # pcr checked cr ratio
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError('CR ratio is required when PCR is checked.')

    # email validation
    @api.constrains('email')
    def _check_email_valid(self):
        import re
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for rec in self:
            if rec.email and not re.match(regex, rec.email):
                raise ValidationError('Invalid email format!')
