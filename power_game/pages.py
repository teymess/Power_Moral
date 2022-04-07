from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class DelayDisclaimer(Page):
    def before_next_page(self):
        self.subsession.role_assignment()
        if self.timeout_happened:
            self.player.timeout_DelayDisclaimer = True

    timeout_seconds = 120


class RoleReveal(Page):
    def vars_for_template(self):
        if self.player.power_role == 'wor':
            p_role = 'worker'
        else:
            p_role = 'manager'

        return {'power_role': p_role,
                'treatment': self.player.participant.treatment,
                'power_role_abb': self.player.power_role
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_RoleReveal = True

    timeout_seconds = 1200


class PlaceboWait(Page):  # placebo wait page that is only displayed to first movers
    def is_displayed(self):
        global first_mover
        if self.player.power_role == 'wor':
            if self.player.participant.treatment != 'sim':
                first_mover = 0
        else:
            first_mover = 1
        return first_mover == 1

    timeout_seconds = 15


page_sequence = [DelayDisclaimer,
                 RoleReveal,
                 PlaceboWait]
