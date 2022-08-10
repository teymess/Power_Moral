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
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1
    reward = 0.8

    ########################################################################################
    # Design slider
    ########################################################################################

    basic_background_color = '#FFFFFF'
    basic_border_color = '#000'
    follow_color = '#C0D2E8'
    fill_color = '#DBE6C4'
    marking_color = '#FAFAFA'
    track_border_width = '2px'

    track_width = '340px'
    track_height = '120px'
    thumb_height = '125px'
    thumb_width = '5px'
    thumb_background = '#FF0000'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    timeout_Survey1 = models.BooleanField(initial=False)
    timeout_Survey2 = models.BooleanField(initial=False)

    age = models.IntegerField(min=18, max=120, label="What is your age?")

    gender = models.IntegerField(
        choices=[
            [1, 'Female'],
            [2, 'Male'],
            [3, 'Other'],
            [9, 'Prefer not to say'],
        ]
        , label="What is your gender?"
    )

    education = models.IntegerField(
        choices=[
            [1, 'Less than High school degree'],
            [2, 'High school degree or equivalent (e.g. GED)'],
            [3, 'Some college, but no degree'],
            [4, 'Associate degree'],
            [5, 'Bachelor degree'],
            [6, 'Graduate degree'],
        ]
        , label="What is the highest level of education you have completed or the highest degree you have received?"
    )



    risk = models.IntegerField(
        #widget=widgets.RadioSelectHorizontal,
        #choices=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        #label="How do you see yourself in general: Are you a person who takes risk (10) or do you try to avoid risks (0)?",
        #blank=False,
        min=0,
        max=10,
        initial=5
    )

    trust = models.IntegerField(
        widget=widgets.RadioSelectHorizontal,
        choices=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        label="How do you see yourself in general: Are you a person who is willing to trust others completely (10) or not at all (0)?"
    )

    ee = models.IntegerField(
        min=0,
        max=9,
        label="There are 9 other teams that share an account with your team. What do you think - how many of the 9 other teams chose to leave the token in the shared account? (You get an additional payment of $0.40 when your guess is correct)"
    )

    pnb = models.IntegerField(
        choices=[
            [0, "Take"],
            [1, "Leave"],
        ],
        label="In your own opinion - what is the morally right thing to do?"
    )

    ne = models.IntegerField(
        min=0,
        max=100,
        label="What share of participants think that <b>leaving</b> the token in the shared account is the morally right thing to do? (You get an additional payment of $0.40 when your guess is within 10 percentage points of the true value)"
    )

    feedback = models.StringField(
        label="Do you have any comments about this study?",
        blank=True
    )

