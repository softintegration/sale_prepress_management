# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res =super(SaleOrder, self).action_confirm()
        if any((order_line.product_id.type == 'product' and order_line.product_id.bat_product and not order_line.prepress_proof_id) for order_line in self.mapped("order_line")):
            raise ValidationError(_("The Prepress proof is required before the confirmation of sale order!"))
        return res











