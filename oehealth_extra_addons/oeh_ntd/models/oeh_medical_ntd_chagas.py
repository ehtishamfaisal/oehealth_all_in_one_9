
from openerp.osv import osv, fields
import datetime

class OeHealthNTDChagas(osv.osv):
    _name = 'oeh.medical.ntd.chagas'
    _description = 'Chagas DU Entomological Survey'

    DU_STATUS = [
        ('Initial', 'Initial'),
        ('Unchanged', 'Unchanged'),
        ('Improved', 'Improved'),
        ('Worsen', 'Worsen'),
    ]

    VECTOR = [
        ('T. infestans', 'T. infestans'),
        ('T. brasilensis', 'T. brasilensis'),
        ('R. prolixus', 'R. prolixus'),
        ('T. dimidiata', 'T. dimidiata'),
        ('P. megistus', 'P. megistus'),
    ]

    _columns = {
        'name': fields.char('Survey Code', size=128, readonly=True),
        'du': fields.many2one('oeh.medical.domiciliary.unit', 'Domiciliary Unit', required=True),
        'survey_date': fields.datetime('Survey Date', required=True),
        'du_status': fields.selection(DU_STATUS, 'Status', help="DU status compared to last visit", required=True),
        'triatomines': fields.boolean('Triatomines', help="Check this box if triatomines were found"),
        'vector': fields.selection(VECTOR, 'Vector'),
        'nymphs': fields.boolean('Nymphs', help="Check this box if triatomine nymphs were found"),
        't_in_house': fields.boolean('Domiciliary', help="Check this box if triatomines were found inside the house"),
        't_peri': fields.boolean('Peri-Domiciliary', help="Check this box if triatomines were found in the peridomiciliary area"),
        'dfloor': fields.boolean('Floor', help="Current floor can host triatomines"),
        'dwall': fields.boolean('Walls', help="Wall materials or state can host triatomines"),
        'droof': fields.boolean('Roof', help="Roof materials or state can host triatomines"),
        'dperi': fields.boolean('Peri-domicilary', help="Peri domiciliary area can host triatomines"),
        'bugtraps': fields.boolean('Bug traps', help="The DU has traps to detect triatomines"),
        'du_fumigation': fields.boolean('Fumigation', help="The DU has been fumigated"),
        'fumigation_date': fields.date('Fumigation Date',help="Last Fumigation Date"),
        'du_paint': fields.boolean ('Insecticide Paint', help="The DU has been treated with insecticide-containing paint"),
        'paint_date': fields.date('Paint Date', help="Last Paint Date"),
        'observations': fields.text('Observations'),
        'next_survey_date': fields.date('Next survey'),
    }
    _defaults = {
       'name': lambda obj, cr, uid, context: '/',
       'survey_date': datetime.datetime.now(),
    }
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.ntd.chagas') or '/'
        return super(OeHealthNTDChagas, self).create(cr, uid, vals, context=context)