##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp.osv import osv
from openerp.osv import fields


class oeHealthProduct(osv.osv):
    _inherit = 'product.product'

    _columns = {
        'is_medicine': fields.boolean(string='Medicine', help='Check if the product is a medicine'),
        'is_bed': fields.boolean(string='Bed', help='Check if the product is a bed'),
        'is_vaccine': fields.boolean(string='Vaccine', help='Check if the product is a vaccine'),
        'is_medical_supply' : fields.boolean(string='Medical Supply', help='Check if the product is a medical supply'),
        'is_insurance_plan' : fields.boolean(string='Insurance Plan', help='Check if the product is an insurance plan'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
