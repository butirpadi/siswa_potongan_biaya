# -*- coding: utf-8 -*-
from flectra import http

# class /media/eries/mywork/flectra-erp/customAddons/11/siswaPotonganBiaya(http.Controller):
#     @http.route('//media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya//media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya//media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya.listing', {
#             'root': '//media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya//media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya',
#             'objects': http.request.env['/media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya./media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya'].search([]),
#         })

#     @http.route('//media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya//media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya/objects/<model("/media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya./media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/media/eries/mywork/flectra-erp/custom_addons/11/siswa_potongan_biaya.object', {
#             'object': obj
#         }) 