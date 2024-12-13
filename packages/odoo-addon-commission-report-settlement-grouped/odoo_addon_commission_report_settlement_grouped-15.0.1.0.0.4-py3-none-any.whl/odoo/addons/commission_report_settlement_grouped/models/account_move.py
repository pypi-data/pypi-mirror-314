# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_commission_total_by_salesman(self, salesman):
        self.ensure_one()
        return sum(
            self.line_ids.agent_ids.filtered(lambda al: al.agent_id == salesman).mapped(
                "amount"
            )
        )
