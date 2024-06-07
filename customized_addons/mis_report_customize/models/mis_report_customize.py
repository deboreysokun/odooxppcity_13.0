from copy import copy

from odoo.addons.mis_builder.models.kpimatrix import KpiMatrixRow

from odoo import models


class MisReportInstanceCustomize(models.Model):
    _inherit = "mis.report.instance"

    def _compute_matrix(self):
        kpi_matrix = super(MisReportInstanceCustomize, self)._compute_matrix()
        # new customized code
        # Extend parent account hierarchy
        new_rows = {}
        for kpi, account_rows in kpi_matrix._detail_rows.items():
            # Get all the account transaction for each kpi
            for account_id, account_row in account_rows.items():
                account = self.env['account.account'].browse(account_id)
                parent_path = account.parent_path.strip('/').split('/')
                parent_ids = [int(x) for x in parent_path[:len(parent_path) - 1]]
                account_row.style_props['indent_level'] = account_row.style_props.get('indent_level', 1) * len(
                    parent_ids)
                account_parents = self.env['account.account'].search(
                    [('id', 'in', parent_ids), ('internal_group', '!=', 'off_balance')])
                for account_parent in account_parents:
                    level = len(account_parent.parent_path.strip('/').split('/')) - 1
                    account_parent_id = int(account_parent.id)
                    if kpi not in new_rows:
                        new_rows[kpi] = {}
                    account_parent_row = KpiMatrixRow(kpi_matrix, kpi, account_parent_id)
                    if account_parent_id not in new_rows[kpi]:
                        account_parent_row.style_props['indent_level'] = account_parent_row.style_props.get(
                            'indent_level', 1) * level
                        new_rows[kpi][account_parent_id] = account_parent_row
                        # Copy account transaction cell for each column to the new parent row
                        # and modify drilldown_arg for treeview action on click the row balance cell
                        for col_key, col in kpi_matrix._cols.items():
                            cells = col.get_cell_tuple_for_row(account_row)
                            cpy_cells = []
                            if not cells: continue
                            for cell in cells:
                                cpy_cell = copy(cell)
                                cpy_cell.drilldown_arg = copy(cell.drilldown_arg)
                                cpy_cell.drilldown_arg['account_id'] = account_parent_id
                                cpy_cell.drilldown_arg['child_acc_ids'] = set([account_id])
                                cpy_cells.append(cpy_cell)
                            col._set_cell_tuple(account_parent_row, cpy_cells)
                    else:
                        # Add the child balance to the parent row
                        # and append new account_id to child_acc_ids for the treeview domain
                        for col_key, col in kpi_matrix._cols.items():
                            account_parent_row = new_rows[kpi][account_parent_id]
                            child_cells = col.get_cell_tuple_for_row(account_row)
                            parent_cells = col.get_cell_tuple_for_row(account_parent_row)
                            if not child_cells: continue
                            if not parent_cells:
                                # In case parent_cells initailization is skip
                                cpy_cells = []
                                for cell in child_cells:
                                    cpy_cell = copy(cell)
                                    cpy_cell.drilldown_arg = copy(cell.drilldown_arg)
                                    cpy_cell.drilldown_arg['account_id'] = account_parent_id
                                    cpy_cell.drilldown_arg['child_acc_ids'] = set([account_id])
                                    cpy_cells.append(cpy_cell)
                                col._set_cell_tuple(account_parent_row, cpy_cells)
                                continue
                            for child_cell, parent_cell in zip(child_cells, parent_cells):
                                parent_cell.val += child_cell.val
                                parent_cell.val_rendered = kpi_matrix._style_model.render(
                                    kpi_matrix.lang, account_parent_row.style_props, kpi.type, parent_cell.val
                                )
                                parent_cell.drilldown_arg['child_acc_ids'].add(account_id)
        for kpi in new_rows:
            kpi_matrix._detail_rows[kpi].update(new_rows[kpi])
        return kpi_matrix

    def drilldown(self, arg):
        result = super(MisReportInstanceCustomize, self).drilldown(arg)
        domain = result['domain']
        if arg.get('child_acc_ids'):
            child_acc_ids = arg.get('child_acc_ids').strip('}{').split(', ')
            child_acc_ids = [int(acc_id) for acc_id in child_acc_ids]
            domain[0] = ('account_id', 'in', child_acc_ids)
        return result
