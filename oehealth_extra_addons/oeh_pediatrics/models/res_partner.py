##############################################################################
#    Copyright (C) 2016 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp.osv import osv
from openerp.osv import fields


class oeHealthPartner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'is_baby': fields.boolean(string='Baby',
                            help='Check if the party is a baby'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
