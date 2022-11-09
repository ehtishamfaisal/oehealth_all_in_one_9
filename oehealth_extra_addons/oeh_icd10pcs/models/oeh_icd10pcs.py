# -*- encoding: utf-8 -*-
from openerp import pooler, tools, api
from openerp.osv import osv, fields


class OeHealthIC10Procedures(osv.osv):
    _name = 'oeh.medical.procedure'
    _description = 'IC10 Procedure Codes'

    _columns = {
        'name': fields.char('Code', size=16, required=True),
        'description' : fields.char('Long Text', size=256, required=True),
    }

