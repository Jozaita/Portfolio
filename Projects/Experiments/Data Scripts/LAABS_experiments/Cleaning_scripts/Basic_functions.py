import numpy as np
import pandas as pd 
import os 
from functools import reduce



def pre_inscription_day_2(session):
	"""Create inscription and save variables for the first day to be used in the second one"""
	### Go to session/data_apps and grab svotree file
	os.chdir('./'+session+'/data_apps')
	sv_file = pd.read_csv(list(filter(lambda x: "svotree" in x, os.listdir()))[0])
	### Go up and grab inscription from day 1
	os.chdir('..')
	new_links = pd.read_csv("ID_links.csv")
	inscription = pd.read_csv("Inscription_1.csv")
	### Get the code from the participants that have norm_compliance_payoff > 0 
	active_players = sv_file[sv_file['player.norm_compliance_payoff'] > 0]["participant.code"].values
	print(active_players)
	### Create code column so we can select based on it 
	inscription["participant.code"] = inscription["Link"].apply(lambda x: x[-9:-1])
	### Set it as index and .loc the codes of active players
	final_df = inscription.set_index("participant.code").loc[active_players].reset_index().drop("participant.code",axis=1).iloc[:,:6]
	final_df = final_df.merge(new_links,on='ID Number')

	### Save the result
	if "Inscription_2.csv" not in os.listdir():
		final_df.to_csv("Inscription_2.csv")
	
	### Create the temporal dataframe for variables of the first day 
	col_int = ["participant.code","player.risk_lottery_payoff","player.lottery_choice","player.lottery_win","player.selectionYellow",
        "player.norm_compliance_payoff","player.slider_paid","player.self_paid","player.payoff_svo"]
	df_temp = sv_file.copy()[col_int]
	col_int = [col.split(".")[1] for col in col_int if ('participant.code' not in col)]
	col_int.insert(0,'participant.code')
	df_temp.columns = col_int 
	### Recreate the old Id numbers 
	df_temp  = df_temp.merge(inscription[['ID Number','participant.code']],on='participant.code').drop('participant.code',axis=1)
	
	df_temp = df_temp.merge(new_links,on='ID Number')
	df_temp['code'] = df_temp["Link"].apply(lambda x: x[-9:-1])
	df_temp.drop('Link',axis=1,inplace=True)

	df_temp.to_csv('df_combined.csv')


def create_dataframe_player(session):
	### Change directory to the session
	os.chdir('./'+session+'/data_apps')
	### Create dict_data with all the raw information with all the apps
	apps = ["big_five","risk_lottery","norm_compliance","questionnaire","svotree","non_linear","payment"]
	dict_data = {}
	for app in apps: 
	    dict_data[app] = pd.read_csv(list(filter(lambda x: app in x, os.listdir()))[0])
	    ### The main information is included, except the questions from non_linear_cpr in the final page of every experiment
	    num_players = int(dict_data[app]["participant.id_in_session"].max())
	    ### Extra code to calculate the number of absences
	    if (app == "non_linear"):
	    	col_absence = [col for col in dict_data[app].columns if ("absent" in col) or ('participant.code' in col)]
	    	absence = dict_data[app][col_absence]
	    	questions = dict_data[app][[col for col in dict_data["non_linear"].columns if ("question" in col) or ("correct" in col) or ("participant.code" in col) ]][:num_players]
	    	absence.columns = [col+"_"+app  if "participant.code" not in col else col for col in absence.columns]
	    	questions.columns = [col+"_"+app  if "participant.code" not in col else col for col in questions.columns]
	    dict_data[app] =dict_data[app].iloc[-num_players:]
	### Save variables that contain NaNs 
	special_columns = dict_data["payment"][["participant.code","player.paypal","player.comments"]]
	special_columns.columns =  [col+"_payment"  if "participant.code" not in col else col for col in special_columns.columns]
	special_columns = pd.merge(special_columns,absence.groupby("participant.code").count().reset_index(),on="participant.code")
	special_columns = pd.merge(special_columns,questions,on="participant.code")
	special_columns.rename(columns={"participant.code":"code"},inplace=True)
	### Drop NaNs
	for app in apps: 
	    dict_data[app] = dict_data[app].dropna(axis=1)
	    dict_data[app].columns = [col+"_"+app  if "participant.code" not in col else col for col in dict_data[app].columns]
	### Create df from ids in order to translate the data of two participant codes
	os.chdir('..')
	df_id = []
	for file in list(filter(lambda x: 'Inscription' in x, os.listdir()))[:2]:
	    df = pd.read_csv(file)
	    df["participant.code"] = df["Link"].apply(lambda x:x.split("/")[-2])
	    df_id.append(df[["ID Number","First name","Last name","participant.code"]])
	df_inactive_first_day = df_id[0].drop("participant.code",axis=1).merge(df_id[1].drop("participant.code",axis=1), indicator=True, how='outer').loc[lambda df:df['_merge'] == 'right_only'].drop("_merge",axis=1)
	df_translate = df_id[1].merge(df_id[0],on="ID Number",suffixes=(None,"_x"))[["ID Number","First name","Last name","participant.code","participant.code_x"]]
	df_translate.columns = ["ID Number","First name","Last name","code_app_1","code_app_2"]
	###Dictionary of translation between the codes of two apps
	dict_translate=dict(zip(list(df_translate["code_app_1"]),list(df_translate["code_app_2"])))
	
	
	
	###Merge the dataframes for all the apps, cleaning the columns that do not sustain information
	apps_1 = apps[:5]
	apps_2 = apps[5:]
	data_frames = [dict_data[app] for app in apps_1]
	df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['participant.code'],
		                                    how='outer'), data_frames)
	df_merged.rename(columns={"participant.code":"code","player.payoff_svo_svotree":"player.svo_payoff_svotree"},inplace=True)
	keywords = ["participant","session","timeout","player.payoff","payoff_x","payoff_y","id_in_group"]
	for keyword in keywords: 
	    df_merged.drop([col for col in df_merged.columns if keyword in col],axis=1,inplace=True)
	df_merged["code"] = df_merged["code"].map(dict_translate)
	data_frames = [dict_data[app] for app in apps_2]
	df_merged_2 = pd.merge(dict_data["non_linear"],dict_data["payment"],on="participant.code")
	df_merged_2.rename(columns={"participant.code":"code"},inplace=True)
	keywords = ["participant","session","timeout","payoff_x","payoff_y","player.payoff","id_in_group","win_week","contribution","expectations","normative","earnings","unconditional","correct_answers"]
	for keyword in keywords: 
	    df_merged_2.drop([col for col in df_merged_2.columns if keyword in col],axis=1,inplace=True)
	
	### We have df_merged_1 and df_merged_2, now we create an entire one and include special columns. Then compute absent_contribution and global_payoff
	df_players = pd.merge(df_merged,df_merged_2,on="code")
	df_players = pd.merge(df_players,special_columns,on="code")
	df_players.fillna(" ",inplace=True)
	df_players.columns = [col.split(".")[1] if "." in col else col for col in df_players.columns]
	df_players["global_payoff"] = df_players.apply(lambda x:x.non_linear_payoff_payment+x.svo_payoff_svotree+x.norm_compliance_payoff_svotree+x.risk_lottery_payoff_svotree,axis=1)
	df_players.loc[df_players.winner_payment == 1, 'global_payoff'] = 3000
	df_players["global_payoff_euros"] = df_players.apply(lambda x:round(x.global_payoff/30 + 2),axis=1)
	df_players.loc[df_players.absent_contribution_non_linear > 4, ['global_payoff','global_payoff_euros']] = 0

	### Create payment file
	with open('pagos.txt', 'w') as f:
    		for row in df_players.loc[df_players["absent_contribution_non_linear"]<5][["paypal_payment","global_payoff_euros"]].iterrows():
        		f.write("{}\t{}\tEUR\n".format(row[1]["paypal_payment"], row[1]["global_payoff_euros"]))
	### Create inactivity file 
	#### select in df_players
	inactive = df_players.loc[df_players["absent_contribution_non_linear"]>=5]["code"]
	with open('inactive.txt', 'w') as f:
		f.write('Inactive list (ID numbers):\n')
		for row in df_inactive_first_day.iterrows():
			f.write("{}, {} {}\n".format(row[1]["ID Number"],row[1]["First name"],row[1]["Last name"]))
		for row in df_translate.set_index("code_app_2").loc[inactive].iterrows():
			f.write("{}, {} {}\n".format(row[1]["ID Number"],row[1]["First name"],row[1]["Last name"]))
	
	
	if 'cleaned_data' not in os.listdir():
		os.mkdir('cleaned_data')
	df_players.to_csv("cleaned_data/df_players.csv",index=False)
	

def create_dataframe_experiment(session):
	### Change directory to the session
	os.chdir('./'+session+'/data_apps')
	app = "non_linear"
	df_exp = pd.read_csv(list(filter(lambda x: app in x, os.listdir()))[0])
	col_absent = [col for col in df_exp.columns if 'absent' in col]
	df_exp[col_absent] = df_exp[col_absent].fillna(value=0)
	df_exp.dropna(axis=1,inplace=True)
	df_exp_save = df_exp[[col for col in df_exp.columns if ("participant.code" in col) or ("player" in col) or ("subsession.round_number" in col)] or ('absent' in col)].drop(["player.payoff","player.correct_answers"],axis=1)
	df_exp_save.columns = [col.split(".")[1] for col in df_exp_save.columns]
		### Some numbers are not correctly stored
	cols_trouble = ['common_account_earnings','unconditional_payoff']
	for col in cols_trouble:
		df_exp_save[col] = df_exp_save[col].apply(lambda x: round(x,2))
	os.chdir('..')
	if 'cleaned_data' not in os.listdir():
		os.mkdir('cleaned_data')
	df_exp_save.to_csv("cleaned_data/df_experiment.csv",index=False)


def create_global_dataframe(treatment):
	if treatment == "0": 
		sessions = ["26_27_4","5_6_5_11","5_6_5_19","16_17_5_10"]
	elif treatment == "1":
		sessions = ["9_10_5_11","9_10_5_19","16_17_5_16","23_24_5_16"]
	df_player_global = pd.DataFrame()
	df_experiment_global = pd.DataFrame()
	base_dir = os.getcwd()
	for session in sessions:
		## Go and take the active dataframes 
		os.chdir(base_dir+"/"+session+"/cleaned_data")
		df_player_active = pd.read_csv("df_players_active.csv")
		df_experiment_active = pd.read_csv("df_experiment_active.csv")
		df_player_active["session"] = session
		df_experiment_active["session"] = session
		df_player_global = pd.concat([df_player_global,df_player_active],axis = 0)
		df_experiment_global = pd.concat([df_experiment_global,df_experiment_active],axis = 0)
		 
	os.chdir(base_dir)
	if treatment == "0": 
		df_player_global.to_csv("df_player_global_without authority.csv")
		df_experiment_global.to_csv("df_experiment_global_without authority.csv")
	if treatment == "1": 
		df_player_global.to_csv("df_player_global_with authority.csv")
		df_experiment_global.to_csv("df_experiment_global_with authority.csv")
