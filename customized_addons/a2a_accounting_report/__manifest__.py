# -*- coding: utf-8 -*-
{
  'name': "A2A Accounting Report",
  'summary': """
      Add new cutom customer invoice and Vendor bill template in PDF, 
      Customize all Reporting in Excel template. Requirement Agreement Page: 4,5,9,10""",
  'author': "Reth Sokmeta(B8), Thy Saonan(B8), Pich Rachana(B8)",
  'website': 'https://docs.google.com/document/d/1BzFCpYVMn_hsKkT7A2cCzyCqhN5ytPrSaeNFpKMo8Qk',
  'category': 'Accounting',
  'version': '13.2.1',
  'depends': ['base', 'accounting_pdf_reports', 'odoo_report_xlsx', 'inventory_fields_customize'],
  'data': [
    'reports/customer_invoice/paperformat.xml',
    'reports/customer_invoice/report.xml',
    'reports/customer_invoice/a2a_commercial_invoice.xml',
    'reports/customer_invoice/a2a_template.xml',
    'reports/customer_invoice/commercial_package_2020.xml',
    'reports/customer_invoice/a2a_commercial_invoice.xml',
    'reports/customer_invoice/a2a_tax_invoice.xml',
    'reports/customer_invoice/tax_package_2020.xml',
    'reports/customer_invoice/vkirirom_commercial_invoice.xml',
    'reports/customer_invoice/vkirirom_tax_invoice.xml',
    'reports/customer_invoice/a2a_it_service_commercial_invoice.xml',
    'reports/customer_invoice/a2a_it_service_tax_invoice.xml',
    'reports/customer_invoice/jobify_tax_invoice.xml',
    'reports/customer_invoice/jobify_commercial_invoice.xml',
    'reports/customer_invoice/vkirirom_pte_invoice.xml',
    'reports/customer_invoice/kit_commercial_invoice.xml',
    'reports/customer_invoice/kit_tax_invoice.xml',
    'reports/customer_invoice/vkis_invoice.xml',
    'reports/report_journal_audit.xml',
    'reports/vendor_bill/paperformat.xml',
    'reports/vendor_bill/report.xml',
    'reports/vendor_bill/payment_voucher_template.xml',
    'reports/vendor_bill/payment_voucher_report_pdf_template.xml',
    'reports/vendor_bill/vkr_payment_voucher_report_pdf_template.xml',
    'reports/vendor_bill/mkl_payment_voucher_report_pdf.xml',
    'reports/report.xml',
    'wizards/account_trial_balance_report_customize.xml',
    'wizards/account_excel_button.xml',
    'wizards/report_financial_customize.xml',
    'views/accounting_report_assets.xml',
  ],
  'installable': True,
}
