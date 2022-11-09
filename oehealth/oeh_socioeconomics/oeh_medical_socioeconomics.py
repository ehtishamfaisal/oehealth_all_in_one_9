##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp import pooler, tools, api
from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _
from datetime import timedelta

# Occupation Master table
class OeHealthOccupations(osv.osv):
    _name = "oeh.medical.occupation"
    _columns = {
        'name' : fields.char('Occupation', size=128, required=True),
        'code' : fields.char('Code', size=128),
    }
    _order = 'code'
    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'The occupation name must be unique !')]

# Inherit Patient screen to add Socioeconomics fields

class OeHealthPatient(osv.osv):
    _inherit = 'oeh.medical.patient'

    SOCIO_STATUS = [
        ('Lower', 'Lower'),
        ('Lower-middle', 'Lower-middle'),
        ('Middle', 'Middle'),
        ('Middle-upper', 'Middle-upper'),
        ('Higher', 'Higher'),
    ]

    EDUCATION_LEVEL = [
        ('None', 'None'),
        ('Incomplete Primary School', 'Incomplete Primary School'),
        ('Primary School', 'Primary School'),
        ('Incomplete Secondary School', 'Incomplete Secondary School'),
        ('Secondary School', 'Secondary School'),
        ('University', 'University'),
    ]

    HOUSING_CONDITION = [
        ('Shanty, deficient sanitary conditions', 'Shanty, deficient sanitary conditions'),
        ('Small, crowded but with good sanitary conditions', 'Small, crowded but with good sanitary conditions'),
        ('Comfortable and good sanitary conditions', 'Comfortable and good sanitary conditions'),
        ('Roomy and excellent sanitary conditions', 'Roomy and excellent sanitary conditions'),
        ('Luxury and excellent sanitary conditions', 'Luxury and excellent sanitary conditions'),
    ]

    APGAR_HELP = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    APGAR_DISCUSSION = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    APGAR_DESICIONS = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    APGAR_TIMESHARING = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    APGAR_AFFECTION = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    INCOME = [
        ('High', 'High'),
        ('Medium / Average', 'Medium / Average'),
        ('Low', 'Low'),
    ]

    _columns = {
        'socioeconomics': fields.selection(SOCIO_STATUS, 'Socioeconomics',help="SES - Socioeconomic Status"),
        'education_level': fields.selection(EDUCATION_LEVEL, 'Education Level'),
        'housing_condition': fields.selection(HOUSING_CONDITION, 'Housing conditions',help="Housing and sanitary living conditions"),
        'hostile_area' : fields.boolean('Hostile Area', help="Check this box if the patient lives in a zone of high hostility (eg, war)"),
		'sewers': fields.boolean('Sanitary Sewers'),
		'water': fields.boolean('Running Water'),
		'trash': fields.boolean('Trash recollection'),
		'electricity': fields.boolean('Electrical supply'),
		'gas': fields.boolean('Gas supply'),
		'telephone': fields.boolean('Telephone'),
		'television': fields.boolean('Television'),
		'internet': fields.boolean('Internet'),
		'single_parent': fields.boolean('Single parent family'),
		'domestic_violence': fields.boolean('Domestic violence'),
		'working_children': fields.boolean('Working children'),
		'teenage_pregnancy': fields.boolean('Teenage pregnancy'),
		'sexual_abuse': fields.boolean('Sexual abuse'),
		'drug_addiction': fields.boolean('Drug addiction'),
		'school_withdrawal': fields.boolean('School withdrawal'),
		'prison_past': fields.boolean('Has been in prison'),
		'prison_current': fields.boolean('Is currently in prison'),
		'relative_in_prison': fields.boolean('Relative in prison',help="Check if someone from the nuclear family - parents / sibblings  is or has been in prison"),
		'info' : fields.text("Extra info"),
        'apgar_help': fields.selection(APGAR_HELP, 'Family Help',help="Is the patient satisfied with the level of help coming from the family when there is a problem ?"),
        'apgar_discussion': fields.selection(APGAR_DISCUSSION, 'Family discussions on problems',help="Is the patient satisfied with the level talking over the problems as family ?"),
        'apgar_decision': fields.selection(APGAR_DESICIONS, 'Family decision ability',help="Is the patient satisfied with the level of making important decisions as a group ?"),
        'apgar_timesharing': fields.selection(APGAR_TIMESHARING, 'Family time sharing',help="Is the patient satisfied with the level of time that they spend together ?"),
        'apgar_affection': fields.selection(APGAR_AFFECTION, 'Family affection',help="Is the patient satisfied with the level of affection coming from the family ?"),
        'income': fields.selection(INCOME, 'Income (Monthly)',help="Patient's monthly income"),
        'occupation': fields.many2one('oeh.medical.occupation','Occupation'),
		'works_at_home': fields.boolean('Works at home',help="Check if the patient works at his / her house"),
		'hours_outside': fields.integer('Hours stay outside home',help="Number of hours a day the patient spend outside the house"),
    }