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
import datetime as dt

author = 'Juan Ozaita Corral'

doc = """
Plataforma para el experimento asociado al paper "The emergence of segregation: from observable markers to group specific norms"
"""


class Constants(BaseConstants):
    name_in_url = 'e1_ethnic_markers'
    players_per_group = 10
    num_rounds = 75
    max_absence = 4
    delta = 0.5
    e = 1

    timeout_sombreros = 22
    timeout_aspiraciones = 32
    timeout_resultados = 12
    timeout_instrucciones = 302
    timeout_bias = 32

    date_exp = "jueves, 24 de junio de 2021 a las 17:00"

class Subsession(BaseSubsession):
    #def before_session_starts(self):
    #    if self.round_number == 1:
    #        players = self.get_players()
    #        N = len(players)
    #        assignation = int(N/2)*['amarillo']+int(N/2)*['azul']
    #        for p in players:
    #            p.absence = 0
    #            p.success = 0
    #            p.payoff = c(0)
    #            p.global_payoff = c(0)
    #            p.participant.vars['marker'] = assignation.pop(
    #                rd.randint(0, len(assignation)-1))
    pass

class Group(BaseGroup):
    def assign_markers(self):
            players = self.get_players()
            N = len(players)
            assignation = int(N/2)*['amarillo']+int(N/2)*['azul']
            for p in players:
                if p.absence == None:
                    p.absence = 0
                p.success = 0
                p.payoff = c(0)
                p.global_payoff = c(0)
                p.participant.vars['marker'] = assignation.pop(
                    rd.randint(0, len(assignation)-1))

    def find_partners(self):
        players = self.get_players()
        for player in players:
            player.shape_sequence = rd.choice([1,2])
        ##Meto aquí o da shape sequence pra amosar a coordinación    
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
               p.payoff = 1
               if self.round_number == 1:
                    p.success = 1
                
               else: 
                    p.success = p.in_previous_rounds()[-1].success + 1
            else:
               p.payoff = -0.5
               if p.round_number > 1:
                   p.success = p.in_previous_rounds()[-1].success
            if p.round_number == 1:
                p.global_payoff = p.payoff
                if p.global_payoff < 0:
                     p.global_payoff = 0
            else:
                p.global_payoff = p.in_previous_rounds()[-1].global_payoff + p.payoff 
                if p.global_payoff <= 0:
                    p.global_payoff = 0
            p.marker = p.participant.vars['marker']
    
    def recall(self):
        players = self.get_players()
        for p in players:
            p.absence = p.in_previous_rounds()[-1].absence

class Player(BasePlayer):
    couple_id = models.IntegerField()
    acción = models.PositiveIntegerField()
    acción_partner = models.PositiveIntegerField()
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
    bias_payoff = models.CurrencyField(verbose_name="")
    success = models.PositiveIntegerField()
    absence = models.PositiveIntegerField()
    global_payoff = models.CurrencyField()
    marker = models.CharField()
    shape_sequence = models.PositiveIntegerField(verbose_name = "")
    #Shape sequence == 0 --> Circle, then triangle
    #Shape sequence == 1 --> Triangle, then circle
 
   
    def extra_payoff(self):
        delta = abs(563-self.bias)

        self.bias_payoff = 0
        if delta < 31:
            self.bias_payoff = math.ceil(10/31*(31-delta))
            self.payoff += self.bias_payoff
            self.global_payoff += self.bias_payoff
        self.participant.vars['absence'] = self.absence 
        self.participant.vars['global_payoff'] = self.global_payoff
        self.participant.vars['max_absence'] = Constants.max_absence

class Link(BaseLink):
    pass
