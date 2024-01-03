from . import models
from .models import Constants
from ._builtin import Page
from otree.db.models import BooleanField as m
import otree.forms


class Info(Page):
    timeout_seconds = 32

    def is_displayed(self):
        return self.subsession.round_number == 1


class Questions(Page):

    timeout_seconds = 12

    form_model = models.Player
    form_fields = ['selectionYellow', 'selectionBlue']

    def vars_for_template(self):
        return {
            'ball_number': self.subsession.round_number,
            'condition': 1,
        }

    def error_message(self, values):
        if values['selectionYellow'] == None and values['selectionBlue'] == None:
            return "Select at least one box."
        elif values['selectionYellow'] != None and values['selectionBlue'] != None:
            if values['selectionYellow'] + values['selectionBlue'] == 2:

                self.player.selectionYellow = None
                self.player.selectionBlue = None
                return "Select only one box."

    def before_next_page(self):
        # if self.round_number == 20:
        self.player.storePayments()
        self.player.total_payment()


class Final(Page):
    def is_displayed(self):
        return self.round_number == 20

    def vars_for_template(self):
        # global_payoff = self.participant.vars['global_payoff']
        # global_payoff += sum([p.payoff for p in self.player.in_all_rounds()])
        return {'global_payoff': self.participant.vars['payoffNormCompliance'],
                'total_payoff': self.participant.vars['total_pay']
                }


class Paypal(Page):
    def is_displayed(self):
        return self.round_number == 20

    form_model = models.Player
    form_fields = ['paypal']


class Final_2(Page):
    def is_displayed(self):
        return self.round_number == 20

    pass


page_sequence = [
    Info,
    Questions,
    Final,
    Paypal,
    Final_2
]
