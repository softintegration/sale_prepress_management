# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv.expression import OR


class PrepressProof(models.Model):
    _inherit = 'prepress.proof'


    @api.model
    def _get_by_product(self,product_id):
        """ Get the Prepress proof by specified product"""
        # we have to search the validated/flashed prepress_proof first and only if we have not found we search the In progress ones
        domain = self._get_favorite_prepress_proof_domain()
        domain.append(('product_id','=',product_id.id))
        prepress_proof = self.search(domain,limit=1)
        if not prepress_proof:
            domain = self._get_accepted_prepress_proof_domain()
            domain.append(('product_id', '=', product_id.id))
            prepress_proof = self.search(domain,limit=1)
        return prepress_proof


    def _get_favorite_prepress_proof_domain(self):
        favorite_states = ('validated','flashed')
        return [('state','in',favorite_states)]

    @api.model
    def _get_accepted_prepress_proof_domain(self):
        accepted_states = ('in_progress',)
        accepted_domain = [('state','in',accepted_states)]
        return OR([self._get_favorite_prepress_proof_domain(),accepted_domain])