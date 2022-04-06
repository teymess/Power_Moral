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
    form_fields = ['a1_test1', 'a1_test2', 'a1_test3', 'a1_test4', 'a1_test5']

    def before_next_page(self):
        self.player.check_comprehension_a1()
        self.player.check_comprehension_final()
        if self.timeout_happened:
            self.player.timeout_Comprehension1 = True

    timeout_seconds = 120


class FailedAttempt1(Page):
    def is_displayed(self):
        return self.player.a1_comprehension == 0

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_FailedAttempt1 = True

    timeout_seconds = 120


class Comprehension2(Page):
    form_model = 'player'
    form_fields = ['a2_test1', 'a2_test2', 'a2_test3', 'a2_test4', 'a2_test5']

    def is_displayed(self):
        return self.player.a1_comprehension == 0

    def before_next_page(self):
        self.player.check_comprehension_a2()
        self.player.check_comprehension_final()
        if self.timeout_happened:
            self.player.timeout_Comprehension2 = True

    timeout_seconds = 120


class FailedAttempt2(Page):
    def is_displayed(self):
        return self.player.a2_comprehension == 0

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_FailedAttempt2 = True

    timeout_seconds = 120


class Comprehension3(Page):
    form_model = 'player'
    form_fields = ['a3_test1', 'a3_test2', 'a3_test3', 'a3_test4', 'a3_test5']

    def is_displayed(self):
        return self.player.a2_comprehension == 0

    def before_next_page(self):
        self.player.check_comprehension_a3()
        self.player.check_comprehension_final()
        if self.timeout_happened:
            self.player.timeout_Comprehension3 = True

    timeout_seconds = 120


class ComprehensionFailed(Page):
    def is_displayed(self):
        return self.player.full_comprehension == 0


class ComprehensionSuccess(Page):
    def is_displayed(self):
        return self.player.full_comprehension == 1


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
