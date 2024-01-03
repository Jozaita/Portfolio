from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random as rd
import datetime as dt
from . import models


class Consentimiento_juan(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


#class Organize_groups(WaitPage):
#    template_name = "e1_ethnic_markers/New_round_juan.html"
#    group_by_arrival_time = True
#    def is_displayed(self):
#        return self.round_number == 1

class Pre_experimento_juan(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    

class Welcome_juan(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

class Instructions_juan(Page):
    timeout_seconds = Constants.timeout_instrucciones
    def is_displayed(self):
        return self.subsession.round_number == 1
    def before_next_page(self):
        if self.timeout_happened:
            self.participant.label = 1 
        else:
            self.participant.label = 0
        
class Organizing_groups(WaitPage):
    wait_for_all_groups = True
    def is_displayed(self):
        return self.round_number == 1
   
    def after_all_players_arrive(self):
        sorted_players = sorted(self.subsession.get_players(),key = lambda player:player.participant.label)
        group_matrix = []
        ppg = Constants.players_per_group
        for i in range(0,len(sorted_players),ppg):
            group_matrix.append(sorted_players[i:i+ppg])
        self.subsession.set_group_matrix(group_matrix)
        for subsession in self.subsession.in_rounds(2,Constants.num_rounds):         
             subsession.group_like_round(1)
class Introduction_juan(Page):
    timeout_seconds = Constants.timeout_sombreros

    def is_displayed(self):
        return self.round_number == 1
    
    def vars_for_template(self):
        inactive = True if self.group.id_in_subsession == len(self.subsession.get_group_matrix()) else False
        if inactive:
            self.player.absence = Constants.max_absence
        return {"inactive":inactive}
#WaitPage pra actualizar as ausencias
class In_between_rounds_juan(WaitPage):
    template_name = "e1_ethnic_markers/New_round_juan.html"

    def after_all_players_arrive(self):
        if self.round_number == 1:
            self.group.assign_markers()
        if self.round_number > 1:
            self.group.recall()

#class Not_aspiration_juan(WaitPage):
#    template_name = "e1_ethnic_markers/New_round_juan.html"
#    def is_displayed(self):
#        return self.subsession.round_number % 15 != 0
#     
#    def vars_for_template(self):
#         inactive = True if self.player.absence >= Constants.max_absence else False
#         return{ 'inactive': inactive,}

class Aspiration_juan(Page):
    timeout_seconds = Constants.timeout_aspiraciones
    def is_displayed(self):
        return self.subsession.round_number % 15 == 0 or self.subsession.round_number == 1
    form_model = models.Player
    form_fields = ['pay_1_val', 'pay_2_val']

    def before_next_page(self):
        if self.timeout_happened:
            self.player.absence += 1
            self.player.pay_1_val = rd.choice([1, 2, 3, 4, 5, 6, 7])
            self.player.pay_2_val = rd.choice([1, 2, 3, 4, 5, 6, 7])

    def vars_for_template(self):
        inactive = True if self.player.absence >= Constants.max_absence else False
        return {
                'inactive' : inactive,
                }

class Find_Partner(WaitPage):
    template_name = "e1_ethnic_markers/Find_partner_juan.html"

    def after_all_players_arrive(self):
        self.group.find_partners()

    def vars_for_template(self):
        inactive = True if self.player.absence >= Constants.max_absence else False
        return {'inactive':inactive,}

class Coordination_juan(Page):
    timeout_seconds = Constants.timeout_sombreros

    form_model = models.Player
    form_fields = ['acción']
    
    def before_next_page(self):
        if self.timeout_happened:
            self.player.absence += 1
            self.player.acción = rd.choice([1,2])
    
    def vars_for_template(self):
        inactive = True if self.player.absence >= Constants.max_absence else False
        return{ 'inactive': inactive,}


class ResultsWaitPage(WaitPage):
    template_name = "e1_ethnic_markers/ResultsWaitPage_juan.html"

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def vars_for_template(self):
        inactive = True if self.player.absence >= Constants.max_absence else False
        return {'inactive':inactive,}

class Results_juan(Page):
    timeout_seconds = Constants.timeout_resultados
    def vars_for_template(self):
        inactive = True if self.player.absence >= Constants.max_absence  else False
        return {
                'inactive': inactive,
                }

class Bias_juan(Page):
    timeout_seconds = Constants.timeout_bias

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def before_next_page(self):
        if self.timeout_happened:
           self.player.absence += 1
    
    def vars_for_template(self):
        inactive = True if self.player.absence >=Constants.max_absence else False
        return {'inactive':inactive,}

class Bias_2_juan(Page):
    timeout_seconds = Constants.timeout_bias

    form_model = models.Player
    form_fields = ['bias']

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.extra_payoff()
        if self.timeout_happened:
            self.player.absence +=1
            self.player.bias = 0
    
    def vars_for_template(self):
        inactive = True if self.player.absence >= Constants.max_absence else False
        return {'inactive':inactive,}

class Final_juan(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        inactive = True if self.player.absence >= Constants.max_absence else False
        return {
                'inactive' : inactive,
                }


page_sequence = [
    Consentimiento_juan,
    Pre_experimento_juan,
    #Welcome_juan,
    Instructions_juan,
    Organizing_groups,
    In_between_rounds_juan,
    Introduction_juan,
    Aspiration_juan,
 #   Not_aspiration_juan,
    Find_Partner,
    Coordination_juan,
    ResultsWaitPage,
    Results_juan,
    Bias_juan,
    Bias_2_juan,
    Final_juan
]
