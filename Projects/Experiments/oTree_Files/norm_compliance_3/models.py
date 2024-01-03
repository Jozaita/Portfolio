from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    BaseLink,
    Currency as c, currency_range
)
from otree.db.models import BooleanField as m

author = 'Juan Ozaita'
doc = """
Compliance to a certain norm experiment.
"""


class Constants(BaseConstants):
    name_in_url = 'questions2'
    players_per_group = None
    num_rounds = 20


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Modelos para guardar las participant vars
    paypal = models.CharField(verbose_name="Cuenta de Paypal:")
    payoff_norm = models.FloatField()
    payoff_total = models.FloatField()
    selectionYellow = models.PositiveIntegerField(blank=True, default=None, choices=[
        [1, '']], widget=widgets.RadioSelect, verbose_name="")
    selectionBlue = models.PositiveIntegerField(blank=True, default=None, choices=[
        [1, '']], widget=widgets.RadioSelect, verbose_name="")

    def storePayments(self):
        self.participant.vars['payoffNormCompliance'] = sum([0.5 for p in self.in_all_rounds(
        ) if p.selectionYellow == 1]) + sum([1 for p in self.in_all_rounds() if p.selectionBlue == 1])
        self.payoff_norm = self.participant.vars['payoffNormCompliance']

    def total_payment(self):
        self.participant.vars['total_pay'] = self.participant.vars['global_payoff'] + \
            self.participant.vars['payoffNormCompliance']
        self.payoff_total = self.participant.vars['total_pay']


class Link(BaseLink):
    # class Link():
    pass
