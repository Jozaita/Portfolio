from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    BaseLink,
    Currency as c,
    currency_range,
)
import random as rd
import math

author = 'Juan Ozaita Corral'

doc = """
Plataforma para el experimento asociado al paper "The emergence of segregation: from observable markers to group specific norms"
"""


class Constants(BaseConstants):
    name_in_url = 'e05_ethnic_markers'
    players_per_group = 10
    num_rounds = 3 
    delta = 0.5
    e = 0.5

class Subsession(BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1:
            players = self.get_players()
            N = len(players)
            assignation = int(N/2)*['amarillo']+int(N/2)*['azul']
            for p in players:
                p.payoff = c(0)
                p.participant.vars['success'] = 0
                p.participant.vars['absence'] = 0
                p.participant.vars['marker'] = assignation.pop(
                    rd.randint(0, len(assignation)-1))


class Group(BaseGroup):
    def find_partners(self):
        players = self.get_players()
        markers = [p.participant.vars['marker'] for p in players]
        ids2 = [p.id_in_group for p in players]
        yellows = [
            p.id_in_group for p in players if p.participant.vars['marker'] == 'amarillo']
        blues = [
            p.id_in_group for p in players if p.participant.vars['marker'] == 'azul']
        ids = yellows+blues
        partners = []
        while ids != []:
            p = rd.choice(ids)
            ids.remove(p)
            ids = yellows + blues
            if markers[ids2.index(p)] == 'amarillo':
                yellows.remove(p)
                if (rd.uniform(0, 1) > Constants.e):
                    # Efeitos de tamaño finito
                    if len(yellows) > 0:
                        partner = rd.choice(yellows)
                        yellows.remove(partner)
                    else:
                        partner = rd.choice(yellows+blues)
                        if partner in yellows:
                            yellows.remove(partner)
                        if partner in blues:
                            blues.remove(partner)
                    partners.append([p, partner])
                else:
                    partner = rd.choice(yellows+blues)
                    partners.append([p, partner])
                    if partner in yellows:
                        yellows.remove(partner)
                    if partner in blues:
                        blues.remove(partner)
            elif markers[ids2.index(p)] == 'azul':
                blues.remove(p)
                if (rd.uniform(0, 1) > Constants.e):
                    if len(blues) > 0:
                        partner = rd.choice(blues)
                        blues.remove(partner)
                    else:
                        partner = rd.choice(yellows+blues)
                        if partner in yellows:
                            yellows.remove(partner)
                        if partner in blues:
                            blues.remove(partner)
                    partners.append([p, partner])
                else:
                    partner = rd.choice(yellows+blues)
                    partners.append([p, partner])
                    if partner in yellows:
                        yellows.remove(partner)
                    if partner in blues:
                        blues.remove(partner)
            ids = yellows+blues

        for i in range(len(partners)):
            players[ids2.index(partners[i][0])].couple_id = partners[i][1]
            players[ids2.index(partners[i][1])].couple_id = partners[i][0]
            players[ids2.index(partners[i][0])].marker_partner = markers[ids2.index(
                players[ids2.index(partners[i][0])].couple_id)]
            players[ids2.index(partners[i][1])].marker_partner = markers[ids2.index(
                players[ids2.index(partners[i][1])].couple_id)]

    def set_payoffs(self):
        players = self.get_players()
        ids2 = [p.id_in_group for p in players]
        for p in players:
            p.acción_partner = players[ids2.index(p.couple_id)].acción
            if p.acción == p.acción_partner:
                p.payoff += 1+Constants.delta
                p.participant.vars['success'] += 1
            else:
                p.payoff += 1
            p.participant.vars['global_payoff'] = sum(
                [q.payoff for q in p.in_all_rounds()])
            p.global_payoff = p.participant.vars['global_payoff']
            p.marker = p.participant.vars['marker']
            p.success = p.participant.vars['success']
            p.absence = p.participant.vars['absence']
           

    # def find_examples(self):
    #    players = self.get_players()
    #    for p in players:
    #        history = p.in_all_rounds()
    #        marker_history = [h.marker_partner for h in history]
    #        if "azul" and "amarillo" in marker_history:
    #            p.i_azul = marker_history.index("azul") + 1
    #            p.i_amarillo = marker_history.index("amarillo") + 1
    #        else:
    #            p.i_azul, p.i_amarillo = 0, 0


class Player(BasePlayer):
    couple_id = models.IntegerField()
    acción = models.PositiveIntegerField(
        choices=[
            [1, 'A'],
            [2, 'B'], ])
    acción_partner = models.PositiveIntegerField(
        choices=[
            [1, 'A'],
            [2, 'B'], ],
    )
    marker_partner = models.CharField()
    pay_1_val = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], verbose_name="",
        widget=widgets.RadioSelectHorizontal()
    )
    pay_2_val = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7], verbose_name="",
        widget=widgets.RadioSelectHorizontal()
    )

    bias = models.PositiveIntegerField(verbose_name="")
    bias_payoff = models.PositiveIntegerField(verbose_name="")
    #i_azul = models.IntegerField()
    #i_amarillo = models.IntegerField()
    ################
    # Creamos una serie de modelos para las participant.vars
    global_payoff = models.FloatField()
    success = models.PositiveIntegerField()
    absence = models.PositiveIntegerField()
    marker = models.CharField()
    def extra_payoff(self):
        delta = abs(563-self.bias)
        self.bias_payoff = 0
        if delta < 31:
            self.bias_payoff = math.ceil(10/31*(31-delta))
            self.payoff += self.bias_payoff
            self.participant.vars['global_payoff'] = sum(
                [q.payoff for q in self.in_all_rounds()])
            self.global_payoff = self.participant.vars['global_payoff']
            #self.payoff += 1
            # self.participant.vars['global_payoff'] = sum(
            #    [q.payoff for q in self.in_all_rounds()])
            #self.global_payoff = self.participant.vars['global_payoff']


class Link(BaseLink):
    pass
