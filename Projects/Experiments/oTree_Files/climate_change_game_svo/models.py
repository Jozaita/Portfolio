from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, BaseLink,
	Currency as c, currency_range
)

import random
import datetime

class Link(BaseLink):
	pass


class Constants(BaseConstants):
	name_in_url = 'ccsv'
	players_per_group = 2
	num_rounds = 1
	language = "SPA"
	timeout_SliderContinuous = 120
	timeout_WaitNext = int(datetime.timedelta(days=1).total_seconds())
	instructions_slider = 'svotree_AA/SliderInstructions.html'
	instructions_9tdm = 'svotree_AA/NineItemTDMInstructions.html'


class Subsession(BaseSubsession):
	
	def before_session_starts(self):
		self.group_randomly()


class Group(BaseGroup):

	def set_payoffs(self):
		p1 = self.get_player_by_id(1)
		p2 = self.get_player_by_id(2)

		p1.participant.vars["self_paid"] = random.randint(0, 1)

		if p1.participant.vars["self_paid"] == 1:
			p2.participant.vars["self_paid"] = 0
			p1.payoff = p1.paid_slider_self
			p2.payoff = p1.paid_slider_other

		elif p1.participant.vars["self_paid"] == 0:
			p2.participant.vars["self_paid"] = 1
			p1.payoff = p2.paid_slider_other
			p2.payoff = p2.paid_slider_self

		for p in self.get_players():
			p.participant.vars['payoff_svo'] = p.payoff
			p.participant.vars["global_payoff"] += p.payoff 

class Player(BasePlayer):
	def payoff_precursor(self):
		self.slider1_self = 85
		self.slider2_self = round(85+self.slider2*0.15)
		self.slider3_self = round(50+self.slider3*0.35)
		self.slider4_self = round(50+self.slider4*0.35)
		self.slider5_self = round(100-self.slider5*0.50)
		self.slider6_self = round(100-self.slider6*0.15)

		self.slider1_other = round(85-self.slider1*0.70)
		self.slider2_other = round(15+self.slider2*0.35)
		self.slider3_other = round(100-self.slider3*0.15)
		self.slider4_other = round(100-self.slider4*0.85)
		self.slider5_other = round(50+self.slider5*0.50)
		self.slider6_other = round(50+self.slider6*0.35)

		self.participant.vars["slider_paid"] = random.randint(1, 6)

		if self.participant.vars['slider_paid'] == 1:
			self.paid_slider_self = self.slider1_self
			self.paid_slider_other = self.slider1_other
		elif self.participant.vars['slider_paid'] == 2:
			self.paid_slider_self = self.slider2_self
			self.paid_slider_other = self.slider2_other
		elif self.participant.vars['slider_paid'] == 3:
			self.paid_slider_self = self.slider3_self
			self.paid_slider_other = self.slider3_other
		elif self.participant.vars['slider_paid'] == 4:
			self.paid_slider_self = self.slider4_self
			self.paid_slider_other = self.slider4_other
		elif self.participant.vars['slider_paid'] == 5:
			self.paid_slider_self = self.slider5_self
			self.paid_slider_other = self.slider5_other
		elif self.participant.vars['slider_paid'] == 6:
			self.paid_slider_self = self.slider6_self
			self.paid_slider_other = self.slider6_other



	risk_lottery_payoff = models.PositiveIntegerField()
	lottery_choice = models.PositiveIntegerField()
	lottery_win = models.PositiveIntegerField()
	selectionYellow = models.PositiveIntegerField()
	norm_compliance_payoff = models.PositiveIntegerField()
	slider_paid = models.PositiveIntegerField()
	self_paid = models.PositiveIntegerField()
	payoff_svo = models.PositiveIntegerField()

	paid_slider_self = models.PositiveIntegerField()
	paid_slider_other = models.PositiveIntegerField()

	slider1 = models.FloatField()
	slider2 = models.FloatField()
	slider3 = models.FloatField()
	slider4 = models.FloatField()
	slider5 = models.FloatField()
	slider6 = models.FloatField()
	slider_angle = models.DecimalField(decimal_places=2, max_digits=5)
	slider_classification = models.CharField()

	slider1_self = models.PositiveIntegerField()
	slider2_self = models.PositiveIntegerField()
	slider3_self = models.PositiveIntegerField()
	slider4_self = models.PositiveIntegerField()
	slider5_self = models.PositiveIntegerField()
	slider6_self = models.PositiveIntegerField()

	slider1_other = models.PositiveIntegerField()
	slider2_other = models.PositiveIntegerField()
	slider3_other = models.PositiveIntegerField()
	slider4_other = models.PositiveIntegerField()
	slider5_other = models.PositiveIntegerField()
	slider6_other = models.PositiveIntegerField()

	nine_item_tdm_1 = models.CharField()
	nine_item_tdm_2 = models.CharField()
	nine_item_tdm_3 = models.CharField()
	nine_item_tdm_4 = models.CharField()
	nine_item_tdm_5 = models.CharField()
	nine_item_tdm_6 = models.CharField()
	nine_item_tdm_7 = models.CharField()
	nine_item_tdm_8 = models.CharField()
	nine_item_tdm_9 = models.CharField()
	nine_item_tdm_prosocial = models.IntegerField()
	nine_item_tdm_individualistic = models.IntegerField()
	nine_item_tdm_competitive = models.IntegerField()
	nine_item_tdm_classification = models.CharField()
