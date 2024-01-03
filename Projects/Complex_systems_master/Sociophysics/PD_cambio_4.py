import numpy as np 
import networkx as nx
import random as rd
import time
import sys
import csv
from matplotlib import pyplot as plb
#Functions used to compute the difference between two lists and the clustering of 
#the network
def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]
def cl(ib):
        clustlinks=0
        veci=G.neighbors(ib)
        grado=G.degree(ib)
        if grado>1:
         
         for ik in veci:
            for ij in veci:    
                if G.has_edge(ik,ij)==True:
                    clustlinks+=1
         clustlinks=2*clustlinks/((grado)*(grado-1))
        return clustlinks
#Conditions of the population            
N=100
tfinal=100
sim=100
trange=np.arange(1,2,0.05)
mediacop=[0]*(len(trange))
varianzacop=[0]*(len(trange))
mediadeg=[0]*(len(trange))
varianzadeg=[0]*(len(trange))
varianzanorm=[0]*(len(trange))
varianzanorm1=[0]*(len(trange))
payoffcop=[0]*len(trange)
payoffdef=[0]*len(trange)
payoffdif=[0]*len(trange)
fraccop=[0]*tfinal
fraccop2=[0]*tfinal
varcop=[0]*tfinal
averdeg=[0]*tfinal

vardeg=[0]*tfinal
agents=[i for i in range(0,N)]
satisf=[]
a=np.array([1,0])
b=np.array([0,1])
K=2.5
mediacop=[0]*(len(trange))
varianzacop=[0]*(len(trange))
clust=[0]*len(trange)
mediadeg=[0]*(len(trange))
varianzadeg=[0]*(len(trange))
states=[a,b]
start=time.time()
#We define all the vectors that change with t1(t in theoretical model)
for t1 in trange:
  conta=0
  indice=0
  while conta<100:
   probdef=[0]*tfinal
   probcop=[0]*tfinal
   probcross=[0]*tfinal
   payoffvec=[0]*tfinal      
   fraccop=[0]*tfinal
   fraccop2=[0]*tfinal  
   varcop=[0]*tfinal
   averdeg=[0]*tfinal
   vardeg=[0]*tfinal   

   indice=int((t1-trange[0])/(trange[1]-trange[0]))
   A=np.zeros([2,2])
   A[0,0]=r=1
   A[1,0]=s=0
   A[0,1]=t1
   A[1,1]=p=0
   #We create the graph and set the initial values for the agents
   
   G=nx.Graph()
   G.add_nodes_from([i for i in range(0,N)])
   for i in range(0,int(K*N)):
       i1=rd.choice(agents)
       i2=rd.choice(agents)
       while G.has_edge(i1,i2)==True:
         i2=rd.choice(agents)
       G.add_edge(i1,i2)
   
   pos=nx.spring_layout(G)
   inicond=[a]*int(0.6*N)+[b]*int(0.4*N)
   rd.shuffle(inicond)
   for i in range(0,N):
      G.node[i]['v']=inicond[i]
     
   values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
   fraccop[0]=fraccop[0]+sum([values[i] for i in range(0,N)])/N
   averdeg[0]=averdeg[0]+sum([G.degree(i) for i in range(0,N)])/N
   vardeg[0]=vardeg[0]+sum([(G.degree(i)**2) for i in range(0,N)])/N
   
   
 #For each time step, every agent plays PD with his neighbours
   for t in range(1,tfinal):
      unsatisf=[]
      payoff=np.zeros([N])  
      for part in agents:       
          for i in list(G.neighbors(part)):
              u=nx.get_node_attributes(G,'v')[part]
              u2=nx.get_node_attributes(G,'v')[i]
              for k in range(0,len(u)):
                  for k2 in range(0,len(u2)):
                      payoff[part]=payoff[part]+u[k]*A[k2,k]*u2[k2]
      payoffvec[t]=sum(payoff)/N  
      maximo=max(payoff)
      lead=np.where( payoff==maximo )
      
      
#Once a round has been played, every agent updates his strategy
      for j in agents:
          payme=payoff[j]
          vecinos=list(G.neighbors(j))
          if vecinos!=[]:
           payrest=[payoff[i] for i in vecinos]
           paywin=max(payrest)
           if payme<paywin:
              unsatisf.append(j)
              k=payrest.index(paywin)
              k=vecinos[k]
              G.node[j]['v']=nx.get_node_attributes(G,'v')[k]
              values[j]=G.nodes(data='v')[j][0]
             
#Rewire with (1-q) probability the links between defectos in the unsatisfied list

      for j in unsatisf:
          vecinos=list(G.neighbors(j))
          for k in vecinos:
              if values[k]==0 and values[j]==0 :
                  p=rd.uniform(0,1)
                  q=0.5
                  if p>q:
                      q1=rd.uniform(0,1)
                      #Implementation of local neighbourhood selection
                      q2=0.75
                      if q1>q2 :
                       G.remove_edge(j,k)
                       vecinos2=list(G.neighbors(j))
                       if vecinos2!=[]:
                        k11=rd.choice(vecinos2)
                        vecvec=list(G.neighbors(k11))
                       
                        while vecvec==[]:
                          k11=rd.choice(vecinos)
                          vecvec=list(G.neighbors(k11))
                        k1=rd.choice(vecvec)
                      
                      else:
                       G.remove_edge(j,k)
                       k11=diff(agents,vecinos)
                       k1=rd.choice(diff(k11,[j]))
                      G.add_edge(j,k1)
                      
#For single simulation measures, we calculate the probability of linking between the
#the two types of agents

      links=list(G.edges())
      with open('Nodosprueba.csv','w',newline='') as csvfile:
       escrito=csv.writer(csvfile)
       escrito.writerow(['Node','Attribute'])
       for i in range(0,100):
        escrito.writerow([i,values[i]])
      with open('Linksprueba.csv','w',newline='') as csvfile:
       escrito=csv.writer(csvfile,delimiter=' ',quotechar=',',quoting=csv.QUOTE_MINIMAL)
       escrito.writerow(['ID','source','target'])
       for i in range(0,len(links)):   
         escrito.writerow([i, links[i][0],links[i][1]])
     



                      
      
      
      for ih in links: 
          if values[ih[0]]==0 and values[ih[1]]==0:
              probdef[t]=probdef[t]+1/len(links)
          if values[ih[0]]==1 and values[ih[1]]==1:
              probcop[t]=probcop[t]+1/len(links)
          if values[ih[0]]==0 and values[ih[1]]==1:
              probcross[t]=probcross[t]+1/len(links)
          if values[ih[0]]==1 and values[ih[1]]==0:
              probcross[t]=probcross[t]+1/len(links)
           

      values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
      fraccop[t]=fraccop[t]+sum([values[i] for i in range(0,N)])/N
      averdeg[t]=averdeg[t]+sum([G.degree(i) for i in range(0,N)])/N
      vardeg[t]=vardeg[t]+sum([(G.degree(i)**2) for i in range(0,N)])/N
      print(t)
      #Implementation of node attacking, changing cooperator leaders to defectors
      #at a certain time
      #if t==30:
      #    grados=[]
      #    grados2=[]
      #    for i in range(0,100):
      #     grados.append(G.degree(i))
      #     grados2.append(G.degree(i))
      #    grados2.sort(reverse=True)
      #    for iu in range(0,12):
      #     target=grados.index(grados2[iu])
      #     grados[target]=max(grados)+1
      #     G.node[target]['v']=b
      #     values[target]=0
    
   #For single-simulation measures we put here a sys.exit()       
   sys.exit() 
   #Taking measures and averaging overall the simulations
   if fraccop[tfinal-1]>0.05:
    ccp=0
    ccd=0
    payoffcop2=[]
    payoffdef2=[]
    for iy in range(0,len(values)):
        if values[iy]==1:
            payoffcop[indice]+=payoff[iy]
            payoffcop2.append(payoff[iy])
            ccp+=1
        if values[iy]==0:
            payoffdef[indice]+=payoff[iy]
            payoffdef2.append(payoff[iy])
            ccd+=1
    if ccp!=0:
     payoffcop[indice]=payoffcop[indice]/ccp
    if ccd!=0:
     payoffdef[indice]=payoffdef[indice]/ccd
    
    payoffdif[indice]=payoffdef[indice]-payoffcop[indice]       
    mediacop[indice]+=fraccop[tfinal-1]
    varianzacop[indice]+=np.var(fraccop[:int(tfinal/2)])
    mediadeg[indice]+=averdeg[tfinal-1]
    varianzadeg[indice]+=vardeg[tfinal-1]
    for ib in agents:
     clust[indice]+=cl(ib)/K
    
    payoffvec[indice]=sum(payoff)/N
    conta+=1
    tiempo=time.time()-start
    print(tiempo,t1,conta)       
  
 
   
  if conta!=0:
   payoffcop[indice]=payoffcop[indice]/conta   
   payoffdef[indice]=payoffdef[indice]/conta
   payoffdif[indice]=payoffdif[indice]/conta
   clust[indice]=clust[indice]/conta
   mediacop[indice]=mediacop[indice]/conta
   varianzacop[indice]=varianzacop[indice]/conta
   mediadeg[indice]=mediadeg[indice]/conta
   varianzadeg[indice]=varianzadeg[indice]/conta 
   varianzanorm1[indice]=(varianzacop[indice]-mediacop[indice]**2)/mediacop[indice]
   varianzanorm[indice]=(varianzadeg[indice]-mediadeg[indice]**2)/mediadeg[indice]
    
  
plb.plot(trange,mediacop)
#f1=plb.figure()
#plb.plot(fraccop)
#plb.plot(varcop)
#f3=plb.figure()
#plb.plot(averdeg)
#plb.plot(vardeg)


    