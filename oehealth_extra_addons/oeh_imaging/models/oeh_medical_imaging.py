from openerp.osv import osv, fields
import time
import datetime
from openerp.tools.translate import _

# Imaging Test Type Management

class OeHealthImagingTestType (osv.osv):
    _name = 'oeh.medical.imaging.test.type'
    _description = 'Imaging Test Type Configuration'
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'code': fields.char('Code', size=25, required=True),
        'test_charge': fields.float('Test Charge', required=True),
    }
    _defaults = {
        'test_charge': lambda *a: 0.0,
    }
    _sql_constraints = [('name_uniq', 'unique(name)', 'The Imaging test type name must be unique')]


# Imaging Test Management

class OeHealthImagingTypeManagement (osv.osv):
    _name = 'oeh.medical.imaging'
    _description = 'Imaging Test Management'

    IMAGING_STATE = [
        ('Draft', 'Draft'),
        ('Test In Progress', 'Test In Progress'),
        ('Completed', 'Completed'),
        ('Invoiced', 'Invoiced'),
    ]

    _columns = {
        'name': fields.char('Test #', size=16, required=True, readonly=True),
        'patient': fields.many2one ('oeh.medical.patient','Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]}),
        'test_type': fields.many2one('oeh.medical.imaging.test.type','Test Type', required=True, readonly=True, states={'Draft': [('readonly', False)]}, help="Imaging Test type"),
        'requestor' : fields.many2one('oeh.medical.physician', 'Doctor who requested the test', domain=[('is_pharmacist','=',False)], help="Doctor who requested the test", readonly=True, states={'Draft': [('readonly', False)]}),
        'analysis': fields.text('Analysis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'conclusion' : fields.text ('Conclusion', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'date_requested': fields.datetime('Date requested', readonly=True, states={'Draft': [('readonly', False)]}),
        'date_analysis': fields.datetime('Date of the Analysis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'state': fields.selection(IMAGING_STATE, 'State',readonly=True),
        'image1': fields.binary("Image 1", readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'image2': fields.binary("Image 2", readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'image3': fields.binary("Image 3", readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'image4': fields.binary("Image 4", readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'image5': fields.binary("Image 5", readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
        'image6': fields.binary("Image 6", readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}),
    }
    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
        'date_requested': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'state': lambda *a: 'Draft',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.imaging') or '/'
        return super(OeHealthImagingTypeManagement, self).create(cr, uid, vals, context=context)

    def print_patient_imaging(self, cr, uid, ids, context=None):
        '''
        This function prints the xray test
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        return self.pool['report'].get_action(cr, uid, ids, 'oehealth_imaging.report_oeh_medical_patient_imaging', context=context)


    # Preventing deletion of a imaging details which is not in draft state
    def unlink(self, cr, uid, ids, context=None):
        stat = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for t in stat:
            if t['state'] in ('Draft'):
                unlink_ids.append(t['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), _('You can not delete imaging information which is not in "Draft" state !!'))
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True

    def set_to_test_start(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Test In Progress','date_analysis':datetime.datetime.now()}, context=context)

    def set_to_test_complete(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Completed'}, context=context)

    def _default_account(self,cr,uid,ids,context=None):
        journal_ids = self.pool.get('account.journal').search(cr,uid,[('type', '=', 'sale')],context=context, limit=1)
        journal = self.pool.get('account.journal').browse(cr, uid, journal_ids, context=context)
        return journal.default_credit_account_id.id

    def action_imaging_invoice_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        invoice_obj = self.pool.get("account.invoice")
        invoice_line_obj = self.pool.get("account.invoice.line")
        inv_ids = []
        inv_line_ids = []

        for imaging in self.browse(cr, uid, ids, context=context):
            # Create Invoice
            if imaging.patient:
                curr_invoice = {
                    'partner_id': imaging.patient.partner_id.id,
                    'account_id': imaging.patient.partner_id.property_account_receivable_id.id,
                    'patient': imaging.patient.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice':datetime.datetime.now(),
                    'origin': "Imaging Test# : " + imaging.name,
                    'target': 'new',
                }

                inv_ids = invoice_obj.create(cr, uid, curr_invoice, context)
                self.write(cr, uid, [imaging.id], {'state': 'Invoiced'})

                if inv_ids:
                    prd_account_id = self._default_account(cr,uid,ids,context)
                    if imaging.test_type:

                        # Create Invoice line
                        curr_invoice_line = {
                            'name': "Charge for " + str(imaging.test_type.name) + " Imaging test",
                            'price_unit': imaging.test_type.test_charge or 0,
                            'quantity': 1.0,
                            'account_id': prd_account_id,
                            'invoice_id': inv_ids,
                        }

                        inv_line_ids = invoice_line_obj.create(cr, uid, curr_invoice_line, context)

        return {
                'domain': "[('id','=', " + str(inv_ids) + ")]",
                'name': 'Imaging Test Invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }