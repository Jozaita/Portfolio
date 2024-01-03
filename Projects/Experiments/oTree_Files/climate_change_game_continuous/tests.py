from otree.api import Currency as c, currency_range
from . import views
from otree.api import Bot, SubmissionMustFail
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random


class PlayerBot(Bot):

	def play_round(self):
		yield Submission(views.Initialisation, timeout_happened=True, check_html=False)

		if self.subsession.round_number == 1:
			yield (views.Instructions)
			yield (views.Example)
			yield (views.Control, {'question_1': random.randint(0, 2), 'question_2': random.randint(0, 2), 'question_3': random.randint(0, 2), 'question_4': random.randint(0, 1), 'question_5': random.randint(0, 1)})
			yield (views.Answers)

		if self.subsession.round_number > 1 and self.player.inactive < self.session.config['inactive_threshold']:
			yield Submission(views.PreviousResults, timeout_happened=True, check_html=False)

		if self.player.inactive < self.session.config['inactive_threshold']:
			yield (views.Preparation)

			if self.player.belief_elicit_before == 1:
				yield (views.Beliefs_before_EE, {'empirical_expectations0': random.randint(0, Constants.endowment)})				
				if self.subsession.round_number in Constants.PNB_NE_rounds:
					yield (views.Beliefs_before_PNB, {'personal_normative_beliefs': random.randint(0, Constants.endowment)})
					yield (views.Beliefs_before_NE, {'normative_expectations0': random.randint(0, Constants.endowment)})
			
			if self.subsession.round_number not in Constants.uncond_cond_rounds:
				yield (views.Contribute_uncond, {'contribution': random.randint(0, Constants.endowment)})
				#yield Submission(views.Contribute_uncond, timeout_happened=True)
				#line above for testing. It makes players inactive. If you want to stop making them inactive then uncomment the line above it
			elif self.subsession.round_number in Constants.uncond_cond_rounds:
				yield (views.Contribute_uncond, {'contribution': random.randint(0, Constants.endowment)})
				#yield Submission(views.Contribute_uncond, timeout_happened=True)
				yield Submission(views.Contribute_cond, {'contribution_hh': random.randint(0, Constants.endowment), 'contribution_hl': random.randint(0, Constants.endowment), 'contribution_lh': random.randint(0, Constants.endowment), 'contribution_ll': random.randint(0, Constants.endowment)})

			if self.player.belief_elicit_before == 0:
				yield (views.Beliefs_after_EE, {'empirical_expectations0': random.randint(0, Constants.endowment)})
				if self.subsession.round_number in Constants.PNB_NE_rounds:
					yield (views.Beliefs_after_PNB, {'personal_normative_beliefs': random.randint(0, Constants.endowment)})
					yield (views.Beliefs_after_NE, {'normative_expectations0': random.randint(0, Constants.endowment)})

			yield Submission(views.AnotherInitialisation, timeout_happened=True, check_html=False)
			yield (views.Results)
			yield Submission(views.WaitNextRound, timeout_happened=True, check_html=False)

		
		elif self.player.inactive >= self.session.config['inactive_threshold']:
			yield Submission(views.Preparation, timeout_happened=True, check_html=False)
			
			if self.player.belief_elicit_before == 1:
				yield Submission(views.Beliefs_before_EE, timeout_happened=True, check_html=False)
				if self.subsession.round_number in Constants.PNB_NE_rounds:
					yield Submission(views.Beliefs_before_PNB, timeout_happened=True, check_html=False)
					yield Submission(views.Beliefs_before_NE, timeout_happened=True, check_html=False)
			
			if self.subsession.round_number not in Constants.uncond_cond_rounds:
				yield Submission(views.Contribute_uncond, timeout_happened=True, check_html=False)
			
			elif self.subsession.round_number in Constants.uncond_cond_rounds:
				yield Submission(views.Contribute_uncond, timeout_happened=True, check_html=False)
				yield Submission(views.Contribute_cond, timeout_happened=True, check_html=False)
		
			if self.player.belief_elicit_before == 0:
				yield Submission(views.Beliefs_after_EE, timeout_happened=True, check_html=False)

				if self.subsession.round_number in Constants.PNB_NE_rounds:
					yield Submission(views.Beliefs_after_PNB_NE, timeout_happened=True, check_html=False)			
	
			yield Submission(views.AnotherInitialisation, timeout_happened=True, check_html=False)
			yield Submission(views.Results, timeout_happened=True, check_html=False)
			yield Submission(views.WaitNextRound, timeout_happened=True, check_html=False)