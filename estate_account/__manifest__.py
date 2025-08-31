{
    'name': 'Real Estate Account',
    'author': 'Abdulrahman Fouad',
    'version': '18.0.0.1.0',
    'license': 'LGPL-3',
    'category': 'Training',
    'summary': 'My second module for training on odoo 18',
    'sequence': 10,
    'description': """Real Estate Account module training module from Odoo docs""",
    'depends': ['estate', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_account_view.xml',
    ],
    'assets': {
    },
    'application': True,
}

