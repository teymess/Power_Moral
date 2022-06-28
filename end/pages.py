from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class End(Page):
    def vars_for_template(self):
        return {'treatment': self.player.participant.vars['treatment'],
                'completion_code': Constants.completion_code,
                'comprehension': self.player.participant.vars['comprehension']
                }



page_sequence = [End]
