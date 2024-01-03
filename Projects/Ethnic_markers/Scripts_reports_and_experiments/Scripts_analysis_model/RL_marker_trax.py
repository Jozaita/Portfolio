##Imports
import random as rd
import numpy as np
##Simulation variables
def RL_marker_trax(l,e):
    N=20
    T=40
    sim=1000
    h=0
    pdif=4 #number of different probabilities (2xbehaviours)
    prob2 = 1#Probability of learner in a population
    prob3 = 0	 #Probability of conformist
    bins = 40   
    A=np.zeros([2,2])   #Payoff matrix
    A[0,0]=1
    A[0,1]=-0.5
    A[1,0]=-0.5
    A[1,1]=1
    ##Agents variables
    agents=[[0]*8 for i in range(N)] ##(beh,mar,pay,int,asp)
    prob=[[0]*pdif for i in range(N)]##(p=a,p=b,p!a,p!b)
    stim=[0]*2
    action=[0]*2
    a=[0]*2
    
    
     
    ####Cutoff for pearsonR
    cutoff=1/100
    ##Functions
    def interact(a,b):
        a[3]+=1
        b[3]+=1
        if(a[0]==b[0]):
            a[2]+=1
            b[2]+=1
        else:
            a[2]+=0
            b[2]+=0
        return
    def norm(prob,action):
        if (np.mod(action,2)==0):
            action2=action+1
        else:
                    action2=action-1
        prob[action2]=1-prob[action]
        return
    
    coord_dist_global_mark = [0]*bins
    coord_dist_global_2_mark =[0]*bins
    prob_dist_global_mark = [0]*bins
    prob_err_global_mark = [0]*bins
    for s in range(sim):
        ##Initial conditions
        for i in range(N):
            agents[i][0]=rd.randint(0,1)
            agents[i][1]=rd.randint(0,1)
            agents[i][2] = 0
            agents[i][3] = 0
            agents[i][4]=rd.choice([0]*round(N*prob2)+[-1]*round(N*prob3))
            agents[i][5] = 0
            agents[i][6] = 0
            agents[i][7] = 0
            
            for j in range(pdif):
                if (np.mod(j,2)==0):
                    #prob[i][j]=rd.uniform(0,1)
                    prob[i][j] = 0.5
                else:
                    prob[i][j]=1-prob[i][j-1]
        ##Dynamics
        for t in range(T):
            subset_total = [i for i in range(N)]
            for n in range(round(N/2)):
                ##Parameter e
                a11=rd.uniform(0,1)
                if (a11>e): ##Marker interaction, choose field of action
                    same_marker = [i for i in range(N) if agents[i][1] == rd.randint(0,1)]  
                    same_marker = [elem for elem in same_marker if elem in subset_total]
                    if len(same_marker)>2:
                        couple = rd.sample(same_marker,2)
                    else:
                        couple = rd.sample(subset_total,2)
                else:
                    couple = rd.sample(subset_total,2)
                subset_total.remove(couple[0])
                subset_total.remove(couple[1])
                    ##Choose field of action
                kaux=0
                if agents[couple[0]][1] != agents[couple[1]][1]: kaux=2
                    
                agents[couple[0]][6] = A[agents[couple[0]][0],agents[couple[1]][0]]
                agents[couple[1]][6] = A[agents[couple[0]][0],agents[couple[1]][0]]
                for i in range(2):
                    a[i]=rd.uniform(0,1)
                    k=0+kaux
                    action[i] = prob[couple[i]][k]
                    while(a[i]>action[i]):
                        k+=1
                        action[i]+=prob[couple[i]][k]
                    action[i]=k
                    agents[couple[i]][5] = agents[couple[i]][0]
                    agents[couple[i]][0]=np.mod(action[i],2)
                    
                ####
                interact(agents[couple[0]],agents[couple[1]])
               
                for i in couple:
                    if agents[i][6]<0 & agents[i][5] == agents[i][0]:
                        agents[i][7] += 1
                
                ##Collect payoff, calculate aspiration and stimulus
                k=-1
                for i in couple:
                    k+=1
                    for j in range(2):
                        stim[j]=abs(A[j,0]-agents[i][4])
                    stimulus=(A[agents[couple[0]][0],agents[couple[1]][0]]-agents[i][4])/max(stim) ##So válido pra xogo de coordinación
                    agents[i][4]=(1-h)*agents[i][4]+h*A[agents[couple[0]][0],agents[couple[1]][0]]
                    ##Calculate probability update
                    if (stimulus>=0):
                        prob[i][action[k]]+=(1-prob[i][action[k]])*l*stimulus
                    else:
                        prob[i][action[k]]+=prob[i][action[k]]*l*stimulus
                    norm(prob[i],action[k])    
            
                
            if t == 39:
                coord_dist = np.histogram([agents[i][2] for i in range(N)],bins=bins,range=(0,40))[0]
                prob_dist = np.histogram([prob[i][0] for i in range(N)],bins=bins,range=(0,1))[0]
                prob_err = np.histogram([agents[i][-1] for i in range(N)],bins = bins,range=(0,40))[0]
                
        coord_dist_global_mark = [x+y for  x,y in zip(coord_dist_global_mark,coord_dist)]
        coord_dist_global_2_mark = [x+y**2 for  x,y in zip(coord_dist_global_2_mark,coord_dist)]
        prob_dist_global_mark = [x+y for x,y in zip(prob_dist_global_mark,prob_dist)]
        prob_dist_global_2_mark = [x+y**2 for x,y in zip(prob_dist_global_mark,prob_dist)]
        prob_err_global_mark = [x+y for x,y in zip(prob_err_global_mark,prob_err)]
    coord_dist_global_mark = [x/sim for x in coord_dist_global_mark]
    prob_dist_global_mark = [x/sim for x in prob_dist_global_mark]
    coord_dist_global_2_mark = [x/sim for x in coord_dist_global_2_mark]
    coord_dist_global_2_mark = [np.sqrt(x-y**2) for x,y in zip(coord_dist_global_2_mark,coord_dist_global_mark)]
    prob_dist_global_2_mark = [np.sqrt(x-y**2) for x,y in zip(prob_dist_global_2_mark,prob_dist_global_mark)]
    prob_err_global_mark = [x/sim for x in prob_err_global_mark]
    
    final_results_mark = [coord_dist_global_mark,
                          coord_dist_global_2_mark,
                          prob_dist_global_mark,
                          prob_err_global_mark]
    
    return final_results_mark
    
    
    
    
    
    
    
        
