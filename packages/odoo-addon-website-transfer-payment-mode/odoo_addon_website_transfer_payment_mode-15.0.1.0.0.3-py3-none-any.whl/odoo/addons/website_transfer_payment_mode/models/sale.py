# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Pasar a la SO el tipo de pago seleccionado al enviar un correo
    def _send_order_confirmation_mail(self):
        if self.website_id or self.require_payment:
            transaction_ids = self.env["payment.transaction"].search(
                [
                    ("sale_order_ids", "in", self.id),
                    ("state", "in", ["pending", "authorized", "done"]),
                ],
                order="create_date desc",
            )
            if (
                transaction_ids
                and transaction_ids[0]
                and transaction_ids[0].acquirer_id is not False
                and transaction_ids[0].acquirer_id.sale_payment_mode_id
            ):
                self.payment_mode_id = transaction_ids[
                    0
                ].acquirer_id.sale_payment_mode_id.id
        super(SaleOrder, self)._send_order_confirmation_mail()
