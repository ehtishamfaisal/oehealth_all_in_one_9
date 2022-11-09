##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp.osv import osv
from openerp.osv import fields


class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    _columns = {
        'patient': fields.many2one('oeh.medical.patient','Related Patient', help="Patient Name"),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
