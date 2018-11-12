# -*- coding: utf-8 -*-
{
    'name': "Potongan Siswa Biaya",

    'summary': """
        Module for Potongan Biaya""",

    'description': """
        Module for Potongan Biaya
    """,

    'author': "Tepat Guna Karya",
    'website': "http://www.tepatguna.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'siswa_keu_ocb11', 'siswa_psb_ocb11'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/potongan_view.xml',
        'views/pembayaran_view.xml',
        'views/wizard_batch_create_potongan_view.xml',
        'views/calon_siswa_biaya_view.xml',
        # 'views/siswa_biaya.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,

} 