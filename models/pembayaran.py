# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.addons import decimal_precision as dp
from datetime import datetime
from pprint import pprint

class pembayaran(models.Model):
    _inherit = 'siswa_keu_ocb11.pembayaran'

    # override default actioni_cancel
    def action_cancel(self):
        super(pembayaran, self).action_cancel()
        # reset amount_due on pembayaran_lines
        print('reset amount due on siswa_biaya using potongan_biaya ...')
        for bayar in self.pembayaran_lines:
            self.env['siswa_keu_ocb11.siswa_biaya'].search([('id','=',bayar.biaya_id.id)]).write({
                'amount_due' : bayar.biaya_id.amount_due  + bayar.jumlah_potongan,
                'dibayar' : bayar.biaya_id.dibayar - bayar.jumlah_potongan,
            })

            # update amount_due on siswa
            print('update amount_due_biaya on siswa ...')
            self.siswa_id.write({
                'amount_due_biaya' : self.siswa_id.amount_due_biaya + bayar.jumlah_potongan
            })

            # reset status potongan_biaya
            if bayar.biaya_id.potongan_ids:
                for pot in bayar.biaya_id.potongan_ids:
                    pot.state = 'open'
            

    # override default action confirm (total replace)
    def action_confirm(self):
        self.ensure_one()
        # check if pembayaran is set or no
        if len(self.pembayaran_lines) > 0:
            # update state
            self.write({
                'state' : 'paid'
            })
            # set paid to siswa_biaya
            for bayar in self.pembayaran_lines:
                if bayar.bayar == bayar.amount_due - bayar.jumlah_potongan:
                    bayar.biaya_id.write({
                        'state' : 'paid',
                        'amount_due' : 0,
                        'dibayar' : bayar.biaya_id.dibayar + bayar.bayar,
                    })
                else:
                    bayar.biaya_id.write({
                        # 'amount_due' : bayar.biaya_id.amount_due - bayar.jumlah_potongan - bayar.bayar,
                        'amount_due' : bayar.biaya_id.amount_due - bayar.bayar,
                        'dibayar' : bayar.biaya_id.dibayar + bayar.bayar
                    })
                # update amount_due_biaya on siswa
                self.siswa_id.write({
                    'amount_due_biaya' : self.siswa_id.amount_due_biaya - bayar.bayar
                })

                # set potongan biaya to paid 
                if bayar.biaya_id.potongan_ids:
                    for pot_by in bayar.biaya_id.potongan_ids:
                        pot_by.state = 'paid'
            
            # add confirm progress to table action_confirm
            self.env['siswa_keu_ocb11.action_confirm'].create({
                'pembayaran_id' : self.id
            })
            

            # update kas statement per item pembayaran lines
            for pb in self.pembayaran_lines:
                akun_kas_id = self.env['siswa_keu_ocb11.kas_kategori'].search([('biaya_id','=',pb.biaya_id.biaya_id.id)]).id
                
                kas = self.env['siswa_keu_ocb11.kas'].create({
                    'tanggal' : self.tanggal,
                    'jumlah' : pb.bayar,
                    'pembayaran_id' : self.id ,
                    'is_related' : True ,
                    'kas_kategori_id' : akun_kas_id,
                })
                kas.action_confirm()

            # if is_potong_tabungan = True, maka potong tabungan
            if self.is_potong_tabungan:
                # create trans tabungan
                new_tab = self.env['siswa_tab_ocb11.tabungan'].create({
                    'siswa_id' : self.siswa_id.id,
                    'tanggal' : self.tanggal,
                    'jenis' : 'tarik',
                    'jumlah_temp' : self.jumlah_potongan_tabungan,
                    'desc' : 'Pembayaran ' + self.name,
                })
                new_tab.action_confirm()
                self.tabungan_id = new_tab.id
            
            # recompute keuangan dashboard
            self.recompute_keuangan_dashboard()

            # reload
            return self.reload_page()

        else:
            raise exceptions.except_orm(_('Warning'), _('There is no data to confirm, complete payment first!'))
