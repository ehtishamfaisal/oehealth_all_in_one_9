from openerp.osv import osv, fields
import datetime
from openerp import api
from openerp.tools.translate import _
import calendar
import time

class OeHealthSurgeryRCRI(osv.osv):
    _name = "oeh.medical.surgery.rcri"
    _description = "Revised Cardiac Risk Index"

    RCRI_CLASS = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
    ]

    def get_rcri_name(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        rcri_name = ''
        for rc in self.browse(cr, uid, ids, context=context):
            rcri_name = 'Points: ' + str(rc.rcri_total) + ' (Class ' + str(rc.rcri_class) + ')'
            result[rc.id] = rcri_name
        return result

    _columns = {
        'name': fields.function(get_rcri_name, string="RCRI", type="char", size=64),
        'patient': fields.many2one('oeh.medical.patient','Patient', help="Patient Name",required=True),
        'doctor': fields.many2one('oeh.medical.physician','Physician', domain=[('is_pharmacist','=',False)], help="Health professional / Cardiologist who signed the assesment RCRI"),
        'rcri_date': fields.datetime('Date', required=True),
        'rcri_high_risk_surgery': fields.boolean('High Risk surgery', help='Includes andy suprainguinal vascular, intraperitoneal or intrathoracic procedures'),
        'rcri_ischemic_history': fields.boolean('History of Ischemic heart disease', help='History of MI or a positive exercise test, current complaint of chest pain considered to be secondary to myocardial ischemia, use of nitrate therapy, or ECG with pathological Q waves; do not count prior coronary revascularization procedure unless one of the other criteria for ischemic heart disease is present"'),
        'rcri_congestive_history': fields.boolean('History of Congestive heart disease'),
        'rcri_diabetes_history': fields.boolean('Preoperative Diabetes', help="Diabetes Mellitus requiring treatment with Insulin"),
        'rcri_cerebrovascular_history': fields.boolean('History of Cerebrovascular disease'),
        'rcri_kidney_history': fields.boolean('Preoperative Kidney disease', help="Preoperative serum creatinine >2.0 mg/dL (177 mol/L)"),
        'rcri_total': fields.integer('Score', help='Points 0: Class I Very Low (0.4% complications)\n'
        'Points 1: Class II Low (0.9% complications)\n'
        'Points 2: Class III Moderate (6.6% complications)\n'
        'Points 3 or more : Class IV High (>11% complications)'),
        'rcri_class': fields.selection(RCRI_CLASS, 'RCRI Class', required=True),
    }
    _defaults = {
        'rcri_total': lambda *a: 0,
        'rcri_class': lambda *a: 'I',
        'rcri_date': datetime.datetime.now(),
    }

    @api.multi
    def on_change_with_rcri(self, rcri_high_risk_surgery, rcri_ischemic_history, rcri_congestive_history, rcri_diabetes_history, rcri_cerebrovascular_history, rcri_kidney_history):
        total = 0
        rcri_class = 'I'
        if rcri_high_risk_surgery:
            total = total + 1
        if rcri_ischemic_history:
            total = total + 1
        if rcri_congestive_history:
            total = total + 1
        if rcri_diabetes_history:
            total = total + 1
        if rcri_kidney_history:
            total = total + 1
        if rcri_cerebrovascular_history:
            total = total + 1

        if total == 1:
            rcri_class = 'II'
        if total == 2:
            rcri_class = 'III'
        if (total > 2):
            rcri_class = 'IV'

        return {'value': {'rcri_total': total,'rcri_class': rcri_class}}

class OeHealthSurgeryTeam(osv.osv):
    _name = "oeh.medical.surgery.team"
    _description = "Surgery Team"
    _columns = {
        'name': fields.many2one('oeh.medical.surgery', 'Surgery'),
        'team_member': fields.many2one('oeh.medical.physician','Member', help="Health professional that participated on this surgery", domain=[('is_pharmacist','=',False)], required=True),
        'role': fields.many2one('oeh.medical.speciality', 'Role'),
        'notes': fields.char('Notes'),
    }

    def onchange_team_member(self, cr, uid, ids, team_member, context=None):
        if team_member:
            therapist_obj = self.pool.get('oeh.medical.physician')
            therapist = therapist_obj.browse(cr, uid, team_member, context=context)
            role = therapist.speciality.id
            return {'value': {'role': role}}
        return {'value': {}}

class OeHealthSurgerySupply(osv.osv):
    _name = "oeh.medical.surgery.supply"
    _description = "Supplies related to the surgery"
    _columns = {
        'name': fields.many2one('oeh.medical.surgery', 'Surgery'),
        'qty': fields.integer('Initial required quantity', required=True, help="Initial required quantity"),
        'supply': fields.many2one('product.product', 'Supply', required=True, help="Supply to be used in this surgery"),
        'notes': fields.char('Notes'),
        'qty_used': fields.integer('Actual quantity used', required=True, help="Actual quantity used"),
    }
    _defaults = {
        'qty': lambda *a: 0,
        'qty_used': lambda *a: 0,
    }

class OeHealthSurgery(osv.osv):
    _name = "oeh.medical.surgery"
    _description = "Surgerical Management"

    CLASSIFICATION = [
        ('Optional', 'Optional'),
        ('Required', 'Required'),
        ('Urgent', 'Urgent'),
        ('Emergency', 'Emergency'),
    ]

    STATES = [
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
        ('Signed', 'Signed'),
        ('Cancelled', 'Cancelled'),
    ]

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Female -> Male','Female -> Male'),
        ('Male -> Female','Male -> Female'),
    ]

    PREOP_MALLAMPATI = [
        ('Class 1', 'Class 1: Full visibility of tonsils, uvula and soft '
                    'palate'),
        ('Class 2', 'Class 2: Visibility of hard and soft palate, '
                    'upper portion of tonsils and uvula'),
        ('Class 3', 'Class 3: Soft and hard palate and base of the uvula are '
                    'visible'),
        ('Class 4', 'Class 4: Only Hard Palate visible'),
    ]

    PREOP_ASA = [
        ('PS 1', 'PS 1 : Normal healthy patient'),
        ('PS 2', 'PS 2 : Patients with mild systemic disease'),
        ('PS 3', 'PS 3 : Patients with severe systemic disease'),
        ('PS 4', 'PS 4 : Patients with severe systemic disease that is'
            ' a constant threat to life '),
        ('PS 5', 'PS 5 : Moribund patients who are not expected to'
            ' survive without the operation'),
        ('PS 6', 'PS 6 : A declared brain-dead patient who organs are'
            ' being removed for donor purposes'),
    ]

    SURGICAL_WOUND = [
        ('I', 'Clean . Class I'),
        ('II', 'Clean-Contaminated . Class II'),
        ('III', 'Contaminated . Class III'),
        ('IV', 'Dirty-Infected . Class IV'),
    ]

    def _surgery_duration(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for su in self.browse(cr, uid, ids, context=context):
            if su.surgery_end_date and su.surgery_date:
                surgery_date = 1.0*calendar.timegm(time.strptime(su.surgery_date, "%Y-%m-%d %H:%M:%S"))
                surgery_end_date = 1.0*calendar.timegm(time.strptime(su.surgery_end_date, "%Y-%m-%d %H:%M:%S"))
                duration = (surgery_end_date - surgery_date)/3600
                result[su.id] = duration
        return result

    def _patient_age_at_surgery(self, cr, uid, ids, name, arg, context={}):
        def compute_age_from_dates (patient_dob,patient_surgery_date):
            if (patient_dob):
                dob = datetime.datetime.strptime(patient_dob,'%Y-%m-%d').date()
                surgery_date = datetime.datetime.strptime(patient_surgery_date,'%Y-%m-%d %H:%M:%S').date()
                delta= surgery_date - dob
                years_months_days = str(delta.days // 365)+" years "+ str(delta.days%365)+" days"
            else:
                years_months_days = "No DoB !"
            return years_months_days
        result={}
        for patient_data in self.browse(cr, uid, ids, context=context):
            result[patient_data.id] = compute_age_from_dates (patient_data.patient.dob,patient_data.surgery_date)
        return result

    def _get_surgeon(self, cr, uid, context=None):
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
        'name': fields.char ('Surgery #',size=64, readonly=True, required=True),
        'patient': fields.many2one ('oeh.medical.patient','Patient', help="Patient Name",required=True, readonly=True,states={'Draft': [('readonly', False)]}),
        'admission': fields.many2one ('oeh.medical.appointment','Admission', help="Patient Name", readonly=True,states={'Draft': [('readonly', False)]}),
        'procedures': fields.many2many('oeh.medical.procedure', 'oeh_surgery_procedure_rel','surgery_id','procedure_id', 'Procedures',help="List of the procedures in the surgery. Please enter the first one as the main procedure", readonly=True,states={'Draft': [('readonly', False)]}),
        'pathology': fields.many2one('oeh.medical.pathology', 'Condition', help="Base Condition / Reason", readonly=True,states={'Draft': [('readonly', False)]}),
        'classification': fields.selection(CLASSIFICATION, 'Urgency', help="Urgency level for this surgery", required=True, readonly=True,states={'Draft': [('readonly', False)]}),
        'surgeon': fields.many2one('oeh.medical.physician','Surgeon', help="Surgeon who did the procedure", domain=[('is_pharmacist','=',False)], required=True, readonly=True,states={'Draft': [('readonly', False)]}),
        'anesthetist': fields.many2one('oeh.medical.physician','Anesthetist', help="Anesthetist in charge", domain=[('is_pharmacist','=',False)], required=True, readonly=True,states={'Draft': [('readonly', False)]}),
        'surgery_date': fields.datetime('Start date & time', help="Start of the Surgery", readonly=True,states={'Draft': [('readonly', False)]}),
        'surgery_end_date': fields.datetime('End date & time', help="End of the Surgery", readonly=True,states={'Draft': [('readonly', False)]}),
        'surgery_length': fields.function(_surgery_duration, method=True, type='float', string='Duration',help="Length of the surgery", readonly=True,states={'Draft': [('readonly', False)]}),
        'computed_age': fields.function(_patient_age_at_surgery, method=True, type='char', size=32, string='Age during surgery',help="Computed patient age at the moment of the surgery", readonly=True,states={'Draft': [('readonly', False)]}),
        'gender': fields.selection(GENDER, 'Gender', readonly=True,states={'Draft': [('readonly', False)]}),
        'signed_by': fields.many2one('res.users','Signed by', help="Health Professional that signed this surgery document"),
        'description': fields.text('Description', readonly=True,states={'Draft': [('readonly', False)]}),
        'preop_mallampati': fields.selection(PREOP_MALLAMPATI, 'Mallampati Score', readonly=True,states={'Draft': [('readonly', False)]}),
        'preop_bleeding_risk': fields.boolean('Risk of Massive bleeding', help="Patient has a risk of losing more than 500 ml in adults of over 7ml/kg in infants. If so, make sure that intravenous access and fluids are available", readonly=True,states={'Draft': [('readonly', False)]}),
        'preop_oximeter': fields.boolean('Pulse Oximeter in place', help="Pulse oximeter is in place and functioning", readonly=True, states={'Draft': [('readonly', False)]}),
        'preop_site_marking': fields.boolean('Surgical Site Marking', help="The surgeon has marked the surgical incision", readonly=True, states={'Draft': [('readonly', False)]}),
        'preop_antibiotics': fields.boolean('Antibiotic Prophylaxis', help="Prophylactic antibiotic treatment within the last 60 minutes", readonly=True, states={'Draft': [('readonly', False)]}),
        'preop_sterility': fields.boolean('Sterility Confirmed', help="Nursing team has confirmed sterility of the devices and room", readonly=True, states={'Draft': [('readonly', False)]}),
        'preop_asa': fields.selection(PREOP_ASA, 'ASA PS', help="ASA pre-operative Physical Status", readonly=True,states={'Draft': [('readonly', False)]}),
        'preop_rcri': fields.many2one('oeh.medical.surgery.rcri', 'RCRI', help='Patient Revised Cardiac Risk Index\n Points 0: Class I Very Low (0.4% complications)\n Points 1: Class II Low (0.9% complications)\n Points 2: Class III Moderate (6.6% complications)\n Points 3 or more : Class IV High (>11% complications)', readonly=True,states={'Draft': [('readonly', False)]}),
        'surgical_wound': fields.selection(SURGICAL_WOUND, 'Surgical Wound', readonly=True,states={'Draft': [('readonly', False)]}),
        'info': fields.text('Extra Info', readonly=True, states={'Draft': [('readonly', False)]}),
        'anesthesia_report': fields.text('Anesthesia Report', readonly=True, states={'Draft': [('readonly', False)]}),
        'institution': fields.many2one('oeh.medical.health.center','Health Center',help="Health Center", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'postoperative_dx': fields.many2one('oeh.medical.pathology', 'Post-op dx', help="Post-operative diagnosis", readonly=True,states={'Draft': [('readonly', False)]}),
        'surgery_team': fields.one2many('oeh.medical.surgery.team', 'name', 'Team Members', help="Professionals Involved in the surgery", readonly=True, states={'Draft': [('readonly', False)]}),
        'supplies': fields.one2many('oeh.medical.surgery.supply', 'name', 'Supplies', help="List of the supplies required for the surgery", readonly=True, states={'Draft': [('readonly', False)]}),
        'building': fields.many2one('oeh.medical.health.center.building','Building',help="Building of the selected Health Center", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'operating_room': fields.many2one('oeh.medical.health.center.ot', 'Operation Theater', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'state': fields.selection(STATES, 'State',readonly=True),
    }
    _defaults = {
        'surgery_date': datetime.datetime.now(),
        'name': lambda obj, cr, uid, context: '/',
        'state': lambda *a: 'Draft',
        'surgeon': _get_surgeon,
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.surgery') or '/'
        return super(OeHealthSurgery, self).create(cr, uid, vals, context=context)

    def action_surgery_confirm(self, cr, uid, ids, context=None):
        ot_obj = self.pool.get("oeh.medical.health.center.ot")
        for surgery in self.browse(cr, uid, ids):
            if surgery.operating_room:
                ot_obj.write(cr,uid,[surgery.operating_room.id], {'state': 'Reserved'}, context=context)
        return self.write(cr, uid, ids, {'state': 'Confirmed'}, context=context)

    def action_surgery_start(self, cr, uid, ids, context=None):
        ot_obj = self.pool.get("oeh.medical.health.center.ot")
        for surgery in self.browse(cr, uid, ids):
            if surgery.operating_room:
                ot_obj.write(cr,uid,[surgery.operating_room.id], {'state': 'Occupied'}, context=context)
        return self.write(cr, uid, ids, {'state': 'In Progress', 'surgery_date':datetime.datetime.now()}, context=context)

    def action_surgery_cancel(self, cr, uid, ids, context=None):
        ot_obj = self.pool.get("oeh.medical.health.center.ot")
        for surgery in self.browse(cr, uid, ids):
            if surgery.operating_room:
                ot_obj.write(cr,uid,[surgery.operating_room.id], {'state': 'Free'}, context=context)
        return self.write(cr, uid, ids, {'state': 'Cancelled'}, context=context)

    def action_surgery_set_to_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Draft'}, context=context)

    def action_surgery_end(self, cr, uid, ids, context=None):
        ot_obj = self.pool.get("oeh.medical.health.center.ot")
        for surgery in self.browse(cr, uid, ids):
            if surgery.operating_room:
                ot_obj.write(cr,uid,[surgery.operating_room.id], {'state': 'Free'}, context=context)
        return self.write(cr, uid, ids, {'state': 'Done', 'surgery_end_date':datetime.datetime.now()}, context=context)

    def action_surgery_sign(self, cr, uid, ids, context=None):
        phy_obj = self.pool.get("oeh.medical.physician")
        user = False
        domain = [('oeh_user_id', '=', uid)]
        user_ids = phy_obj.search(cr, uid, domain, context=context)
        if user_ids:
            user = user_ids[0] or False
        else:
            raise osv.except_osv(_('Error'), _('No physician associated to logged in user'))
        return self.write(cr, uid, ids, {'state': 'Signed', 'signed_by':uid}, context=context)


# Inheriting Patient module to add "Surgeries" screen reference
class OeHealthPatient(osv.osv):
    _inherit='oeh.medical.patient'
    _columns = {
        'pediatrics_surgery_ids': fields.one2many('oeh.medical.surgery','patient','Surgeries'),
    }



