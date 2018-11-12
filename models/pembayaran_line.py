
from flectra import models, fields, api
from flectra.addons import decimal_precision as dp
from pprint import pprint

class pembayaran_line(models.Model):
    _inherit = 'siswa_keu_ocb11.pembayaran_line'

    # jumlah_potongan = fields.Float(string='Potongan')
    jumlah_potongan = fields.Float('Potongan', compute="_compute_potongan")
    # potongannya = fields.Float(string='Potongan', related="siswa_biaya_id.potongan_ids")

    # @api.onchange('biaya_id')
    # def biaya_id_change(self):
    #     # get jumlah ptongan
    #     print('Get jumlah potongan .........')
    #     if self.biaya_id.potongan_ids and self.biaya_id.potongan_ids.state == 'open' :
    #         self.jumlah_potongan = self.biaya_id.potongan_ids.jumlah_potongan
    #         self.bayar = self.amount_due - self.jumlah_potongan
    #         print(self.jumlah_potongan)
    
    @api.depends('biaya_id')
    def _compute_potongan(self):
        for rec in self:
            jml_pot = 0
            for pot in rec.biaya_id.potongan_ids:
                jml_pot += pot.jumlah_potongan
            rec.jumlah_potongan = jml_pot
            # rec.bayar = rec.amount_due - jml_pot
            # print('inside _compute_potongan on pembayaran_line')
            # print(rec.jumlah_potongan)
            # print(jml_pot)
            # print(rec.amount_due)
            # print(rec.bayar)
            # pprint(rec) 