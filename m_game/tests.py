from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        yield pages.DelayDisclaimer
        yield pages.RoleReveal
        yield pages.FirstMove, dict(decision=random.choice([0, 1]))
        yield pages.Transition
