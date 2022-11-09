##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp.osv import osv, fields

# Ethnic Groups Management

class OeHealthEthnicGroups(osv.Model):
    _name = 'oeh.medical.ethnicity'
    _description = "Ethnic Groups"

    _columns = {
        'name':fields.char('Ethnic Groups', size=256,required=True),
    }
    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'The ethnic group must be unique !')]