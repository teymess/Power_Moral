from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class DelayDisclaimer(Page):
    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_DelayDisclaimer = True

    timeout_seconds = 120


class RoleReveal(Page):
    def vars_for_template(self):
        return {'treatment': self.player.participant.vars['treatment'],
                }

    def before_next_page(self):
        self.player.get_first_mover_data()

        if self.player.participant.vars['treatment'] == 'obs':
            self.player.decision = 99
            self.player.determine_result()


        if self.timeout_happened:
            self.player.timeout_RoleReveal = True


    timeout_seconds = 120

class SecondMove(Page):
    form_model = 'player'
    form_fields = ['decision']

    def is_displayed(self):
        return self.player.participant.vars['treatment'] != 'obs'

    def vars_for_template(self):
        return {'manager_d': self.player.manager_decision,
                'treatment': self.player.participant.vars['treatment']
                }

    def before_next_page(self):
        self.player.determine_result()

        if self.timeout_happened:
            self.player.timeout_FirstMove = True


class Result(Page):
    def vars_for_template(self):
        return {'treatment': self.player.participant.vars['treatment'],
                'manager_d': self.player.manager_decision,
                'decision': self.player.decision
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Result = True

    timeout_seconds = 120


class Transition(Page):
    def vars_for_template(self):
        return {'reward': Constants.reward,
                'treatment': self.player.participant.vars['treatment']
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Transition = True

    timeout_seconds = 120



page_sequence = [DelayDisclaimer,
                 RoleReveal,
                 SecondMove,
                 Result,
                 Transition]
