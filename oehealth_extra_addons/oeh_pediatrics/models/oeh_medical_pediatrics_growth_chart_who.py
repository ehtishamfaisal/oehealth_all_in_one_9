from openerp.osv import osv, fields

class OeHealthPediatricsNewBorn(osv.osv):
    _name = "oeh.medical.pediatrics.growth.chart.who"

    SEX = [
        ('m', 'Male'),
        ('f', 'Female'),
    ]

    MEASURE = [
        ('p', 'Percentiles'),
        ('z', 'Z-scores'),
    ]

    INDICATOR = [
        ('l/h-f-a', 'Length/height for age'),
        ('w-f-a', 'Weight for age'),
        ('bmi-f-a', 'Body mass index for age (BMI for age)'),
    ]

    _columns = {
        'indicator': fields.selection(INDICATOR, 'Indicator', required=True),
        'measure': fields.selection(MEASURE, 'Measure', required=True),
        'sex': fields.selection(SEX, 'Sex'),
        'month': fields.integer('Month'),
        'type': fields.char('Type', size=56),
        'value': fields.float('Value')
    }