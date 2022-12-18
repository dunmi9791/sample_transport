# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import date


class SampleTransport(models.Model):
    _name = 'sample.transport'
    _description = 'SampleTransport'
    _rec_name = 'st_no'
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
    project = fields.Many2one(
        comodel_name='project.sample',
        string='Project',
        required=False)

    test_type = fields.Many2one(
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
    total_samples_sent = fields.Integer(compute='count_sent',
                                        string='Total samples sent',
                                        )
    total_samples_received = fields.Integer(compute='count_received',
                                            string='Total samples Received',
                                            required=False)
    specimen_type = fields.Char(
        string='Specimen Type',
        required=False)
    temperature_send = fields.Float(
        string='Temperature at Sending Time',
        required=False)
    temperature_receive = fields.Float(
        string='Temperature at Received time',
        required=False)
    third_pl = fields.Many2one(comodel_name='third.pl', string='3PL Name')
    third_pl_phone = fields.Char(string='3PL Phone', related='third_pl.phone', readonly=True)
    patient_sample_details = fields.One2many(
        comodel_name='patient.sampledetails',
        inverse_name='sample_transport_id',
        string='Patient Sample Details',
        required=False)

    @api.multi
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'in process'),
                   ('in process', 'completed'),
                   ]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for sample in self:
            if sample.is_allowed_transition(sample.state, new_state):
                sample.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (sample.state, new_state)
                raise UserError(msg)

    @api.multi
    def sample_deliver(self):
        lines = []
        for rec in self.patient_sample_details:
            # val = {
            #     'id': rec.id,
            #     'state': 'sample received'
            # }
            # lines.append(val)
            patient = self.env['patient.sampledetails'].search([('id', '=', rec.id)]).ensure_one()
            patient.write({
                'state': 'sample received'
            })
        self.change_state('in process')



    @api.model
    def create(self, vals):
        if vals.get('st_no', _('New')) == _('New'):
            vals['st_no'] = self.env['ir.sequence'].next_by_code('increment_sample_transport') or _('New')
        result = super(SampleTransport, self).create(vals)
        return result

    @api.multi
    def count_sent(self):
        patient_sample_details = self.env['patient.sampledetails']
        for sample in self:
            sample.total_samples_sent = patient_sample_details.search_count([('sample_transport_id', '=', sample.id), ('sample_sent', '=', True)])

    @api.multi
    def count_received(self):
        patient_sample_details = self.env['patient.sampledetails']
        for sample in self:
            sample.total_samples_received = patient_sample_details.search_count(
                [('sample_transport_id', '=', sample.id), ('sample_received', '=', True)])
        # return len(self.patient_sample_details)
        # for sent in self:
        #     sent_count = self.env['patient.sampledetails'].search_count([
        #         ('sample_transport_id', '=', self.id)])
        #     return sent_count




class PatientSampleDetails(models.Model):
    _name = 'patient.sampledetails'
    _description = 'Patient Sample Details'
    _rec_name = 'sample_transport_id'

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
    sample_rejected = fields.Boolean(
        string='Sample Rejected',
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
    facility_id = fields.Many2one(comodel_name='lab.facility', required=True)

    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "Patient code already exists !"),
    # ]



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
    linked_sample = fields.Many2one(comodel_name="patient.sampledetails", string='Linked Sample',
                                    )

   
    @api.onchange('patient_code')
    def onchange_patient_code(self):
        for rec in self:
            return {'domain': {'linked_sample': [('patient_code', '=', rec.patient_code.id)]}}


class TestType(models.Model):
    _name = 'test.type'
    _description = 'Test Type'

    name = fields.Char()


class ProjectSample(models.Model):
    _name = 'project.sample'
    _description = 'Projects'

    name = fields.Char()
    client = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=False)
    start_date = fields.Date(
        string='Start date',
        required=False)
    end_date = fields.Date(
        string='End date',
        required=False)








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