
from openerp.osv import osv, fields
import datetime

class OeHealthNTDDengue(osv.osv):
    _name = 'oeh.medical.ntd.dengue'
    _description = 'Dengue DU Survey'

    DU_STATUS = [
        ('Initial', 'Initial'),
        ('Unchanged', 'Unchanged'),
        ('Improved', 'Improved'),
        ('Worsen', 'Worsen'),
    ]

    _columns = {
        'name': fields.char('Survey Code', size=128, readonly=True),
        'du': fields.many2one('oeh.medical.domiciliary.unit', 'Domiciliary Unit', required=True),
        'survey_date': fields.datetime('Survey Date', required=True),
        'du_status': fields.selection(DU_STATUS, 'Status', help="DU status compared to last visit", required=True),
        'ovitraps': fields.boolean('Ovitraps', help="Check if ovitraps are in place"),
        'aedes_larva': fields.boolean('Larvae', help="Check this box if Aedes aegypti larvae were found"),
        'larva_in_house': fields.boolean('Domiciliary', help="Check this box if larvae were found inside the house"),
        'larva_peri': fields.boolean('Peri-Domiciliary', help="Check this box if larva were found in the peridomiciliary area"),
        'old_tyres': fields.boolean('Tyres', help="Old vehicle tyres found"),
        'animal_water_container': fields.boolean('Animal Water containers', help="Animal water containers not scrubbed or clean"),
        'flower_vase': fields.boolean('Flower vase', help="Flower vases without scrubbing or cleaning"),
        'potted_plant': fields.boolean('Potted Plants', help="Potted Plants with saucers"),
        'tree_holes': fields.boolean('Tree holes', help="Unfilled tree holes"),
        'rock_holes': fields.boolean('Rock holes', help="Unfilled rock holes"),
        'du_fumigation': fields.boolean('Fumigation', help="The DU has been fumigated"),
        'fumigation_date': fields.date('Fumigation Date',help="Last Fumigation Date"),
        'observations': fields.text('Observations'),
        'next_survey_date': fields.date('Next survey'),
    }
    _defaults = {
       'name': lambda obj, cr, uid, context: '/',
       'survey_date': datetime.datetime.now(),
    }
    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.ntd.dengue') or '/'
        return super(OeHealthNTDDengue, self).create(cr, uid, vals, context=context)
