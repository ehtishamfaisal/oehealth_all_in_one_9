##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp.osv import osv, fields
import datetime

# Perinantal Monitor Management
class OeHealthPerinatalMonitor(osv.osv):
    _name = "oeh.medical.perinatal.monitor"
    _description = "Gyneco Perinatal Monitor"

    FETUS_POSITION = [
        ('Correct','Correct'),
        ('Occiput / Cephalic Posterior', 'Occiput / Cephalic Posterior'),
        ('Frank Breech', 'Frank Breech'),
        ('Complete Breech', 'Complete Breech'),
        ('Transverse Lie', 'Transverse Lie'),
        ('Footling Breech', 'Footling Breech'),
    ]

    _columns = {
        'name': fields.char('Internal Code', size=128, required=True, readonly=True),
        'date': fields.datetime('Date and Time', required=True),
        'systolic': fields.integer('Systolic Pressure'),
        'diastolic': fields.integer('Diastolic Pressure'),
        'contractions': fields.integer('Contractions'),
        'frequency': fields.integer('Mother\'s Heart Frequency'),
        'dilation': fields.integer('Cervix Dilation'),
        'f_frequency': fields.integer('Fetus Heart Frequency'),
        'meconium': fields.boolean('Meconium'),
        'bleeding': fields.boolean('Bleeding'),
        'fundal_height': fields.integer('Fundal Height'),
        'fetus_position': fields.selection(FETUS_POSITION, 'Fetus Position', select=True),
        'gyneco_id': fields.many2one('oeh.medical.gyneco','Gynecology', ondelete='cascade'),
    }
    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
        'date': datetime.datetime.now(),
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.perinatal.monitor') or '/'
        return super(OeHealthPerinatalMonitor, self).create(cr, uid, vals, context=context)


# Puerperium Monitor Management
class OeHealthPuerperiumMonitor(osv.osv):
    _name = "oeh.medical.puerperium.monitor"
    _description = "Gyneco Puerperium Monitor"

    LOCHIA_AMOUNT = [
        ('Normal','Normal'),
        ('Abundant', 'Abundant'),
        ('Hemorrhage', 'Hemorrhage'),
    ]

    LOCHIA_COLOR = [
        ('Rubra','Rubra'),
        ('Serosa', 'Serosa'),
        ('Alba', 'Alba'),
    ]

    LOCHIA_ODOR = [
        ('Normal','Normal'),
        ('Offensive', 'Offensive'),
    ]

    _columns = {
        'name': fields.char('Internal Code',size=128, required=True, readonly=True),
        'date': fields.datetime('Date and Time', required=True),
		'systolic': fields.integer('Systolic Pressure'),
		'diastolic': fields.integer('Diastolic Pressure'),
		'frequency': fields.integer('Heart Frequency'),
        'lochia_amount': fields.selection(LOCHIA_AMOUNT,'Lochia Amount'),
        'lochia_color': fields.selection(LOCHIA_COLOR,'Lochia Color'),
        'lochia_odor': fields.selection(LOCHIA_ODOR,'Lochia Odor'),
        'uterus_involution': fields.integer('Fundal Height', help="Distance between the symphysis pubis and the uterine fundus (S-FD) in cm"),
        'temperature': fields.float('Temperature'),
        'gyneco_id': fields.many2one('oeh.medical.gyneco','Gynecology', ondelete='cascade'),
    }

    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
        'date': datetime.datetime.now(),
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.puerperium.monitor') or '/'
        return super(OeHealthPuerperiumMonitor, self).create(cr, uid, vals, context=context)


# Gynecology Management
class OeHealthGyneco(osv.osv):
    _name = "oeh.medical.gyneco"
    _description = "Gynecology Management"

    LABOR_MODE = [
        ('Normal','Normal'),
        ('Induced', 'Induced'),
        ('C-section', 'C-section'),
    ]

    FETUS = [
        ('Correct','Correct'),
        ('Occiput / Cephalic Posterior', 'Occiput / Cephalic Posterior'),
        ('Frank Breech', 'Frank Breech'),
        ('Complete Breech', 'Complete Breech'),
        ('Transverse Lie', 'Transverse Lie'),
        ('Footling Breech','Footling Breech'),
    ]

    _columns = {
        'name': fields.char('Internal Code', size=128, required=True, readonly=True),
        'gravida_number': fields.integer('Gravida #'),
		'abortion': fields.boolean('Abortion'),
        'abortion_reason': fields.char('Abortion Reason', size=128),
		'admission_date': fields.datetime ('Admission Date',help="Date when she was admitted to give birth"),
        'prenatal_evaluations': fields.integer ('# of Visit to Doctor',help="Number of visits to the doctor during pregnancy"),
        'labor_mode': fields.selection(LABOR_MODE, 'Labor Starting Mode'),
        'gestational_weeks': fields.integer('Gestational Weeks'),
		'gestational_days': fields.integer('Gestational Days'),
        'fetus_presentation': fields.selection(FETUS, 'Fetus Presentation'),
        'placenta_incomplete': fields.boolean('Incomplete Placenta'),
		'placenta_retained': fields.boolean('Retained Placenta'),
		'episiotomy': fields.boolean('Episiotomy'),
		'vaginal_tearing': fields.boolean('Vaginal Tearing'),
        'forceps': fields.boolean('Use of Forceps'),
        'perinatal_ids': fields.one2many('oeh.medical.perinatal.monitor','gyneco_id','Perinatal'),
        'puerperium_ids': fields.one2many('oeh.medical.puerperium.monitor','gyneco_id','Puerperium'),
        'dismissed': fields.datetime('Dismissed from Hospital'),
		'died_at_delivery': fields.boolean('Died at Delivery Room'),
		'died_at_the_hospital': fields.boolean('Died at the Hospital'),
		'died_being_transferred': fields.boolean('Died being Transferred',help="The mother died being transferred to another health institution"),
        'notes': fields.text ('Notes'),
        'patient': fields.many2one('oeh.medical.patient','Patient', ondelete='cascade'),
    }

    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.gyneco') or '/'
        return super(OeHealthGyneco, self).create(cr, uid, vals, context=context)


# Inheriting Patient module to add "Gyanecology" screen reference
class OeHealthPatient(osv.osv):
    _inherit = 'oeh.medical.patient'
    _columns = {
        'currently_pregnant': fields.boolean('Currently Pregnant'),
		'fertile': fields.boolean('Fertile', help="Check if patient is in fertile age"),
		'menarche': fields.integer('Menarche Age'),
		'menopausal': fields.boolean('Menopausal'),
		'menopause': fields.integer('Menopause Age'),
		'mammography': fields.boolean('Mammography',help="Check if the patient does periodic mammographys"),
		'mammography_last': fields.date('Last Mammography',help="Enter the date of the last mammography"),
		'breast_self_examination': fields.boolean('Breast Self-examination',help="Check if the patient does and knows how to self examine her breasts"),
		'pap_test': fields.boolean('PAP Test',help="Check if the patient does periodic cytologic pelvic smear screening"),
		'pap_test_last': fields.date('Last PAP Test',help="Enter the date of the last Papanicolau test"),
		'colposcopy': fields.boolean('Colposcopy',help="Check if the patient has done a colposcopy exam"),
		'colposcopy_last': fields.date('Last Colposcopy',help="Enter the date of the last colposcopy"),
		'gravida': fields.integer('Gravida',help="Number of pregnancies"),
		'premature': fields.integer('Premature',help="Premature Deliveries"),
		'abortions': fields.integer('No of Abortions'),
		'full_term': fields.integer('Full Term', help="Full term pregnancies"),
		'gpa': fields.char('GPA',size=32,help="Gravida, Para, Abortus Notation. For example G4P3A1 : 4 Pregnancies, 3 viable and 1 abortion"),
		'born_alive': fields.integer('Born Alive'),
		'deaths_1st_week': fields.integer('Deceased during 1st week',help="Number of babies that die in the first week"),
		'deaths_2nd_week': fields.integer('Deceased after 2nd week',help="Number of babies that die after the second week"),
        'gyneco_ids': fields.one2many('oeh.medical.gyneco','patient','Perinatal'),
    }