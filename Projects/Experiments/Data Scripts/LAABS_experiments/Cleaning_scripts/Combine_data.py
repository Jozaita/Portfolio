import numpy as np 
import pandas as pd
import os
 
df_id_app1 = pd.read_csv('DNI_viejo.csv')
df_id_app2 = pd.read_csv('DNI_nuevo.csv')
df_data_exp = pd.read_csv(list(filter(lambda x: 'svotree' in x, os.listdir()))[0])
##Convert DNI to string
df_id_app1["DNI"] = df_id_app1["DNI"].astype(str)
df_id_app2["DNI"] = df_id_app2["DNI"].astype(str)
##Extract code from link
df_id_app1["participant.code"] = df_id_app1["Link"].apply(lambda x: x[-9:-1])
df_id_app2["participant.code"] = df_id_app2["Link"].apply(lambda x: x[-9:-1])
##Combine, merging on participant.code
col_int = ["participant.code","player.risk_lottery_payoff","player.lottery_choice","player.lottery_win","player.selectionYellow",
        "player.norm_compliance_payoff","player.slider_paid","player.self_paid","player.payoff_svo"]
df_data_exp_to_combine = df_data_exp.copy()[col_int]

df_combined = df_id_app1.merge(df_data_exp_to_combine,on="participant.code")
df_combined.drop(["Link","participant.code"],axis=1,inplace=True)
df_combined_final = df_id_app2.merge(df_combined,on="DNI")
df_combined_final.drop("Link",axis=1,inplace=True)
new_col = [col.split(".")[1] for col in list(df_combined_final.columns)[1:]]
new_col.insert(0,"DNI")
df_combined_final.fillna(0,inplace=True)
df_combined_final.columns = new_col
df_combined_final.to_csv("df_combined.csv",index=False)
