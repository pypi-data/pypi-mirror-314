# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Margin Sale Sync",
    "summary": "Sync invoice margin between invoices and sale orders",
    "version": "15.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/sygel-technology/sy-margin-analysis",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale_margin", "account_invoice_margin"],
    "data": ["views/res_config_settings_views.xml"],
}
