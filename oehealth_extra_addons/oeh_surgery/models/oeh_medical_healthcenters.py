from openerp.osv import osv, fields
from openerp.tools.translate import _

# Operating Theaters (OT) Management
class OeHealthCentersOperatingRooms(osv.osv):

    OT_STATES = [
        ('Free', 'Free'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
        ('Not Available', 'Not Available'),
    ]

    _name = 'oeh.medical.health.center.ot'
    _description = "Information about the health centers operating theaters"
    _columns = {
            'name': fields.char('Operation Theater Name', size=32, required=True),
            'building': fields.many2one ('oeh.medical.health.center.building','Building'),
            'info': fields.text ('Extra Info'),
            'state': fields.selection(OT_STATES,'Status'),
        }
    _defaults = {
            'state': 'Free',
        }
    _sql_constraints = [
            ('name_bed_uniq', 'unique (name)', 'The operation theater name is already occupied !')]

    # Preventing deletion of a operating theaters which is not in draft state
    def unlink(self, cr, uid, ids, context=None):
        stat = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for t in stat:
            if t['state'] in ('Free','Not Available'):
                unlink_ids.append(t['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), _('You can not delete operating theaters(s) which is in "Reserved" or "Occupied" state !!'))
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True

    def action_surgery_set_to_not_available(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Not Available'}, context=context)

    def action_surgery_set_to_available(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'Free'}, context=context)

class OeHealthCentersBuilding(osv.osv):

    def _ot_count(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        oe_ot = self.pool.get('oeh.medical.health.center.ot')
        for building in self.browse(cr, uid, ids, context=context):
            domain = [('building', '=', building.id)]
            ot_ids = oe_ot.search(cr, uid, domain, context=context)
            ots = oe_ot.browse(cr, uid, ot_ids, context=context)
            ot_count = 0
            for ot in ots:
                ot_count+=1
            result[building.id] = ot_count
        return result

    _inherit = 'oeh.medical.health.center.building'
    _columns = {
        'ot_count': fields.function(_ot_count, string="Operation Theaters", type="integer"),
    }

