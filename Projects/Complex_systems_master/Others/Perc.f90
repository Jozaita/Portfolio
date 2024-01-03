program Percolation
implicit none
integer, parameter :: dp = selected_real_kind(15, 307)
integer(dp),parameter:: N=10**4.0d0,tfinal=10**4,sim=100,h=99 
integer(dp),parameter::lambda=5.0d0*10.0d0**4.0d0
integer(dp),parameter,dimension(2)::states
#Condiciones de la poblacion
a=1/(h+1)
tmarket=tfinal/a
states=(-1,1)
size=[0]*tfinal
ret=[0]*tfinal
rnorm=[0]*tfinal
pre=[0]*tfinal
pre[0]=100
lambda1=5*10**4
start=time.time()
#Definimos la grafica y ponemos el estado inicial 
G=nx.Graph()
G.add_nodes_from([i for i in range(0,N)])
for i in range(0,N):
     G.node[i]['v']=0
values=[G.nodes(data='v')[i] for i in  range(0,N)] 

def destroy(j):
    drl=[j]
    while drl!=[]:
     for ij in drl: 
        desnei=list(G.neighbors(ij))
        if desnei!=[]:
         for ik in desnei:
           G.nodes[ik]['v']= G.nodes[ij]['v']
           G.remove_edge(ik,ij)
     drl=[]
     if desnei!=[]:
      for il in range(0,len(desnei)):
        drl.append(desnei[il])
    return

  #Introduce the dynamics for each timestep 
for t in range(0,tfinal-1):
      
      j=rd.randint(0,N-1)
      u=rd.uniform(0,1)
      if u>a:
           G.node[j]['v']=rd.choice(states)
           destroy(j)
      else:
        k=rd.randint(0,N-1)
        while k==j:
            k=rd.randint(0,N-1)
        G.add_edge(k,j)
   #Calculate s 
      values=[G.nodes(data='v')[i] for i in  range(0,N)] 
      si=sum(values)
      size[t]=abs(si)
      pre[t+1]=pre[t]*np.exp(si/lambda1)
      r=pre[t+1]/pre[t]
      ret[t+1]=np.log(r)
end program 
