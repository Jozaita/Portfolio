from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

import random

class PlayerBot(Bot):

	def play_round(self):
		yield (views.MyPage, {'choice_1': random.randint(0, 1), 'choice_2': random.randint(0, 1), 'choice_3': random.randint(0, 1), 'choice_4': random.randint(0, 1), 'choice_5': random.randint(0, 1), 'choice_6': random.randint(0, 1), 'choice_7': random.randint(0, 1), 'choice_8': random.randint(0, 1), 'choice_9': random.randint(0, 1), 'choice_10': random.randint(0, 1)})
