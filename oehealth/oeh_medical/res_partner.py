##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp.osv import osv
from openerp.osv import fields


class oeHealthPartner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'is_insurance_company': fields.boolean(string='Insurance Company',
                            help='Check if the party is an Insurance Company'),
        'is_institution': fields.boolean(string='Institution',
                                help='Check if the party is a Medical Center'),
        'is_doctor': fields.boolean(string='Health Professional',
                            help='Check if the party is a health professional'),
        'is_patient': fields.boolean(string='Patient',
                                     help='Check if the party is a patient'),
        'is_person': fields.boolean(string='Person',
                                    help='Check if the party is a person.'),
        'is_pharmacy': fields.boolean(string='Pharmacy',
                                      help='Check if the party is a Pharmacy'),
        'ref': fields.char(size=256, string='SSN',
                           help='Patient Social Security Number or equivalent'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
