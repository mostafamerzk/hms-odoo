from odoo import models, fields


class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'HMS patient log'

    patient_id = fields.Many2one('hms.patient', string='patient', ondelete='cascade')
    created_by = fields.Many2one('res.users', string='created by', default=lambda self: self.env.user)
    date = fields.Datetime(string='date', default=fields.Datetime.now)
    description = fields.Char(string='description')
