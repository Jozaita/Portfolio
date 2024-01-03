from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, BaseLink,
	Currency as c, currency_range,
)

import random
import datetime
import numpy as np

author = 'Juan Ozaita Corral'

doc = """
TODO"""

class Link(BaseLink):
	pass


class Constants(BaseConstants):
	name_in_url = 'ccc'
	
	####PARAMETERS TO BE SPECIFIED####
	players_per_group = 5
	num_rounds = 1
	inactive_threshold = 4

	language = "ENG"
	real_currency = "euros"
	currency_per_token = 0.5
	#stages are the number of discrete sections of the game (e.g. one week each)
	endowment = 10
	ee_payment = 1
	ne_payment = 1

	d_impact = 1/(endowment*players_per_group)
	d_probability = 0.5 
	##################################
	EE_options = 10  
	NE_options = 10

	dict_instructions = {
		'other_players_per_group':players_per_group -1,
		'token_value':currency_per_token*endowment,
		'd_impact_percentage':int(d_impact*100),
		'half_tokens':endowment/2,
		'dis_prob_percentage':d_probability*100,
		'comp_dis_prob_percentage': 100 - (d_probability*100),
		'dis_prob_number':int(d_probability*10),
		'comp_dis_prob_number':10 - int(d_probability*10),
		'currency_per_token':currency_per_token,
		'endowment':endowment,
		'ee_payment':ee_payment,
		'ne_payment':ne_payment,
		'd_impact':d_impact,
		'd_probability':d_probability}

	templates_dir = "climate_change_game_continuous/"+language+"/"


	language_dict = {
		"SPA":{
			"err_message_lw":"Ha asignado un total de {} tokens, menos de lo esperado. Debe asignar un total de 100 tokens.",
			"err_message_up":"Ha asignado un total de {} tokens, más de lo esperado. Debe asignar un total de 100 tokens.",
			"dist_label_0":"Porcentaje que contribuye 0 puntos",
			"dist_label_1":"Porcentaje que contribuye 1 punto",
			"dist_label_2":"Porcentaje que contribuye 2 puntos",
			"dist_label_3":"Porcentaje que contribuye 3 puntos",
			"dist_label_4":"Porcentaje que contribuye 4 puntos",
			"dist_label_5":"Porcentaje que contribuye 5 puntos",
			"dist_label_6":"Porcentaje que contribuye 6 puntos",
			"dist_label_7":"Porcentaje que contribuye 7 puntos",
			"dist_label_8":"Porcentaje que contribuye 8 puntos",
			"dist_label_9":"Porcentaje que contribuye 9 puntos",
			"dist_label_10":"Porcentaje que contribuye 10 puntos",
			"comments_verbose":"Comentarios:",
			"paypal_verbose":"Cuenta de PayPal:"
		},
		"ENG":{
			"err_message_lw":"You have assigned a total of {} tokens, lower than required. You must assign a total of 100 tokens.",
			"err_message_up":"You have assigned a total of {} tokens, higher than required. You must assign a total of 100 tokens.",
			"dist_label_0":"Percentage that contributes 0 tokens",
			"dist_label_1":"Percentage that contributes 1 token",
			"dist_label_2":"Percentage that contributes 2 tokens",
			"dist_label_3":"Percentage that contributes 3 tokens",
			"dist_label_4":"Percentage that contributes 4 tokens",
			"dist_label_5":"Percentage that contributes 5 tokens",
			"dist_label_6":"Percentage that contributes 6 tokens",
			"dist_label_7":"Percentage that contributes 7 tokens",
			"dist_label_8":"Percentage that contributes 8 tokens",
			"dist_label_9":"Percentage that contributes 9 tokens",
			"dist_label_10":"Percentage that contributes 10 tokens",
			"comments_1_verbose":"- What do you think is the purpose of this study?",
			"comments_2_verbose":"- Do you see any link between this study and situations in the real world?",
			"comments_3_verbose":"- Were any parts of this study unclear to you?",
			"comments_4_verbose":"- Was there any part of this study that did not work properly?",
			"paypal_verbose":"Paypal account:",
			"question_1_text":"How many tokens does every participant receive?",
			"question_2_text":"How many players are there in your group (excluding yourself)?",
			"question_3_text":"What is the return of a token kept privately?",
			"question_4_text":"What is the return of a token put in the collective fund?",
			"question_5_text":"By how much does each token contributed to the collective fund reduce the impact of a disaster? (just the number, in percentage)",
			"question_6_text":"By how much does each token kept privately reduce the impact of a disaster? (just the number,in percentage)",
			"question_7_text":"What is the probability that a disaster occurs? (just the number, in percentage)",
			"question_8_text":"What would have been the impact of a disaster? (in percentage)",
			"question_9_text":"How many tokens did player 1 earn in this case?",
			"question_10_text":"What would have been the impact of a disaster? (in percentage)",
			"question_11_text":"How many tokens did player 1 earn in this case?",

			}
		}
	answer_1 = endowment
	answer_2 = players_per_group - 1 
	answer_3 = 1
	answer_4 = 0.2
	answer_5 = d_impact*100
	answer_6 = 0
	answer_7 = d_probability*100
	answer_8 = 60
	answer_9 = 12
	answer_10 = 30
	answer_11 = 7



class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	total_contribution = models.IntegerField()
	disaster = models.IntegerField()
	impact = models.FloatField()

	def calc_disaster(self):
	#Calculates the boolean of disaster given the prob and risk profile
		self.total_contribution = sum([p.contribution for p  in self.get_players()])
		self.disaster = random.random() < Constants.d_probability
		self.impact = 1 - Constants.d_impact*self.total_contribution


	def set_payoffs(self):
		#Unconditional payoff calculations
		for p1 in self.get_players():
			p1.private_tokens = Constants.endowment - p1.contribution
			p1.public_tokens = self.total_contribution/Constants.players_per_group
			p1.unconditional_payoff = (p1.private_tokens+p1.public_tokens)*(1-self.disaster*self.impact)
			p1.payoff = p1.unconditional_payoff + p1.payoff_empirical_expectations + p1.payoff_normative_expectations
			p1.payoff_currency = p1.unconditional_payoff*Constants.currency_per_token+p1.payoff_empirical_expectations+p1.payoff_normative_expectations

	def group_other_contributions(self):
		for p in self.get_players():
			p.participant.vars["other_contributions"] = [other.contribution for other in p.get_others_in_group()]
			p.participant.vars["other_inactive"] = ["\u274C" if other.absent_contribution == True else " " for other in p.get_others_in_group()]
			p.participant.vars["contribution_inactive"] = [str(i[0])+i[1] for i in zip(p.participant.vars["other_contributions"],p.participant.vars["other_inactive"])]

	def group_empirical_expectations(self):
		for p1 in self.get_players():
			p1.ee_accuracy = 0
			if p1.participant.vars["absence"] < p1.participant.vars["max_absence"]:
				list_empirical = [p2.contribution for p2 in self.subsession.get_players()]
				dist_empirical = np.histogram(list_empirical,range=(-0.5,10.5),bins=11)[0]
				dist_empirical = dist_empirical/sum(dist_empirical)*100
				dict_EE = {key:value for key,value in p1.__dict__.items() if key.startswith("empirical_expectations")}
				list_EE = [dict_EE["empirical_expectations{}".format(i)] for  i in range(Constants.EE_options)]
				for i, item in enumerate(list_EE):
					if item != None:
						p1.ee_accuracy += min(item,dist_empirical[i])/100
			p1.payoff_empirical_expectations = p1.ee_accuracy*Constants.ee_payment

	def group_normative_expectations(self):
		for p1 in self.get_players():
			p1.ne_accuracy = 0
			if p1.participant.vars["absence"] < p1.participant.vars["max_absence"]:
				list_normative = [p2.personal_normative_beliefs for p2 in self.subsession.get_players()]
				dist_normative = np.histogram(list_normative,range=(-0.5,10.5),bins=11)[0]
				dist_normative = dist_normative/sum(dist_normative)*100
				dict_NE = {key:value for key,value in p1.__dict__.items() if key.startswith('normative_expectations')}
				list_NE = [dict_NE["normative_expectations{}".format(i)] for i in range(Constants.NE_options)]
				for i,item in enumerate(list_NE):
					if item != None: 
						p1.ne_accuracy += min(item,dist_normative[i])/100
			p1.payoff_normative_expectations = p1.ne_accuracy*Constants.ne_payment


class Player(BasePlayer):


	def percentage_field(name=None):

		return models.IntegerField(min=0,max=100,initial=0,verbose_name=name,widget=widgets.SliderInput())

	empirical_expectations0 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_0"])
	empirical_expectations1 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_1"])
	empirical_expectations2 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_2"])
	empirical_expectations3 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_3"])
	empirical_expectations4 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_4"])
	empirical_expectations5 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_5"])
	empirical_expectations6 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_6"])
	empirical_expectations7 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_7"])
	empirical_expectations8 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_8"])
	empirical_expectations9 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_9"])
	empirical_expectations10 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_10"])


	normative_expectations0 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_0"])
	normative_expectations1 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_1"])
	normative_expectations2 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_2"])
	normative_expectations3 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_3"])
	normative_expectations4 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_4"])
	normative_expectations5 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_5"])
	normative_expectations6 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_6"])
	normative_expectations7 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_7"])
	normative_expectations8 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_8"])
	normative_expectations9 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_9"])
	normative_expectations10 = percentage_field(name=Constants.language_dict[Constants.language]["dist_label_10"])

	ee_accuracy = models.FloatField()
	ne_accuracy = models.FloatField()
	payoff_currency = models.FloatField()
	click_count_input = models.IntegerField(initial = 0, blank=True)


	contribute_0 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="0%")
	contribute_10 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="10%")
	contribute_20 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="20%")
	contribute_30 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="30%")
	contribute_40 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="40%")
	contribute_50 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="50%")
	contribute_60 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="60%")
	contribute_70 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="70%")
	contribute_80 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="80%")
	contribute_90 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="90%")
	contribute_100 = models.PositiveIntegerField(choices = list(range(0,11)),widget=widgets.RadioSelectHorizontal(),verbose_name="100%")

	question_1 = models.FloatField()
	question_2 = models.FloatField()
	question_3 = models.FloatField()
	question_4 = models.FloatField()
	question_5 = models.FloatField()
	question_6 = models.FloatField()
	question_7 = models.FloatField()
	question_8 = models.FloatField()
	question_9 = models.FloatField()
	question_10 = models.FloatField()
	question_11 = models.FloatField()


	buying_contribution = models.PositiveIntegerField(\
			choices = list(range(0,11)),
			widget=widgets.RadioSelectHorizontal())
	contribution = models.PositiveIntegerField(\
			choices = list(range(0,11)),
			widget=widgets.RadioSelectHorizontal())
	confidence_empirical = models.PositiveIntegerField(choices=[[1,'Not at all confident'],
	    [2,'Slightly confident'],
	    [3,'Moderately confident'],
	    [4,'Very confident'],
	    [5,'Extremely confident']])
	confidence_normative = models.PositiveIntegerField(choices=[[1,'Not at all confident'],
	    [2,'Slightly confident'],
	    [3,'Moderately confident'],
	    [4,'Very confident'],
	    [5,'Extremely confident']])
	public_tokens = models.FloatField()
	private_tokens = models.IntegerField()
	unconditional_payoff = models.FloatField()
	payoff_empirical_expectations = models.FloatField(default=0)
	payoff_normative_expectations = models.FloatField(default=0)

	total_payoff = models.IntegerField()


	correct_answers_1 = models.PositiveIntegerField(initial=0)
	correct_answers_2 = models.PositiveIntegerField(initial=0)
	correct_answers_3 = models.PositiveIntegerField(initial=0)

	personal_normative_beliefs = models.IntegerField(choices=list(range(11)),widget=widgets.RadioSelectHorizontal())


	absent_contribution = models.PositiveIntegerField()
	absent_conditional = models.PositiveIntegerField()
	absent_pnb = models.PositiveIntegerField()
	absent_empirical = models.PositiveIntegerField()
	absent_normative = models.PositiveIntegerField()

	consent = models.PositiveIntegerField()
	prolific_id = models.CharField()
	comments_1 = models.TextField(blank=True,verbose_name=Constants.language_dict[Constants.language]["comments_1_verbose"])
	comments_2 = models.TextField(blank=True,verbose_name=Constants.language_dict[Constants.language]["comments_2_verbose"])
	comments_3 = models.TextField(blank=True,verbose_name=Constants.language_dict[Constants.language]["comments_3_verbose"])
	comments_4 = models.TextField(blank=True,verbose_name=Constants.language_dict[Constants.language]["comments_4_verbose"])
	def request_variables(self):
		#df_variables = pd.read_csv(os.getcwd()+'/climate_change_game_AA/df_combined.csv').set_index("code")
		#for col in df_variables.columns:
			#self.participant.vars[col] = df_variables[col].loc[self.participant.code]
		self.participant.vars["absence"] = 0
		self.participant.vars["max_absence"] = self.session.config["inactive_threshold"]
		#self.participant.vars["global_payoff"] = self.participant.vars["risk_lottery_payoff"]+self.participant.vars["norm_compliance_payoff"]+self.participant.vars["payoff_svo"]
		self.participant.vars["global_payoff"] = 0
	def creating_score(self):
		if self.participant.vars["absence"] >= self.participant.vars['max_absence']:
			self.participant.vars["score"] = 1
		else:
			self.participant.vars["score"] = random.random()

	def save_participant_vars(self):
		for i in range(11):
			empiric_field = "empirical_expectations"+"{}".format(i)
			normative_field = "normative_expectations"+"{}".format(i)
			self.participant.vars[empiric_field] = getattr(self,empiric_field)
			self.participant.vars[normative_field] = getattr(self,normative_field)
		self.participant.vars["contribution"] = self.contribution
		self.participant.vars["personal_normative_beliefs"] = self.personal_normative_beliefs
		self.participant.vars["total_contribution"] = self.group.total_contribution
		
		for k,v in Constants.dict_instructions.items():
			self.participant.vars[k] = v


	def control_calc(self,start,end,suffix):
		for _ in range(start,end):
			if getattr(self,"question_{}".format(_)) == getattr(Constants,"answer_{}".format(_)):
				setattr(self,'correct_answers_{}'.format(suffix),\
					getattr(self,'correct_answers_{}'.format(suffix)) + 1)  

	
	def inactive_contribution(self):
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
			self.contribution = Constants.endowment/2

	def inactive_pnb(self):
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
			self.personal_normative_beliefs = Constants.endowment/2


	def cumulative_payoff(self):
		if self.round_number == Constants.num_rounds:
			self.participant.vars["climate_payoff"] = sum([p.payoff for p in self.in_all_rounds()])
			self.participant.vars["global_payoff"] += self.participant.vars["climate_payoff"]


