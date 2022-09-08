from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Introduction
        yield pages.Instructions
        yield pages.Comprehension1, dict(a1_test1 = 1, a1_test2 = 2, a1_test3 = 1, a1_test4 = 2, a1_test5 = 2)
        yield pages.ComprehensionResult, dict(prior_pref=random.choice([0,1]))
