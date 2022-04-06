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


class Instructions(Page):
    def vars_for_template(self):
        return {'treatment': self.player.treatment
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Instructions = True

    timeout_seconds = 120


class Comprehension1(Page):
    form_model = 'player'
    form_fields = ['test1', 'test2', 'test3', 'test4', 'test5']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Comprehension1 = True

    timeout_seconds = 120


class FailedAttempt1(Page):
    def is_displayed(self):
        if not self.a1_comprehension:
            return

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_FailedAttempt1 = True

    timeout_seconds = 120


class Comprehension2(Page):
    form_model = 'player'
    form_fields = ['test1', 'test2', 'test3', 'test4', 'test5']

    def is_displayed(self):
        if not self.a1_comprehension:
            return

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Comprehension2 = True

    timeout_seconds = 120


class FailedAttempt2(Page):
    def is_displayed(self):
        if not self.a2_comprehension:
            return

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_FailedAttempt2 = True

    timeout_seconds = 120


class Comprehension3(Page):
    form_model = 'player'
    form_fields = ['test1', 'test2', 'test3', 'test4', 'test5']

    def is_displayed(self):
        if not self.a2_comprehension:
            return

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Comprehension3 = True

    timeout_seconds = 120


class ComprehensionFailed(Page):
    def is_displayed(self):
        if not self.a3_comprehension and not self.a2_comprehension and not self.a1_comprehension:
            return


class ComprehensionSuccess(Page):
    def is_displayed(self):
        if self.a1_comprehension or self.a2_comprehension or self.a3_comprehension:
            return


page_sequence = [Introduction,
                 Instructions,
                 Comprehension1,
                 FailedAttempt1,
                 Comprehension2,
                 FailedAttempt2,
                 Comprehension3,
                 ComprehensionFailed,
                 ComprehensionSuccess
                 ]
