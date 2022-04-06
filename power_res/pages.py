from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time

class Introduction(Page):
    def vars_for_template(self):
        return {'max_bonus': Constants.max_bonus,
                'treatment': self.player.treatment
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Introduction = True

    timeout_seconds = 120

page_sequence = [Introduction]
