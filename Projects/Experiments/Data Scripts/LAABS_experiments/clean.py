import numpy as np
import pandas as pd


def dar_xeito(df_1,df_2,participants,rounds_1,rounds_2,num_participants):
    ### Primeiro, temos que desbotar ós que quedaron inactivos 
    inactives = df_1['participant.id_in_session'][df_1['participant.label'] == 1].unique()
    num_participants -= len(inactives)
    print('Inactives:')
    for inactive in inactives:
            if inactive in participants['Player'].unique():
                print(participants[participants['Player'] == inactive].squeeze(axis=0))
                print('***********')
                print(df_1['player.absence'][df_1['participant.id_in_session'] == inactive].iloc[-1])
                print('***********')
                
            df_1.drop(df_1[df_1['participant.id_in_session'] == inactive].index,inplace = True)
            df_2.drop(df_2[df_2['participant.id_in_session'] == inactive].index,inplace = True)
            participants.drop(participants[participants['Player'] == inactive].index,inplace = True)
    ###
    df_1_cols = df_1.columns
    col_1_interest = ['participant.code','participant.label','participant.id_in_session','subsession.round_number','group.id_in_subsession']
    for col in df_1_cols:
        if 'player' in col:
            col_1_interest.append(col)
    df_2_cols =df_2.columns
    col_2_interest = ['participant.code','participant.id_in_session','subsession.round_number']
    for col in df_2_cols:
        if 'player' in col:
            col_2_interest.append(col)
    df_1 = df_1[col_1_interest]
    df_1 = df_1.iloc[:num_participants*rounds_1]
    df_2 = df_2[col_2_interest]
    df_2 = df_2.iloc[:num_participants*rounds_2]
    df_2.fillna(-1,inplace=True)
    participants['Paypal'] = list(df_2['player.paypal'].iloc[len(df_2)-num_participants:])
    participants['Bias'] = list(df_1['player.bias'].iloc[len(df_1)-num_participants:])
    participants['Bias_payoff'] = list(df_1['player.bias_payoff'].iloc[len(df_1)-num_participants:])
    participants['Marker'] = list(df_1['player.marker'].iloc[len(df_1)-num_participants:])
    participants['Comments'] = list(df_2['player.comments'].iloc[len(df_2)-num_participants:])
    participants['id_in_session'] = list(df_1['participant.id_in_session'].iloc[len(df_1)-num_participants:])
    participants['id_in_subsession'] = list(df_1['group.id_in_subsession'].iloc[len(df_1)-num_participants:])
    del df_1['group.id_in_subsession']
    del df_1['player.bias']
    del df_1['player.bias_payoff']
    del df_1['player.marker']
    del df_2['player.paypal']
    del df_2['player.payoff']
    del df_2['player.comments']
    
    df_1.columns = [col.split('.')[-1] for col in df_1.columns]
    df_2.columns = [col.split('.')[-1] for col in df_2.columns]
    ########
    players_info = [[0 for i in range(3)] for j in range(num_participants)]

    for i,j in enumerate(df_1['id_in_session'].unique()):
        players_info[i][0] = participants[participants["Player"] == j].squeeze(axis=0)
        players_info[i][1] = df_1[df_1['id_in_session'] == j]
        players_info[i][2] = df_2[df_2['id_in_session'] == j]
    del df_1['id_in_session']
    return players_info


#### Coming from players_info, function to create pagos.txt
def crear_txt(players_info,fecha):
    f = open("pagos_"+fecha+".txt","a")
    for i in range(len(players_info)):
    ###Include conversion rate and participation fee
        if players_info[i][1]['absence'].iloc[-1] < 4:
            pago = round(players_info[i][2]['payoff_total'].iloc[-1]*0.125+2,2)
            pago = str(pago).replace('.',',')
            f.write("{}\t{}\tEUR\n".format(players_info[i][0]['Paypal'], pago))
        elif players_info[i][1]['label'].iloc[-1] == 0 and players_info[i][1]['absence'].iloc[-1] > 4 : 
            pago = 2
            pago = str(pago).replace('.',',')
            f.write("{}\t{}\tEUR\n".format(players_info[i][0]['Paypal_database'], pago))
        
    f.close()
    return 

### erase dropouts and recreate the main dataframe
def update_players_info(players_info,df_1,participants):
    dropout = list(df_1['participant.id_in_session'][df_1['player.absence']>4].unique())
    players_info_2 = [[0 for i in range(3)] for j in range(len(players_info)-len(dropout))]
    k = 0
    print('Dropout:')
    for i in range(len(players_info)):
        if players_info[i][1]['id_in_session'].iloc[-1] not in dropout:
            players_info_2[k][0] = players_info[i][0]
            players_info_2[k][1] = players_info[i][1]
            players_info_2[k][2] = players_info[i][2]
            k +=1
        else:

            print(participants.iloc[i])
            print('***********')
            print(df_1['player.absence'][df_1['participant.id_in_session'] == participants['Player'].iloc[i]].iloc[-1])
            print('***********')
    return players_info_2
