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
    name_in_url = 'pr_hit_v0' # appears in the link that participants click
    players_per_group = 2
    num_rounds = 1
    token_pool = 10 # since each team makes a decision for 1 token, this constant is also used for the number of teams in a collective
    multiplicator = 4 # gives MPCR if divided by token_pool
    token_per_group = 1
    reward = 0.8 # unconditional base reward if participant passes comprehension test
    bonus_per_token = 1 # token to USD exchange rate
    max_bonus = int(token_per_group*bonus_per_token + (token_pool-1)*4/token_pool) # max possible bonus
    max_payoff = max_bonus + reward # max possible payoff
    completion_code = 937268 # MTurk completion code to return the HIT



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
