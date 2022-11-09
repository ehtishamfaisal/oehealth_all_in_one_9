##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp import pooler, tools, api
from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _
from openerp.exceptions import UserError

class OeHealthAppointmentWalkin(osv.osv):
    _name = "oeh.medical.appointment.register.walkin"

    MARITAL_STATUS = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Divorced', 'Divorced'),
        ('Separated', 'Separated'),
    ]

    SEX = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    BLOOD_TYPE = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    RH = [
        ('+','+'),
        ('-','-'),
    ]

    WALKIN_STATUS = [
            ('Scheduled', 'Scheduled'),
            ('Completed', 'Completed'),
            ('Invoiced', 'Invoiced'),
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
        'name': fields.char('Queue #', size=128, required=True, readonly=True),
        'patient': fields.many2one('oeh.medical.patient','Patient', help="Patient Name",required=True, readonly=True,states={'Scheduled': [('readonly', False)]}),
        'dob': fields.date ('Date of Birth', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'sex': fields.selection(SEX, 'Sex', select=True, readonly=True,states={'Scheduled': [('readonly', False)]}),
        'marital_status': fields.selection(MARITAL_STATUS, 'Marital Status', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'blood_type': fields.selection(BLOOD_TYPE, 'Blood Type', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'rh': fields.selection(RH, 'Rh', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'doctor': fields.many2one('oeh.medical.physician', 'Responsible Physician', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'state': fields.selection(WALKIN_STATUS, 'State', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'comments': fields.text('Comments', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'date': fields.datetime('Date', required=True, readonly=True,states={'Scheduled': [('readonly', False)]}),
        'evaluation_ids': fields.one2many('oeh.medical.evaluation','walkin','Evaluation', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'prescription_ids': fields.one2many('oeh.medical.prescription','walkin','Prescriptions', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'lab_test_ids': fields.one2many('oeh.medical.lab.test','walkin','Lab Tests', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'inpatient_ids': fields.one2many('oeh.medical.inpatient','walkin','Inpatient Admissions', readonly=True,states={'Scheduled': [('readonly', False)]}),
        'vaccine_ids': fields.one2many('oeh.medical.vaccines','walkin','Vaccines', readonly=True,states={'Scheduled': [('readonly', False)]}),
    }
    _sql_constraints = [
        ('full_name_uniq', 'unique (name)', 'The Queue Number must be unique')
    ]
    _defaults = {
           'name': lambda obj, cr, uid, context: '/',
           'date': datetime.datetime.now(),
           'doctor': _get_physician,
           'state': lambda *a: 'Scheduled',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.appointment.register.walkin') or '/'
        return super(OeHealthAppointmentWalkin, self).create(cr, uid, vals, context=context)

    @api.multi
    def onchange_patient(self, patient):
        if patient:
            patient = self.env['oeh.medical.patient'].browse(patient)
            return {'value': {'dob': patient.dob, 'sex': patient.sex, 'marital_status': patient.marital_status, 'blood_type': patient.blood_type, 'rh': patient.rh}}
        return {}

    def _default_account(self,cr,uid,ids,context=None):
        journal_ids = self.pool.get('account.journal').search(cr,uid,[('type', '=', 'sale')],context=context, limit=1)
        journal = self.pool.get('account.journal').browse(cr, uid, journal_ids, context=context)
        return journal.default_credit_account_id.id

    def action_walkin_invoice_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        invoice_obj = self.pool.get("account.invoice")
        invoice_line_obj = self.pool.get("account.invoice.line")
        inv_ids = []

        for acc in self.browse(cr, uid, ids, context=context):
            # Create Invoice
            if acc.doctor:
                curr_invoice = {
                    'partner_id': acc.patient.partner_id.id,
                    'account_id': acc.patient.partner_id.property_account_receivable_id.id,
                    'patient': acc.patient.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice':acc.date,
                    'origin': "Walkin # : " + acc.name,
                }

                inv_ids = invoice_obj.create(cr, uid, curr_invoice, context)
                self.write(cr, uid, [acc.id], {'state': 'Invoiced'})

                if inv_ids:
                    prd_account_id = self._default_account(cr,uid,ids,context)

                    # Create Invoice line
                    curr_invoice_line = {
                        'name':"Consultancy invoice for " + acc.name,
                        'price_unit':acc.doctor.consultancy_price,
                        'quantity':1,
                        'account_id':prd_account_id,
                        'invoice_id':inv_ids,
                    }

                    inv_line_ids = invoice_line_obj.create(cr, uid, curr_invoice_line, context)
            else:
                raise UserError(_('Configuration error!\nCould not find any physician to create the invoice !'))

        return {
                'domain': "[('id','=', " + str(inv_ids) + ")]",
                'name': 'Walkin Invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }

    def set_to_completed(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Completed'}, context=context)

# Physician schedule management for Walkins

class OeHealthPhysicianWalkinSchedule (osv.osv):
    _name = "oeh.medical.physician.walkin.schedule"
    _description = "Information about walkin schedule"
    _columns = {
        'name': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
        'physician_id': fields.many2one('oeh.medical.physician', 'Physician',select=True,ondelete='cascade'),
    }
    _order = 'name desc'


# Inheriting Physician screen to add walkin schedule lines

class OeHealthPhysician (osv.osv):
    _inherit = "oeh.medical.physician"
    _columns = {
        'walkin_schedule_lines': fields.one2many('oeh.medical.physician.walkin.schedule', 'physician_id', 'Walkin Schedule'),
    }

# Inheriting Inpatient module to add "Walkin" screen reference
class OeHealthInpatient(osv.osv):
    _inherit='oeh.medical.inpatient'
    _columns = {
        'walkin': fields.many2one('oeh.medical.appointment.register.walkin','Queue #', readonly=True, states={'Draft': [('readonly', False)]}),
    }

# Inheriting Prescription module to add "Walkin" screen reference
class OeHealthPrescription(osv.osv):
    _inherit='oeh.medical.prescription'
    _columns = {
        'walkin': fields.many2one('oeh.medical.appointment.register.walkin','Queue #', readonly=True, states={'Draft': [('readonly', False)]}),
    }

# Inheriting Evaluation module to add "Walkin" screen reference
class OeHealthPatientEvaluation(osv.osv):
    _inherit='oeh.medical.evaluation'
    _columns = {
        'walkin': fields.many2one('oeh.medical.appointment.register.walkin','Queue #'),
    }

# Inheriting Evaluation module to add "Walkin" screen reference
class OeHealthLabTests(osv.osv):
    _inherit='oeh.medical.lab.test'
    _columns = {
        'walkin': fields.many2one('oeh.medical.appointment.register.walkin','Queue #', readonly=True, states={'Draft': [('readonly', False)]}),
    }

# Inheriting Evaluation module to add "Walkin" screen reference
class OeHealthVaccines(osv.osv):
    _inherit='oeh.medical.vaccines'
    _columns = {
        'walkin': fields.many2one('oeh.medical.appointment.register.walkin','Queue #'),
    }
