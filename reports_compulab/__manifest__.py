# -*- coding: utf-8 -*-
{
    'name': "reports_compulab",

    'summary': """
        Vista personalizada de los reportes""",

    'description': """
        Vista personalizada de los reportes
    """,

    'author': "PSDC",
    'website': "http://www.psdc.com.pa",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Ventas',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/template.xml',
    ],
    'css':[
        'static/src/css/customlab.css',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}