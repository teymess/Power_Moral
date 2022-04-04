from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import numpy as np
import math
author = 'Moritz Sommerlad'

doc = """

"""


class Constants(BaseConstants):


    name_in_url = 'GroupDecision'
    players_per_group = 2
    fee = 5
    baserate = 1
    num_rounds = 1
    deduction = 0.05
    cheat = 5
    comply = 3
    cost = 0.20
    bonus = 0.40



class Subsession(BaseSubsession):


    treatment1 = models.BooleanField()
    treatment2 = models.BooleanField()

    def creating_session(self):
        self.group_randomly()
        self.treatment1 = self.session.config.get('treatment1')
        self.treatment2 = self.session.config.get('treatment2')
        self.session.vars['treatment1'] = self.session.config.get('treatment1')
        self.session.vars['treatment2'] = self.session.config.get('treatment2')


    session_countcheat = models.IntegerField(initial=0)
    session_exchangerate = models.FloatField()
    session_moral = models.IntegerField(initial=0)

    def set_sessioncountcheat(self):
        self.session_countcheat = sum(g.groupdecision for g in self.get_groups())

    def set_sessionexchangerate(self):
        self.session_exchangerate = Constants.baserate - Constants.deduction * self.session_countcheat

    def set_gamepayoff(self):
            for p in self.get_players():
                p.gamepayoff = p.tokens * self.session_exchangerate

    def set_sessionmoral(self):
        self.session_moral = 2-sum(p.moral for p in self.get_players())


class Group(BaseGroup):



    groupdecision = models.IntegerField()

    def set_groupdecision(self):
        if self.session.vars['treatment1'] == False:
            self.groupdecision = self.manager_decision
        else:
            if self.session.vars['treatment2'] == False:
                if self.worker_veto == 1:
                    self.groupdecision = 0
                else:
                    self.groupdecision = self.manager_decision
            else:
                if self.worker_decision == self.manager_decision:
                    self.groupdecision = self.manager_decision
                else:
                    self.groupdecision = 0


    groupdecution = models.FloatField(initial = 0)

    def set_groupdecution(self):
        if self.session.vars['treatment1'] == False:
            self.groupdecution = 0
        else:
            if self.session.vars['treatment2'] == False:
                if self.worker_veto == 1:
                    self.groupdecution = Constants.cost
            else:
                if self.worker_decision == self.manager_decision:
                    self.groupdecution = 0
                else:
                    self.groupdecution = Constants.cost




    def set_tokens(self):
        for p in self.get_players():
            if self.groupdecision == 1:
                p.tokens = Constants.cheat
            else:
                p.tokens = Constants.comply

    worker_decision = models.IntegerField(choices=[[0,'Comply'],[1,'Cheat']],initial = 0, widget=widgets.RadioSelect() , label="What do you choose?",blank=True)
    manager_decision = models.IntegerField(choices=[[0,'Comply'],[1,'Cheat']], initial = 0, widget=widgets.RadioSelect() , label="What do you choose?")
    worker_feedback = models.IntegerField(choices=[[0,'I like your choice'],[1,"I don't like your choice"],[3,"send no message"]],
                                          initial = 2,widget=widgets.RadioSelect() , label="Which feedback do you, as worker, want to send to the manager?",blank=True)
    worker_veto = models.IntegerField(choices=[[0,'no (your team will cheat)'], [1,'yes (team will comply and €0.20 are deducted from your payoff)']],
                                          initial = 0,widget=widgets.RadioSelect(), label="Do you want to veto the decision of the manager", blank=True)

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = (p.gamepayoff + p.bonus - self.groupdecution)*1000

class Player(BasePlayer):


    test1 = models.IntegerField(choices=[[0,'True'],[1,'False']], widget=widgets.RadioSelect() , label="")
    test2 = models.IntegerField(choices=[[0,'False'],[1,'True']],widget=widgets.RadioSelect() , label="")


    bonus = models.FloatField(initial = 0)

    def set_bonus(self):
        if self.qcheater == self.subsession.session_countcheat:
           self.bonus = self.bonus + Constants.bonus

        if self.qgroupmorals == math.ceil((self.subsession.session_moral/2)*10):
           self.bonus = self.bonus + Constants.bonus



    tokens = models.IntegerField()

    gamepayoff = models.FloatField()


    qcheater = models.IntegerField(min=0, max=10,  label="")

    moral = models.IntegerField(choices=[[0,'to comply'],[1,'to cheat']], widget=widgets.RadioSelect() ,label="")

    risk = models.IntegerField(min=0, max=10,  label="")

    qgroupmorals = models.IntegerField(
        choices=[
            [0, '0%'],
            [1, '1% - 10%'],
            [2, '11% - 20%'],
            [3, '21% - 30%'],
            [4, '31% - 40%'],
            [5, '41% - 50%'],
            [6, '51% - 60%'],
            [7, '61% - 70%'],
            [8, '71% - 80%'],
            [9, '81% - 90%'],
            [10, '91% - 100%'],
        ],
        label="")



    age = models.IntegerField(min=14, max=120, label="How old are you?")

    gender = models.IntegerField(
        choices=[
            [1, 'Female'],
            [2, 'Male'],
            [3, 'Non-binary'],
            [9, 'Prefer not to say'],
        ]
        , label="What gender do you identify with?")

    education = models.IntegerField(
        choices=[
            [1, 'No diploma'],
            [2, 'High school diploma'],
            [3, 'Bachelors degree'],
            [4, 'Masters degree'],
            [9, 'Prefer not to say'],
        ]
        , label="What is the highest level of education you have completed?")

    experience = models.IntegerField(
        choices=[
            [1, 'This is the first time'],
            [2, 'A few times'],
            [3, 'More than 10'],
        ]
        , label="How often did you participate in experiments like this so far?")


    relationship = models.IntegerField(
        choices=[
            [1, 'Single'],
            [2, 'Long-term relationship'],
            [3, 'Married'],
            [4, 'Divorced'],
            [9, 'Prefer not to say'],
        ], label="What is your relationship status?")


    children = models.IntegerField(
        choices=[
            [0, '0'],
            [1, '1'],
            [2, '2'],
            [3, '3'],
            [4, '4'],
            [9, 'Prefer not to say'],
        ], label="How many children do you have?")



    timeout_Introduction = models.BooleanField(initial=False)
    timeout_Instruction = models.BooleanField(initial=False)
    timeout_Comp1 = models.BooleanField(initial=False)
    timeout_Comp1Results = models.BooleanField(initial=False)
    timeout_Comp2 = models.BooleanField(initial=False)
    timeout_Comp2Results = models.BooleanField(initial=False)
    timeout_Manager = models.BooleanField(initial=False)
    timeout_ManagerFeedback = models.BooleanField(initial=False)
    timeout_Worker = models.BooleanField(initial=False)
    timeout_WorkerFeedback = models.BooleanField(initial=False)
    timeout_Results = models.BooleanField(initial=False)
    timeout_Questions = models.BooleanField(initial=False)
    timeout_Questions2 = models.BooleanField(initial=False)
