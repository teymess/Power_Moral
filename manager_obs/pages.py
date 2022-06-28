from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time




class PlaceboWait(Page):  # placebo wait page that is only displayed to first movers
    def is_displayed(self):
        return self.participant.vars['power_role'] != 'wor'

    def before_next_page(self):
        self.player.determine_partner()

    timeout_seconds = 15


class FirstMove(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return {'partner': self.player.partner_pref,
                'power_role_abb': self.participant.vars['power_role'],
                'random_low': self.player.random_low,
                'random_high': self.player.random_high,
                }

    def is_displayed(self):
        return self.participant.vars['power_role'] != 'wor'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_FirstMove = True

    timeout_seconds = 120




page_sequence = [PlaceboWait,
                 FirstMove,]
