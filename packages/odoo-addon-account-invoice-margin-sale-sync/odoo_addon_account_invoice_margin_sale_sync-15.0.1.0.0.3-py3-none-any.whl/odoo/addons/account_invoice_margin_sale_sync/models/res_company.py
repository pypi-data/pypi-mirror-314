# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    cost_sale_sync_invoice_posted = fields.Boolean(
        string="Sync cost on posted invoices",
        default=True,
    )
