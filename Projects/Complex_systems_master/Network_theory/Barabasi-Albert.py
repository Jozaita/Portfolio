import networkx as nx
import numpy as np
from matplotlib import pyplot as plb
from scipy import stats
import random
import time
#build the seed graph

m0=5
m=5
Deg=[1]
maximo=max(Deg)
i=m0
mfinal=100
G=nx.Graph()
G=nx.complete_graph(m0)
suma=sum(Deg)

#Adding node and mechanism of iteration 
while i<10**3:
    Nod=[]
    Deg=[]
    start = time.time()
    for k in range(0,len(G.degree())):
        Deg.append(G.degree(k))
        Nod.append(k)
    maximo=max(Deg)
    exito=[]
    long=len(exito)
    n=0
    G.add_node(i)
    while n!=m:
     j=random.choice(Nod)
     p=Deg[j]/suma
     q=np.random.uniform()
     if p>q:
       G.add_edge(i,j)
       Nod.remove(j)
       n=n+1    
    suma=suma+2*m
    i=i+1
   
hist=np.histogram(Deg,bins=len(Deg)-1,range=(m,len(Deg)),normed=1)
f1=plb.figure()
ax=plb.gca()
plb.loglog(hist[1][:-1],hist[0],'o')
plb.ylim(((1/i),1))
plb.xlim((1,int(i)))
xregre=[]
yregre=[]

for k in range(0,len(hist[0])):
 if  hist[0][k]>10/i and hist[0][k]<100/i:
        yregre.append(np.log(hist[0][k]))
        xregre.append(np.log(hist[1][k]))
slope, intercept, r_value, p_value, std_err = stats.linregress(xregre,yregre)
yplot=[]
for i in range(0,len(hist[1])):
    yplot.append(hist[1][i]**slope*np.exp(intercept))
plb.loglog(hist[1] ,yplot)
end = time.time()
print(end - start)





