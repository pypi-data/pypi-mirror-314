# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    sale_payment_mode_id = fields.Many2one(
        name="Sale Payment Mode",
        comodel_name="account.payment.mode",
        domain=[("payment_type", "=", "inbound")],
    )
