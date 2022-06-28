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

author = 'Tillmann Eymess'

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'game_1'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    timeout_FirstMove = models.BooleanField(initial=False)


    partner_pref = models.IntegerField()
    random_high = models.FloatField(initial=0)
    random_low = models.FloatField(initial=0)

    decision = models.IntegerField(choices=[[0, 'take'], [1, 'leave']], widget=widgets.RadioSelect(), label="")

    def determine_partner(self):
        if self.participant.vars['power_role'] == 'wor' or self.participant.vars['power_role'] == 'man_con':
            self.partner_pref = 2  # outside option that is never used
        elif self.participant.vars['power_role'] == 'man_hi':
            import random
            self.random_high = random.uniform(0, 1)
            if self.random_high <= 0.2:
                self.partner_pref = 0  # worker prefers take
            else:
                self.partner_pref = 1  # worker prefers leave
        elif self.participant.vars['power_role'] == 'man_low':
            import random
            self.random_low = random.uniform(0, 1)
            if self.random_low <= 0.2:
                self.partner_pref = 1  # worker prefers leave
            else:
                self.partner_pref = 0  # worker prefers take

        self.participant.vars['partner_pref'] = self.partner_pref



