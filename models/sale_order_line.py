# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    prepress_proof_id = fields.Many2one('prepress.proof',string='Prepress proof',readonly=True)

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        self._update_prepress_proof()
        return res

    def _update_prepress_proof(self):
        if not self.product_id:
            return
        prepress_proof = self.env['prepress.proof']._get_by_product(self.product_id)
        self.update({'prepress_proof_id': prepress_proof and prepress_proof.id or False})









