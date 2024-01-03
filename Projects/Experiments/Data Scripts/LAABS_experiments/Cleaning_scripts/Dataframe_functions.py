import numpy as np
import pandas as pd 
import os 

def create_dataframe_active(session):
	### read
	os.chdir("./"+session+"/cleaned_data")
	df_experiment = pd.read_csv("df_experiment.csv")
	df_players = pd.read_csv("df_players.csv")
	### select
	active = df_players[df_players["absent_contribution_non_linear"]<5]["code"]
	df_experiment_active = df_experiment.set_index("code").loc[active].sort_values("round_number")
	df_players_active = df_players[df_players["absent_contribution_non_linear"]<5].reset_index().drop("index",axis=1)
	### write
	df_experiment_active.to_csv("df_experiment_active.csv")
	df_players_active.to_csv("df_players_active.csv",index=False)
	
	
	
