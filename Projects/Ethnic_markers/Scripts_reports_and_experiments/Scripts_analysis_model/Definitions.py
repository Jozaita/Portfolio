#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:37:49 2020

@author: juan
"""
import networkx as nx
import random as rd
import numpy as np

list_strategies = ['a','b']
list_markers = ['yellow','blue']
pay_matrix = np.matrix([[1.5,1],[1,1.5]])
mean_asp, var_asp = 1, 0.1

def relu(x):
    if x<0: 0
    if x>0:x


class Agent():
        def __init__(self):
            self.action = list_strategies
            self.marker = rd.choice(list_markers)
            self.graf = nx.Graph()
            self.graf.add_nodes_from(list_strategies)
            self.info = []
            self.asp = rd.gauss(mean_asp,var_asp)

    
    
        def gen_stim(self,act_sub,act_obj):
            aspi = self.asp
            x = pay_matrix[act_sub,act_obj]-aspi
            diff_mat = abs(pay_matrix-aspi)
            den = diff_mat.max()
            stimulus = x/den
            return stimulus
        
        def update_network(self,stimulus,mark_obj,act_obj):
            grafica = self.graf
            if mark_obj not in grafica.nodes():
                grafica.add_node(mark_obj)
            if not(grafica.has_edge(act_obj,mark_obj)):
                grafica.add_edge(act_obj,mark_obj,strength = relu(stimulus))
            else:
                grafica[act_obj][mark_obj]['strength'] += relu(stimulus)
        
    