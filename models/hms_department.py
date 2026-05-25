from odoo import models, fields


class HmsDepartment(models.Model):
    _name = 'hms.department'
    _description = 'HMS department'

    name = fields.Char(string='name', required=True)
    capacity = fields.Integer(string='capacity')
    is_opened = fields.Boolean(string='is opened', default=True)
    patient_ids = fields.One2many('hms.patient', 'department_id', string='patients')
