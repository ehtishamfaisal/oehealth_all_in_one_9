##############################################################################
#    Copyright (C) 2015 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from openerp.osv import osv, fields

# Recreational Drugs Management
class OeHealthRecreationalDrug(osv.osv):
    _name = "oeh.medical.recreational.drugs"
    _description = "Recreational Drugs"

    TOXICITY = [
        ('None', 'None'),
        ('Low', 'Low'),
        ('High', 'High'),
        ('Extreme', 'Extreme'),
    ]

    ADDICTION_LEVEL = [
        ('None', 'None'),
        ('Low', 'Low'),
        ('High', 'High'),
        ('Extreme', 'Extreme'),
    ]

    LEGAL = [
        ('Legal', 'Legal'),
        ('Illegal', 'Illegal'),
    ]

    DRUG_CATEGORY = [
        ('Cannabinoids', 'Cannabinoids'),
        ('Depressants', 'Depressants'),
        ('Dissociative Anesthetics', 'Dissociative Anesthetics'),
        ('Hallucinogens', 'Hallucinogens'),
        ('Opioids', 'Opioids'),
        ('Stimulants', 'Stimulants'),
        ('Others', 'Others'),
    ]

    _columns = {
        'name': fields.char('Drug Name', size=128, required=True),
        'street_name': fields.char('Street Names', size=256, help="Common name of the drug in street jargon"),
        'toxicity': fields.selection(TOXICITY, 'Toxicity', required=True),
        'addiction_level': fields.selection(ADDICTION_LEVEL, 'Addiction Level', required=True),
        'legal_status': fields.selection(LEGAL, 'Legal Status', required=True),
        'category': fields.selection(DRUG_CATEGORY, 'Category', required=True),
        'withdrawal_level': fields.integer("Withdrawal Level", help="Presence and severity ofcharacteristic withdrawal symptoms."),
        'reinforcement_level': fields.integer("Reinforcement Level", help="A measure of the substance's ability to get users to take it again and again, and in preference to other substances."),
        'tolerance_level': fields.integer("Tolerance Level", help="How much of the substance is needed to satisfy increasing cravings for it, and the level of stable need that is eventually reached."),
        'dependence_level': fields.integer("Dependence", help="How difficult it is for the user to quit, the relapse rate, the percentage of people who eventually become dependent, the rating users give their own need for the substance and the degree to which the substance will be used in the face of evidence that it causes harm."),
        'intoxication_level': fields.integer("Intoxication", help="the level of intoxication is associated with addiction and increases the personal and social damage a substance may do."),
        'route_oral': fields.boolean('Oral'),
        'route_popping': fields.boolean('Skin Popping', help="Subcutaneous or Intradermical administration"),
        'route_inhaling': fields.boolean('Smoke / Inhale', help="Insufflation, exluding nasal"),
        'route_sniffing': fields.boolean('Sniffing', help="Also called snorting - inhaling through the nares  "),
        'route_injection': fields.boolean('Injection', help="Injection - Intravenous, Intramuscular..."),
        'dea_schedule_i': fields.boolean('DEA schedule I', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
        'dea_schedule_ii': fields.boolean('II', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
        'dea_schedule_iii': fields.boolean('III', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
        'dea_schedule_iv': fields.boolean('IV', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
        'dea_schedule_v': fields.boolean('V', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter"),
        'info': fields.text ('Extra Info'),
    }

# Inheriting Patient module to add information to manage Patient's Lifestyles
class OeHealthPatient(osv.osv):
    _inherit='oeh.medical.patient'

    SEXUAL_PREFERENCE = [
        ('Heterosexual', 'Heterosexual'),
        ('Homosexual', 'Homosexual'),
        ('Bisexual', 'Bisexual'),
        ('Transexual', 'Transexual'),
    ]

    SEXUAL_PRACTICES = [
        ('Safe / Protected sex', 'Safe / Protected sex'),
        ('Risky / Unprotected sex', 'Risky / Unprotected sex'),
    ]

    SEXUAL_PARTNERS = [
        ('Monogamous', 'Monogamous'),
        ('Polygamous', 'Polygamous'),
    ]

    ANTI_CONCEPTIVE = [
        ('None', 'None'),
        ('Pill / Minipill', 'Pill / Minipill'),
        ('Male Condom', 'Male Condom'),
        ('Vasectomy', 'Vasectomy'),
        ('Female Sterilisation', 'Female Sterilisation'),
        ('Intra-uterine Device', 'Intra-uterine Device'),
        ('Withdrawal Method', 'Withdrawal Method'),
        ('Fertility Cycle Awareness', 'Fertility Cycle Awareness'),
        ('Contraceptive Injection', 'Contraceptive Injection'),
        ('Skin Patch', 'Skin Patch'),
        ('Female Condom', 'Female Condom'),
    ]

    SEXUAL_ORAL = [
        ('None', 'None'),
        ('Active', 'Active'),
        ('Passive', 'Passive'),
        ('Both', 'Both'),
    ]

    SEXUAL_ANAL = [
        ('None', 'None'),
        ('Active', 'Active'),
        ('Passive', 'Passive'),
        ('Both', 'Both'),
    ]

    _columns = {
        'exercise': fields.boolean('Exercise'),
        'exercise_minutes_day': fields.integer('Minutes / day', help="How many minutes a day the patient exercises"),
        'sleep_hours': fields.integer('Hours of Sleep', help="Average hours of sleep per day"),
        'sleep_during_daytime': fields.boolean('Sleeps at Daytime', help="Check if the patient sleep hours are during daylight rather than at night"),
        'number_of_meals': fields.integer('Meals / day'),
        'eats_alone' : fields.boolean('Eats alone', help="Check this box if the patient eats by him / herself."),
        'salt': fields.boolean('Salt', help="Check if patient consumes salt with the food"),
        'coffee': fields.boolean('Coffee'),
        'coffee_cups': fields.integer('Cups / day', help="Number of cup of coffee a day"),
        'soft_drinks': fields.boolean('Soft Drinks (sugar)', help="Check if the patient consumes soft drinks with sugar"),
        'diet': fields.boolean('Currently on a Diet', help="Check if the patient is currently on a diet"),
        'diet_info': fields.char('Diet Info', size=256, help="Short description on the diet"),
        'smoking': fields.boolean('Smokes'),
        'smoking_number': fields.integer('Cigarretes a Day'),
        'ex_smoker': fields.boolean('Ex-smoker'),
        'second_hand_smoker': fields.boolean('Passive Smoker', help="Check it the patient is a passive / second-hand smoker"),
        'age_start_smoking': fields.integer('Age Started to Smoke'),
        'age_quit_smoking': fields.integer('Age of Quitting',help="Age of quitting smoking"),
        'alcohol': fields.boolean('Drinks Alcohol'),
        'age_start_drinking': fields.integer('Age Started to Drink ',help="Date to start drinking"),
        'age_quit_drinking': fields.integer('Age Quit Drinking ',help="Date to stop drinking"),
        'ex_alcoholic': fields.boolean('Ex Alcoholic'),
        'alcohol_beer_number': fields.integer('Beer / day'),
        'alcohol_wine_number': fields.integer('Wine / day'),
        'alcohol_liquor_number': fields.integer('Liquor / day'),
        'drug_usage': fields.boolean('Drug Habits'),
        'ex_drug_addict': fields.boolean('Ex Drug Addict'),
        'drug_iv': fields.boolean('IV Drug User',help="Check this option if the patient injects drugs"),
        'age_start_drugs': fields.integer('Age Started Drugs ',help="Age of start drugs"),
        'age_quit_drugs': fields.integer('Age Quit Drugs ',help="Date of quitting drugs"),
        'drugs': fields.many2many('oeh.medical.recreational.drugs','oeh_medical_patient_recreational_drugs_rel','partner_id','oeh_drugs_recreational_id', 'Recreational Drugs', help="Name of drugs that the patient consumes"),
        'traffic_laws': fields.boolean('Obeys Traffic Laws', help="Check if the patient is a safe driver"),
        'car_revision': fields.boolean('Car Revision', help="Maintain the vehicle. Do periodical checks - tires, engine, breaks ..."),
        'car_seat_belt': fields.boolean('Seat Belt', help="Safety measures when driving : safety belt"),
        'car_child_safety': fields.boolean('Car Child Safety', help="Safety measures when driving : child seats, proper seat belting, not seating on the front seat, ...."),
        'home_safety': fields.boolean('Home Safety', help="Keep safety measures for kids in the kitchen, correct storage of chemicals, ..."),
        'motorcycle_rider': fields.boolean('Motorcycle Rider', help="The patient rides motorcycles"),
        'helmet': fields.boolean('Uses Helmet', help="The patient uses the proper motorcycle helmet"),
        'lifestyle_info':fields.text('Extra Information'),
        'sexual_preferences': fields.selection(SEXUAL_PREFERENCE, 'Sexual Orientation'),
        'sexual_practices': fields.selection(SEXUAL_PRACTICES, 'Sexual Practices'),
        'sexual_partners': fields.selection(SEXUAL_PARTNERS, 'Sexual Partners'),
        'sexual_partners_number': fields.integer('Number of Sexual Partners'),
        'first_sexual_encounter': fields.integer('Age first Sexual Encounter'),
        'anticonceptive': fields.selection(ANTI_CONCEPTIVE, 'Anticonceptive Method'),
        'sex_oral': fields.selection(SEXUAL_PARTNERS, 'Oral Sex'),
        'sex_anal': fields.selection(SEXUAL_PARTNERS, 'Anal Sex'),
        'prostitute': fields.boolean('Prostitute', help="Check if the patient (he or she) is a prostitute"),
        'sex_with_prostitutes': fields.boolean('Sex with Prostitutes', help="Check if the patient (he or she) has sex with prostitutes"),
        'sexuality_info': fields.text('Extra Information'),
    }