from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time



class Survey1(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'risk', 'trust']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Survey1 = True

    timeout_seconds = 120

class Survey2(Page):
    form_model = 'player'
    form_fields = ['ee', 'pnb', 'ne', 'feedback']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Survey2 = True

    timeout_seconds = 120

page_sequence = [Survey1,
                 Survey2]
