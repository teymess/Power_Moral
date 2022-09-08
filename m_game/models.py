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
import random

author = 'Tillmann Eymess'

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None
    num_rounds = 1
    reward = 0.80

class Subsession(BaseSubsession):
    def role_assignment(subsession):
        for player in subsession.get_players():
            player.participant.vars['power_role'] = random.choice(['man_hi', 'man_con', 'man_low'])
            player.power_role = player.participant.vars['power_role']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # role variable
    power_role = models.StringField()

    # timeout variables (will be set to 'true' if participants don't progress within 2 minutes)
    timeout_DelayDisclaimer = models.BooleanField(initial=False)
    timeout_RoleReveal = models.BooleanField(initial=False)
    timeout_FirstMove = models.BooleanField(initial=False)
    timeout_Transition = models.BooleanField(initial=False)

    partner_pref = models.IntegerField()
    random_high = models.FloatField(initial=0)
    random_low = models.FloatField(initial=0)

    decision = models.IntegerField(choices=[[0, 'take'], [1, 'leave']], widget=widgets.RadioSelect(), label="")

    def determine_partner(self):
        if self.participant.vars['power_role'] == 'man_con':
            self.partner_pref = 99  # outside option that is never used
        elif self.participant.vars['power_role'] == 'man_hi':
            import random
            self.random_high = random.uniform(0, 1)
            if self.random_high <= 0.2:
                self.partner_pref = 0  # will match with worker who prefers take
            else:
                self.partner_pref = 1  # will match with worker who prefers leave
        elif self.participant.vars['power_role'] == 'man_low':
            import random
            self.random_low = random.uniform(0, 1)
            if self.random_low <= 0.2:
                self.partner_pref = 1  # will match with worker who prefers leave
            else:
                self.partner_pref = 0  # will match with worker who prefers take

        self.participant.vars['partner_pref'] = self.partner_pref


