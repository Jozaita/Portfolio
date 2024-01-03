from matplotlib import pyplot as plb
import numpy as np
tiempo=np.arange(1,49)
grados=[]
for i in range(0,100):
    grados.append(G.degree(i))
f1=plb.figure(figsize=(10,8))
plb.hist(payoffcop2,label='Cooperators')
plb.hist(payoffdef2,label='Defectors')
plb.title('Payoff histogram',fontsize=16)
plb.xlabel('Payoff',fontsize=16)
plb.ylabel('Number of agents',fontsize=16)
plb.legend()
f1.savefig('Histogrampayoff.jpg')

f2=plb.figure(figsize=(10,8))
plb.hist(grados,label='Grados')

plb.title('Payoff histogram',fontsize=16)
plb.xlabel('Grados',fontsize=16)
plb.ylabel('Number of agents',fontsize=16)
plb.legend()
f1.savefig('Histogrados.jpg')