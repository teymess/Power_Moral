from os import environ


#############################################
###########  DO NOT TOUCH ###################
#############################################

mturk_hit_settings = {
        'keywords': ['academic','study','common pool','experiment','money','short'],
        'title': "common resource experiment (few minutes to complete, earn real money)",
        'description': 'Academic decision making experiment',
        'frame_height':500,
        'template': 'global/mturk_template.html',
        'minutes_allotted_per_assignment':40,
        'expiration_hours':2*24,
        'qualification_requirements':[
            # Only US
            {
                'QualificationTypeId': "00000000000000000071",
                'Comparator': "EqualTo",
                'LocaleValues': [{'Country': "US"}]
            },
            # At least 15 HITs approved
            {
                'QualificationTypeId': "00000000000000000040",
                'Comparator': "GreaterThanOrEqualTo",
                'IntegerValues': [15]
            },
            # At least 95% of HITs approved
            {
                'QualificationTypeId': "000000000000000000L0",
                'Comparator': "GreaterThanOrEqualTo",
                'IntegerValues': [95]
            },
            {
                'QualificationTypeId': "3RATMYZWZZZG4KUH0L0UJ5Q3TR01Y9",
                'Comparator': "DoesNotExist",
            },
        ]

}
#############################################

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']


SESSION_CONFIG_DEFAULTS= {
    "real_world_currency_per_point": 1,
    'participation_fee': 0.80,
     'doc': "",
    "mturk_hit_settings": mturk_hit_settings
}

#  PARTICIPANT_FIELDS = ['treatment', 'comprehension', 'power_role', 'preference', 'partner_pref']
SESSION_FIELDS = [
    'take_type_matches_obs',
    'leave_type_matches_obs',
    'take_type_matches_veto',
    'leave_type_matches_veto',
    'take_type_matches_sim',
    'leave_type_matches_sim'

]


##################################################
####### ENTER THE SESSIONS YOU WANT TO PLAY ######
#################################################
SESSION_CONFIGS = [
    dict(name='observe',
        display_name="observe",
        num_demo_participants=2,
        app_sequence=['Game'],
        treatment1 = 0,
        treatment2 = 0
    ),
    dict(name='veto',
         display_name="veto",
         num_demo_participants=2,
         app_sequence=['Game'],
         treatment1=True,
         treatment2=False

         ),
    dict(name='symmetry',
         display_name="symmetry",
         num_demo_participants=2,
         app_sequence=['Game'],
         treatment1=True,
         treatment2=True
         ),
    dict(name='PR_M',
         display_name='PR_manager',
         num_demo_participants=3,
         app_sequence=['quiz',
                       'w_game',
                       'survey',
                       'end']
         ),
    dict(name='PR_W',
         display_name='PR_worker',
         num_demo_participants=9,
         app_sequence=['quiz',
                       'w_game',
                       'survey',
                       'end']
         )

]


#############################################


#############################################
###########  Otree Settings #################
#############################################
# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('password')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'gqu#5o1o$fci0cbu!9%*8$1obvpnm9&=w%*^z4nur4pb(dw!^p'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
#  EXTENSION_APPS = ['leavable_wait_page']

AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID = environ.get("AWS_SECRET_ACCESS_KEY_ID")
#############################################

