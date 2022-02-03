# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import date



class SampleTransport(models.Model):
    _name = 'sample.transport'
    _description = 'SampleTransport'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    state = fields.Selection(
        string='State',
        selection=[('draft', 'draft'),
                   ('in process', 'in process'),
                   ('completed', 'completed'),],
        required=False, default='draft', track_visibility=True, trace_visibility='onchange',)
    st_no = fields.Char(string="Sample Transport No.", default=lambda self: _('New'), requires=False, readonly=True,
                          trace_visibility='onchange', )

    test_type = fields.Many2many(
        comodel_name='test.type',
        string='Test Type')
        
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
    sending_staff = fields.Many2one(comodel_name='staff.facility', string='Sending staff', required=False)
    date_time_sent = fields.Datetime(string='Date and Time Sent')
    date_time_received = fields.Datetime(string='Date and Time Received')
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
    third_pl = fields.Many2one(comodel_name='third.pl', string='3PL Name')
    third_pl_phone = fields.Char(string='3PL Phone', related='third_pl.phone', readonly=True)
    patient_sample_details = fields.One2many(
        comodel_name='patient.sampledetails',
        inverse_name='sample_transport_id',
        string='Patient Sample Details',
        required=False)

    @api.model
    def create(self, vals):
        if vals.get('st_no', _('New')) == _('New'):
            vals['st_no'] = self.env['ir.sequence'].next_by_code('increment_sample_transport') or _('New')
        result = super(SampleTransport, self).create(vals)
        return result


class PatientSampleDetails(models.Model):
    _name = 'patient.sampledetails'
    _description = 'Patient Sample Details'

    sample_transport_id = fields.Many2one(
       comodel_name='sample.transport',
       string='Sample transport id',
       required=False)
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
    state = fields.Selection(
        string='Status',
        selection=[('draft', 'draft'),
                   ('sample sent', 'sample sent'),
                   ('sample received', 'received awaiting result'),
                   ('sample rejected', 'sample rejected'),
                   ('result dispatched', 'result dispatched'),
                   ('result delivered', 'result delivered')],
        required=False, default='draft', track_visibility=True, trace_visibility='onchange', )
    turnaround_time = fields.Char(string='Turnaround Time', required=False)


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


class ResultTransport(models.Model):
    _name = 'result.transport'
    _description = 'Result Transport'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    test_type = fields.Many2many(
        comodel_name='test.type',
        string='Test Type')
    state = fields.Selection(
        string='State',
        selection=[('draft', 'draft'),
                   ('in process', 'in process'),
                   ('completed', 'completed'), ],
        required=False, default='draft', track_visibility=True, trace_visibility='onchange', )
    rt_no = fields.Char(string="Sample Transport No.", default=lambda self: _('New'), requires=False, readonly=True,
                        trace_visibility='onchange', )
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
    date_time_sent = fields.Datetime(string='Date and Time Sent')
    date_time_received = fields.Datetime(string='Date and Time Received')
    total_results_sent = fields.Integer(
        string='Total results sent',
        required=False)
    total_results_received = fields.Integer(
        string='Total results Received',
        required=False)
    specimen_type = fields.Char(
        string='Specimen Type',
        required=False)
    temperature_send = fields.Float(
        string='Temperature at Sending Time',
        required=False)
    third_pl = fields.Many2one(comodel_name='third.pl', string='3PL')
    patient_result_details = fields.One2many(
        comodel_name='patient.resultdetails',
        inverse_name='result_transport_id',
        string='Patient_result_details',
        required=False)
    third_pl_phone = fields.Char(string='3PL Phone', related='third_pl.phone', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('rt_no', _('New')) == _('New'):
            vals['rt_no'] = self.env['ir.sequence'].next_by_code('increment_result_transport') or _('New')
        result = super(ResultTransport, self).create(vals)
        return result


class PatientResultDetails(models.Model):
    _name = 'patient.resultdetails'
    _description = 'Patient Result Details'

    result_transport_id = fields.Many2one(
        comodel_name='result.transport',
        string='Result transport id',
        required=False)
    patient_code = fields.Many2one(comodel_name='patient.code', string='Patient Code')
    result_sent = fields.Boolean(
        string='Results sent',
        required=False)
    result_received = fields.Boolean(
        string='Results Received',
        required=False)
    result_accepted = fields.Boolean(
        string='Results Accepted',
        required=False)
    reason_for_rejection = fields.Text(
        string="Reason for rejection",
        required=False)
    comment = fields.Text(string='Comment', required=False)
    state = fields.Selection(
        string='Status',
        selection=[('draft', 'draft'),
                   ('result sent', 'result sent'),
                   ('result received', 'received '),
                   ('sample rejected', 'sample rejected'),
                   ('result dispatched', 'result dispatched'),
                   ('result delivered', 'result delivered')],
        required=False, default='draft', track_visibility=True, trace_visibility='onchange', )
    linked_sample = fields.Many2one(comodel_name="patient.sampledetails", string='Linked Sample')


class TestType(models.Model):
    _name = 'test.type'
    _description = 'Test Type'

    name = fields.Char()








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