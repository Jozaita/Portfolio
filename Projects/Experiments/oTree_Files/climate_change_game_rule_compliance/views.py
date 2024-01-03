from . import models
from .models import Constants
from ._builtin import Page
from otree.db.models import BooleanField as m
import otree.forms


class Info(Page):
    template_name = "climate_change_game_rule_compliance/Info.html"
    def is_displayed(self):
        return self.subsession.round_number == 1
    
    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >=self.participant.vars['max_absence']  else False
        return {'inactive':inactive}
    
class Questions(Page):
    #timeout_seconds = 12
    template_name = "climate_change_game_rule_compliance/Questions.html"
    form_model = models.Player
    form_fields = ['selectionYellow', 'selectionBlue']

    def vars_for_template(self):
        inactive = True if self.participant.vars['absence'] >=self.participant.vars['max_absence'] else False
        return {
            'ball_number': self.subsession.round_number,
            'condition': 1,
            'inactive': inactive
        }


page_sequence = [
    Info,
    Questions,
]
