# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from pprint import pprint
from datetime import datetime, date
import math

class calon_siswa_biaya(models.Model):
    _inherit = 'siswa_psb_ocb11.calon_siswa_biaya'

    qty = fields.Integer('Qty', default=1)
    jumlah_harga = fields.Float('Jumlah Harga' )
    potongan_harga = fields.Float('Potongan')

    @api.onchange('potongan_harga')
    def potongan_harga_change(self):
        # self.jumlah_harga = (self.qty * self.harga) - (self.qty * self.potongan_harga)
        # self.dibayar = self.jumlah_harga
        print('qty : ' + str(self.qty))
        print('harga : ' + str(self.harga))
        print('potongan_harga : ' + str(self.potongan_harga))
        harga_setelah_potong = (self.qty * self.harga) - (self.qty * self.potongan_harga)
        print('harga setelah potong : ' + str(harga_setelah_potong))
        # self.write({
        #     'jumlah_harga' : harga_setelah_potong,
        #     'dibayar' : harga_setelah_potong,
        # })
        # self.write({
        #         'jumlah_harga' : harga_setelah_potong,
        #         'dibayar' : harga_setelah_potong,
        #     })

        self.jumlah_harga = harga_setelah_potong
        self.dibayar = harga_setelah_potong
        
        
        # for rec in self:
        #     harga_setelah_potong = (rec.qty * rec.harga) - (rec.qty * rec.potongan_harga)
        #     rec.write({
        #         'jumlah_harga' : harga_setelah_potong,
        #         'dibayar' : harga_setelah_potong,
        #     })
    
    @api.onchange('biaya_id')
    def biaya_id_change(self):
        self.potongan_harga = 0
    
    # def get_default_harga(self):
    #     return self.harga


    @api.multi
    def write(self, vals):
        if 'potongan_harga' in vals:
            vals['jumlah_harga'] = (self.qty * self.harga) - (self.qty * vals['potongan_harga'])
        return super(calon_siswa_biaya, self).write(vals)