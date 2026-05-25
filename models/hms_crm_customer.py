from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Link to patient
    related_patient_id = fields.Many2one('hms.patient', string='related patient')

    # Prevents duplicate email
    @api.constrains('related_patient_id', 'email')
    def _check_patient_email(self):
        for rec in self:
            if rec.related_patient_id and rec.related_patient_id.email == rec.email:
                raise ValidationError('Customer email cannot be the same as the linked patient email!')

    # prevents deletion
    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError('Cannot delete customer linked to a patient!')
        return super(ResPartner, self).unlink()
