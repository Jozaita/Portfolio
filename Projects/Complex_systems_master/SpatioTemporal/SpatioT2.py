from numpy import * 
from matplotlib import pyplot as plb 
import math
import decimal
from scipy import stats
# Definition of parameters


eps=-10**(-2)
paso=5
tini=0
#minrango=0.489730025
#maxrangoa=0.489730031
minrango=0.4901201
maxrangoa=0.49012019405

acrit=0.490120194065
maxrangob=(maxrangoa)
pasosrango=101  
rangoa=linspace(minrango,maxrangoa,pasosrango)
h=10**(-1)
rcrit=10**3
b=0.5
p=10**(-6)
a=0.2
peri=[0]*pasosrango

#condicion de la precision , percal 
indice=-1
for a in rangoa:
        indice+=1       
        def xpunto(x,y):
            return y
                
        def ypunto(x,y):
            return -a+x**2+eps*(b*y+x*y)
        tie=[]
        tray=[]
        x=0
        y=0
        t=tini
        maximosx=[]
        periodo=[]
        r=x**2+y**2
        per=0
        while t<10**5*h: 
          
            k1=xpunto(x,y)
            k11=ypunto(x,y)
            k2=xpunto(x+h*k1/2,y+h*k11/2)
            k22=ypunto(x+h*k1/2,y+h*k11/2)
            k3=xpunto(x+h*k2/2,y+h*k22/2)
            k33=ypunto(x+h*k2/2,y+h*k22/2)
            k4=xpunto(x+h*k3,y+h*k33)
            k44=ypunto(x+h*k3,y+h*k33)
            
            x=x+(k1+2*k2+2*k3+k4)*h/6
            y=y+(k11+2*k22+2*k33+k44)*h/6
            r=x**2+y**2
            t=t+h
            tray.append(x)
            tie.append(t)
        #if math.isnan(r)==True:
        #  if a<acrit:
        #        acrit=a
        for k in range(1,len(tray)-1):
            if tray[k]*tray[k-1]<0 :
                periodo.append(tie[k])
        for k2 in range(int(len(periodo)/1.5),len(periodo)):
            per+=periodo[k2]-periodo[k2-1]
        peri[indice]=2*per/(len(periodo)-1)
cos=0
#acrit=rangoa[peri.index(max(peri))]
rangoab=[0]*len(rangoa)            
c=sqrt(a)
for h in range(0,len(rangoa)):
    rangoab[h]=-log(abs(rangoa[h]-acrit))
    peri[h]=(peri[h])
slope, intercept, r_value, p_value, std_err = stats.linregress(rangoab[:-1],peri[:-1])
c=sqrt(a)
l=(eps*(b+sqrt(a))+sqrt(eps**2*(b+sqrt(a))**2+8*sqrt(a)))*0.5    
l2=(eps*(b+c)-sqrt(eps**2*(b+sqrt(a))**2+8*c))*0.5
l3=(eps*(b-c)+sqrt(eps**2*(b-sqrt(a))**2-8*c))*0.5
l4=(eps*(b-c)-sqrt(eps**2*(b-sqrt(a))**2-8*c))*0.5
rangoabc=[0]*len(rangoab)
for h in range(0,len(rangoab)):
    rangoabc[h]=slope*rangoab[h]+intercept
f3=plb.figure(2,figsize=(12,8))
ax=plb.gca()
plb.plot(rangoab,peri,'o',label='Example of period')
plb.plot(rangoab,rangoabc,label='Fit')
plb.title('Example of period',fontsize=16)
plb.xlabel('-log(a-a_{c})',fontsize=16)
plb.ylabel('T',fontsize=16)
plb.legend()
f3.savefig('STP2.eps')         