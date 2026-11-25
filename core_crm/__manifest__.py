{
    'name': "Core CRM",

    'summary': "Keep track of sales leads",

    'description': "Create and manage sales leads with contact details and notes.",

    'author': "My Company",

    'category': 'Sales/CRM',
    'version': '2.9',

    'depends': ['base'],

    'data': [
        # Odoo 20 stores model access rules in ir.access.csv.
        'security/ir.access.csv',
        'views/views.xml',
        'views/core_crm_tag.xml',
        'views/core_crm_pipeline.xml',
        'views/core_crm_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'core_crm/static/src/css/tag_color.css',
            'core_crm/static/src/js/tag_color_picker.js',
            'core_crm/static/src/js/lead_tag_list.js',
            'core_crm/static/src/js/lead_color_tags.js',
            'core_crm/static/src/xml/tag_color_picker.xml',
            'core_crm/static/src/xml/lead_tag_list.xml',
            'core_crm/static/src/xml/lead_color_tags.xml',
        ],
    },
}

