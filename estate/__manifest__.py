{
    'name': 'Real Estate',
    'author': 'Abdulrahman Fouad',
    'version': '18.0.0.1.0',
    'license': 'LGPL-3',
    'category': 'Training',
    'summary': 'My first module for training on odoo 18',
    'sequence': 10,
    'description': """Real Estate module training module from Odoo docs""",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_offer_view.xml',
    ],
    'assets': {
        },
    'application': True,
}

