{
    'name': 'SFHealth Extra Addons',
    'version': '1.0',
    'author': "Solutionfounder",
    'category': 'Generic Modules/Medical',
    'summary': 'Pediatrics, Nursing, Surgical, Ophthalmology, Imaging, Neglected Tropical Diseases and Procedure Coding System Management',
    'depends': ['oehealth','product'],
    'description': """

About SFHealth Extra Addons
----------------------------


1) Pediatrics Management:

- Newborn Baby & APGAR Management
- Pediatrics Symptom Checklist
- WHO Pediatrics Growth Chart

2) Surgical Management

- Manage complete details of the Surgery
- Revised Cardiac Risk Index
- Supplies related to the surgery
- Record details of Team Involved in the surgery

3) Ophthalmology Management

- Ophthalmology Visits
- Ophthalmology Findings

4) Nursing & Ambulatory Management

- Manage daily roundings and record details of patients during each rounding.
- Patient Ambulatory care management

5) Imaging Management

- Management of different imaging tests like X-Ray, Ultrasound, MRI, CT Scan and PET Scan
- Choose from existing test types or add custom one
- Print the report and generate invoice for the tests

6) Neglected Tropical Diseases Management

- Domiciliary Unit Management
- Chagas DU Entomological Survey Management
- Surveillance and management of Dengue fever

7) Record complete historical report based on Patient's Evaluation

8) Procedure Coding System for Medical : ICD-10-PCS

""",
    "website": "http://solutionfounder.com",
    "data": [
        'sequence/oeh_sequence.xml',

        'oeh_pediatrics/views/res_partner_view.xml',
        'oeh_pediatrics/views/oeh_medical_pediatrics_newborn_view.xml',
        'oeh_pediatrics/views/oeh_medical_pediatrics_pcs_view.xml',
        'oeh_pediatrics/views/oeh_medical_pediatrics_growth_chart_view.xml',
        'oeh_pediatrics/data/oeh_medical_wfa_boys_p.xml',
        'oeh_pediatrics/data/oeh_medical_wfa_boys_z.xml',
        'oeh_pediatrics/data/oeh_medical_wfa_girls_p.xml',
        'oeh_pediatrics/data/oeh_medical_wfa_girls_z.xml',
        'oeh_pediatrics/data/oeh_medical_lhfa_boys_p.xml',
        'oeh_pediatrics/data/oeh_medical_lhfa_boys_z.xml',
        'oeh_pediatrics/data/oeh_medical_lhfa_girls_p.xml',
        'oeh_pediatrics/data/oeh_medical_lhfa_girls_z.xml',
        'oeh_pediatrics/data/oeh_medical_bmi_boys_p.xml',
        'oeh_pediatrics/data/oeh_medical_bmi_boys_z.xml',
        'oeh_pediatrics/data/oeh_medical_bmi_girls_p.xml',
        'oeh_pediatrics/data/oeh_medical_bmi_girls_z.xml',

        "oeh_icd10pcs/views/oeh_icd10pcs_view.xml",

        'oeh_surgery/views/oeh_medical_healthcenters_view.xml',
        'oeh_surgery/views/oeh_medical_surgery_view.xml',

        'oeh_ophthalmology/views/oeh_medical_ophthalmology_view.xml',
        'oeh_ophthalmology/views/oeh_medical_ophthalmology_report.xml',
        'oeh_ophthalmology/views/oeh_medical_report.xml',

        "oeh_nursing/views/oeh_medical_nursing_view.xml",
        "oeh_nursing/views/oeh_medical_rounding_report.xml",
        "oeh_nursing/views/oeh_medical_report.xml",

        "oeh_imaging/views/oeh_medical_imaging_view.xml",
        "oeh_imaging/views/report_patient_imaging.xml",
        "oeh_imaging/views/oeh_medical_imaging_report.xml",
        "oeh_imaging/data/oeh_imaging_test_types.xml",

        "oeh_ntd/views/oeh_medical_domiciliary_unit_view.xml",
        "oeh_ntd/views/oeh_medical_ntd_chagas_view.xml",
        "oeh_ntd/views/oeh_medical_ntd_dengue_view.xml",
        "oeh_ntd/data/oeh_lab_test_types.xml",

        "oeh_evaluation_history/views/oeh_medical_evaluation_report.xml",
        "oeh_evaluation_history/views/oeh_medical_report.xml",

        'security/oeh_security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',

        "oeh_icd10pcs/data/oeh_icd_10_pcs_2009_part1.xml",
        "oeh_icd10pcs/data/oeh_icd_10_pcs_2009_part2.xml",
        "oeh_icd10pcs/data/oeh_icd_10_pcs_2009_part3.xml",
    ],
    "images": ['images/main_screenshot.png'],
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