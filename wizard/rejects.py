# models.py

from odoo import models, fields, api


class SampleRiderWizard(models.TransientModel):
    _name = 'sample.rider.wizard'

    detail_ids = fields.Many2many('patient.sampledetails', string='Patient Codes')
    reason = fields.Text(string="Reason", required=False)

    def apply_action(self):
        # Implement the action you want to perform with the selected records
        selected_details = self.detail_ids
        # Your custom logic here
        for rec in selected_details:
            # val = {
            #     'id': rec.id,
            #     'state': 'sample received'
            # }
            # lines.append(val)
            patient = self.env['patient.sampledetails'].search([('id', '=', rec.id)]).ensure_one()
            patient.write({
                'state': 'sample rejected',
                'sample_received': False,
                'sample_accepted': False,
                'sample_rejected': True,
                'reason_for_rejection': self.reason,
            })

    @api.model
    def default_get(self, fields):
        res = super(SampleRiderWizard, self).default_get(fields)
        default_detail_ids = self.env.context.get('default_detail_ids')
        if default_detail_ids:
            res['detail_ids'] = default_detail_ids
        return res
