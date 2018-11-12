# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from pprint import pprint
from datetime import datetime, date
import calendar

class calon_siswa(models.Model):
    _inherit = 'siswa_psb_ocb11.calon_siswa'

    qty = fields.Integer('Qty', default=1)

    # override on generate pembayaran default
    def generate_pembayaran_default(self):
        super(calon_siswa, self).generate_pembayaran_default()
        # recalculate jumlah harga
        for by in self.payment_lines:
            if by.biaya_id.is_bulanan:
                by.qty = 12
            
            by.jumlah_harga = (by.harga - by.potongan_harga) * by.qty
            # by.dibayar = by.jumlah_harga
            by.dibayar = (by.harga - by.potongan_harga) * by.qty
    
    def generate_biaya_optional(self):
        newid = super(calon_siswa, self).generate_biaya_optional()
        # print('tampilkan biaya optional')
        # pprint(newid)
        if newid.biaya_id.is_bulanan:
            newid.qty = 12
            newid.jumlah_harga = (newid.harga - newid.potongan_harga) * newid.qty
            # newid.dibayar = newid.jumlah_harga
            newid.dibayar = (newid.harga - newid.potongan_harga) * newid.qty
    
    # override calculate bayar tunai, (replace)
    def calculate_bayar_tunai(self):
        print('inside inherited calculate_bayar_tunai')
        tunai = self.bayar_tunai
        for pay_line in self.payment_lines:
            if tunai > 0 :
                if tunai > pay_line.jumlah_harga :
                    # dibayar = (pay_line.qty * pay_line.harga) - pay_line.potongan_harga
                    dibayar = pay_line.qty * (pay_line.harga - pay_line.potongan_harga)
                    pay_line.dibayar = dibayar
                    tunai -= pay_line.dibayar
                else:
                    pay_line.dibayar = tunai
                    tunai = 0
            else:
                # jika tunai tidak mencukupi maka hapus saja payment nya
                # pay.unlink()
                # ralat jika tunai tidak mencukupi makan set bayar = 0 
                pay_line.dibayar = 0

    # override action confirm (replace)
    def action_confirm(self):
        # check pembayaran is set or not
        if len(self.payment_lines) > 0:
            # register siswa to res.partner
            if self.is_siswa_lama:
                # update siswa lama
                self.env['res.partner'].search([('id','=',self.siswa_id.id)]).write({
                    # 'rombels' : [(0, 0,  { 'rombel_id' : self.rombel_id.id, 'tahunajaran_id' : self.tahunajaran_id.id })],
                    # 'active_rombel_id' : self.rombel_id.id,
                    'is_siswa_lama' : True,
                    'calon_siswa_id' : self.id, 
                })
            else:
                # insert into res_partner
                new_siswa = self.env['res.partner'].create({
                    'is_customer' : 1,
                    'name' : self.name, 
                    'calon_siswa_id' : self.id, 
                    'street' : self.street,
                    'street2' : self.street2,
                    'zip' : self.zip,
                    'city' : self.city,
                    'state_id' : self.state_id.id,
                    'country_id' : self.country_id.id,
                    'phone' : self.phone,
                    'mobile' : self.mobile,
                    'tanggal_registrasi' : self.tanggal_registrasi,
                    'tahunajaran_id' : self.tahunajaran_id.id,
                    'nis' : self.nis,
                    'panggilan' : self.panggilan,
                    'jenis_kelamin' : self.jenis_kelamin,
                    'tanggal_lahir' : self.tanggal_lahir,
                    'tempat_lahir' : self.tempat_lahir, 
                    'alamat' : self.alamat,
                    'telp' : self.telp,
                    'ayah' : self.ayah,
                    'pekerjaan_ayah_id' : self.pekerjaan_ayah_id.id,
                    'telp_ayah' : self.telp_ayah,
                    'ibu' : self.ibu,
                    'pekerjaan_ibu_id' : self.pekerjaan_ibu_id.id,
                    'telp_ibu' : self.telp_ibu,
                    # 'rombels' : [(0, 0,  { 'rombel_id' : self.rombel_id.id, 'tahunajaran_id' : self.tahunajaran_id.id })],
                    # 'active_rombel_id' : self.rombel_id.id,
                    'is_siswa' : True,
                    'anak_ke' : self.anak_ke,
                    'dari_bersaudara' : self.dari_bersaudara
                })
                # self.siswa_id = new_siswa.id 
                self.registered_siswa_id = new_siswa.id
                # self.siswa_id = new_siswa.id

            # update state
            self.state = 'reg'

            # assign siswa biaya
            # get tahunajaran_jenjang
            ta_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([('tahunajaran_id', '=', self.tahunajaran_id.id),
            ('jenjang_id', '=', self.jenjang_id.id)
            ])
            
            # assign biaya to siswa
            total_biaya = 0.0
            if self.is_siswa_lama:
                id_siswa = self.siswa_id.id 
            else:
                id_siswa = new_siswa.id

            for by in ta_jenjang.biayas:

                # cek biaya apakah is_optional dan apakah di pilih dalam payment_lines
                by_found = False
                if by.biaya_id.is_optional:
                    for by_in_pay in self.payment_lines:
                        if by.biaya_id.id == by_in_pay.biaya_id.id:
                            by_found = True
                    if not by_found:
                        continue
                        
                if self.is_siswa_lama and by.biaya_id.is_siswa_baru_only:
                    print('skip')
                    continue
                else:
                    print('JENJANG ID : ' + str(self.jenjang_id.id))
                    if by.biaya_id.is_bulanan:
                        for bulan_index in range(1,13):
                            harga = by.harga
                            
                            if by.is_different_by_gender:
                                if self.jenis_kelamin == 'perempuan':
                                    harga = by.harga_alt

                            self.env['siswa_keu_ocb11.siswa_biaya'].create({
                                'name' : by.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                                'siswa_id' : id_siswa,
                                'tahunajaran_id' : self.tahunajaran_id.id,
                                'biaya_id' : by.biaya_id.id,
                                'bulan' : bulan_index,
                                'harga' : harga,
                                'amount_due' : harga,
                                'jenjang_id' : self.jenjang_id.id
                            })
                            total_biaya += harga
                    else:
                        harga = by.harga
                        
                        if by.is_different_by_gender:
                            if self.jenis_kelamin == 'perempuan':
                                harga = by.harga_alt

                        self.env['siswa_keu_ocb11.siswa_biaya'].create({
                            'name' : by.biaya_id.name,
                            'siswa_id' : id_siswa,
                            'tahunajaran_id' : self.tahunajaran_id.id,
                            'biaya_id' : by.biaya_id.id,
                            'harga' : harga,
                            'amount_due' : harga,
                            'jenjang_id' : self.jenjang_id.id
                        })
                        total_biaya += harga
            
            # add potongan biaya
            for pay_a in self.payment_lines:
                if pay_a.potongan_harga > 0:
                    if pay_a.biaya_id.is_bulanan:
                        print('inside biaya is bulanan')
                        biaya_bulanan_ids = self.env['siswa_keu_ocb11.siswa_biaya'].search([
                                        ('siswa_id','=',id_siswa),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ('biaya_id','=',pay_a.biaya_id.id),
                                        # ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ])
                        for by_bul in biaya_bulanan_ids:
                            a_pot = self.env['siswa.potongan_biaya'].create({
                                'siswa_id' : id_siswa,
                                'siswa_biaya_id' : by_bul.id,
                                'jumlah_potongan' : pay_a.potongan_harga
                            })
                            a_pot.action_confirm()
                    else:
                        print('inside biaya not bulanan')
                        print(id_siswa)
                        print(pay_a.biaya_id.id)
                        print(self.tahunajaran_id.id)
                        siswa_by_id = self.env['siswa_keu_ocb11.siswa_biaya'].search([
                                        ('siswa_id','=',id_siswa),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ('biaya_id','=',pay_a.biaya_id.id),
                                        # ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ]).id
                        # siswa_by_id = self.env['siswa_keu_ocb11.siswa_biaya'].search([
                        #                         ('id','=',id_siswa),
                        #                         ('biaya_id','=',pay_a.biaya_id.id),
                        #                         ('tahunajaran_id','=',self.tahunajaran_id.id),
                        #                     ])
                        pprint(siswa_by_id)
                        a_pot = self.env['siswa.potongan_biaya'].create({
                            'siswa_id' : id_siswa,
                            'siswa_biaya_id' : siswa_by_id,
                            'jumlah_potongan' : pay_a.potongan_harga
                        })
                        a_pot.action_confirm()

        #     # set total_biaya dan amount_due
        #     # total_biaya = sum(by.harga for by in self.biayas)
        #     print('ID SISWA : ' + str(id_siswa))
        #     res_partner_siswa = self.env['res.partner'].search([('id','=',id_siswa)])
        #     self.env['res.partner'].search([('id','=',id_siswa)]).write({
        #         'total_biaya' : total_biaya,
        #         'amount_due_biaya' : res_partner_siswa.amount_due_biaya + total_biaya,
        #     })         

            # add pembayaran
            pembayaran = self.env['siswa_keu_ocb11.pembayaran'].create({
                'tanggal' : self.tanggal_registrasi ,
                'tahunajaran_id' : self.tahunajaran_id.id,
                'siswa_id' : id_siswa,
            })

            # reset pembayaran_lines
            pembayaran.pembayaran_lines.unlink()
            pembayaran.total = 0

            total_bayar = 0.0
            for pay in self.payment_lines:

                print('Payment Lines : ')
                print('harga : ' + str(pay.harga))
                print('dibayar : ' + str(pay.dibayar))
                print('biaya_id : ' + str(pay.biaya_id.id))

                # get siswa_biaya
                if pay.dibayar > 0: # jangan dimasukkan ke pembayaran untuk yang nilai dibayarnya = 0
                    if pay.biaya_id:
                        if pay.biaya_id.is_bulanan:
                            # pay_biaya_id = self.env['siswa_keu_ocb11.siswa_biaya'].search([
                            #             ('siswa_id','=',id_siswa),
                            #             ('tahunajaran_id','=',self.tahunajaran_id.id),
                            #             ('biaya_id','=',pay.biaya_id.id),
                            #             ('tahunajaran_id','=',self.tahunajaran_id.id),
                            #             ('bulan','=',pay.bulan),
                            #             ]).id
                            # untuk section ini diganti sesuai dengan ketentuan potongan biaya
                            biaya_bulanan_ids = self.env['siswa_keu_ocb11.siswa_biaya'].search([
                                        ('siswa_id','=',id_siswa),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ('biaya_id','=',pay.biaya_id.id),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ])
                            dibayar_untuk_biaya_ini = pay.dibayar
                            for by_bln in biaya_bulanan_ids:
                                if dibayar_untuk_biaya_ini > 0:
                                    if dibayar_untuk_biaya_ini > by_bln.harga:
                                        pembayaran.pembayaran_lines =  [(0, 0,  { 
                                                            'biaya_id' : by_bln.id, 
                                                            'jumlah_potongan' : pay.potongan_harga, 
                                                            'amount_due' : by_bln.amount_due, 
                                                            'bayar' : by_bln.harga - pay.potongan_harga
                                                            })]
                                        dibayar_untuk_biaya_ini -= (by_bln.harga - pay.potongan_harga)
                                        total_bayar += by_bln.harga
                                    else:
                                        pembayaran.pembayaran_lines =  [(0, 0,  { 
                                                            'biaya_id' : by_bln.id, 
                                                            'jumlah_potongan' : pay.potongan_harga, 
                                                            'amount_due' : by_bln.amount_due, 
                                                            'bayar' : dibayar_untuk_biaya_ini 
                                                            })]
                                        total_bayar += dibayar_untuk_biaya_ini
                                        dibayar_untuk_biaya_ini = 0
                        else:
                            pay_biaya_id = self.env['siswa_keu_ocb11.siswa_biaya'].search([
                                        ('siswa_id','=',id_siswa),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ('biaya_id','=',pay.biaya_id.id),
                                        # ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ])

                            # ini juga di rubah
                            pembayaran.pembayaran_lines =  [(0, 0,  { 
                                                    'biaya_id' : pay_biaya_id.id, 
                                                    'jumlah_potongan' : pay.potongan_harga, 
                                                    'amount_due' : pay_biaya_id.amount_due, 
                                                    'bayar' : pay.dibayar 
                                                    })]
                            total_bayar += pay.dibayar
                
                print('pay_biaya_id : ' + str(pay_biaya_id))
                print('-------------------')

            # raise exceptions.except_orm(_('Warning'), _('TEST ERROR'))

            # confirm pembayaran 
            pembayaran.action_confirm()

            # set terbilang
            if total_bayar == 0:
                self.terbilang = 'nol'
            else:
                t = self.terbilang_(total_bayar)
                while '' in t:
                    t.remove('')
                self.terbilang = ' '.join(t) 
            
            self.terbilang += ' Rupiah'
            # set total
            self.total = total_bayar

            # raise exceptions.except_orm(_('Warning'), _('You can not delete Done state data'))
        else:
            raise exceptions.except_orm(_('Warning'), _('Can not confirm this registration, complete payment first!'))

