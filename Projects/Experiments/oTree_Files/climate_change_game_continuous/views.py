from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import datetime


class Welcome(Page):
	template_name = Constants.templates_dir+"Welcome.html"
	form_model = models.Player
	form_fields = ['consent','prolific_id']
	def is_displayed(self):
		return self.round_number == 1
	def before_next_page(self):
		self.player.request_variables()
		if self.timeout_happened: 
			self.participant.vars["absence"] += self.participant.vars["max_absence"]


class Instructions_1(Page):
	template_name = Constants.templates_dir+"Instructions_1.html"

	def is_displayed(self):
		return self.round_number == 1


	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {"inactive":inactive,
				"absence":self.participant.vars["absence"],
				"max_absence":self.participant.vars["max_absence"],
				**Constants.dict_instructions,	
				}

class Instructions_2(Page):
	template_name = Constants.templates_dir+"Instructions_2.html"
	form_model = models.Player
	form_fields = ['click_count_input']


	def is_displayed(self):
		return self.round_number == 1


	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {"inactive":inactive,
				"absence":self.participant.vars["absence"],
				"max_absence":self.participant.vars["max_absence"],
				**Constants.dict_instructions,	
				}

class Instructions_3(Page):
	template_name = Constants.templates_dir+"Instructions_3.html"

	def is_displayed(self):
		return self.round_number == 1


	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {"inactive":inactive,
				"absence":self.participant.vars["absence"],
				"max_absence":self.participant.vars["max_absence"],
				**Constants.dict_instructions,	
				}

class Example(Page):
	template_name = Constants.templates_dir+"Example.html"


	def is_displayed(self):
		return self.round_number == 1

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'all_contribute_all':Constants.endowment*Constants.players_per_group,
			'half_endowment':Constants.endowment/2,
			'all_contribute_half':Constants.endowment*Constants.players_per_group/2,
			'token_value':Constants.endowment*Constants.currency_per_token,
			'token_half_value':Constants.endowment*Constants.currency_per_token/2,
			'rounds':Constants.num_rounds,
			'other_players_per_group':Constants.players_per_group-1,
			**Constants.dict_instructions,
		}

class Control_1(Page):
	template_name = Constants.templates_dir+'Control_1.html'
	form_model = models.Player

	def get_form_fields(self):
	    return ["question_{}".format(i) for i in range(1,5)]


	def is_displayed(self):
		return self.round_number == 1

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds':Constants.num_rounds,
			'other_players_per_group':Constants.players_per_group-1,
			**Constants.dict_instructions,
			**{key:value for key,value in Constants.language_dict[Constants.language].items() if "question" in key}
			}

	def before_next_page(self):
		self.player.control_calc(1,5,1)

class Control_2(Page):
	template_name = Constants.templates_dir+'Control_2.html'
	form_model = models.Player

	def get_form_fields(self):
	    return ["question_{}".format(i) for i in range(5,8)]


	def is_displayed(self):
		return self.round_number == 1

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds':Constants.num_rounds,
			'other_players_per_group':Constants.players_per_group-1,
			**Constants.dict_instructions,
			**{key:value for key,value in Constants.language_dict[Constants.language].items() if "question" in key}
			}

	def before_next_page(self):
		self.player.control_calc(5,8,2)

class Control_3_1(Page):
	template_name = Constants.templates_dir+'Control_3_1.html'
	form_model = models.Player

	def get_form_fields(self):
	    return ["question_{}".format(i) for i in range(8,10)]


	def is_displayed(self):
		return self.round_number == 1

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds':Constants.num_rounds,
			'other_players_per_group':Constants.players_per_group-1,
			**Constants.dict_instructions,
			**{key:value for key,value in Constants.language_dict[Constants.language].items() if "question" in key}
			}

class Control_3_2(Page):
	template_name = Constants.templates_dir+'Control_3_2.html'
	form_model = models.Player

	def get_form_fields(self):
	    return ["question_{}".format(i) for i in range(10,12)]


	def is_displayed(self):
		return self.round_number == 1

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds':Constants.num_rounds,
			'other_players_per_group':Constants.players_per_group-1,
			**Constants.dict_instructions,
			**{key:value for key,value in Constants.language_dict[Constants.language].items() if "question" in key}
			}

	def before_next_page(self):
		self.player.control_calc(8,12,3)

class Answers_1(Page):
	template_name = Constants.templates_dir+"Answers_1.html"

	def is_displayed(self):
		return self.round_number == 1 


	def vars_for_template(self):		
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'half_spending': Constants.endowment/2,
			**Constants.dict_instructions,
			**{key:value for key,value in Constants.language_dict[Constants.language].items() if "question" in key}
		}

class Answers_2(Page):
	template_name = Constants.templates_dir+"Answers_2.html"

	def is_displayed(self):
		return self.round_number == 1 


	def vars_for_template(self):		
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'half_spending': Constants.endowment/2,
			**Constants.dict_instructions,
			**{key:value for key,value in Constants.language_dict[Constants.language].items() if "question" in key}
		}

class Answers_3(Page):
	template_name = Constants.templates_dir+"Answers_3.html"

	def is_displayed(self):
		return self.round_number == 1 


	def vars_for_template(self):		
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'half_spending': Constants.endowment/2,
			**Constants.dict_instructions,
			**{key:value for key,value in Constants.language_dict[Constants.language].items() if "question" in key}
		}


class Contribute_uncond(Page):
	template_name = Constants.templates_dir+"Contribute_uncond.html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	form_model = models.Player
	form_fields = ['contribution']


	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds':Constants.num_rounds,
			'round_number':self.round_number,
			**Constants.dict_instructions,
			}

	def before_next_page(self):
		if self.timeout_happened:
			self.participant.vars["absence"] += 1
			self.player.absent_contribution = True
			self.player.inactive_contribution()


class Beliefs_after_PNB(Page):
	template_name = Constants.templates_dir+"Beliefs_PNB.html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"

	form_model = models.Player
	form_fields = ['personal_normative_beliefs']


	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds':Constants.num_rounds,
			'round_number':self.round_number,
			'other_players_per_group':Constants.players_per_group-1,
			**Constants.dict_instructions,
			}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.absent_pnb = True
			self.player.inactive_pnb()


class Beliefs_after_EE(Page):
	template_name = Constants.templates_dir+"Beliefs_EE.html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	form_model = models.Player
	

	def get_form_fields(self):
		return ['empirical_expectations{}'.format(i) for i in range(Constants.EE_options+1)]
	
	@staticmethod
	def error_message(values):
		suma = sum([int(values["empirical_expectations{}".format(i)]) for i in range(Constants.EE_options+1)])
		if suma < 100:
			return Constants.language_dict[Constants.language]["err_message_lw"].format(suma)
		if suma > 100:
			return Constants.language_dict[Constants.language]["err_message_up"].format(suma) 
	


	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		list_fields = ['empirical_expectations{}'.format(i) for i in range(Constants.EE_options+1)]
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds':Constants.num_rounds,
			'round_number':self.round_number,
			'other_players_per_group':Constants.players_per_group-1,
			'list_fields':list_fields,
			**Constants.dict_instructions,
			}


	def before_next_page(self):
		if self.timeout_happened:
			for _ in range(Constants.EE_options+1):
				setattr(self.player,"empirical_expectations{}".format(_),0)
			self.player.absent_empirical = True

class Confidence_empirical(Page):
	template_name = Constants.templates_dir+"Confidence_empirical.html"
	form_model = models.Player
	form_fields = ['confidence_empirical']

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"]>= self.participant.vars["max_absence"] else False
		return {'inactive':inactive}

class Beliefs_after_NE(Page):
	template_name = Constants.templates_dir+"Beliefs_NE.html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	form_model = models.Player

	def get_form_fields(self):
		return ['normative_expectations{}'.format(i) for i in range(0, Constants.NE_options+1)]


	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds':Constants.num_rounds,
			'round_number':self.round_number,
			'other_players_per_group':Constants.players_per_group-1,
			**Constants.dict_instructions,
			}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.absent_normative = True
			for _ in range(Constants.NE_options+1):
				setattr(self.player,'normative_expectations{}'.format(_),0)


class Confidence_normative(Page):
	template_name = Constants.templates_dir+"Confidence_normative.html"
	form_model = models.Player
	form_fields = ['confidence_normative']

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"]>= self.participant.vars["max_absence"] else False
		return {'inactive':inactive}



class ResultsWaitPage1(WaitPage):
	template_name = Constants.templates_dir+'WaitNextRound1.html'

	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'other_players_per_group':Constants.players_per_group-1,
		}

	def after_all_players_arrive(self):
		self.group.group_other_contributions()
		self.group.group_empirical_expectations()
		self.group.group_normative_expectations()
		self.group.calc_disaster()
		self.group.set_payoffs()	

class Results(Page):
	template_name = Constants.templates_dir+"Results.html"

	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			'reduced_impact': (1 -self.group.impact)*100,
			'impact':self.group.impact*100,
			'all_tokens':self.player.public_tokens + self.player.private_tokens,
			'round_number':self.round_number,
			'contribution_inactive':self.participant.vars["contribution_inactive"],
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'other_players_per_group':Constants.players_per_group-1,
			**Constants.dict_instructions,
			'half_unconditional':self.player.unconditional_payoff/2,
			'ee_accuracy':self.player.ee_accuracy*100,
			'ne_accuracy':self.player.ne_accuracy*100,
			'int_payoff':float(self.player.payoff)
		}

	def before_next_page(self):
		self.player.cumulative_payoff()

class Final(Page):
	template_name = Constants.templates_dir+"Final.html"

	def is_displayed(self):
		return self.round_number == Constants.num_rounds
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False

		return {
			"inactive":inactive,
			"curr_url":"https://cambridge.ibsen-h2020.eu/InitializeParticipant/"+self.participant.code+"/"
			}

class Buying_social_information(Page):
	template_name = Constants.templates_dir+"Buying_social_information.html"
	form_model = models.Player
	form_fields = ['buying_contribution']

	def is_displayed(self):
		return self.round_number == Constants.num_rounds
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			}

class Risk_sensitivity(Page):
	template_name = Constants.templates_dir+"Risk_sensitivity.html"
	form_model = models.Player

	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	def get_form_fields(self):
	    return ['contribute_{}'.format(i) for i in range(0,110,10)]

	def vars_for_template(self):
		inactive = True if self.participant.vars['absence']>=self.participant.vars["max_absence"] else False
		return {
			'inactive':inactive,
			**Constants.dict_instructions}

	def before_next_page(self):
		self.player.save_participant_vars()


class About(Page):
	template_name = Constants.templates_dir+"About.html"
	form_model = models.Player
	form_fields = ['comments_1','comments_2','comments_3','comments_4']

	def is_displayed(self):
		return self.round_number == Constants.num_rounds

	def vars_for_template(self):
		inactive=True if self.participant.vars['absence'] >= self.participant.vars['max_absence'] else False
		return {
			'inactive':inactive}

	def before_next_page(self):
		self.player.save_participant_vars()

class Ready(Page):
	template_name = Constants.templates_dir+"Ready.html"

	def is_displayed(self):
		return self.round_number == 1

	def vars_for_template(self):
		inactive=True if self.participant.vars['absence'] >= self.participant.vars['max_absence'] else False
		return {
			'inactive':inactive}


page_sequence = [
	Welcome,
	Instructions_1,
	Control_1,
	Answers_1,
	Instructions_2,
	Control_2,
	Answers_2,
	Instructions_3,
	Control_3_1,
	Control_3_2,
	Answers_3,
	Ready,
	Contribute_uncond,
	Beliefs_after_EE,
	Confidence_empirical,
	Beliefs_after_PNB,
	Beliefs_after_NE,
	Confidence_normative,
	Buying_social_information,
	Risk_sensitivity,
#	About,
#	Final,
#	ResultsWaitPage1,
#	Results,
]	
