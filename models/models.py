# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SampleTransport(models.Model):
    _name = 'sample.transport'
    _description = 'SampleTransport'

    name = fields.Char()
    test_type = fields.Selection(
        string='Test_type',
        selection=[('viral load', 'Viral Load'),
                   ('eid', 'EID'),
                   ('sputum(genxpert/culture', 'Sputum(GeneXpert/Culture'),
                   ],
        required=False, )
        
    receiving_lab = fields.Many2one(
        comodel_name='lab.facility',
        string='Receiving Facility',
        required=False)
    receiving_staff = fields.Many2one(
        comodel_name='facility.staff',
        string='Receiving staff',
        required=False)
    sending_lab = fields.Many2one(
        comodel_name='lab.facility',
        string='Sending Facility',
        required=False)
    sending_staff = fields.Many2one(comodel_name='facility.staff', string='Sending staff', required=False)
    date_time_sent = fields.DateTimeField(string='Date and Time Sent')
    date_time_received = fields.DateTimeField(string='Date and Time Received')
    total_samples_sent = fields.Integer(
        string='Total samples sent',
        required=False)
    total_samples_received = fields.Integer(
        string='Total samples Received',
        required=False)
    specimen_type = fields.Char(
        string='Specimen Type',
        required=False)
    temperature_send = fields.Float(
        string='Temperature at Sending Time',
        required=False)
    third_pl = fields.Many2one(comodel_name='third.pl', string='3PL')
    patient_code = fields.Many2one(comodel_name='patient.code', string='Patient Code')
    sample_sent = fields.Boolean(
        string='Sample sent',
        required=False)
    sample_received = fields.Boolean(
        string='Sample Received',
        required=False)
    sample_accepted = fields.Boolean(
        string='Sample Accepted',
        required=False)
    reason_for_rejection = fields.Text(
        string="Reason for rejection",
        required=False)
    comment = fields.Text(string='Comment', required=False)


class ThirdPl(models.Model):
    _name = 'third.pl'
    _description = '3pl list'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone Number')


class Patient(models.Model):
    _name = 'patient.code'
    _description = 'Patient Codes'

    name = fields.Char(string='Patient Code', required=False)
    age = fields.Integer(string='Age', required=True)
    sex = fields.Selection(
        string='Sex',
        selection=[('male', 'male'), ('female', 'female'), ],
        required=False, )


class LaboratoryFacilities(models.Model):
    _name = 'lab.facility'
    _description = 'Laboratory Facilities'

    name = fields.Char(string='Facility Name/Code')
    state = fields.Many2one(
        comodel_name='sates.nigeria',
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


class FacilityStaff(models.Model):
    _name = 'staff.facility'
    _description = 'Facility Staff'

    name = fields.Char(string='Name')
    phone = fields.Char(string='Phone Number')
    facility_id = fields.Many2one(comodel_name='lab.facility')
# class sample_transport(models.Model):
#     _name = 'sample_transport.sample_transport'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100