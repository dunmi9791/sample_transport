# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import date


class LaboratoryFacilities(models.Model):
    _name = 'lab.facility'
    _description = 'Laboratory Facilities'

    name = fields.Char(string='Facility Name/Code')
    state = fields.Many2one(
        comodel_name='states.nigeria',
        string='State',
        required=False)
    lga = fields.Many2one(
        comodel_name='lga.state',
        string='LGA',
    )
    facility_staff = fields.One2many(
        comodel_name='staff.facility',
        inverse_name='facility_id',
        string='Facility staff',
        required=False)
    facility_patient = fields.One2many(
        comodel_name='patient.code',
        inverse_name='facility_id',
        string='Facility Patients',
        required=False)


class FacilityStaff(models.Model):
    _name = 'staff.facility'
    _description = 'Facility Staff'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone Number')
    facility_id = fields.Many2one(comodel_name='lab.facility')

