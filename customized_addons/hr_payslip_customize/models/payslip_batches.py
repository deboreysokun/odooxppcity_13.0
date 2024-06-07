from odoo import api, fields, models, _


class CustomizeHrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    # add company_id field in hr_payslip_run to be able to create rule in security.xml
    # add field exchange_rate to make the slip computed based on the exchange_rate input
    # add attachments field to let user attach the reference of each slip
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company.id, readonly=True)
    exchange_rate = fields.Integer(string='Exchange Rate', required=True)
    attachment_ids = fields.Many2many('ir.attachment', 'slipbatch_attachment_rel', 'slipbatch_ref', 'slipbatch_ref1',
                                              string="Attachments", help='You can attach the documents here')