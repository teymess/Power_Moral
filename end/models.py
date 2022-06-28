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


doc = """
"""


class Constants(BaseConstants):
    name_in_url = 'end'
    players_per_group = None
    num_rounds = 1
    completion_code = 937268  # MTurk completion code to return the HIT




class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
