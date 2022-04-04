from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class Introduction(Page):
    def vars_for_template(self):
        return {'treatment1': self.subsession.treatment1,
                'treatment2': self.subsession.treatment2,
                'cost': Constants.cost,
                'cheat': Constants.cheat,
                'base' :Constants.baserate,
                'comply':Constants.comply,
                'deduction':Constants.deduction}


    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Introduction = True

    timeout_seconds = 120

class Instruction(Page):
    def vars_for_template(self):
        return {'treatment1': self.subsession.treatment1,
                'treatment2': self.subsession.treatment2,
                'cost': Constants.cost,
                'cheat': Constants.cheat,
                'base' :Constants.baserate,
                'comply':Constants.comply,
                'deduction':Constants.deduction}

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Instruction = True

    timeout_seconds = 120

class Comp1(Page):
    form_model = 'player'
    form_fields = ['test1']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Comp1 = True

    timeout_seconds = 120


class Comp1Results(Page):

    def vars_for_template(self):
        return {'test1': self.player.test1,
                'base': Constants.baserate,
                'comply': Constants.comply,
                'deduction': Constants.deduction}

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Comp1Results = True

    timeout_seconds = 120
class Comp2(Page):
    form_model = 'player'
    form_fields = ['test2']

    def vars_for_template(self):
        return {'treatment1': self.subsession.treatment1,
                'treatment2': self.subsession.treatment2,
                'base': Constants.baserate,
                'comply': Constants.comply,
                'deduction': Constants.deduction,
                'cost':Constants.cost}

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Comp2 = True

    timeout_seconds = 120

class Comp2Results(Page):

    def vars_for_template(self):
        return {'test2': self.player.test2,
                'base': Constants.baserate,
                'comply': Constants.comply,
                'cost': Constants.cost,
                'deduction': Constants.deduction,
                'treatment1': self.subsession.treatment1,
                'treatment2': self.subsession.treatment2}

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Comp2Results = True

    timeout_seconds = 120


class Manager(Page):

    def is_displayed(self):
        return self.player.id_in_group == 1

    form_model = 'group'
    form_fields = ['manager_decision']

    def vars_for_template(self):
        return {'treatment1': self.session.vars['treatment1'],
                'treatment2': self.session.vars['treatment2'],
                'base':Constants.baserate,
                'deduction': Constants.deduction,
                'cost': Constants.cost,
                }



    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Manager = True

    timeout_seconds = 120

class ManagerFeedback(Page):

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {'treatment1': self.session.vars['treatment1'],
                'treatment2': self.session.vars['treatment2'],
                'mdecision': self.group.manager_decision,
                'wdecision': self.group.worker_decision,
                'wfeedback':self.group.worker_feedback,
                'wveto':self.group.worker_veto}


    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_ManagerFeedback = True

    timeout_seconds = 120


class Worker(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2

    form_model = 'group'
    form_fields = ['worker_decision']


    def vars_for_template(self):
        return {'treatment1': self.session.vars['treatment1'],
                'treatment2': self.session.vars['treatment2'],
                'cost': Constants.cost,
                'base': Constants.baserate,
                'deduction': Constants.deduction}


    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Worker = True

    timeout_seconds = 120



class WorkerFeedback(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2

    form_model = 'group'
    form_fields = ['worker_veto','worker_feedback']

    def vars_for_template(self):
        return {'treatment1': self.session.vars['treatment1'],
                'treatment2': self.session.vars['treatment2'],
                'mdecision': self.group.manager_decision,
                'wfeedback':self.group.worker_feedback,
                'wveto':self.group.worker_veto}


    def before_next_page(self):
        self.group.set_groupdecision()
        if self.timeout_happened:
            self.player.timeout_WorkerFeedback = True

    timeout_seconds = 120

class Wait1(WaitPage):
    body_text = "Please wait for your co-player to finish the current task."

class Wait2(WaitPage):
    body_text = "Please wait for your co-player to finish the current task."
    def after_all_players_arrive(self,):
        self.group.set_groupdecution()
        self.group.set_tokens()




class Results(Page):
    def vars_for_template(self):
        return {'groupdecision':self.group.groupdecision,
                'tokens':self.player.tokens,
                'cost':self.group.groupdecution,
                'treatment1': self.session.vars['treatment1'],
                'treatment2': self.session.vars['treatment2'],
                'mdecision': self.group.manager_decision,
                'wdecision': self.group.worker_decision,
                'wveto': self.group.worker_veto}

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Results = True

    timeout_seconds = 120



class Results2(Page):
    def vars_for_template(self):
        return {'tokens':self.player.tokens,
                'groupdeduction': self.group.groupdecution,
                'countcheat': self.subsession.session_countcheat,
                'exchangerate':self.subsession.session_exchangerate,
                'moral':self.subsession.session_moral,
                'cost':self.group.groupdecution,
                'treatment1': self.session.vars['treatment1'],
                'treatment2': self.session.vars['treatment2'],
                'bonus':self.player.bonus,
                'gamepayoff': self.player.gamepayoff,
                'payoff': self.participant.payoff_plus_participation_fee(),
                'fee': self.session.config['participation_fee']}




class GroupWait(WaitPage):
    body_text ="Waiting for for the other groups to finish the task"

    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.set_sessioncountcheat()
        self.subsession.set_sessionexchangerate()
        self.subsession.set_gamepayoff()

class GroupWait2(WaitPage):
    body_text ="Waiting for for the other groups to finish the task"

    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.set_sessionmoral()



class Questions(Page):
    form_model = 'player'
    form_fields = ['qcheater','moral','qgroupmorals']

    def vars_for_template(self):
        return {'bonus':Constants.bonus,
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_Questions = True

    timeout_seconds = 120
class Questions2(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'experience','risk','relationship','children']

    def before_next_page(self):
        self.player.set_bonus()
        self.group.set_payoffs()
        if self.timeout_happened:
            self.player.timeout_Questions2 = True

    timeout_seconds = 120


page_sequence = [Introduction,
                 Instruction,
                 Comp1,
                 Comp1Results,
                 Comp2,
                 Comp2Results,
                 Wait1,
                 Manager,
                 Worker,
                 Wait1,
                 WorkerFeedback,
                 Wait1,
                 ManagerFeedback,
                 Wait2,
                 Results,
                 GroupWait,
                 Questions,
                 GroupWait2,
                 Questions2,
                 Results2
                    ]