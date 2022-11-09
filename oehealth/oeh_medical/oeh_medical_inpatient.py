##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp import pooler, tools, api
from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _
from datetime import date

# Inpatient Hospitalization Management

class OeHealthInpatient(osv.osv):
    _name = 'oeh.medical.inpatient'
    _description = "Information about the Patient administration"

    ADMISSION_TYPE = [
            ('Routine', 'Routine'),
            ('Maternity', 'Maternity'),
            ('Elective', 'Elective'),
            ('Urgent', 'Urgent'),
            ('Emergency', 'Emergency'),
            ('Other', 'Other'),
        ]

    INPATIENT_STATES = [
            ('Draft', 'Draft'),
            ('Hospitalized', 'Hospitalized'),
            ('Invoiced', 'Invoiced'),
            ('Discharged', 'Discharged'),
            ('Cancelled', 'Cancelled'),
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
        'name': fields.char('Inpatient #', size=128, readonly=True, required=True),
        'patient': fields.many2one('oeh.medical.patient', 'Patient', help="Patient Name", required=True, readonly=True,states={'Draft': [('readonly', False)]}),
        'admission_type': fields.selection(ADMISSION_TYPE, 'Admission Type', required=True, readonly=True,states={'Draft': [('readonly', False)]}),
        'admission_reason': fields.many2one('oeh.medical.pathology', 'Reason for Admission', help="Reason for Admission", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'admission_date': fields.datetime('Hospitalization Date', readonly=True, states={'Draft': [('readonly', False)]}),
        'discharge_date': fields.datetime('Discharge Date', readonly=False, states={'Discharged': [('readonly', True)]}),
        'attending_physician': fields.many2one('oeh.medical.physician', 'Attending Physician', readonly=False,states={'Discharged': [('readonly', True)]}),
        'operating_physician': fields.many2one('oeh.medical.physician', 'Operating Physician', readonly=False,states={'Discharged': [('readonly', True)]}),
        'ward': fields.many2one('oeh.medical.health.center.ward', 'Ward', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'bed': fields.many2one('oeh.medical.health.center.beds', 'Bed', required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'nursing_plan': fields.text('Nursing Plan', readonly=False,states={'Discharged': [('readonly', True)]}),
        'discharge_plan': fields.text('Discharge Plan', readonly=False,states={'Discharged': [('readonly', True)]}),
        'admission_condition': fields.text('Condition before Admission', readonly=True,states={'Draft': [('readonly', False)]}),
        'info': fields.text ('Extra Info', readonly=False,states={'Discharged': [('readonly', True)]}),
        'state': fields.selection(INPATIENT_STATES, 'State'),
    }
    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
        'state': lambda *a: 'Draft',
        'attending_physician': _get_physician,
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.inpatient') or '/'
        return super(OeHealthInpatient, self).create(cr, uid, vals, context=context)

    def _default_account(self,cr,uid,ids,context=None):
        journal_ids = self.pool.get('account.journal').search(cr,uid,[('type', '=', 'sale')],context=context, limit=1)
        journal = self.pool.get('account.journal').browse(cr, uid, journal_ids, context=context)
        return journal.default_credit_account_id.id

    def set_to_hospitalized(self, cr, uid, ids, context=None):
        hospitalized_date = False
        bed_obj = self.pool.get("oeh.medical.health.center.beds")
        for ina in self.browse(cr, uid, ids):
            if ina.admission_date:
                hospitalized_date = ina.admission_date
            else:
                hospitalized_date = datetime.datetime.now()

            if ina.bed:
                bed_obj.write(cr,uid,[ina.bed.id], {'state': 'Occupied'}, context=context)
        return self.write(cr, uid, ids, {'state': 'Hospitalized', 'admission_date': hospitalized_date}, context=context)

    def set_to_discharged(self, cr, uid, ids, context=None):
        discharged_date = False
        bed_obj = self.pool.get("oeh.medical.health.center.beds")
        for ina in self.browse(cr, uid, ids):
            if ina.discharge_date:
                discharged_date = ina.discharge_date
            else:
                discharged_date = datetime.datetime.now()

            if ina.bed:
                bed_obj.write(cr,uid,[ina.bed.id], {'state': 'Free'}, context=context)
        return self.write(cr, uid, ids, {'state': 'Discharged', 'discharge_date': discharged_date}, context=context)

    def set_to_invoiced(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        invoice_obj = self.pool.get("account.invoice")
        invoice_line_obj = self.pool.get("account.invoice.line")
        inv_ids = []
        res = {}

        for inpatient in self.browse(cr, uid, ids, context=context):

            # Calculate Hospitalized duration
            duration = 1

            if inpatient.admission_date and inpatient.discharge_date:
                #delta = datetime.datetime(inpatient.admission_date) - datetime.datetime(inpatient.discharge_date)
                #duration = delta.days
                admission_date = datetime.datetime.strptime(inpatient.admission_date, "%Y-%m-%d %H:%M:%S")
                discharge_date = datetime.datetime.strptime(inpatient.discharge_date, "%Y-%m-%d %H:%M:%S")
                delta = date(discharge_date.year,discharge_date.month,discharge_date.day) - date(admission_date.year,admission_date.month,admission_date.day)
                if delta.days == 0:
                    duration = 1
                else:
                    duration = delta.days

            # Create Invoice
            if inpatient.bed:
                curr_invoice = {
                    'partner_id': inpatient.patient.partner_id.id,
                    'account_id': inpatient.patient.partner_id.property_account_receivable_id.id,
                    'patient': inpatient.patient.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice': datetime.datetime.now(),
                    'origin': "Inpatient# : " + inpatient.name,
                    'target': 'new',
                }

                inv_ids = invoice_obj.create(cr, uid, curr_invoice, context)

                prd_account_id = self._default_account(cr,uid,ids,context)

                # Create Invoice line
                curr_invoice_line = {
                    'name': "Inpatient Admission charge for " + str(duration) + " day(s) of " + inpatient.bed.product_id.name,
                    'product_id': inpatient.bed.product_id.id,
                    'price_unit': duration * inpatient.bed.list_price,
                    'quantity': 1.0,
                    'account_id': prd_account_id,
                    'invoice_id': inv_ids,
                }
                inv_line_ids = invoice_line_obj.create(cr, uid, curr_invoice_line, context)
                #invoice_obj.button_compute(cr, uid, [inv_ids], context=context, set_total=('type' in ('in_invoice', 'in_refund')))
                res = self.write(cr, uid, ids, {'state': 'Invoiced'}, context=context)

            else:
                raise osv.except_osv(_('Error'), _('Please first select bed to raise an invoice !'))
        return res

    def set_to_cancelled(self, cr, uid, ids, context=None):
        bed_obj = self.pool.get("oeh.medical.health.center.beds")
        for ina in self.browse(cr, uid, ids):
            if ina.bed:
                bed_obj.write(cr,uid,[ina.bed.id], {'state': 'Free'}, context=context)
        return self.write(cr, uid, ids, {'state': 'Cancelled'}, context=context)

    def set_to_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Draft'}, context=context)

class OeHealthInpatientProfile(osv.osv):
    _name = "oeh.medical.inpatient.mydetails"
    _description = "Patient view only own admissions"
    _auto = False

    INPATIENT_STATES = [
            ('Draft', 'Draft'),
            ('Hospitalized', 'Hospitalized'),
            ('Invoiced', 'Invoiced'),
            ('Discharged', 'Discharged'),
            ('Cancelled', 'Cancelled'),
        ]

    _columns = {
        'name': fields.char('Inpatient #', size=128, readonly=True),
        'patient': fields.many2one('oeh.medical.patient', 'Patient', help="Patient Name", readonly=True),
        'admission_type': fields.char('Admission Type', size=128, readonly=True),
        'admission_reason': fields.many2one('oeh.medical.pathology', 'Reason for Admission', help="Reason for Admission", readonly=True),
        'admission_date': fields.datetime('Hospitalization Date', readonly=True),
        'discharge_date': fields.datetime('Discharge Date', readonly=True),
        'attending_physician': fields.many2one('oeh.medical.physician', 'Attending Physician', readonly=True),
        'operating_physician': fields.many2one('oeh.medical.physician', 'Operating Physician', readonly=True),
        'ward': fields.many2one('oeh.medical.health.center.ward', 'Ward', required=True, readonly=True),
        'bed': fields.many2one('oeh.medical.health.center.beds', 'Bed', required=True, readonly=True),
        'nursing_plan': fields.text('Nursing Plan', readonly=True),
        'discharge_plan': fields.text('Discharge Plan', readonly=True),
        'admission_condition': fields.text('Condition before Admission', readonly=True),
        'info': fields.text('Extra Info', readonly=True),
        'state': fields.selection(INPATIENT_STATES, 'State', readonly=True),

    }
    def init(self, cr):

        tools.drop_view_if_exists(cr, 'oeh_medical_inpatient_mydetails')
        cr.execute("""
            create or replace view oeh_medical_inpatient_mydetails as (
                 select
                     o.id as id,
                     o.name as name,
                     o.patient as patient,
                     o.admission_type as admission_type,
                     o.admission_date as admission_date,
                     o.admission_reason as admission_reason,
                     o.discharge_date as discharge_date,
                     o.attending_physician as attending_physician,
                     o.operating_physician as operating_physician,
                     o.ward as ward,
                     o.bed as bed,
                     o.nursing_plan as nursing_plan,
                     o.discharge_plan as discharge_plan,
                     o.admission_condition as admission_condition,
                     o.info as info,
                     o.state as state
                 from
                     oeh_medical_inpatient o
            )
        """)