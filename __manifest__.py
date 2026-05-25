{
    'name': 'HMS',
    'version': '4.0',
    'description': 'a module to manage hospital',
    'author': 'Merzk',
    'depends': ['base', 'crm'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'report/hms_patient_report.xml',
        'views/hms_department_views.xml',
        'views/hms_doctors_views.xml',
        'views/hms_patient_views.xml',
        'views/hms_menus.xml',
        'views/hms_crm_customer_views.xml',
    ],
    'installable': True,
    'application': True,
}
