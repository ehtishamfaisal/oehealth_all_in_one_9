
from openerp.osv import osv, fields
from openerp import api

# Domiciliary Unit Management

class OeHealthDomiciliaryUnit (osv.osv):
    _name = 'oeh.medical.domiciliary.unit'
    _description = 'Domiciliary Unit Management'

    DWELLING = [
        ('Single / Detached House', 'Single / Detached House'),
        ('Apartment', 'Apartment'),
        ('Townhouse', 'Townhouse'),
        ('Factory', 'Factory'),
        ('Building', 'Building'),
        ('Mobile House', 'Mobile House'),
    ]

    MATERIAL = [
        ('Concrete', 'Concrete'),
        ('Adobe', 'Adobe'),
        ('Wood', 'Wood'),
        ('Mud / Straw', 'Mud / Straw'),
        ('Stone', 'Stone'),
    ]

    ROOF_TYPE = [
        ('Concrete', 'Concrete'),
        ('Adobe', 'Adobe'),
        ('Wood', 'Wood'),
        ('Thatched', 'Thatched'),
        ('Mud / Straw', 'Mud / Straw'),
        ('Stone', 'Stone'),
    ]

    HOUSING = [
        ('Shanty, deficient sanitary conditions', 'Shanty, deficient sanitary conditions'),
        ('Small, crowded but with good sanitary conditions', 'Small, crowded but with good sanitary conditions'),
        ('Comfortable and good sanitary conditions', 'Comfortable and good sanitary conditions'),
        ('Roomy and excellent sanitary conditions', 'Roomy and excellent sanitary conditions'),
        ('Luxury and excellent sanitary conditions', 'Luxury and excellent sanitary conditions'),
    ]

    _columns = {
        'name': fields.char('Code', size=128, required=True),
        'desc': fields.char('Desc', size=25, required=True),
        'address_street': fields.char('Street', size=25),
        'address_street_number': fields.integer('Street #'),
        'address_street_bis': fields.char('Apartment', size=25),
        'address_district': fields.char('District', size=25, help="Neighborhood, Village, Barrio...."),
        'address_municipality': fields.char('Municipality', size=25, help="Municipality, Township, county .."),
        'address_city': fields.char('City', size=25),
        'address_zip': fields.char('Zip Code', size=25),
        'address_country': fields.many2one('res.country', 'Country', help='Country'),
        'address_state': fields.many2one('res.country.state', 'State', help='State'),
        'institution': fields.many2one ('oeh.medical.health.center','Health Center'),
        'picture': fields.binary("Picture"),
        'dwelling': fields.selection(DWELLING, 'Type'),
        'materials': fields.selection(MATERIAL, 'Material'),
        'roof_type': fields.selection(ROOF_TYPE, 'Roof'),
        'total_surface': fields.integer('Surface', help="Surface in sq. meters"),
        'bedrooms': fields.integer('Bedrooms'),
        'bathrooms': fields.integer('Bathrooms'),
        'housing': fields.selection(HOUSING, 'Conditions', help="Housing and sanitary living conditions"),
        'sewers': fields.boolean('Sanitary Sewers'),
        'water': fields.boolean('Running Water'),
        'trash': fields.boolean('Trash recollection'),
        'electricity': fields.boolean('Electrical supply'),
        'gas': fields.boolean('Gas supply'),
        'telephone': fields.boolean('Telephone'),
        'television': fields.boolean('Television'),
        'internet': fields.boolean('Internet'),

    }
    _sql_constraints = [('name_uniq', 'unique(name)', 'The Domiciliary Unit name must be unique')]

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}