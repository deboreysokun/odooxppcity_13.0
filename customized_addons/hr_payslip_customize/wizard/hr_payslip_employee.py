from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CustomHrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'
    # inherit hr_payslip_employee wizard to add compute field of employee_ids based on department_id
    employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'payslip_id', 'employee_id', 'Employees')
    department_ids = fields.Many2many('hr.department', required=True)

    @api.onchange('department_ids')
    def _onchange_department_ids(self):
        if self.department_ids:
            # Get all employees in the specified departments
            employees = self.env['hr.employee'].search([('department_id', 'in', self.department_ids.ids)])
            self.employee_ids = [(6, 0, employees.ids)]
        else:
            # If no departments selected, clear the employee_ids
            self.employee_ids = [(5, 0, 0)]

    @api.model
    def compute_sheet(self):
        payslips = self.env['hr.payslip']
        [data] = self.read()
        active_id = self.env.context.get('active_id')
        if active_id:
            [run_data] = self.env['hr.payslip.run'].browse(active_id).read(
                ['date_start', 'date_end', 'credit_note', 'exchange_rate'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        exchange_rate = run_data.get('exchange_rate')
        if not data['employee_ids']:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))
        for employee in self.env['hr.employee'].browse(data['employee_ids']):
            slip_data = self.env['hr.payslip'].onchange_employee_id(from_date, to_date, employee.id, contract_id=False)
            res = {
                'employee_id': employee.id,
                'name': slip_data['value'].get('name'),
                'struct_id': slip_data['value'].get('struct_id'),
                'contract_id': slip_data['value'].get('contract_id'),
                'payslip_run_id': active_id,
                'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                'date_from': from_date,
                'date_to': to_date,
                'credit_note': run_data.get('credit_note'),
                'company_id': employee.company_id.id,
                'exchange_rate': exchange_rate,
            }
            payslips += self.env['hr.payslip'].create(res)
        payslips.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}