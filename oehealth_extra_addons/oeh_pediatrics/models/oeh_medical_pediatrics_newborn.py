from openerp import pooler, tools, api
from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _
from openerp.exceptions import UserError

class OeHealthPediatricsNewBorn(osv.osv):
    _name = "oeh.medical.pediatrics.newborn"
    _inherits={
        'res.partner': 'partner_id',
    }

    SEX = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    PEDIA_STATUS = [
        ('Draft', 'Draft'),
        ('Signed', 'Signed'),
    ]

    # Automatically detect logged in physician
    def _get_physician(self, cr, uid, context=None):
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
        'partner_id': fields.many2one('res.partner', 'Related Partner', required=True,ondelete='cascade', help='Partner-related data of the patient'),
        'newborn_code': fields.char('Newborn ID', size=256, readonly=True),
        'mother': fields.many2one('oeh.medical.patient', 'Mother', domain=[('sex','=','Female')], required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'birth_date': fields.datetime('Date of Birth', required=True, help="Date and Time of birth", readonly=True, states={'Draft': [('readonly', False)]}),
        'sex': fields.selection(SEX, 'Sex', required=True, help="Sex at birth. It might differ from the current patient gender. This is the biological sex.", readonly=True, states={'Draft': [('readonly', False)]}),
        'cephalic_perimeter': fields.integer('Cephalic Perimeter (CP)', help="Cephalic Perimeter in centimeters (cm)", readonly=True, states={'Draft': [('readonly', False)]}),
        'length': fields.integer('Length (in)', help="Length in centimeters (cm)", readonly=True, states={'Draft': [('readonly', False)]}),
        'weight': fields.float('Weight (pound or kg)', help="Weight in grams (g)", readonly=True, states={'Draft': [('readonly', False)]}),
        'apgar_scores': fields.one2many('oeh.medical.pediatrics.neonatal.apgar', 'name', 'APGAR scores', readonly=True, states={'Draft': [('readonly', False)]}),
        'meconium': fields.boolean('Meconium', readonly=True, states={'Draft': [('readonly', False)]}),
        'congenital_diseases': fields.many2one('oeh.medical.pathology', 'Congenital Diseases', help="Choose a disease for this medicament from the disease list. It can be an existing disease of the patient or a prophylactic.", states={'Draft': [('readonly', False)]}),
        'reanimation_stimulation': fields.boolean('Stimulation', readonly=True, states={'Draft': [('readonly', False)]}),
        'reanimation_aspiration': fields.boolean('Aspiration', readonly=True, states={'Draft': [('readonly', False)]}),
        'reanimation_intubation': fields.boolean('Intubation', readonly=True, states={'Draft': [('readonly', False)]}),
        'reanimation_mask': fields.boolean('Mask', readonly=True, states={'Draft': [('readonly', False)]}),
        'reanimation_oxygen': fields.boolean('Oxygen', readonly=True, states={'Draft': [('readonly', False)]}),
        'test_vdrl': fields.boolean('VDRL', readonly=True, states={'Draft': [('readonly', False)]}),
        'test_toxo': fields.boolean('Toxoplasmosis', readonly=True, states={'Draft': [('readonly', False)]}),
        'test_chagas': fields.boolean('Chagas', readonly=True, states={'Draft': [('readonly', False)]}),
        'test_billirubin': fields.boolean('Billirubin', readonly=True, states={'Draft': [('readonly', False)]}),
        'test_audition': fields.boolean('Audition', readonly=True, states={'Draft': [('readonly', False)]}),
        'test_metabolic': fields.boolean('Metabolic ("heel stick screening")', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_ortolani': fields.boolean('Positive Ortolani', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_barlow': fields.boolean('Positive Barlow', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_hernia': fields.boolean('Hernia', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_ambiguous_genitalia': fields.boolean('Ambiguous Genitalia', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_erbs_palsy': fields.boolean('Erbs Palsy', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_hematoma': fields.boolean('Hematomas', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_talipes_equinovarus': fields.boolean('Talipes Equinovarus', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_polydactyly': fields.boolean('Polydactyly', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_syndactyly': fields.boolean('Syndactyly', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_moro_reflex': fields.boolean('Moro Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_grasp_reflex': fields.boolean('Grasp Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_stepping_reflex': fields.boolean('Stepping Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_babinski_reflex': fields.boolean('Babinski Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_blink_reflex': fields.boolean('Blink Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_sucking_reflex': fields.boolean('Sucking Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_swimming_reflex': fields.boolean('Swimming Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_tonic_neck_reflex': fields.boolean('Tonic Neck Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_rooting_reflex': fields.boolean('Rooting Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_palmar_crease': fields.boolean('Transversal Palmar Crease', readonly=True, states={'Draft': [('readonly', False)]}),
        'neonatal_sucking_reflex': fields.boolean('Sucking Reflex', readonly=True, states={'Draft': [('readonly', False)]}),
        'medication': fields.many2one('oeh.medical.medicines','Medicines',help="Prescribed Medicines",domain=[('medicament_type','=','Medicine')], readonly=True, states={'Draft': [('readonly', False)]}),
        'doctor': fields.many2one('oeh.medical.physician','Doctor in charge', readonly=True, states={'Draft': [('readonly', False)]}),
        'signed_by': fields.many2one('oeh.medical.physician','Signed by', readonly=True, states={'Draft': [('readonly', False)]}),
        'dismissed': fields.datetime('Discharged', readonly=True, states={'Draft': [('readonly', False)]}),
        'notes': fields.text('Notes', readonly=True, states={'Draft': [('readonly', False)]}),
        'bd': fields.boolean('Stillbirth', readonly=True, states={'Draft': [('readonly', False)]}),
        'died_at_delivery': fields.boolean('Died at delivery room', readonly=True, states={'Draft': [('readonly', False)]}),
        'died_at_the_hospital': fields.boolean('Died at the hospital', readonly=True, states={'Draft': [('readonly', False)]}),
        'died_being_transferred': fields.boolean('Died being transferred', readonly=True, states={'Draft': [('readonly', False)]}),
        'time_of_death': fields.datetime('Time of Death', readonly=True, states={'Draft': [('readonly', False)]}),
        'cause_of_death': fields.many2one('oeh.medical.pathology', 'Cause of Death', readonly=True, states={'Draft': [('readonly', False)]}),
        'institution': fields.many2one('oeh.medical.health.center','Birth at Health Center', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'state': fields.selection(PEDIA_STATUS, 'State', readonly=True),
    }
    _defaults = {
           'newborn_code': lambda obj, cr, uid, context: '/',
           'date': datetime.datetime.now(),
           'doctor': _get_physician,
           'state': lambda *a: 'Draft',
           'is_baby': True
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('newborn_code','/')=='/':
            vals['newborn_code'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.pediatrics.newborn') or '/'
        return super(OeHealthPediatricsNewBorn, self).create(cr, uid, vals, context=context)

    def sign_newborn(self, cr, uid, ids, context=None):
        signed_by = []
        for nb in self.browse(cr, uid, ids, context):
            therapist_obj = self.pool.get('oeh.medical.physician')
            domain = [('oeh_user_id', '=', uid)]
            user_ids = therapist_obj.search(cr, uid, domain, context=context)
            if user_ids:
                signed_by = user_ids[0] or False
            else:
                raise osv.except_osv(_('Invalid Action!'), _('Correct Physician ID not found to complete the signing process !!'))
        return self.write(cr, uid, ids, {'state': 'Signed', 'signed_by': signed_by}, context=context)

class OeHealthPediatricsAPGAR(osv.osv):
    _name = "oeh.medical.pediatrics.neonatal.apgar"
    _description = "Neonatal APGAR Score"

    APGAR_APPEARANCE = [
        ('0', 'Central Cyanosis'),
        ('1', 'Acrocyanosis'),
        ('2', 'No Cyanosis'),
    ]

    APGAR_PULSE = [
        ('0', 'Absent'),
        ('1', '< 100'),
        ('2', '> 100'),
    ]

    APGAR_GRIMACE = [
        ('0', 'No response to stimulation'),
        ('1', 'Grimace when stimulated'),
        ('2', 'Cry or pull away when stimulated'),
    ]

    APGAR_ACTIVITY = [
        ('0', 'None'),
        ('1', 'Some flexion'),
        ('2', 'Flexed arms and legs'),
    ]

    APGAR_RESPIRATION = [
        ('0', 'Absent'),
        ('1', 'Weak / Irregular'),
        ('2', 'Strong'),
    ]

    _columns = {
        'name': fields.many2one('oeh.medical.pediatrics.newborn', 'Newborn ID', ondelete='cascade'),
        'apgar_minute': fields.integer('Minute', required=True),
        'apgar_appearance': fields.selection(APGAR_APPEARANCE, 'Appearance', required=True),
        'apgar_pulse': fields.selection(APGAR_PULSE, 'Pulse', required=True),
        'apgar_grimace': fields.selection(APGAR_GRIMACE, 'Grimace', required=True),
        'apgar_activity': fields.selection(APGAR_ACTIVITY, 'Activity', required=True),
        'apgar_respiration': fields.selection(APGAR_RESPIRATION, 'Respiration', required=True),
        'apgar_score': fields.integer('APGAR Score', required=True),
    }
    _defaults = {
       'apgar_score': lambda *a: 0,
    }

    @api.multi
    def on_change_with_apgar_score(self, apgar_appearance, apgar_pulse, apgar_grimace, apgar_activity, apgar_respiration):
        apgar_appearance = apgar_appearance or '0'
        apgar_pulse = apgar_pulse or '0'
        apgar_grimace = apgar_grimace or '0'
        apgar_activity = apgar_activity or '0'
        apgar_respiration = apgar_respiration or '0'

        apgar_score = int(apgar_appearance) + int(apgar_pulse) + \
            int(apgar_grimace) + int(apgar_activity) + int(apgar_respiration)

        return {'value': {'apgar_score': apgar_score}}