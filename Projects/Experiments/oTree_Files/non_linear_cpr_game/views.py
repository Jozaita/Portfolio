from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import datetime

class Pre_Experiment(Page):
	template_name = 'non_linear_cpr_game/Pre_Experiment_'+Constants.language+'.html'
	def is_displayed(self):
		return self.round_number == 1
class Welcome(Page):
	template_name = 'non_linear_cpr_game/Welcome_'+Constants.language+'.html'
	def is_displayed(self):
		return self.round_number == 1
 
	def before_next_page(self):
		self.player.request_variables()
		if self.timeout_happened:
			self.participant.vars["absence"] += self.participant.vars["max_absence"]

class Initialisation(Page):
	timeout_seconds = 1

	def before_next_page(self): # this function is used to bring participants values from previous apps
		self.player.creating_score()
class ShuffleWaitPage(WaitPage):
	template_name = 'non_linear_cpr_game/ShuffleWaitPage_'+Constants.language+'.html'
	wait_for_all_groups = True
	def after_all_players_arrive(self):
		sorted_players = sorted(
			self.subsession.get_players(),
			key=lambda player: player.participant.vars['score']
		)
		group_matrix = []
		ppg = Constants.players_per_group
		for i in range(0, len(sorted_players), ppg):
			group_matrix.append(sorted_players[i:i+ppg])
		self.subsession.set_group_matrix(group_matrix)
		for p in self.subsession.get_players():
			p.participant.vars["initial_time"] = datetime.datetime.now()
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return{"inactive":inactive,
		"absence":self.participant.vars["absence"],
		"max_absence":self.participant.vars["max_absence"]}

class Instructions(Page):

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = Constants.timeout_instructions
		else:
			self.timeout_seconds = 1
	template_name = "non_linear_cpr_game/Instructions_"+Constants.language+".html"
	def is_displayed(self):
		return self.round_number == 1
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': Constants.num_rounds
		}
class Example(Page):

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = Constants.timeout_example
		else:
			self.timeout_seconds = 1
	template_name = "non_linear_cpr_game/Example_"+Constants.language+".html"
	def is_displayed(self):
		return self.round_number == 1

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False 
		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'no_spending': Constants.endowment*0,
			'one_quarter_spending': Constants.endowment*1/4,
			'half_spending': Constants.endowment*1/2,
			'three_quarters_spending': Constants.endowment*3/4,
			'full_spending': Constants.endowment,
			'sum1': (Constants.players_per_group-1) * Constants.endowment*1/2,
			'sum2': Constants.players_per_group * Constants.endowment*3/4,
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
            'rounds': Constants.num_rounds
		}
	#def before_next_page(self):
	#	if self.timeout_happened:
	#		self.participant.vars["absence"] += 1
class Control(Page):
	form_model = models.Player
	form_fields = ['question_1_1', 'question_1_2', 'question_2_1', 'question_2_2', 'question_3_1', 'question_3_2', 'question_4_1', 'question_4_2', 'question_5']
	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = Constants.timeout_control
		else:
			self.timeout_seconds = 1
	template_name = "non_linear_cpr_game/Control_"+Constants.language+".html"
	def is_displayed(self):
		return self.round_number == 1
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
            'rounds': Constants.num_rounds
		}

	def before_next_page(self):
		self.player.control_calc()
		#if self.timeout_happened:
		#	self.participant.vars["absence"] += 1
class Answers(Page):

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = Constants.timeout_control
		else:
			self.timeout_seconds = 1
	template_name = "non_linear_cpr_game/Answers_"+Constants.language+".html"

	def is_displayed(self):
		return self.round_number == 1
	def vars_for_template(self):
		if self.player.question_1_1 == 0:
			question_1_1 = "25"
		elif self.player.question_1_1 == 1:
			question_1_1 = "15"
		elif self.player.question_1_1 == 2:
			question_1_1 = "5"

		if self.player.question_1_2 == 0:
			question_1_2 = "72.9"
		elif self.player.question_1_2 == 1:
			question_1_2 = "52.2"
		elif self.player.question_1_2 == 2:
			question_1_2 = "31.8"

		if self.player.question_2_1 == 0:
			question_2_1 = "25"
		elif self.player.question_2_1 == 1:
			question_2_1 = "15"
		elif self.player.question_2_1 == 2:
			question_2_1 = "5"

		if self.player.question_2_2 == 0:
			question_2_2 = "72.9"
		elif self.player.question_2_2 == 1:
			question_2_2 = "52.2"
		elif self.player.question_2_2 == 2:
			question_2_2 = "10.7"

		if self.player.question_3_1 == 0:
			question_3_1 = "22"
		elif self.player.question_3_1 == 1:
			question_3_1 = "5"
		elif self.player.question_3_1 == 2:
			question_3_1 = "2"

		if self.player.question_3_2 == 0:
			question_3_2 = "6.3"
		elif self.player.question_3_2 == 1:
			question_3_2 = "354.9"
		elif self.player.question_3_2 == 2:
			question_3_2 = "14"

		if self.player.question_4_1 == 0:
			question_4_1 = "2"
		elif self.player.question_4_1 == 1:
			question_4_1 = "6"
		elif self.player.question_4_1 == 2:
			question_4_1 = "15"

		if self.player.question_4_2 == 0:
			question_4_2 = "6.3"
		elif self.player.question_4_2 == 1:
			question_4_2 = "150.4"
		elif self.player.question_4_2 == 2:
			question_4_2 = "14"

		if self.player.question_5 == 0:
			question_5 = "Nada"
		elif self.player.question_5 == 1:
			question_5 = "Seré excluído"
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False

		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'q_1_1': question_1_1,
			'q_1_2': question_1_2,
			'q_2_1': question_2_1,
			'q_2_2': question_2_2,
			'q_3_1': question_3_1,
			'q_3_2': question_3_2,
			'q_4_1': question_4_1,
			'q_4_2': question_4_2,
			'q_5': question_5,
			'a11': 25,
			'a12': 72.9,
			'a21': 25,
			'a22': 10.7,
			'a31': 2,
			'a32': 354.9,
			'a41': 2,
			'a42': 6.3,
			'a5': "Seré excluído del experimento",
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}
	#def before_next_page(self):
	#	if self.timeout_happened:
	#		self.participant.vars["absence"] += 1
class Wait_Start(WaitPage):	
	template_name = 'non_linear_cpr_game/Wait_Start_'+Constants.language+'.html'
	wait_for_all_groups = True
	def is_displayed(self):
		return self.round_number == 1
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False

		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}


##################TIMEOUT_CHANGES_FOR_FIRST_ROUNDS##################


class Preparation_first_rounds(Page):
	template_name = "non_linear_cpr_game/Preparation_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"] +Constants.timeout_first_rounds
		else:
			self.timeout_seconds = 1


	def is_displayed(self):
		return self.round_number <= 5

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'treatment':Constants.treatment,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'days_completed': (self.round_number + 1)/2,
			'days_total': (Constants.num_rounds + 2)/2,
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': Constants.num_rounds
			}
			
	def before_next_page(self):
		self.player.payment_rounds()
		#if self.timeout_happened:
		#	self.participant.vars["absence"] += 1



class Beliefs_before_PNB_first_rounds(Page):

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"] + Constants.timeout_first_rounds
		else:
			self.timeout_seconds = 1

	form_model = models.Player
	form_fields = ['personal_normative_beliefs']
	#timeout_seconds = Constants.timeout_beliefs_pnb + Constants.timeout_first_rounds
	def is_displayed(self):
		return self.round_number <= 5
	template_name = "non_linear_cpr_game/Beliefs_before_PNB_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.inactive_pnb()
			self.player.absent_pnb = True

class Beliefs_before_EE_first_rounds(Page):

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"] + Constants.timeout_first_rounds
		else:
			self.timeout_seconds = 1

	form_model = models.Player
	#timeout_seconds = Constants.timeout_beliefs_ee + Constants.timeout_first_rounds
	def is_displayed(self):
		return self.round_number <= 5
	template_name = "non_linear_cpr_game/Beliefs_before_EE_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	def get_form_fields(self):
		return ['empirical_expectations{}'.format(i) for i in range(0, Constants.players_per_group-1)]
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'max_ee_earning': Constants.belief_correct_pay * (Constants.players_per_group-1),
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.absent_empirical = True
			self.player.empirical_expectations0 = 0
			self.player.empirical_expectations1 = 0
			self.player.empirical_expectations2 = 0
			self.player.empirical_expectations3 = 0
			self.player.empirical_expectations4 = 0
		

	def error_message(self, values):
		if (Constants.players_per_group-1) == 2:
			if values["empirical_expectations0"] < values["empirical_expectations1"]:
				return "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

		if (Constants.players_per_group-1) == 3:
			if values["empirical_expectations0"] < values["empirical_expectations1"] or values["empirical_expectations0"] < values["empirical_expectations2"] or values["empirical_expectations1"] < values["empirical_expectations2"]:
				return "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

		if (Constants.players_per_group-1) == 4:
			if values["empirical_expectations0"] < values["empirical_expectations1"] or values["empirical_expectations0"] < values["empirical_expectations2"] or values["empirical_expectations0"] < values["empirical_expectations3"] or values["empirical_expectations1"] < values["empirical_expectations2"]	or values["empirical_expectations1"] < values["empirical_expectations3"] or values["empirical_expectations2"] < values["empirical_expectations3"]:
				return "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"
			
		if (Constants.players_per_group-1) == 5:
			if values["empirical_expectations0"] < values["empirical_expectations1"] or values["empirical_expectations0"] < values["empirical_expectations2"] or values["empirical_expectations0"] < values["empirical_expectations3"] or values["empirical_expectations0"] < values["empirical_expectations4"] or values["empirical_expectations1"] < values["empirical_expectations2"] or values["empirical_expectations1"] < values["empirical_expectations3"] or values["empirical_expectations1"] < values["empirical_expectations4"] or values["empirical_expectations2"] < values["empirical_expectations3"] or values["empirical_expectations2"] < values["empirical_expectations4"] or values["empirical_expectations3"] < values["empirical_expectations4"]:
				return "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

class Beliefs_before_NE_first_rounds(Page):


	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"] + Constants.timeout_first_rounds
		else:
			self.timeout_seconds = 1

	form_model = models.Player
	#timeout_seconds = Constants.timeout_beliefs_ne + Constants.timeout_first_rounds
	def is_displayed(self):
		return self.round_number <= 5
	template_name = "non_linear_cpr_game/Beliefs_before_NE_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	def get_form_fields(self):
		return ['normative_expectations{}'.format(i) for i in range(0, Constants.players_per_group-1)]
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
                        'absence':self.participant.vars["absence"],
                        'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'max_ne_earning': Constants.belief_correct_pay * (Constants.players_per_group-1),
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.absent_normative = True
			self.player.normative_expectations0 = 0
			self.player.normative_expectations1 = 0
			self.player.normative_expectations2 = 0
			self.player.normative_expectations3 = 0
			self.player.normative_expectations4 = 0
		

	def error_message(self, values):
		if (Constants.players_per_group-1) == 2:
			if values["normative_expectations0"] < values["normative_expectations1"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

		if (Constants.players_per_group-1) == 3:
			if values["normative_expectations0"] < values["normative_expectations1"] or values["normative_expectations0"] < values["normative_expectations2"] or values["normative_expectations1"] < values["normative_expectations2"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

		if (Constants.players_per_group-1) == 4:
			if values["normative_expectations0"] < values["normative_expectations1"] or values["normative_expectations0"] < values["normative_expectations2"] or values["normative_expectations0"] < values["normative_expectations3"] or values["normative_expectations1"] < values["normative_expectations2"]	or values["normative_expectations1"] < values["normative_expectations3"] or values["normative_expectations2"] < values["normative_expectations3"]:
				return "Please ensure that your inputs are orderer from high to low such that the highest number is in the top row and the lowest in the bottom"
			
		if (Constants.players_per_group-1) == 5:
			if values["normative_expectations0"] < values["normative_expectations1"] or values["normative_expectations0"] < values["normative_expectations2"] or values["normative_expectations0"] < values["normative_expectations3"] or values["normative_expectations0"] < values["normative_expectations4"] or values["normative_expectations1"] < values["normative_expectations2"] or values["normative_expectations1"] < values["normative_expectations3"] or values["normative_expectations1"] < values["normative_expectations4"] or values["normative_expectations2"] < values["normative_expectations3"] or values["normative_expectations2"] < values["normative_expectations4"] or values["normative_expectations3"] < values["normative_expectations4"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

class Contribute_uncond_first_rounds(Page):
	template_name = "non_linear_cpr_game/Contribute_uncond_"+Constants.language+".html"

	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"] + Constants.timeout_first_rounds
		else:
			self.timeout_seconds = 1
	form_model = models.Player
	form_fields = ['contribution']
	#timeout_seconds = Constants.timeout_contribute_uncond + Constants.timeout_first_rounds
	def is_displayed(self):
		return (self.round_number <= 5) 
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
                        'absence':self.participant.vars["absence"],
                        'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number,
			'par_a': Constants.p_a,
			'par_b': Constants.p_b,
		}

	def before_next_page(self):
		if self.timeout_happened:
			self.participant.vars["absence"] += 1
			self.player.inactive_contribution()
			self.player.absent_contribution = True

class ResultsWaitPage1_first_rounds(WaitPage):
	template_name = 'non_linear_cpr_game/WaitNextRound1_'+Constants.language+'.html'

	def is_displayed(self):
		return self.round_number <= 5
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False

		return {
			"inactive":inactive,
                        'absence':self.participant.vars["absence"],
                        'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}

	def after_all_players_arrive(self):
		self.group.group_other_contributions()
		self.group.group_empirical_expectations()
		self.group.group_normative_expectations()
		self.group.set_payoffs()

class Results_first_rounds(Page):
	template_name = "non_linear_cpr_game/Results_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = Constants.timeout_results+Constants.timeout_first_rounds
		else:
			self.timeout_seconds = 1

	def is_displayed(self):
		return self.round_number <= 5
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'round_number':self.round_number,
			'contribution_inactive':self.participant.vars["contribution_inactive"],
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'unconditional_payoff':self.player.unconditional_payoff,
			'display_payoff': self.player.unconditional_payoff,
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
		}

	def before_next_page(self):
		self.player.cumulative_payoff()
		#if self.timeout_happened:
		#	self.participant.vars["absence"] +=1


####################################################################

class Preparation(Page):
	template_name = "non_linear_cpr_game/Preparation_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"]
		else:
			self.timeout_seconds = 1

	def is_displayed(self):
		return self.round_number > 5

	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'treatment':Constants.treatment,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'days_completed': (self.round_number + 1)/2,
			'days_total': (Constants.num_rounds + 2)/2,
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': Constants.num_rounds
			}
			
	def before_next_page(self):
		self.player.payment_rounds()
		#if self.timeout_happened:
		#	self.participant.vars["absence"] += 1

                      

class Beliefs_before_PNB(Page):
	form_model = models.Player
	form_fields = ['personal_normative_beliefs']

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"]
		else:
			self.timeout_seconds = 1
	def is_displayed(self):
		return self.round_number >5
	template_name = "non_linear_cpr_game/Beliefs_before_PNB_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.inactive_pnb()
			self.player.absent_pnb = True

class Beliefs_before_EE(Page):
	form_model = models.Player

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"]
		else:
			self.timeout_seconds = 1
	def is_displayed(self):
		return self.round_number > 5
	template_name = "non_linear_cpr_game/Beliefs_before_EE_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	def get_form_fields(self):
		return ['empirical_expectations{}'.format(i) for i in range(0, Constants.players_per_group-1)]
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'max_ee_earning': Constants.belief_correct_pay * (Constants.players_per_group-1),
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.absent_empirical = True
			self.player.empirical_expectations0 = 0
			self.player.empirical_expectations1 = 0
			self.player.empirical_expectations2 = 0
			self.player.empirical_expectations3 = 0
			self.player.empirical_expectations4 = 0

	def error_message(self, values):
		if (Constants.players_per_group-1) == 2:
			if values["empirical_expectations0"] < values["empirical_expectations1"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

		if (Constants.players_per_group-1) == 3:
			if values["empirical_expectations0"] < values["empirical_expectations1"] or values["empirical_expectations0"] < values["empirical_expectations2"] or values["empirical_expectations1"] < values["empirical_expectations2"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

		if (Constants.players_per_group-1) == 4:
			if values["empirical_expectations0"] < values["empirical_expectations1"] or values["empirical_expectations0"] < values["empirical_expectations2"] or values["empirical_expectations0"] < values["empirical_expectations3"] or values["empirical_expectations1"] < values["empirical_expectations2"]	or values["empirical_expectations1"] < values["empirical_expectations3"] or values["empirical_expectations2"] < values["empirical_expectations3"]:
				return   "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"
 
			
		if (Constants.players_per_group-1) == 5:
			if values["empirical_expectations0"] < values["empirical_expectations1"] or values["empirical_expectations0"] < values["empirical_expectations2"] or values["empirical_expectations0"] < values["empirical_expectations3"] or values["empirical_expectations0"] < values["empirical_expectations4"] or values["empirical_expectations1"] < values["empirical_expectations2"] or values["empirical_expectations1"] < values["empirical_expectations3"] or values["empirical_expectations1"] < values["empirical_expectations4"] or values["empirical_expectations2"] < values["empirical_expectations3"] or values["empirical_expectations2"] < values["empirical_expectations4"] or values["empirical_expectations3"] < values["empirical_expectations4"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"


class Beliefs_before_NE(Page):
	form_model = models.Player

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"]
		else:
			self.timeout_seconds = 1
	def is_displayed(self):
		return self.round_number > 5
	template_name = "non_linear_cpr_game/Beliefs_before_NE_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"
	def get_form_fields(self):
		return ['normative_expectations{}'.format(i) for i in range(0, Constants.players_per_group-1)]
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
                        'absence':self.participant.vars["absence"],
                        'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'max_ne_earning': Constants.belief_correct_pay * (Constants.players_per_group-1),
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.absent_normative = True
			self.player.normative_expectations0 = 0
			self.player.normative_expectations1 = 0
			self.player.normative_expectations2 = 0
			self.player.normative_expectations3 = 0
			self.player.normative_expectations4 = 0

	def error_message(self, values):
		if (Constants.players_per_group-1) == 2:
			if values["normative_expectations0"] < values["normative_expectations1"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"


		if (Constants.players_per_group-1) == 3:
			if values["normative_expectations0"] < values["normative_expectations1"] or values["normative_expectations0"] < values["normative_expectations2"] or values["normative_expectations1"] < values["normative_expectations2"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"


		if (Constants.players_per_group-1) == 4:
			if values["normative_expectations0"] < values["normative_expectations1"] or values["normative_expectations0"] < values["normative_expectations2"] or values["normative_expectations0"] < values["normative_expectations3"] or values["normative_expectations1"] < values["normative_expectations2"]	or values["normative_expectations1"] < values["normative_expectations3"] or values["normative_expectations2"] < values["normative_expectations3"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"

			
		if (Constants.players_per_group-1) == 5:
			if values["normative_expectations0"] < values["normative_expectations1"] or values["normative_expectations0"] < values["normative_expectations2"] or values["normative_expectations0"] < values["normative_expectations3"] or values["normative_expectations0"] < values["normative_expectations4"] or values["normative_expectations1"] < values["normative_expectations2"] or values["normative_expectations1"] < values["normative_expectations3"] or values["normative_expectations1"] < values["normative_expectations4"] or values["normative_expectations2"] < values["normative_expectations3"] or values["normative_expectations2"] < values["normative_expectations4"] or values["normative_expectations3"] < values["normative_expectations4"]:
				return  "Por favor, asegúrese de que introduce valores ordenados de mayor a menor, de manera que el valor más alto aparezca arriba y el más pequeño abajo"


class Contribute_uncond(Page):
	template_name = "non_linear_cpr_game/Contribute_uncond_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"

	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"]
		else:
			self.timeout_seconds = 1
	form_model = models.Player
	form_fields = ['contribution']
	#timeout_seconds = Constants.timeout_contribute_uncond
	def is_displayed(self):
		return (self.round_number > 5)
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
                        'absence':self.participant.vars["absence"],
                        'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number,
			'par_a': Constants.p_a,
			'par_b': Constants.p_b,
		}

	def before_next_page(self):
		if self.timeout_happened:
			self.participant.vars["absence"] += 1
			self.player.inactive_contribution()
			self.player.absent_contribution = True
class ResultsWaitPage1(WaitPage):
	template_name = 'non_linear_cpr_game/WaitNextRound1_'+Constants.language+'.html'
	def is_displayed(self):
		return self.round_number > 5
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False

		return {
			"inactive":inactive,
                        'absence':self.participant.vars["absence"],
                        'max_absence':self.participant.vars["max_absence"],
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
			'rounds': self.round_number
		}

	def after_all_players_arrive(self):
		self.group.group_other_contributions()
		self.group.group_empirical_expectations()
		self.group.group_normative_expectations()
		self.group.set_payoffs()

class Results(Page):


	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = Constants.timeout_results
		else:
			self.timeout_seconds = 1

	template_name = "non_linear_cpr_game/Results_"+Constants.language+".html"
	timer_text = "Tiempo para completar todas las decisiones de la ronda:"

	def is_displayed(self):
		return self.round_number > 5
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'round_number':self.round_number,
			'contribution_inactive':self.participant.vars["contribution_inactive"],
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'unconditional_payoff':self.player.unconditional_payoff,
			'display_payoff': self.player.unconditional_payoff,
			'inactive_threshold': self.session.config['inactive_threshold'],
			'email': self.session.config['email'],
			'num_subjects_win': self.session.config['num_subjects_win'],
			'win_multiplier': self.session.config['win_multiplier'],
		}

	def before_next_page(self):
		self.player.cumulative_payoff()
		#if self.timeout_happened:
		#	self.participant.vars["absence"] +=1

########Extra warning message #########
class Warning_message(Page):
	def is_displayed(self):
		return Constants.warning_message == 1 
	def set_extra_attributes(self):
		if self.participant.vars["absence"] < self.participant.vars["max_absence"]:
			self.timeout_seconds = -(datetime.datetime.now()-self.participant.vars["initial_time"]).total_seconds() + self.session.config["seconds_per_round"]
		else:
			self.timeout_seconds = 1

	template_name = "non_linear_cpr_game/Warning_message_"+Constants.language+".html"
	def is_displayed(self):
		return Constants.warning_message == 1
	def vars_for_template(self):
		inactive = True if self.participant.vars["absence"] >= self.participant.vars["max_absence"] else False
		return {
			"inactive":inactive,
			'absence':self.participant.vars["absence"],
			'max_absence':self.participant.vars["max_absence"],
			'rounds': Constants.num_rounds
		}
###########

page_sequence = [
	Pre_Experiment,
	Welcome,
	Initialisation,
	Instructions,
	Example,
	Control,
	Answers,
	Wait_Start,
	ShuffleWaitPage,
	Preparation_first_rounds,
	Warning_message,
	Beliefs_before_PNB_first_rounds,
	Beliefs_before_EE_first_rounds,
	Beliefs_before_NE_first_rounds,
	Contribute_uncond_first_rounds,
	ResultsWaitPage1_first_rounds,
	Results_first_rounds,
	Preparation,
	Beliefs_before_PNB,
	Beliefs_before_EE,
	Beliefs_before_NE,
	Contribute_uncond,
	ResultsWaitPage1,
	Results
]
