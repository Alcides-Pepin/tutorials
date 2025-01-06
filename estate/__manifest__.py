{
    'name': 'Real Estate',
    'version': '18.0.1.0',
    'category': 'Customizations',
    'sequence': 10,
    'summary': 'Module for managing activities',
    'description': """
    Module for managing activities
    """,
    'author': 'Pépin, Alcides DE OLIVEIRA GUERRA',
    'depends': ['base'],
    'data': [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_menus.xml",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
