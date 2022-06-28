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
    name_in_url = 'intro_and_quiz'  # appears in the link that participants click
    players_per_group = None
    num_rounds = 1
    token_pool = 10  # since each team makes a decision for 1 token, this constant is also used for the number of
    # teams in a collective
    multiplicator = 4  # gives MPCR if divided by token_pool
    token_per_group = 1
    reward = 0.8  # unconditional base reward if participant passes comprehension test
    bonus_per_token = 1  # token to USD exchange rate
    belief_incentive = 0.4
    max_bonus = round((token_per_group * bonus_per_token + (token_pool - token_per_group) * multiplicator / token_pool + 2 * belief_incentive),
                      1)  # max possible bonus
    max_payoff = max_bonus + reward  # max possible payoff

class Subsession(BaseSubsession):
    def creating_session(subsession):
        import itertools
        treatments = itertools.cycle(['obs', 'veto', 'sim'])
        for player in subsession.get_players():
            player.participant.vars['treatment'] = next(treatments)
            player.treatment = player.participant.vars['treatment']

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # treatment and role variable
    treatment = models.StringField()
    power_role = models.StringField()

    # comprehension variable
    a1_comprehension = models.IntegerField(initial=0)  # comprehension after first attempt
    a2_comprehension = models.IntegerField(initial=0)  # comprehension after second attempt
    a3_comprehension = models.IntegerField(initial=0)  # comprehension after third attempt
    full_comprehension = models.IntegerField(initial=0)  # comprehension after third attempt

    # comprehension questions
    a1_test1 = models.IntegerField(choices=[[1, 'Two members'], [2, 'Three members'], [3, 'Five members']],
                                widget=widgets.RadioSelect(), label="")
    a1_test2 = models.IntegerField(
        choices=[[1, '5 teams (my team and 4 other teams)'], [2, '10 teams (my team and 9 other teams)'],
                 [3, '15 teams (my team and 14 other teams)']], widget=widgets.RadioSelect(), label="")
    a1_test3 = models.IntegerField(choices=[[1, 'leave or take'], [2, 'north or south'], [3, 'left or right']],
                                widget=widgets.RadioSelect(), label="")
    a1_test4 = models.IntegerField(choices=[[1, '1 token = $0.50'], [2, '1 token = $1'], [3, '1 token = $2']],
                                widget=widgets.RadioSelect(), label="")
    a1_test5 = models.IntegerField(
        choices=[[1, 'The manager earns more than the worker'], [2, 'The manager earns the same amount as the worker'],
                 [3, 'The manager earns less than the worker']], widget=widgets.RadioSelect(), label="")

    a2_test1 = models.IntegerField(choices=[[1, 'Two members'], [2, 'Three members'], [3, 'Five members']],
                                   widget=widgets.RadioSelect(), label="")
    a2_test2 = models.IntegerField(
        choices=[[1, '5 teams (my team and 4 other teams)'], [2, '10 teams (my team and 9 other teams)'],
                 [3, '15 teams (my team and 14 other teams)']], widget=widgets.RadioSelect(), label="")
    a2_test3 = models.IntegerField(choices=[[1, 'leave or take'], [2, 'north or south'], [3, 'left or right']],
                                   widget=widgets.RadioSelect(), label="")
    a2_test4 = models.IntegerField(choices=[[1, '1 token = $0.50'], [2, '1 token = $1'], [3, '1 token = $2']],
                                   widget=widgets.RadioSelect(), label="")
    a2_test5 = models.IntegerField(
        choices=[[1, 'The manager earns more than the worker'], [2, 'The manager earns the same amount as the worker'],
                 [3, 'The manager earns less than the worker']], widget=widgets.RadioSelect(), label="")

    a3_test1 = models.IntegerField(choices=[[1, 'Two members'], [2, 'Three members'], [3, 'Five members']],
                                   widget=widgets.RadioSelect(), label="")
    a3_test2 = models.IntegerField(
        choices=[[1, '5 teams (my team and 4 other teams)'], [2, '10 teams (my team and 9 other teams)'],
                 [3, '15 teams (my team and 14 other teams)']], widget=widgets.RadioSelect(), label="")
    a3_test3 = models.IntegerField(choices=[[1, 'leave or take'], [2, 'north or south'], [3, 'left or right']],
                                   widget=widgets.RadioSelect(), label="")
    a3_test4 = models.IntegerField(choices=[[1, '1 token = $0.50'], [2, '1 token = $1'], [3, '1 token = $2']],
                                   widget=widgets.RadioSelect(), label="")
    a3_test5 = models.IntegerField(
        choices=[[1, 'The manager earns more than the worker'], [2, 'The manager earns the same amount as the worker'],
                 [3, 'The manager earns less than the worker']], widget=widgets.RadioSelect(), label="")

    def check_comprehension_a1(self):
        if self.a1_test1 != 1 or self.a1_test2 != 2 or self.a1_test3 != 1 or self.a1_test4 != 2 or self.a1_test5 != 2:
            return self.a1_comprehension
        else:
            self.a1_comprehension = 1
            self.a2_comprehension = 1
            self.a3_comprehension = 1
            return self.a1_comprehension

    def check_comprehension_a2(self):
        if self.a2_test1 != 1 or self.a2_test2 != 2 or self.a2_test3 != 1 or self.a2_test4 != 2 or self.a2_test5 != 2:
            return self.a2_comprehension
        else:
            self.a2_comprehension = 1
            self.a3_comprehension = 1
            return self.a2_comprehension

    def check_comprehension_a3(self):
        if self.a3_test1 != 1 or self.a3_test2 != 2 or self.a3_test3 != 1 or self.a3_test4 != 2 or self.a3_test5 != 2:
            return self.a3_comprehension
        else:
            self.a3_comprehension = 1
            return self.a3_comprehension

    def check_comprehension_final(self):
        if self.a1_comprehension == 1 or self.a2_comprehension == 1 or self.a3_comprehension == 1:
            self.full_comprehension = 1
        else:
            self.full_comprehension = 0
        self.participant.vars['comprehension'] = self.full_comprehension
        return self.full_comprehension

    # preference question
    prior_pref = models.IntegerField(choices=[[0, 'take'], [1, 'leave']], widget=widgets.RadioSelect(), label="")



    # timeout variables (will be set to 'true' if participants don't progress within 2 minutes)
    timeout_Introduction = models.BooleanField(initial=False)
    timeout_Instructions = models.BooleanField(initial=False)
    timeout_Comprehension1 = models.BooleanField(initial=False)
    timeout_FailedAttempt1 = models.BooleanField(initial=False)
    timeout_Comprehension2 = models.BooleanField(initial=False)
    timeout_FailedAttempt2 = models.BooleanField(initial=False)
    timeout_Comprehension3 = models.BooleanField(initial=False)
    timeout_ComprehensionFailed = models.BooleanField(initial=False)
    timeout_ComprehensionSuccess = models.BooleanField(initial=False)
    timeout_DelayDisclaimer = models.BooleanField(initial=False)

