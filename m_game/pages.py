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
        return {'treatment': self.player.participant.vars['treatment'],
                'power_role_abb': self.player.participant.vars['power_role']
                }

    def before_next_page(self):
        self.player.determine_partner()
        if self.timeout_happened:
            self.player.timeout_RoleReveal = True

    timeout_seconds = 120

class FirstMove(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return {'partner': self.player.partner_pref,
                'power_role_abb': self.participant.vars['power_role'],
                'treatment': self.player.participant.vars['treatment']
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_FirstMove = True


class Transition(Page):
    def vars_for_template(self):
        return {'reward': Constants.reward
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Transition = True

    timeout_seconds = 120


page_sequence = [DelayDisclaimer,
                 RoleReveal,
                 FirstMove,
                 Transition]
