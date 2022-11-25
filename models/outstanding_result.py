20# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import date


class OutstandingResult(models.Model):
    _name = 'outstanding.result'
    _description = 'Samples awaiting results'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    patient_code = fields.Many2one(comodel_name='patient.code', string='Patient Code')
    sentfacility_lab = fields.Many2one(
        comodel_name='lab.facility',
        string='Sending Facility',
        required=False)
    received_facility = fields.Many2one(comodel_name='lab.facility', string='Received Facility', required=True)
    date_time_received = fields.Datetime(string='Date and Time Received')
    state = fields.Selection(
        string='State',
        selection=[('draft', 'draft'),
                   ('in process', 'in process'),
                   ('completed', 'completed'), ],
        required=False, default='draft', track_visibility=True, trace_visibility='onchange', )
    sample_transport_id = fields.Many2one(
        comodel_name='sample.transport',
        string='Sample transport ref',
        required=False)
    result_transport_id = fields.Many2one(
        comodel_name='result.transport',
        string='Result transport ref',
        required=False)



