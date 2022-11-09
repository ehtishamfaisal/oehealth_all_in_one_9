from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _

# Ophthalmology Management

class OeHealthOphthalmology(osv.osv):
    _name = "oeh.medical.ophthalmology"
    _description = "Ophthalmology Management"

    SEX = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    OPHTHO_STATUS = [
        ('Draft', 'Draft'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    SNELL_CHART = [
        ('6_6', '6/6'),
        ('6_9', '6/9'),
        ('6_12', '6/12'),
        ('6_18', '6/18'),
        ('6_24', '6/24'),
        ('6_36', '6/36'),
        ('6_60', '6/60'),
        ('5_60', '5/60'),
        ('4_60', '4/60'),
        ('3_60', '3/60'),
        ('2_60', '2/60'),
        ('1_60', '1/60'),
        ('1 Meter FC', '1 Meter FC'),
        ('1/2 Meter FC', '1/2 Meter FC'),
        ('HMCF', 'HMCF'),
        ('P/L', 'P/L'),
    ]

    NEAR_VISION_CHART = [
        ('N6', 'N6'),
        ('N8', 'N8'),
        ('N12', 'N12'),
        ('N18', 'N18'),
        ('N24', 'N24'),
        ('N36', 'N36'),
        ('N60', 'N60'),
    ]

    IOP_METHOD = [
        ('Non-contact tonometry', 'Non-contact tonometry'),
        ('Schiotz tonometry', 'Schiotz tonometry'),
        ('Goldman tonometry', 'Goldman tonometry'),
    ]

    def _patient_age_at_evaluation(self, cr, uid, ids, name, arg, context={}):
        def compute_age_from_dates (patient_dob,patient_visit_date):
            if (patient_dob):
                dob = datetime.datetime.strptime(patient_dob,'%Y-%m-%d').date()
                visit_date = datetime.datetime.strptime(patient_visit_date,'%Y-%m-%d %H:%M:%S').date()
                delta= visit_date - dob
                years_months_days = str(delta.days // 365)+" years "+ str(delta.days%365)+" days"
            else:
                years_months_days = "No DoB !"
            return years_months_days
        result={}
        for patient_data in self.browse(cr, uid, ids, context=context):
            result[patient_data.id] = compute_age_from_dates (patient_data.patient.dob,patient_data.visit_date)
        return result

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
        'name': fields.char('Visit #', size=64, readonly=True),
        'patient': fields.many2one('oeh.medical.patient','Patient', help="Patient Name",required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'visit_date': fields.datetime('Date', help="Date of Consultation", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'doctor': fields.many2one('oeh.medical.physician','Physician', domain=[('is_pharmacist','=',False)], help="Health professional / Ophthalmologist / OptoMetrist", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'rdva': fields.selection(SNELL_CHART, 'RDVA', help="Right Eye Vision of Patient without aid", readonly=True, states={'Draft': [('readonly', False)]}),
        'ldva': fields.selection(SNELL_CHART, 'LDVA', help="Left Eye Vision of Patient without aid", readonly=True, states={'Draft': [('readonly', False)]}),
        'rdva_pinhole': fields.selection(SNELL_CHART, 'RDVA', help="Right Eye Vision Using Pin Hole", readonly=True, states={'Draft': [('readonly', False)]}),
        'ldva_pinhole': fields.selection(SNELL_CHART, 'LDVA', help="Left Eye Vision Using Pin Hole", readonly=True, states={'Draft': [('readonly', False)]}),
        'rdva_aid': fields.selection(SNELL_CHART, 'RDVA AID', help="Vision with glasses or contact lens", readonly=True, states={'Draft': [('readonly', False)]}),
        'ldva_aid': fields.selection(SNELL_CHART, 'LDVA AID', help="Vision with glasses or contact lens", readonly=True, states={'Draft': [('readonly', False)]}),
        'rspherical': fields.float('SPH',help='Right Eye Spherical', readonly=True, states={'Draft': [('readonly', False)]}),
        'lspherical': fields.float('SPH',help='Left Eye Spherical', readonly=True, states={'Draft': [('readonly', False)]}),
        'rcylinder': fields.float('CYL',help='Right Eye Cylinder', readonly=True, states={'Draft': [('readonly', False)]}),
        'lcylinder': fields.float('CYL',help='Left Eye Cylinder', readonly=True, states={'Draft': [('readonly', False)]}),
        'raxis': fields.float('Axis',help='Right Eye Axis', readonly=True, states={'Draft': [('readonly', False)]}),
        'laxis': fields.float('Axis',help='Left Eye Axis', readonly=True, states={'Draft': [('readonly', False)]}),
        'rnv_add': fields.float('NV Add',help='Right Eye Best Corrected NV Add', readonly=True, states={'Draft': [('readonly', False)]}),
        'lnv_add': fields.float('NV Add',help='Left Eye Best Corrected NV Add', readonly=True, states={'Draft': [('readonly', False)]}),
        'rnv': fields.selection(SNELL_CHART, 'RNV', help="Right Eye Near Vision", readonly=True, states={'Draft': [('readonly', False)]}),
        'lnv': fields.selection(SNELL_CHART, 'LNV', help="Left Eye Near Vision", readonly=True, states={'Draft': [('readonly', False)]}),
        'rbcva_spherical': fields.float('SPH',help='Right Eye Best Corrected Spherical', readonly=True, states={'Draft': [('readonly', False)]}),
        'lbcva_spherical': fields.float('SPH',help='Left Eye Best Corrected Spherical', readonly=True, states={'Draft': [('readonly', False)]}),
        'rbcva_cylinder': fields.float('CYL',help='Right Eye Best Corrected Cylinder', readonly=True, states={'Draft': [('readonly', False)]}),
        'lbcva_cylinder': fields.float('CYL',help='Left Eye Best Corrected Cylinder', readonly=True, states={'Draft': [('readonly', False)]}),
        'rbcva_axis': fields.float('Axis',help='Right Eye Best Corrected Axis', readonly=True, states={'Draft': [('readonly', False)]}),
        'lbcva_axis': fields.float('Axis',help='Left Eye Best Corrected Axis', readonly=True, states={'Draft': [('readonly', False)]}),
        'rbcva_nv_add': fields.float('BCVA - Add',help='Right Eye Best Corrected NV Add', readonly=True, states={'Draft': [('readonly', False)]}),
        'lbcva_nv_add': fields.float('BCVA - Add',help='Left Eye Best Corrected NV Add', readonly=True, states={'Draft': [('readonly', False)]}),
        'rbcva': fields.selection(SNELL_CHART, 'RBCVA', help="Right Eye Best Corrected VA", readonly=True, states={'Draft': [('readonly', False)]}),
        'lbcva': fields.selection(SNELL_CHART, 'LBCVA', help="Left Eye Best Corrected VA", readonly=True, states={'Draft': [('readonly', False)]}),
        'rbcva_nv': fields.selection(SNELL_CHART, 'RBCVANV', help="Right Eye Best Corrected Near Vision", readonly=True, states={'Draft': [('readonly', False)]}),
        'lbcva_nv': fields.selection(SNELL_CHART, 'LBCVANV', help="Left Eye Best Corrected Near Vision", readonly=True, states={'Draft': [('readonly', False)]}),
        'notes': fields.text('Notes', readonly=True, states={'Draft': [('readonly', False)]}),
        'iop_method': fields.selection(SNELL_CHART, 'Method', help="Tonometry / Intraocular pressure reading method", readonly=True, states={'Draft': [('readonly', False)]}),
        'riop': fields.float('RIOP',help='Right Intraocular Pressure in mmHg', readonly=True, states={'Draft': [('readonly', False)]}),
        'liop': fields.float('LIOP',help='Left Intraocular Pressure in mmHg', readonly=True, states={'Draft': [('readonly', False)]}),
        'findings': fields.one2many('oeh.medical.ophthalmology.findings', 'name','Findings',  readonly=True, states={'Draft': [('readonly', False)]}),
        'computed_age': fields.function(_patient_age_at_evaluation, method=True, type='char', size=32, string='Age during evaluation',help="Computed patient age at the moment of the surgery", readonly=True),
        'state': fields.selection(OPHTHO_STATUS, 'State', readonly=True),
    }
    _defaults = {
       'name': lambda obj, cr, uid, context: '/',
       'visit_date': datetime.datetime.now(),
       'doctor': _get_physician,
       'state': lambda *a: 'Draft',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.ophthalmology') or '/'
        return super(OeHealthOphthalmology, self).create(cr, uid, vals, context=context)

    # Preventing deletion of a Ophthalmology details which is not in draft state
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

    def start_evaluation(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'In Progress'}, context=context)

    def complete_evaluation(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Completed'}, context=context)

# Opthalmology Findings Management

class OeHealthOphthalmologyFindingslist(osv.osv):
    _name = "oeh.medical.ophthalmology.findings"
    _description = "Ophthalmology Findings Management"

    STRUCTURE = [
        ('Lid', 'Lid'),
        ('Naso-lacrimal System', 'Naso-lacrimal System'),
        ('Conjunctiva', 'Conjunctiva'),
        ('Cornea', 'Cornea'),
        ('Anterior Chamber', 'Anterior Chamber'),
        ('Iris', 'Iris'),
        ('Pupil', 'Pupil'),
        ('Lens', 'Lens'),
        ('Vitreous', 'Vitreous'),
        ('Fundus Disc', 'Fundus Disc'),
        ('Macula', 'Macula'),
        ('Fundus Background', 'Fundus Background'),
        ('Fundus Vessels', 'Fundus Vessels'),
        ('Other', 'Other'),
    ]

    AFFECTED_EYE = [
        ("Right","Right"),
        ("Left","Left"),
        ("Both","Both"),
    ]

    _columns = {
        'name': fields.many2one('oeh.medical.ophthalmology','Evaluation', readonly=True),
        'eye_structure': fields.selection(STRUCTURE, 'Structure', help="Affected eye structure"),
        'affected_eye': fields.selection(AFFECTED_EYE, 'Eye', help="Affected eye"),
        'finding': fields.char('Finding', size=56),
    }