# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    prepress_proof_id = fields.Many2one('prepress.proof', string='Prepress proof', readonly=True)

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        warning = self._update_prepress_proof()
        if warning:
            return warning
        return res

    def _update_prepress_proof(self):
        if not self.product_id:
            return
        prepress_proof = self.env['prepress.proof']._get_by_product(self.product_id)
        self.update({'prepress_proof_id': prepress_proof and prepress_proof.id or False})
        if prepress_proof.quarantined:
            warning = {
                'title': _("Warning"),
                'message': _(
                    "Prepress Proof %s has already been quarantined!"
                ) % prepress_proof.name,
            }
            return {'warning': warning}

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        for each in self:
            if each.state == 'sale' and each.product_id.type == 'product' and not each.prepress_proof_id:
                raise ValidationError(_("The Prepress proof is required in sale state!"))
        return res
