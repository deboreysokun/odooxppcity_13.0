from odoo import models, fields, api, _


class CustomExpense(models.Model):
    _inherit = 'hr.expense'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', check_company=True,
                                          required=True)
    expense_reference = fields.Char(string='Expense Reference', required=True, copy=False, readonly=True,
                                    default=lambda self: _('Expense Sequence'))
    view_report_count = fields.Integer(string='View Report', compute='_compute_view_report_count')

    def _compute_view_report_count(self):
        for expense in self:
            expense.view_report_count = len(expense.sheet_id)

    @api.model
    def create(self, vals):
        if vals.get('expense_reference', _('New')) == _('New'):
            vals['expense_reference'] = self.env['ir.sequence'].next_by_code('hr.expense') or _('New')
        return super(CustomExpense, self).create(vals)


class HRExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    expense_reference = fields.Char(string='Expense Reference')
    expense_summary_reference = fields.Char(string='Expense Summary Reference', required=True, copy=False,
                                            readonly=True,
                                            default=lambda self: _('Expense Summary Reference'))

    @api.model
    def create(self, vals):
        if vals.get('expense_summary_reference', _('New')) == _('New'):
            vals['expense_summary_reference'] = self.env['ir.sequence'].next_by_code('hr.expense.sheet') or _('New')
        return super(HRExpenseSheet, self).create(vals)
