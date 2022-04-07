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
    name_in_url = 'game'
    players_per_group = 2
    num_rounds = 1

class Subsession(BaseSubsession):
    def role_assignment(subsession):
        import itertools
        roles = itertools.cycle(['wor', 'wor', 'wor', 'man_con', 'man_hi', 'man_low'])
        for player in subsession.get_players():
            player.power_role = next(roles)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # role variable
    power_role = models.StringField()

    # timeout variables (will be set to 'true' if participants don't progress within 2 minutes)
    timeout_DelayDisclaimer = models.BooleanField(initial=False)
    timeout_RoleReveal = models.BooleanField(initial=False)




