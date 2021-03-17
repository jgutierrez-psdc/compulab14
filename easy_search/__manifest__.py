# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Advanced Search & Easy Search",
    "summary": "Search In Relational Fields (Many2one,many2many) \n "
               "By different fields defined in configuration (Base).",
    'description': """
        Advanced Search & Easy Search In Relational Fields (Many2one,many2many) \n 
        By different fields defined in configuration.
    """,
    "version": "13.0.1.0.0",
    "category": "general",
    "website": "",
    "author": "Mahmoud Ramadan",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "product",
    ],
    "data": [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/easy_search.xml',
        'views/res_config.xml',
    ],
    'images': ['static/description/6.png'],
    'price': 5.0,
    'currency': 'EUR',
}
