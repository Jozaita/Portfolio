import numpy as np
import pandas as pd
import random as rd
import networkx as nx

import torch
import torch_geometric.data as data
import torch_geometric.transforms as T
from torch_geometric.utils import negative_sampling,train_test_split_edges,to_dense_adj
from torch_geometric.loader import DataLoader
from sklearn import preprocessing
from torch_geometric.nn import Node2Vec
from sklearn.model_selection import train_test_split

device = "cpu"


def rearrange_values(df_edges, df_nodes):
    if df_edges["to"].nunique() > df_edges["from"].nunique():
        new_vect = np.arange(df_edges["to"].nunique())
        ###
        translation = dict(zip(list(df_edges.sort_values(by="to")["to"].unique()), new_vect))
    else:
        new_vect = np.arange(df_edges["from"].nunique())
        ###
        translation = dict(zip(list(df_edges.sort_values(by="from")["from"].unique()), new_vect))
    df_edges[["from", "to"]] = df_edges[["from", "to"]].replace(translation)
    df_nodes["ID"] = df_nodes["ID"].replace(translation)
    return df_edges, df_nodes


len_datasets = 13
datasets_nodes = [0]*len_datasets
datasets_edges = [0]*len_datasets
datasets_edges_train = [0]*len_datasets
datasets_edges_test = [0]*len_datasets
data_list = [0]*len_datasets
graficas = [0]*len_datasets
for i in range(0,len_datasets):
    datasets_nodes[i] = pd.read_csv(r"Coles/Nodes/Nodes_t"+str(i+1)+".csv",sep=",",encoding = 'unicode_escape')
    datasets_edges[i] = pd.read_csv(r"Coles/Edges/Edges_t"+str(i+1)+".csv",sep=",",encoding = 'unicode_escape')
    #datasets_edges[i][["from","to"]] = datasets_edges[i][["from","to"]].apply(lambda x:x-min(datasets_edges[i]["to"].min(),datasets_edges[i]["from"].min()))
    datasets_edges[i]["Escuela"] = i
    datasets_edges[i]["weight"] = datasets_edges[i]["weight"].apply(lambda x: np.sign(x)).replace({-1:0}).reset_index().drop("index",axis=1)
    datasets_edges[i],datasets_nodes[i] = rearrange_values(datasets_edges[i],datasets_nodes[i])
    datasets_edges[i]["class_classif"] = f_edges(datasets_nodes[i],datasets_edges[i])
    datasets_edges_train[i], datasets_edges_test[i] = train_test_split(datasets_edges[i], test_size=0.2)
    graficas[i] = nx.from_pandas_edgelist(datasets_edges_train[i],source="from",target="to",create_using=nx.DiGraph())
    data_list[i] = data.Data(edge_index = torch.tensor(datasets_edges_train[i][["from","to"]].to_numpy().T))

data_loader = DataLoader(data_list, batch_size=1)