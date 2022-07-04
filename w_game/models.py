from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import numpy as np
import math
import csv
import itertools


author = 'Tillmann Eymess'

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'game2'
    players_per_group = None
    num_rounds = 1
    reward = 0.80
    MANAGER_FILE = 'manager_input.csv'

class Subsession(BaseSubsession):
    def creating_session(subsession):
        # load the data from the csv into the subsession

        take_type_matches_obs = []
        leave_type_matches_obs = []
        take_type_matches_veto = []
        leave_type_matches_veto = []
        take_type_matches_sim = []
        leave_type_matches_sim = []

        # open the first mover file, read it line by line
        with open(Constants.MANAGER_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # get the data from each line into a dictionary
                data = {'id': row['id'], 'treatment': row['treatment'], 'partner_pref': row['partner_pref'], 'manager_decision': row['manager_decision']}

                # separate the data into several lists, one for each type
                if row['partner_pref'] == '0' and row['treatment'] == 'obs':
                    take_type_matches_obs.append(data)
                if row['partner_pref'] == '1' and row['treatment'] == 'obs':
                    leave_type_matches_obs.append(data)
                if row['partner_pref'] == '0' and row['treatment'] == 'veto':
                    take_type_matches_veto.append(data)
                if row['partner_pref'] == '1' and row['treatment'] == 'veto':
                    leave_type_matches_veto.append(data)
                if row['partner_pref'] == '0' and row['treatment'] == 'sim':
                    take_type_matches_sim.append(data)
                if row['partner_pref'] == '1' and row['treatment'] == 'sim':
                    leave_type_matches_sim.append(data)

        # make sure you have added these variables in settings!
        subsession.session.vars['take_type_matches_obs'] = itertools.cycle(take_type_matches_obs)
        subsession.session.vars['leave_type_matches_obs'] = itertools.cycle(leave_type_matches_obs)
        subsession.session.vars['take_type_matches_veto'] = itertools.cycle(take_type_matches_veto)
        subsession.session.vars['leave_type_matches_veto'] = itertools.cycle(leave_type_matches_veto)
        subsession.session.vars['take_type_matches_sim'] = itertools.cycle(take_type_matches_sim)
        subsession.session.vars['leave_type_matches_sim'] = itertools.cycle(leave_type_matches_sim)

        # for this demo: assign each player a type to match with
        # for player in subsession.get_players():
        #    player.match_with_type = random.choice(['A', 'B'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # timeout variables (will be set to 'true' if participants don't progress within 2 minutes)
    timeout_DelayDisclaimer = models.BooleanField(initial=False)
    timeout_RoleReveal = models.BooleanField(initial=False)
    timeout_FirstMove = models.BooleanField(initial=False)
    timeout_Result = models.BooleanField(initial=False)
    timeout_Transition = models.BooleanField(initial=False)

    result = models.StringField()
    partner_pref = models.IntegerField()

    decision = models.IntegerField(choices=[[0, 'take'], [1, 'leave']], widget=widgets.RadioSelect(), label="")

    # id and value from the matched first mover
    matched_with_id = models.StringField()
    manager_decision = models.StringField()

    def get_first_mover_data(self):
        if self.participant.vars['treatment'] == 'obs':
            source = self.session.vars['take_type_matches_obs'] if self.participant.vars['preference'] == 0 else self.session.vars['leave_type_matches_obs']
        elif self.participant.vars['treatment'] == 'veto':
            source = self.session.vars['take_type_matches_veto'] if self.participant.vars['preference'] == 0 else self.session.vars['leave_type_matches_veto']
        elif self.participant.vars['treatment'] == 'sim':
            source = self.session.vars['take_type_matches_sim'] if self.participant.vars['preference'] == 0 else self.session.vars['leave_type_matches_sim']

        first_mover = next(source)

        self.matched_with_id = first_mover['id']
        self.manager_decision = first_mover['manager_decision']


    def determine_result(self):
        # determine the team's action
        if self.participant.vars['treatment'] == 'obs':
            self.result = self.manager_decision

        else:
            if self.manager_decision == '0' and self.decision == '0':
                self.result = '0'
            else:
                self.result = '1'


