##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp import pooler, tools, api
from openerp.osv import osv, fields
import time
import datetime
from openerp.tools.translate import _


# Lab Units Management

class OeHealthLabTestUnits(osv.osv):
    _name = 'oeh.medical.lab.units'
    _description = 'Lab Test Units'
    _columns = {
        'name': fields.char('Unit Name', size=25, required=True),
        'code': fields.char('Code', size=25, required=True),
    }
    _sql_constraints = [('name_uniq', 'unique(name)', 'The Lab unit name must be unique')]


# Lab Test Types Management

class OeHealthLabTestCriteria(osv.osv):
    _name = 'oeh.medical.labtest.criteria'
    _description = 'Lab Test Criteria'
    _columns = {
        'name': fields.char('Tests', size=128, required=True),
        'normal_range': fields.text('Normal Range'),
        'units': fields.many2one('oeh.medical.lab.units', 'Units'),
        'sequence': fields.integer('Sequence'),
        'medical_type_id': fields.many2one('oeh.medical.labtest.types', 'Lab Test Types'),
    }
    _order="sequence"

class OeHealthLabTestTypes(osv.osv):
    _name = 'oeh.medical.labtest.types'
    _description = 'Lab Test Types'
    _columns = {
        'name': fields.char('Lab Test Name', size=128, required=True, help="Test type, eg X-Ray, Hemogram, Biopsy..."),
        'code': fields.char('Code', size=128, help="Short code for the test"),
        'info': fields.text('Description'),
        'test_charge': fields.float('Test Charge'),
        'lab_criteria': fields.one2many('oeh.medical.labtest.criteria','medical_type_id','Lab Test Cases'),
    }
    _defaults = {
        'test_charge': lambda *a: 0.0,
    }

class OeHealthLabTests(osv.osv):
    _name = 'oeh.medical.lab.test'
    _description = 'Lab Tests'

    LABTEST_STATE = [
        ('Draft', 'Draft'),
        ('Test In Progress', 'Test In Progress'),
        ('Completed', 'Completed'),
        ('Invoiced', 'Invoiced'),
    ]

    _columns = {
        'name': fields.char('Lab Test #', size=16, readonly=True, required=True, help="Lab result ID"),
        'test_type': fields.many2one('oeh.medical.labtest.types','Test Type', required=True, readonly=True, states={'Draft': [('readonly', False)]}, help="Lab test type"),
        'patient': fields.many2one ('oeh.medical.patient','Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'pathologist' : fields.many2one('oeh.medical.physician','Pathologist', help="Pathologist", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        #'requestor' : fields.many2one('oeh.medical.physician', 'Physician', help="Doctor who requested the test", readonly=True, states={'Draft': [('readonly', False)]}),
        'requestor' : fields.char('Doctor who requested the test', help="Doctor who requested the test", readonly=True, states={'Draft': [('readonly', False)]}),
        'results': fields.text('Results', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'diagnosis' : fields.text ('Diagnosis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'lab_test_criteria': fields.one2many('oeh.medical.lab.resultcriteria','medical_lab_test_id','Lab Test Result', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'date_requested': fields.datetime('Date requested', readonly=True, states={'Draft': [('readonly', False)]}),
        'date_analysis': fields.datetime('Date of the Analysis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'state': fields.selection(LABTEST_STATE, 'State',readonly=True),
    }
    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
        'date_requested': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': lambda *a: 'Draft',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.lab.test') or '/'
        return super(OeHealthLabTests, self).create(cr, uid, vals, context=context)

    def onchange_test_type_id(self, cr, uid, ids, test_type=False,context=None):
        criteria_obj = self.pool.get('oeh.medical.labtest.criteria')
        labtest_ids =[]

        if context is None:
            context = {}

        #defaults
        res = {'value':{
                'lab_test_criteria':[],
            }
        }

        # if no test type present then nothing will process
        if (not test_type):
            return res

        # Getting lab test lines values
        test_type_ids1 = criteria_obj.search(cr, uid, [('medical_type_id', '=', test_type)], context=context)
        for tt_id in criteria_obj.browse(cr, uid, test_type_ids1, context=context):
                specs = {
                          'name': tt_id.name,
                          'sequence': tt_id.sequence,
                          'normal_range': tt_id.normal_range,
                          'units': tt_id.units.id,
                        }
                labtest_ids += [specs]

        res['value'].update({
            'lab_test_criteria': labtest_ids,
        })
        return res

    def print_patient_labtest(self, cr, uid, ids, context=None):
        '''
        This function prints the lab test
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        return self.pool['report'].get_action(cr, uid, ids, 'oehealth.report_oeh_medical_patient_labtest', context=context)

    def set_to_test_inprogress(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Test In Progress', 'date_analysis': datetime.datetime.now()}, context=context)

    def set_to_test_complete(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Completed'}, context=context)

    def _default_account(self,cr,uid,ids,context=None):
        journal_ids = self.pool.get('account.journal').search(cr,uid,[('type', '=', 'sale')],context=context, limit=1)
        journal = self.pool.get('account.journal').browse(cr, uid, journal_ids, context=context)
        return journal.default_credit_account_id.id

    def action_lab_invoice_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        invoice_obj = self.pool.get("account.invoice")
        invoice_line_obj = self.pool.get("account.invoice.line")
        inv_ids = []
        inv_line_ids = []

        for lab in self.browse(cr, uid, ids, context=context):
            # Create Invoice
            if lab.patient:
                curr_invoice = {
                    'partner_id': lab.patient.partner_id.id,
                    'account_id': lab.patient.partner_id.property_account_receivable_id.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice':datetime.datetime.now(),
                    'origin': "Lab Test# : " + lab.name,
                    'target': 'new',
                }

                inv_ids = invoice_obj.create(cr, uid, curr_invoice, context)
                self.write(cr, uid, [lab.id], {'state': 'Invoiced'})

                if inv_ids:
                    prd_account_id = self._default_account(cr,uid,ids,context)
                    if lab.test_type:

                        # Create Invoice line
                        curr_invoice_line = {
                            'name': "Charge for " + str(lab.test_type.name) + " laboratory test",
                            'price_unit': lab.test_type.test_charge or 0,
                            'quantity': 1.0,
                            'account_id': prd_account_id,
                            'invoice_id': inv_ids,
                        }

                        inv_line_ids = invoice_line_obj.create(cr, uid, curr_invoice_line, context)

        return {
                'domain': "[('id','=', " + str(inv_ids) + ")]",
                'name': 'Lab Test Invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }



class OeHealthLabTestsResultCriteria(osv.osv):
    _name = 'oeh.medical.lab.resultcriteria'
    _description = 'Lab Test Result Criteria'
    _columns = {
        'name': fields.char('Tests', size=128, required=True),
        'result': fields.text('Result'),
        'normal_range': fields.text('Normal Range'),
        'units': fields.many2one('oeh.medical.lab.units', 'Units'),
        'sequence': fields.integer('Sequence'),
        'medical_lab_test_id': fields.many2one('oeh.medical.lab.test', 'Lab Tests'),
    }
    _order="sequence"

# Inheriting Patient module to add "Lab" screen reference
class OeHealthPatient(osv.osv):
    _inherit='oeh.medical.patient'
    _columns = {
        'lab_test_ids': fields.one2many('oeh.medical.lab.test','patient','Lab Tests'),
    }