# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cost_sale_sync_invoice_posted = fields.Boolean(
        related="company_id.cost_sale_sync_invoice_posted", readonly=False
    )
