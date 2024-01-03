from matplotlib import pyplot as plb
import numpy as np

hist1=np.histogram(size,bins=100,range=(1,max(size)))
hist3=np.histogram(size000,bins=100,range=(1,max(size000)))
hist5=np.histogram(size001,bins=100,range=(1,max(size001)))
#hist7=np.histogram(size002,bins=100,range=(1,max(size002)),normed=1)
f1=plb.figure()
ax=plb.gca()
plb.loglog(hist1[1][:-1],hist1[0],'o',label='0.1')
plb.loglog(hist3[1][:-1],hist3[0],'o',label='0.9')
plb.loglog(hist5[1][:-1],hist5[0],'o',label='0.99')
#plb.loglog(hist5[1][:-1],hist7[0],'o')
plb.title('Distribution of Sizes',fontsize=16)
plb.xlabel('S',fontsize=16)
plb.ylabel('P(S)',fontsize=16)
plb.legend()
f1.savefig('Psizes.jpg')


hist2=np.histogram(ret,bins=100)
hist4=np.histogram(ret000,bins=100)
hist6=np.histogram(ret001,bins=100)
#hist8=np.histogram(ret002,bins=100,normed=1)
f2=plb.figure()
ax=plb.gca()
plb.loglog(hist2[1][:-1],hist2[0],'o',label='0.1')
plb.loglog(hist4[1][:-1],hist4[0],'o',label='0.9')
plb.loglog(hist6[1][:-1],hist6[0],'o',label='0.99')
#plb.loglog(hist6[1][:-1],hist8[0],'o')
plb.title('Distribution of returns',fontsize=16)
plb.xlabel('R',fontsize=16)
plb.ylabel('P(R)',fontsize=16)
plb.legend()
f2.savefig('Preturns.jpg')






tiempo=np.arange(0,50)
f1=plb.figure(figsize=(12,8))
plb.plot(tiempo,probcop,marker='o',linestyle='--',label='Cop-Cop')
plb.plot(tiempo,probdef,marker='o',linestyle='--',label='Def-Def')
plb.plot(tiempo,probcross,marker='o',linestyle='--',label='Cop-Def')
plb.title('Probability of interaction',fontsize=16)
plb.xlabel('time',fontsize=16)
plb.ylabel('probability of interaction',fontsize=16)
plb.legend()
f1.savefig('Probability interaction.jpg')