{
    'name': 'SFHealth - Patient Walkins Management',
    'version': '1.0',
    'author': "Solutionfounder",
    'category': 'Medical',
    'summary': 'Quickly record daily patient walkins',
    'depends': ['oehealth'],
    'price': 50,
    'currency': 'EUR',
    'description': """

Features Includes:

- Manage Physician Walkin schedules
- Register Daily patient walkins and view it by date
- Generate invoice for each walkin
- View related details like Evaluation, Vaccines, Prescriptions and Admissions for each walkins


""",
    "website": "http://solutionfounder.com",
    "data": [

        'views/oeh_medical_register_for_walkin_view.xml',
        'sequence/oeh_sequence.xml',
        'security/oeh_security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',

    ],
    'images': ['images/main_screenshot.png'],
    "demo": [

    ],
    'test':[
    ],
    'css': [

    ],
    'js': [

    ],
    'qweb': [

    ],
    "active": False
}