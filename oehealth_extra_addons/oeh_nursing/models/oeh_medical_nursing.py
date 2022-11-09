
from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _

# Patient Roundings Management

class OeHealthPatientRoundingProcedures (osv.osv):
    _name = 'oeh.medical.patient.rounding.procedure'
    _description = 'Patient Procedures For Roundings'

    _columns = {
        'name': fields.many2one('oeh.medical.patient.rounding', 'Rouding'),
        'procedures': fields.many2one('oeh.medical.procedure', 'Procedures', required=True),
        'notes': fields.text('Notes'),
    }

class OeHealthPatientRoundingMedicines (osv.osv):
    _name = 'oeh.medical.patient.rounding.medicines'
    _description = 'Patient Medicines For Roundings'

    _columns = {
        'name': fields.many2one('oeh.medical.patient.rounding', 'Rouding'),
        'medicine': fields.many2one('oeh.medical.medicines', 'Medicines', domain=[('medicament_type','=','Medicine')], required=True),
        'qty': fields.integer("Quantity"),
        'notes': fields.text('Comment'),
    }
    _defaults = {
        'qty': lambda *a: 1,
    }

class OeHealthPatientRoundingManagement (osv.osv):
    _name = 'oeh.medical.patient.rounding'
    _description = 'Patient Rounding Management'

    STATUS = [
        ('Draft', 'Draft'),
        ('Completed', 'Completed'),
    ]

    EVOLUTION = [
        ('Status Quo', 'Status Quo'),
        ('Improving', 'Improving'),
        ('Worsening', 'Worsening'),
    ]

    def _get_patient_rounding(self, cr, uid, context=None):
        """Return default physician value"""
        therapist_id = []
        therapist_obj = self.pool.get('oeh.medical.physician')
        domain = [('oeh_user_id', '=', uid)]
        user_ids = therapist_obj.search(cr, uid, domain, context=context)
        if user_ids:
            return user_ids[0] or False
        else:
            return False

    _columns = {
        'name': fields.char('Rounding #', size=128, readonly=True),
        'inpatient_id': fields.many2one('oeh.medical.inpatient','Registration Code', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'patient': fields.many2one ('oeh.medical.patient','Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'doctor': fields.many2one('oeh.medical.physician','Physician', help="Physician Name", domain=[('is_pharmacist','=',False)], required=True, readonly=True,states={'Draft': [('readonly', False)]}),
        'evaluation_start_date': fields.datetime('Start date & time', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'evaluation_end_date': fields.datetime('End date & time', readonly=True, states={'Draft': [('readonly', False)]}),
        'environmental_assessment': fields.char('Environment', help="Environment assessment. State any disorder in the room.", size=128, readonly=True, states={'Draft': [('readonly', False)]}),
        'weight': fields.integer('Weight', help="Measured weight, in kg", readonly=True, states={'Draft': [('readonly', False)]}),
        'pain': fields.boolean('Pain', help="Check if the patient is in pain", readonly=True, states={'Draft': [('readonly', False)]}),
        'pain_level': fields.boolean('Pain Level', help="Enter the pain level, from 1 to 10", readonly=True, states={'Draft': [('readonly', False)]}),
        'potty': fields.boolean('Potty', help="Check if the patient needs to urinate / defecate", readonly=True, states={'Draft': [('readonly', False)]}),
        'position': fields.boolean('Position', help="Check if the patient needs to be repositioned or is unconfortable", readonly=True, states={'Draft': [('readonly', False)]}),
        'proximity': fields.boolean('Proximity', help="Check if personal items, water, alarm, ... are not in easy reach", readonly=True, states={'Draft': [('readonly', False)]}),
        'pump': fields.boolean('Pumps', help="Check if personal items, water, alarm, ... are not in easy reach", readonly=True, states={'Draft': [('readonly', False)]}),
        'personal_needs': fields.boolean('Personal needs', help="Check if the patient requests anything", readonly=True, states={'Draft': [('readonly', False)]}),
        'systolic': fields.integer('Systolic Pressure', readonly=True, states={'Draft': [('readonly', False)]}),
        'diastolic': fields.integer('Diastolic Pressure', readonly=True, states={'Draft': [('readonly', False)]}),
        'bpm': fields.integer('Heart Rate', help="Heart rate expressed in beats per minute", readonly=True, states={'Draft': [('readonly', False)]}),
        'respiratory_rate': fields.integer('Respiratory Rate', help="Respiratory rate expressed in breaths per minute", readonly=True, states={'Draft': [('readonly', False)]}),
        'osat': fields.integer('Oxygen Saturation', help="Oxygen Saturation(arterial)", readonly=True, states={'Draft': [('readonly', False)]}),
        'temperature': fields.float('Temperature', help="Temperature in celsius", readonly=True, states={'Draft': [('readonly', False)]}),
        'diuresis': fields.integer('Diuresis', help="volume in ml", readonly=True, states={'Draft': [('readonly', False)]}),
        'urinary_catheter': fields.integer('Urinary Catheter', readonly=True, states={'Draft': [('readonly', False)]}),
        'glycemia': fields.integer('Glycemia', help="Blood Glucose level", readonly=True, states={'Draft': [('readonly', False)]}),
        'depression': fields.boolean('Depression Signs', help="Check this if the patient shows signs of depression", readonly=True, states={'Draft': [('readonly', False)]}),
        'evolution': fields.selection(EVOLUTION, 'Evolution', readonly=True, states={'Draft': [('readonly', False)]}),
        'round_summary': fields.text("Round Summary", readonly=True, states={'Draft': [('readonly', False)]}),
        'warning': fields.boolean('Warning', help="Check this box to alert the supervisor about this patient rounding. A warning icon will be shown in the rounding list", readonly=True, states={'Draft': [('readonly', False)]}),
        'procedures': fields.one2many('oeh.medical.patient.rounding.procedure', 'name', 'Procedures', help="List of the procedures in this rounding. Please enter the first one as the main procedure", readonly=True, states={'Draft': [('readonly', False)]}),
        'medicaments': fields.one2many('oeh.medical.patient.rounding.medicines', 'name', 'Medicines', help="List of the medicines assigned in this rounding", readonly=True, states={'Draft': [('readonly', False)]}),
        'state': fields.selection(STATUS, 'State',readonly=True),
    }
    _defaults = {
        'evaluation_start_date': datetime.datetime.now(),
        'name': lambda obj, cr, uid, context: '/',
        'state': lambda *a: 'Draft',
        'doctor': _get_patient_rounding,
    }

    # Preventing deletion of a rounding details which is not in draft state
    def unlink(self, cr, uid, ids, context=None):
        stat = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for t in stat:
            if t['state'] in ('Draft'):
                unlink_ids.append(t['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), _('You can not delete rounding information which is not in "Draft" state !!'))
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.patient.rounding') or '/'
        return super(OeHealthPatientRoundingManagement, self).create(cr, uid, vals, context=context)

    def set_to_completed(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Completed','evaluation_end_date':datetime.datetime.now()}, context=context)

    def print_patient_evaluation(self, cr, uid, ids, context=None):
        '''
        This function prints the xray test
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        return self.pool['report'].get_action(cr, uid, ids, 'oehealth_nursing.report_patient_rounding_evaluation', context=context)

# Patient Ambulatory Care Management

class OeHealthPatientAmbulatoryProcedures (osv.osv):
    _name = 'oeh.medical.patient.ambulatory.procedure'
    _description = 'Patient Procedures For Ambulatory'

    _columns = {
        'name': fields.many2one('oeh.medical.patient.ambulatory', 'Ambulatory'),
        'procedures': fields.many2one('oeh.medical.procedure', 'Procedures', required=True),
        'notes': fields.text('Notes'),
    }

class OeHealthPatientAmbulatoryMedicines (osv.osv):
    _name = 'oeh.medical.patient.ambulatory.medicines'
    _description = 'Patient Medicines For Ambulatory'

    _columns = {
        'name': fields.many2one('oeh.medical.patient.ambulatory', 'Ambulatory'),
        'medicine': fields.many2one('oeh.medical.medicines', 'Medicines', domain=[('medicament_type','=','Medicine')], required=True),
        'qty': fields.integer("Quantity"),
        'notes': fields.text('Comment'),
    }
    _defaults = {
        'qty': lambda *a: 1,
    }

class OeHealthPatientAmbulatoryCare (osv.osv):
    _name = 'oeh.medical.patient.ambulatory'
    _description = 'Patient Ambulatory Management'

    STATUS = [
        ('Draft', 'Draft'),
        ('Completed', 'Completed'),
    ]

    EVOLUTION = [
        ('Initial', 'Initial'),
        ('Status Quo', 'Status Quo'),
        ('Improving', 'Improving'),
        ('Worsening', 'Worsening'),
    ]

    def _get_patient_ambulatory(self, cr, uid, context=None):
        """Return default physician value"""
        therapist_id = []
        therapist_obj = self.pool.get('oeh.medical.physician')
        domain = [('oeh_user_id', '=', uid)]
        user_ids = therapist_obj.search(cr, uid, domain, context=context)
        if user_ids:
            return user_ids[0] or False
        else:
            return False

    _columns = {
        'name': fields.char('Session #', size=128, readonly=True),
        'evaluation_id': fields.many2one('oeh.medical.evaluation','Evaluation #', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'base_condition': fields.many2one('oeh.medical.pathology','Condition', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'patient': fields.many2one ('oeh.medical.patient','Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'doctor': fields.many2one('oeh.medical.physician','Physician', help="Physician Name", domain=[('is_pharmacist','=',False)], required=True, readonly=True,states={'Draft': [('readonly', False)]}),
        'ordering_doctor': fields.many2one('oeh.medical.physician','Requested by', help="Physician Name", domain=[('is_pharmacist','=',False)], readonly=True,states={'Draft': [('readonly', False)]}),
        'evaluation_start_date': fields.datetime('Start date & time', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'evaluation_end_date': fields.datetime('End date & time', readonly=True, states={'Draft': [('readonly', False)]}),
        'systolic': fields.integer('Systolic Pressure', readonly=True, states={'Draft': [('readonly', False)]}),
        'diastolic': fields.integer('Diastolic Pressure', readonly=True, states={'Draft': [('readonly', False)]}),
        'bpm': fields.integer('Heart Rate', help="Heart rate expressed in beats per minute", readonly=True, states={'Draft': [('readonly', False)]}),
        'respiratory_rate': fields.integer('Respiratory Rate', help="Respiratory rate expressed in breaths per minute", readonly=True, states={'Draft': [('readonly', False)]}),
        'osat': fields.integer('Oxygen Saturation', help="Oxygen Saturation(arterial)", readonly=True, states={'Draft': [('readonly', False)]}),
        'temperature': fields.float('Temperature', help="Temperature in celsius", readonly=True, states={'Draft': [('readonly', False)]}),
        'glycemia': fields.integer('Glycemia', help="Blood Glucose level", readonly=True, states={'Draft': [('readonly', False)]}),
        'evolution': fields.selection(EVOLUTION, 'Evolution', readonly=True, states={'Draft': [('readonly', False)]}),
        'session_notes': fields.text("Notes", readonly=True, states={'Draft': [('readonly', False)]}),
        'procedures': fields.one2many('oeh.medical.patient.ambulatory.procedure', 'name', 'Procedures', help="List of the procedures in this ambulatory. Please enter the first one as the main procedure", readonly=True, states={'Draft': [('readonly', False)]}),
        'medicaments': fields.one2many('oeh.medical.patient.ambulatory.medicines', 'name', 'Medicines', help="List of the medicines assigned in this ambulatory", readonly=True, states={'Draft': [('readonly', False)]}),
        'state': fields.selection(STATUS, 'State',readonly=True),
    }
    _defaults = {
        'evaluation_start_date': datetime.datetime.now(),
        'name': lambda obj, cr, uid, context: '/',
        'state': lambda *a: 'Draft',
        'doctor': _get_patient_ambulatory,
    }

    # Preventing deletion of a ambulatory care details which is not in draft state
    def unlink(self, cr, uid, ids, context=None):
        stat = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for t in stat:
            if t['state'] in ('Draft'):
                unlink_ids.append(t['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), _('You can not delete information which is not in "Draft" state !!'))
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.patient.ambulatory') or '/'
        return super(OeHealthPatientAmbulatoryCare, self).create(cr, uid, vals, context=context)

    def set_to_completed(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Completed','evaluation_end_date':datetime.datetime.now()}, context=context)

