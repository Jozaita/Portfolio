import networkx as nx
import numpy as np
from matplotlib import pyplot as plb
from scipy import stats
import random
import time
#build the seed graph
start = time.time()  
m0=2
m=2
Deg=[]
mfinal=100
G=nx.Graph()
G=nx.complete_graph(m0)
e=[i for i in range(0,m0)]
kprueba=[]
kprueba2=[]
kprueba3=[]
kprueba4=[]
prefer=[i for i in range(0,m0)]*m
i=0
#Adding node and mechanism of iteration 
while i<10**6:
    kprueba.append(G.degree(0))
    n=0
    G.add_node(i)
    select=[]
    while n!=m:
     j=random.choice(prefer)
     while j in select:
      j=random.choice(prefer)
     G.add_edge(i,j)
     prefer.append(i)
     prefer.append(j)
     select.append(j)
     n=n+1
     
    if i>10:
     kprueba2.append(G.degree(10))
    if i>100:
     kprueba3.append(G.degree(100))
    if i>1000:
     kprueba4.append(G.degree(1000))
    i=i+1
      

for k in range(0,len(G)):
        Deg.append(G.degree(k))
  
hist=np.histogram(Deg,bins=len(Deg)-1,range=(1,len(Deg)),normed=1)
f1=plb.figure()
ax=plb.gca()
plb.loglog(hist[1][:-1],hist[0],'o')
plb.ylim(((1/i),1))
plb.xlim((1,int(i)))
plb.xlabel('k')
plb.ylabel('Degree ')
plb.title('Degree Distribution')
xregre=[]
yregre=[]
f1.savefig('B-A-distribution.png')

for k in range(0,len(hist[0])):
 if  hist[0][k]>(1/i)*100 and hist[0][k]<(1/i)*10000:
        yregre.append(np.log(hist[0][k]))
        xregre.append(np.log(hist[1][k]))
slope, intercept, r_value, p_value, std_err = stats.linregress(xregre,yregre)
yplot=[]
for i in range(0,len(hist[1])):
    yplot.append(hist[1][i]**slope*np.exp(intercept))
plb.loglog(hist[1] ,yplot)
f2=plb.figure()
plb.xlabel('Number of new nodes')
plb.ylabel('Degree of target k')
plb.title('B-A evolution ')
plb.loglog(kprueba)
plb.loglog(kprueba2)
plb.loglog(kprueba3)
plb.loglog(kprueba4)
x=np.arange(0,len(kprueba))
x2=np.arange(10,len(kprueba))
x3=np.arange(100,len(kprueba))
x4=np.arange(1000,len(kprueba))
plb.loglog(x,m*np.sqrt(x))
plb.loglog(x2,m*np.sqrt(x2/10))
plb.loglog(x3,m*np.sqrt(x3/100))
plb.loglog(x4,m*np.sqrt(x4/1000))
plb.ylim(1,max(kprueba))
f2.savefig('B-A-evolution.png')
end = time.time()
print(end - start)  


#In this example, we have used m=2, but it can be changed by any other with
#the restriction m<=m0

#For the linear regression we obtain, for m=2 and m0=2:
#slope=-2.87 
#intercept=1.96

#Theoretical value for slope: -3
#Theoretical value for intercept: 2.08


#-We can see that the degree distribution fits the one explained in 
#Barabasi paper. Although our results are not exactly the ones that theory 
#predicts (we dont get the same slope and intercept for the linear regression)
# they are really near. The same occurs for the evolution of the degree, we 
# get the square-root dependence but it appears shifted by some quantity that 
#may vary along the time. In order to transform these approximation into real, 
# we should take into account that the former is an stochastic proccess, and 
# we would need several trials in order to capture the behaviour of the average. 

















