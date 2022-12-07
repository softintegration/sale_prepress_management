# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PrepressProof(models.Model):
    _inherit = 'prepress.proof'


    @api.model
    def _get_by_product(self,product_id):
        """ Get the Prepress proof by specified product"""
        domain = self._get_accepted_prepress_proof_domain()
        domain.append(('product_id','=',product_id.id))
        return self.search(domain,limit=1)



    @api.model
    def _get_accepted_prepress_proof_domain(self):
        accepted_states = ('in_progress','validated','flashed')
        return [('state','in',accepted_states)]