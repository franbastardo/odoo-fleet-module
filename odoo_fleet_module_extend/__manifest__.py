# __manifest__.py
{
    'name': 'Gestión de Flota',
    'version': '1.0',
    'summary': 'Módulo para expandir funcionalidad del modulo nativo de flota de odoo.',
    'author': 'Francisco Bastardo',
    'category': 'Fleet',
    'depends': [
        'base',
        'contacts',
        'fleet',
    ],
    'data': [
        #Security and Access Control
        'security/fleet_security.xml',
        'security/ir.model.access.csv',
        # Data files
        'data/config_data.xml',
        'data/ir_sequence_data.xml',
        # Models
        'views/fleet_vehicle_views_inherit.xml',
        'views/res_partner_views.xml',
        'views/api_log_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

    'external_dependencies': {
        'python': ['requests'],
    },
}