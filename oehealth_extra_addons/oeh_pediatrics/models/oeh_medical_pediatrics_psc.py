from openerp import pooler, tools, api
from openerp.osv import osv, fields
import datetime
from openerp.tools.translate import _
from openerp.exceptions import UserError

# Pediatrics Symptom Checklist Management

class OeHealthPediatricSymptomsChecklist(osv.osv):
    _name = "oeh.medical.pediatrics.psc"
    _description = "Pediatrics Symptom Checklist"

    PSC_CONF = [
        ('0', 'Never'),
        ('1', 'Sometimes'),
        ('2', 'Often'),
    ]

    _columns = {
        'name': fields.char('PSC #', size=64, readonly=True, required=True),
        'patient': fields.many2one('oeh.medical.patient','Patient', help="Patient Name",required=True),
        'doctor': fields.many2one('oeh.medical.physician','Physician', domain=[('is_pharmacist','=',False)], help="Current primary care / family doctor", required=True),
        'evaluation_start': fields.datetime('Date', required=True),
        'notes': fields.text('Notes'),
        'psc_aches_pains': fields.selection(PSC_CONF, 'Complains of aches and pains'),
        'psc_less_interest_in_school': fields.selection(PSC_CONF, 'Less interested in school'),
        'psc_spend_time_alone': fields.selection(PSC_CONF, 'Spends more time alone'),
        'psc_tires_easily': fields.selection(PSC_CONF, 'Tires easily, has little energy'),
        'psc_fidgety': fields.selection(PSC_CONF, 'Fidgety, unable to sit still'),
        'psc_trouble_with_teacher': fields.selection(PSC_CONF, 'Has trouble with teacher'),
        'psc_acts_as_driven_by_motor': fields.selection(PSC_CONF, 'Acts as if driven by a motor'),
        'psc_daydreams_too_much': fields.selection(PSC_CONF, 'Daydreams too much'),
        'psc_distracted_easily': fields.selection(PSC_CONF, 'Distracted easily'),
        'psc_afraid_of_new_situations': fields.selection(PSC_CONF, 'Is afraid of new situations'),
        'psc_sad_unhappy': fields.selection(PSC_CONF, 'Feels sad, unhappy'),
        'psc_irritable_angry': fields.selection(PSC_CONF, 'Is irritable, angry'),
        'psc_feels_hopeless': fields.selection(PSC_CONF, 'Feels hopeless'),
        'psc_trouble_concentrating': fields.selection(PSC_CONF, 'Has trouble concentrating'),
        'psc_less_interested_in_friends': fields.selection(PSC_CONF, 'Less interested in friends'),
        'psc_fights_with_others': fields.selection(PSC_CONF, 'Fights with other children'),
        'psc_absent_from_school': fields.selection(PSC_CONF, 'Absent from school'),
        'psc_school_grades_dropping': fields.selection(PSC_CONF, 'School grades dropping'),
        'psc_down_on_self': fields.selection(PSC_CONF, 'Is down on him or herself'),
        'psc_visit_doctor_finds_ok': fields.selection(PSC_CONF, 'Visits the doctor with doctor finding nothing wrong'),
        'psc_trouble_sleeping': fields.selection(PSC_CONF, 'Has trouble sleeping'),
        'psc_worries_a_lot': fields.selection(PSC_CONF, 'Worries a lot'),
        'psc_wants_to_be_with_parents': fields.selection(PSC_CONF, 'Wants to be with you more than before'),
        'psc_feels_is_bad_child': fields.selection(PSC_CONF, 'Feels he or she is bad'),
        'psc_takes_unnecesary_risks': fields.selection(PSC_CONF, 'Takes unnecessary risks'),
        'psc_gets_hurt_often': fields.selection(PSC_CONF, 'Gets hurt frequently'),
        'psc_having_less_fun': fields.selection(PSC_CONF, 'Seems to be having less fun'),
        'psc_act_as_younger': fields.selection(PSC_CONF, 'Acts younger than children his or her age'),
        'psc_does_not_listen_to_rules': fields.selection(PSC_CONF, 'Does not listen to rules'),
        'psc_does_not_show_feelings': fields.selection(PSC_CONF, 'Does not show feelings'),
        'psc_does_not_get_people_feelings': fields.selection(PSC_CONF, 'Does not get people feelings'),
        'psc_teases_others': fields.selection(PSC_CONF, 'Teases others'),
        'psc_blames_others': fields.selection(PSC_CONF, 'Blames others for his or her troubles'),
        'psc_takes_things_from_others': fields.selection(PSC_CONF, 'Takes things that do not belong to him or her'),
        'psc_refuses_to_share': fields.selection(PSC_CONF, 'Refuses to share'),
        'psc_total': fields.integer('PSC Total', required=True),
    }
    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
        'psc_total': lambda *a: 0,
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'oeh.medical.pediatrics.psc') or '/'
        return super(OeHealthPediatricSymptomsChecklist, self).create(cr, uid, vals, context=context)

    @api.multi
    def on_change_with_psc_total(self, psc_aches_pains, psc_spend_time_alone,
                                 psc_tires_easily, psc_fidgety, psc_trouble_with_teacher,
                                 psc_less_interest_in_school, psc_acts_as_driven_by_motor,
                                 psc_daydreams_too_much, psc_distracted_easily,
                                 psc_afraid_of_new_situations, psc_sad_unhappy,
                                 psc_irritable_angry, psc_feels_hopeless,
                                 psc_trouble_concentrating, psc_less_interested_in_friends,
                                 psc_fights_with_others, psc_absent_from_school,
                                 psc_school_grades_dropping, psc_down_on_self,
                                 psc_visit_doctor_finds_ok, psc_trouble_sleeping,
                                 psc_worries_a_lot, psc_wants_to_be_with_parents,
                                 psc_feels_is_bad_child, psc_takes_unnecesary_risks,
                                 psc_gets_hurt_often, psc_having_less_fun,
                                 psc_act_as_younger, psc_does_not_listen_to_rules,
                                 psc_does_not_show_feelings,
                                 psc_does_not_get_people_feelings,
                                 psc_teases_others, psc_takes_things_from_others,
                                 psc_refuses_to_share):

        psc_aches_pains = psc_aches_pains or '0'
        psc_spend_time_alone = psc_spend_time_alone or '0'
        psc_tires_easily = psc_tires_easily or '0'
        psc_fidgety = psc_fidgety or '0'
        psc_trouble_with_teacher = psc_trouble_with_teacher or '0'
        psc_less_interest_in_school = psc_less_interest_in_school or '0'
        psc_acts_as_driven_by_motor = psc_acts_as_driven_by_motor or '0'
        psc_daydreams_too_much = psc_daydreams_too_much or '0'
        psc_distracted_easily = psc_distracted_easily or '0'
        psc_afraid_of_new_situations = psc_afraid_of_new_situations or '0'
        psc_sad_unhappy = psc_sad_unhappy or '0'
        psc_irritable_angry = psc_irritable_angry or '0'
        psc_feels_hopeless = psc_feels_hopeless or '0'
        psc_trouble_concentrating = psc_trouble_concentrating or '0'
        psc_less_interested_in_friends = psc_less_interested_in_friends or '0'
        psc_fights_with_others = psc_fights_with_others or '0'
        psc_absent_from_school = psc_absent_from_school or '0'
        psc_school_grades_dropping = psc_school_grades_dropping or '0'
        psc_down_on_self = psc_down_on_self or '0'
        psc_visit_doctor_finds_ok = psc_visit_doctor_finds_ok or '0'
        psc_trouble_sleeping = psc_trouble_sleeping or '0'
        psc_worries_a_lot = psc_worries_a_lot or '0'
        psc_wants_to_be_with_parents = psc_wants_to_be_with_parents or '0'
        psc_feels_is_bad_child = psc_feels_is_bad_child or '0'
        psc_takes_unnecesary_risks = psc_takes_unnecesary_risks or '0'
        psc_gets_hurt_often = psc_gets_hurt_often or '0'
        psc_having_less_fun = psc_having_less_fun or '0'
        psc_act_as_younger = psc_act_as_younger or '0'
        psc_does_not_listen_to_rules = psc_does_not_listen_to_rules or '0'
        psc_does_not_show_feelings = psc_does_not_show_feelings or '0'
        psc_does_not_get_people_feelings = psc_does_not_get_people_feelings or '0'
        psc_teases_others = psc_teases_others or '0'
        psc_takes_things_from_others = psc_takes_things_from_others or '0'
        psc_refuses_to_share = psc_refuses_to_share or '0'

        psc_total = int(psc_aches_pains) + int(psc_spend_time_alone) + \
            int(psc_tires_easily) + int(psc_fidgety) + \
            int(psc_trouble_with_teacher) + \
            int(psc_less_interest_in_school) + \
            int(psc_acts_as_driven_by_motor) + \
            int(psc_daydreams_too_much) + int(psc_distracted_easily) + \
            int(psc_afraid_of_new_situations) + int(psc_sad_unhappy) + \
            int(psc_irritable_angry) + int(psc_feels_hopeless) + \
            int(psc_trouble_concentrating) + \
            int(psc_less_interested_in_friends) + \
            int(psc_fights_with_others) + int(psc_absent_from_school) + \
            int(psc_school_grades_dropping) + int(psc_down_on_self) + \
            int(psc_visit_doctor_finds_ok) + int(psc_trouble_sleeping) + \
            int(psc_worries_a_lot) + int(psc_wants_to_be_with_parents) + \
            int(psc_feels_is_bad_child) + int(psc_takes_unnecesary_risks) + \
            int(psc_gets_hurt_often) + int(psc_having_less_fun) + \
            int(psc_act_as_younger) + int(psc_does_not_listen_to_rules) + \
            int(psc_does_not_show_feelings) + \
            int(psc_does_not_get_people_feelings) + \
            int(psc_teases_others) + \
            int(psc_takes_things_from_others) + \
            int(psc_refuses_to_share)

        return {'value': {'psc_total': psc_total}}

# Inheriting Patient module to add "Pediatrics Symptom Checklist" screen reference
class OeHealthPatient(osv.osv):
    _inherit='oeh.medical.patient'
    _columns = {
        'pediatrics_psc_ids': fields.one2many('oeh.medical.pediatrics.psc','patient','Pediatrics Symptom Checklist'),
    }