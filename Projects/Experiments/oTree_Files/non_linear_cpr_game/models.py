from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, BaseLink,
    Currency as c, currency_range,
)

import random
import datetime
import os 
import pandas as pd
author = 'Andrea Guido'

doc = """
An implementation of a non-linear Common Pool Resource game.
Features:
- Group sizes maximum of 6 because of tables of player contributions, empirical expectations elicitation, and normative expectation elicitation.
    Apart from that group sizes must be even numbers (for instruction legibility minimum is 4 per group)
- same or different groupings must be fully specified except for round 1 
- current setup for 28 rounds. Minimum number is 4. Number of rounds/stages must be divisible into whole numbers
"""


class Constants(BaseConstants):
    name_in_url = 'page_no'
    language = "SPA"
    timeout_first_rounds = 60 
    timeout_instructions = 300
    timeout_example = 210
    timeout_control = 210
    timeout_answers = 120
    timeout_results = 40
    treatment = 0 #Original message
    warning_message = 1 #Message separated and wider
    players_per_group = 6
    ####PARAMETERS TO BE SPECIFIED####
    #0 = 3 x 1 week of same group and 1 week random group; 1 = 3 weeks random group, 1 week same group; 2 = 4 weeks random matching
    #Groups are formed dynamically in views.py. this constant is used to form groups there
    num_rounds = 35  # change this before the XP (min 5 rounds -- since 5-week payment) / must be a mult. of 5
    endowment = 30  #endowment in the game
    belief_correct_pay = 5
    # payment correct beliefs
    p_a = 15
    p_b = 0.083
    
   # set here the text of the questions

    a1_1 = 0
    a1_2 = 0
    a2_1 = 0
    a2_2 = 2
    a3_1 = 2
    a3_2 = 1
    a4_1 = 0
    a4_2 = 0
    a5 = 1
    # set here the right answers to the questions

    text_Instructions = 'non_linear_cpr_game/text_Instructions.html'
    text_EE = 'non_linear_cpr_game/text_EE.html'
    text_PNB = 'non_linear_cpr_game/text_PNB.html'
    text_NE = 'non_linear_cpr_game/text_NE.html'
    text_Contribute_uncond = 'non_linear_cpr_game/text_Contribute_uncond.html'
    text_Inactive = 'non_linear_cpr_game/text_Inactive.html'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    # XXX DEFINE PAYOFF FUNCTION
    def set_payoffs(self):
        #Unconditional payoff calculations
        for p in self.get_players():
            p.total_contribution = sum([p1.contribution for p1 in self.get_players()])
            if p.total_contribution > 0:
                p.fraction_contribution = p.contribution / p.total_contribution
            else:
                p.fraction_contribution = 0  # if nobody contributed, you included, you get zero
            p.common_account_earnings = (Constants.p_a * p.total_contribution - Constants.p_b * p.total_contribution * p.total_contribution) * p.fraction_contribution
            p.unconditional_payoff = Constants.endowment - p.contribution + p.common_account_earnings
        #Combining unconditional payoffs, conditional payoffs, and belief payoffs, in the relevant periods
        for p in self.get_players():
            if self.round_number in p.participant.vars["paying_rounds"]:
                p.payoff = p.unconditional_payoff + p.payoff_empirical_expectations + p.payoff_normative_expectations
            else:
                p.payoff = 0


    def group_other_contributions(self):
        for p1 in self.get_players():
            p1.participant.vars["other_contributions"] =  [other.contribution for other in p1.get_others_in_group()]
            p1.participant.vars["other_inactive"] = ["\u274C" if other.absent_contribution==True else " " for other in p1.get_others_in_group()]
            p1.participant.vars["contribution_inactive"] = [str(i[0])+i[1] for i in zip(p1.participant.vars["other_contributions"],p1.participant.vars["other_inactive"])]
    def group_empirical_expectations(self):
        #Asegurarse que os inactivos seleccionan None
        for p1 in self.get_players():
            if p1.participant.vars["absence"] < p1.participant.vars["max_absence"]: 
                list_empirical = [p.contribution for p in p1.get_others_in_group()]
                list_empirical.sort(reverse=True)
                list_EE = [value for attr,value in p1.__dict__.items() if attr.startswith("empirical_expectations")]
                for i,item in enumerate(list_EE):
                    if item != None:
                        p1.payoff_empirical_expectations += max(0,Constants.belief_correct_pay - abs(list_empirical[i]-item))
                    else:
                        p1.payoff_empirical_expectations += 0

    def group_normative_expectations(self):
        for p1 in self.get_players():
            if p1.participant.vars["absence"] < p1.participant.vars["max_absence"]:
                list_normative = [p.contribution for p in p1.get_others_in_group()]
                list_normative.sort(reverse=True)
                list_NE = [value for attr,value in p1.__dict__.items() if attr.startswith("normative_expectations")]
                for i,item in enumerate(list_NE):
                    if item != None:
                        p1.payoff_normative_expectations += max(0,Constants.belief_correct_pay - abs(list_normative[i]-item))
                    else:
                        p1.payoff_normative_expectations += 0

                
class Player(BasePlayer):
    total_contribution = models.PositiveIntegerField()
    fraction_contribution = models.FloatField()
    common_account_earnings = models.FloatField()
    contribution = models.IntegerField(min=0, max=Constants.endowment)
    unconditional_payoff = models.FloatField()
    absent_contribution = models.PositiveIntegerField()
    absent_pnb = models.PositiveIntegerField()
    absent_empirical = models.PositiveIntegerField()
    absent_normative = models.PositiveIntegerField()
    # questions in the page Control
    question_1_1 = models.PositiveIntegerField(
        choices=[
            [0, "25"],
            [1, "15"],
            [2, "5"],
        ]
    )

    question_1_2 = models.PositiveIntegerField(
        choices=[
            [0, "97.9"],
            [1, "52.2"],
            [2, "31.8"]
        ]
    )

    question_2_1 = models.PositiveIntegerField(
        choices=[
            [0, "25"],
            [1, "15"],
            [2, "5"]
        ]
    )

    question_2_2 = models.PositiveIntegerField(
        choices=[
            [0, "72.9"],
            [1, "52.2"],
            [2, "35.4"]
        ]
    )

    question_3_1 = models.PositiveIntegerField(
        choices=[
            [0, "22"],
            [1, "5"],
            [2, "2"]
        ]
    )

    question_3_2 = models.PositiveIntegerField(
        choices=[
            [0, "6.3"],
            [1, "356.7"],
            [2, "14"]
        ]
    )


    question_4_1 = models.PositiveIntegerField(
        choices=[
            [0, "2"],
            [1, "6"],
            [2, "15"]
        ]
    )

    question_4_2 = models.PositiveIntegerField(
        choices=[
            [0, "6.7"],
            [1, "150.4"],
            [2, "14"]
        ]
    )

    question_5 = models.PositiveIntegerField(
        choices=[
            [0, "Nada"],
            [1, "Seré excluído del experimento"]
        ]
    )

    correct_answers = models.PositiveIntegerField(default=0)
    personal_normative_beliefs = models.IntegerField(min=0, max=Constants.endowment)
    payoff_empirical_expectations = models.IntegerField(default=0)
    payoff_normative_expectations = models.IntegerField(default=0)

    empirical_expectations0 = models.IntegerField(min=0, max=Constants.endowment)
    empirical_expectations1 = models.IntegerField(min=0, max=Constants.endowment)
    empirical_expectations2 = models.IntegerField(min=0, max=Constants.endowment)
    empirical_expectations3 = models.IntegerField(min=0, max=Constants.endowment)
    empirical_expectations4 = models.IntegerField(min=0, max=Constants.endowment)
    
    normative_expectations0 = models.IntegerField(min=0, max=Constants.endowment)
    normative_expectations1 = models.IntegerField(min=0, max=Constants.endowment)
    normative_expectations2 = models.IntegerField(min=0, max=Constants.endowment)
    normative_expectations3 = models.IntegerField(min=0, max=Constants.endowment)
    normative_expectations4 = models.IntegerField(min=0, max=Constants.endowment)
    
    def request_variables(self):
        df_variables = pd.read_csv(os.getcwd()+'/non_linear_cpr_game/df_combined.csv').set_index("code")
        if self.participant.code in df_variables.index:
            for col in df_variables.columns:
                self.participant.vars[col] = df_variables[col].loc[self.participant.code]
            self.participant.vars["absence"] = 0
            self.participant.vars["max_absence"] = self.session.config["inactive_threshold"]
        else:
            self.participant.vars["absence"] = self.session.config["inactive_threshold"]
            self.participant.vars["max_absence"] = self.session.config["inactive_threshold"]
            self.participant.vars["risk_lottery_payoff"] = 0
            self.participant.vars["norm_compliance_payoff"] = 0
            self.participant.vars["payoff_svo"] = 0 
        self.participant.vars["global_payoff"] = self.participant.vars["risk_lottery_payoff"] + self.participant.vars["norm_compliance_payoff"] + self.participant.vars["payoff_svo"]
    def creating_score(self):
        if self.participant.vars["absence"] >= self.participant.vars["max_absence"]:
            self.participant.vars["score"] = 1
        else:
            self.participant.vars["score"] = random.random()


    # function used to check control questions
    def control_calc(self):
        if self.question_1_1 == Constants.a1_1:
            self.correct_answers += 1
        if self.question_1_2 == Constants.a1_2:
            self.correct_answers += 1
        if self.question_2_1 == Constants.a2_1:
            self.correct_answers += 1
        if self.question_2_2 == Constants.a2_2:
            self.correct_answers += 1
        if self.question_3_1 == Constants.a3_1:
            self.correct_answers += 1
        if self.question_3_2 == Constants.a3_2:
            self.correct_answers += 1
        if self.question_4_1 == Constants.a4_1:
            self.correct_answers += 1
        if self.question_4_2 == Constants.a4_2:
            self.correct_answers += 1
        if self.question_5 == Constants.a5:
            self.correct_answers += 1

    # define contributions of inactive players
    def inactive_contribution(self):  # XXX
        if self.round_number > 1:
            list_contributions = []
            for p in [p_previous.in_round(self.round_number-1) for p_previous in self.get_others_in_subsession()]:
                if (p.participant.vars["absence"] < p.participant.vars["max_absence"]) and (p.contribution is not None):
                    list_contributions.append(p.contribution)

            if len(list_contributions) == 0:
                self.contribution = 0
            elif len(list_contributions) > 0:
                self.contribution = random.choice(list_contributions)  
        else:
            self.contribution = 15
    # define pnb of inactive players
    def inactive_pnb(self): # XXX
        if self.round_number > 1:
            list_pnb = []
            for p in [p_previous.in_round(self.round_number-1) for p_previous in self.get_others_in_subsession()]:
                if (p.participant.vars["absence"] < p.participant.vars["max_absence"]) and (p.personal_normative_beliefs is not None):
                    list_pnb.append(p.personal_normative_beliefs)

            if len(list_pnb) == 0:
                self.personal_normative_beliefs = 0
            elif len(list_pnb) > 0:
                self.personal_normative_beliefs = random.choice(list_pnb)
        else:
            self.personal_normative_beliefs = 15
    # retrieve others' contributions to be displayed on Results page
    def other_contributions(self):
        self.participant.vars["other_contributions"] =  [other.contribution for other in self.get_others_in_group()]
        self.participant.vars["other_inactive"] = [other.participant.vars["absence"] >= other.participant.vars["max_absence"] for other in self.get_others_in_group()]
        self.participant.vars["other_inactive"] = ["\274c" if i==True else " " for i in self.participant.vars["other_inactive"]]
        self.participant.vars["contribution_inactive"] = [str(i[0])+i[1] for i in zip(self.participant.vars["other_contributions"],self.participant.vars["other_inactive"])]
    def empirical_expectations(self):
        #Asegurarse que os inactivos seleccionan None
        if self.participant.vars["absence"] < self.participant.vars["max_absence"]: 
            list_empirical = [p.contribution for p in self.get_others_in_group()]
            list_empirical.sort(reverse=True)
            list_EE = [value for attr,value in self.__dict__.items() if attr.startswith("empirical_expectations")]
            for i,item in enumerate(list_EE):
                if item != None:
                    self.payoff_empirical_expectations += max(0,Constants.belief_correct_pay - abs(list_empirical[i]-item))
                else:
                    self.payoff_empirical_expectations += 0

    def normative_expectations(self):
        if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
            list_normative = [p.personal_normative_beliefs for p in self.get_others_in_group()]
            list_normative.sort(reverse=True)
            list_NE = [value for attr,value in self.__dict__.items() if attr.startswith("normative_expectations")]
            for i,item in enumerate(list_NE):
                if item != None:
                    self.payoff_normative_expectations += max(0,Constants.belief_correct_pay - abs(list_normative[i]-item))
                else:
                    self.payoff_normative_expectations += 0

    # this function defines the rounds that will be considered for payment; stage= week
    def payment_rounds(self):
        if self.round_number == 1:
           self.participant.vars["paying_rounds"] = random.sample(range(1,Constants.num_rounds+1),5)
#           

    def cumulative_payoff(self):
        if self.round_number == Constants.num_rounds:
            self.participant.vars["non_linear_payoff"] = sum([p.payoff for p in self.in_all_rounds()])
            self.participant.vars['global_payoff'] += self.participant.vars["non_linear_payoff"]
            self.participant.vars["final_contribution"] = self.contribution
            self.participant.vars["contributions_payoff"] = [p.unconditional_payoff for p in self.in_all_rounds()]
            self.participant.vars["expectations_payoff"] = [self.in_round(m).payoff_empirical_expectations + self.in_round(m).payoff_normative_expectations for m in self.participant.vars["paying_rounds"]]
            self.participant.vars["treatment"] = Constants.treatment

class Link(BaseLink):
	pass
