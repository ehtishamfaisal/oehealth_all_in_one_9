##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp import pooler, tools, api
from openerp.osv import osv, fields

# Genetics Management

class OeHealthGenetics(osv.osv):
    _name = 'oeh.medical.genetics'
    _description = "Information about the genetics risks"

    DOMINANCE = [
        ('Dominant','Dominant'),
        ('Recessive','Recessive'),
    ]
    _columns = {
        'name': fields.char('Official Symbol', size=16),
        'long_name': fields.char('Official Long Name', size=256),
        'gene_id': fields.char('Gene ID', size=8, help="Default code from NCBI Entrez database."),
        'chromosome': fields.char('Affected Chromosome', size=2, help="Name of the affected chromosome"),
        'location': fields.char('Location', size=32, help="Locus of the chromosome"),
        'dominance': fields.selection(DOMINANCE, 'Dominance', select=True),
        'info': fields.text('Information', size=128, help="Name of the protein(s) affected"),
    }