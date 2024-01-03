from . import models
from ._builtin import Page, WaitPage
from .functions import slider, tdm9
from otree.api import Currency as c, currency_range
from .models import Constants
import datetime


class SliderPrimaryDiscrete(Page):

    form_model = models.Player
    form_fields = ['slider1',
                   'slider2',
                   'slider3',
                   'slider4',
                   'slider5',
                   'slider6',
                ]

    def vars_for_template(self):
        return {'slider_items': [1, 2, 3, 4, 5, 6]}

    def before_next_page(self):
        chosen_values = {
            'item1': self.player.slider1,
            'item2': self.player.slider2,
            'item3': self.player.slider3,
            'item4': self.player.slider4,
            'item5': self.player.slider5,
            'item6': self.player.slider6
        }
        mean_allocations = slider.mean_allocations_discrete(chosen_values)
        svo_slider_angle = slider.svo_angle(mean_allocations['self'], mean_allocations['other'])
        self.player.slider_angle = svo_slider_angle
        self.player.slider_classification = slider.svo_classification(svo_slider_angle)


class SliderPrimaryContinuous(Page):
    form_model = models.Player
    form_fields = ['slider1',
                   'slider2',
                   'slider3',
                   'slider4',
                   'slider5',
                   'slider6',
                ]
    #timeout_seconds = Constants.timeout_SliderContinuous
    template_name = "svotree_AA/SliderPrimaryContinuous_"+Constants.language+".html"
    def vars_for_template(self):
        inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
        return {
            'slider_items': [1, 2, 3, 4, 5, 6],
            'email': self.session.config['email'],
            "inactive":inactive
            }

    def before_next_page(self):
        chosen_values = {
            'item1': self.player.slider1,
            'item2': self.player.slider2,
            'item3': self.player.slider3,
            'item4': self.player.slider4,
            'item5': self.player.slider5,
            'item6': self.player.slider6
        }
        mean_allocations = slider.mean_allocations_continuous(chosen_values)
        svo_slider_angle = slider.svo_angle(mean_allocations['self'], mean_allocations['other'])
        self.player.slider_angle = svo_slider_angle
        self.player.slider_classification = slider.svo_classification(svo_slider_angle)
        self.player.payoff_precursor()
        if self.timeout_happened:
            self.player.timeout_SliderPrimaryContinuous = 1
            #self.participant.vars["absence"] += 1
class NineItemTDM(Page):

    form_model = models.Player
    form_fields = [
        "nine_item_tdm_1",
        "nine_item_tdm_2",
        "nine_item_tdm_3",
        "nine_item_tdm_4",
        "nine_item_tdm_5",
        "nine_item_tdm_6",
        "nine_item_tdm_7",
        "nine_item_tdm_8",
        "nine_item_tdm_9",
    ]

    def vars_for_template(self):

        return {'nine_item_tdm_decisions': tdm9.decisions}

    def before_next_page(self):
        chosen_values = {
            1: self.player.nine_item_tdm_1,
            2: self.player.nine_item_tdm_2,
            3: self.player.nine_item_tdm_3,
            4: self.player.nine_item_tdm_4,
            5: self.player.nine_item_tdm_5,
            6: self.player.nine_item_tdm_6,
            7: self.player.nine_item_tdm_7,
            8: self.player.nine_item_tdm_8,
            9: self.player.nine_item_tdm_9
        }

        self.player.nine_item_tdm_prosocial = tdm9.count_decisions_of_type("Prosocial", chosen_values)
        self.player.nine_item_tdm_individualistic = tdm9.count_decisions_of_type("Individualistic", chosen_values)
        self.player.nine_item_tdm_competitive = tdm9.count_decisions_of_type("Competitive", chosen_values)

        self.player.nine_item_tdm_classification = tdm9.svo_type(chosen_values)


class DebugDisplayPage(Page):

    def vars_for_template(self):
        return {'angle': self.player.slider_angle, 'classification_slider': self.player.slider_classification, 'tdm_prosocial': self.player.nine_item_tdm_prosocial, 'tdm_individualistic': self.player.nine_item_tdm_individualistic, 'tdm_competitive': self.player.nine_item_tdm_competitive, 'classification_tdm': self.player.nine_item_tdm_classification}


class Results(Page):
    pass


class WaitNextRound(Page):
    #timeout_seconds = Constants.timeout_WaitNext
    template_name = "svotree_AA/WaitNextRound_"+Constants.language+".html"
    def vars_for_template(self):
        inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
        return {
            'email': self.session.config['email'],
            "inactive":inactive
            }

class ResultsWaitPage(WaitPage):
    template_name = "svotree_AA/ResultsWaitPage_"+Constants.language+".html"
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        for group in self.subsession.get_groups():
            group.set_payoffs()
    
    def vars_for_template(self):
        inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False 
        return {"inactive":inactive,
                "absence":self.participant.vars["absence"]} 
page_sequence = [
    SliderPrimaryContinuous,
    #DebugDisplayPage,
    #WaitNextRound,
    #ResultsWaitPage,
    #Results,
]
