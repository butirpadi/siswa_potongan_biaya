from flectra import models, fields, api, _

class siswa_biaya(models.Model):
    _inherit = 'siswa_keu_ocb11.siswa_biaya'

    potongan_ids = fields.One2many('siswa.potongan_biaya',inverse_name='siswa_biaya_id')
                     