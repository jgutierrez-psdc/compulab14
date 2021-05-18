# -*- coding: utf-8 -*-
{
    "name": "Propuesta Comercial",
    "summary": "Módulo para la creaciones de propuestas comerciales",
    "description": """
        Módulo para la creaciones de propuestas comerciales.
    """,
    "author": "PSDC Innova",
    "website": "https://psdc.com.pa/",
    "category": "Projects",
    "version": "1.1.0",
    "depends": ['base', 'contacts', 'mail'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sale_comercial_sequence.xml',
        'views/sale_comercial_views.xml',
        'report/sale_comercials_report.xml',
        'report/sale_comercials_report_templates.xml',
        'data/mail_template_data.xml',
    ],
    'qweb': [],
    "demo": [],
    'installable': True,
    'application': True
}