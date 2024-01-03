from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random as rd
from . import models


class Consentimiento_juan(Page):
    #timeout_seconds = 32

    def is_displayed(self):
        return self.subsession.round_number == 1


class Pre_experimento_juan(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    pass


class Welcome_juan(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Instructions_juan(Page):
    timeout_seconds = 302

    def is_displayed(self):
        return self.subsession.round_number == 1


class Introduction_juan(Page):
    timeout_seconds = 22

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['absence'] += 1

    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >= 3 else False 
        return {'inactive':inactive,}

class Aspiration_juan(Page):
    timeout_seconds = 22

    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >= 3 else False
        return {'pay_1_val': [1, 2, 3, 4, 5, 6, 7],
                'pay_2_val': [1, 2, 3, 4, 5, 6, 7],
                'inactive' : inactive,
                }

    form_model = models.Player
    form_fields = ['pay_1_val', 'pay_2_val']

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['absence'] += 1
            self.player.pay_1_val = rd.choice([1, 2, 3, 4, 5, 6, 7])
            self.player.pay_2_val = rd.choice([1, 2, 3, 4, 5, 6, 7])


class Find_Partner(WaitPage):
    template_name = "e05_ethnic_markers/Find_partner_juan.html"

    def after_all_players_arrive(self):
        self.group.find_partners()


class Coordination_juan(Page):
    timeout_seconds = 22
    form_model = models.Player
    form_fields = ['acción']
    
    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['absence'] += 1
            self.player.acción = rd.choice([1, 2])
    
    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >=3 else False
        return{ 'inactive': inactive,}

class ResultsWaitPage(WaitPage):
    template_name = "e05_ethnic_markers/ResultsWaitPage_juan.html"

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results_juan(Page):
    timeout_seconds = 12

    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >=3 else False
        return {'global_payoff': self.participant.vars['global_payoff'],
                'inactive': inactive,
                }

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['absence'] += 1
    pass


# class BiasWaitPage(WaitPage):
#
#    title_text = 'Espere su turno'
#    body_text = 'Estamos haciendo una pregunta de manera ordenada'
#
#    def is_displayed(self):
#        return self.subsession.round_number == Constants.num_rounds
#
#    def after_all_players_arrive(self):
#        self.group.find_examples()


class Bias_juan(Page):
    timeout_seconds = 32

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def before_next_page(self):
        # self.player.find_examples()
        if self.timeout_happened:
            self.participant.vars['absence'] += 1
    
    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >=3 else False
        return {'inactive':inactive,}

class Bias_2_juan(Page):
    timeout_seconds = 32
    form_model = models.Player
    form_fields = ['bias']

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.extra_payoff()
        if self.timeout_happened:
            self.participant.vars['absence'] += 1
            self.player.bias = 0
    
    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >=3 else False
        return {'inactive':inactive,}

class Final_juan(Page):
    timeout_seconds = 22

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >= 3 else False
        return {'global_payoff': self.participant.vars['global_payoff'],
                'inactive' : inactive,
                }


page_sequence = [
    Consentimiento_juan,
    Pre_experimento_juan,
    Welcome_juan,
    Instructions_juan,
    Introduction_juan,
    Aspiration_juan,
    Find_Partner,
    Coordination_juan,
    ResultsWaitPage,
    Results_juan,
    Bias_juan,
    Bias_2_juan,
    Final_juan
]
