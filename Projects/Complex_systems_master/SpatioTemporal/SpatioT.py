from numpy import * 
from matplotlib import pyplot as plb 

# Definition of parameters

a=1
b=1
eps=-10**(-2)
paso=5
tini=0
tfin=10**4
minrango=0.49
maxrangoa=0.51
maxrangob=sqrt(maxrangoa)
pasosrango=11  
rangoa=linspace(minrango,maxrangoa,pasosrango)
rangob=linspace(minrango,maxrangob,pasosrango)
matriz=zeros([pasosrango,pasosrango])
matriz2=zeros([pasosrango,pasosrango])
h=10**(-1)

for a in rangoa:
    for b in rangob:
        
        def xpunto(x,y):
            return y
                
        def ypunto(x,y):
            return -a+x**2+eps*(b*y+x*y)
        tie=[0]*tfin
        x=[0]*tfin   
        y=[0]*tfin
        x[0]=0
        y[0]=0
        tie[0]=tini
        maximosx=[]
        
        for t in range(0,tfin-1):
            tie[t+1]=tini+t*h
            k1=xpunto(x[t],y[t])
            k11=ypunto(x[t],y[t])
            k2=xpunto(x[t]+h*k1/2,y[t]+h*k11/2)
            k22=ypunto(x[t]+h*k1/2,y[t]+h*k11/2)
            k3=xpunto(x[t]+h*k2/2,y[t]+h*k22/2)
            k33=ypunto(x[t]+h*k2/2,y[t]+h*k22/2)
            k4=xpunto(x[t]+h*k3,y[t]+h*k33)
            k44=ypunto(x[t]+h*k3,y[t]+h*k33)
            
            x[t+1]=x[t]+(k1+2*k2+2*k3+k4)*h/6
            y[t+1]=y[t]+(k11+2*k22+2*k33+k44)*h/6
            
        for iy in range(1,len(x)-1):
           if x[iy]>x[iy-1] and x[iy]>x[iy+1]:
               maximosx.append(tie[iy])
        
        if len(maximosx)>1:
            maximos2x=[0]*(len(maximosx)-1)
            for iy in range(0,len(maximosx)-1):
                maximos2x[iy]=maximosx[iy+1]-maximosx[iy]
        indice=int((a-rangoa[0])/(rangoa[1]-rangoa[0])+0.001)
        indice2=int((b-rangob[0])/(rangob[1]-rangob[0])+0.001)
        r=(x[-1]+sqrt(a))**2+y[-1]**2

        matriz[indice2,indice]=r
        if len(maximosx)>1:
            matriz2 [indice2,indice]=average(maximos2x)
            if len(maximos2x)<tfin*h/100:
                matriz2[indice2,indice]=0
                
    print(a,b)
bifhomo=[0]*(len(matriz)-1)
bifhopf=[0]*(len(matriz)-1)
ejper=list(matriz2[:,5])
ind=ejper.index(max(ejper))
per=[]
x3=[]
for il in range(ind,len(ejper)):
    per.append(ejper[il])
    x3.append(il*(rangoa[1]-rangoa[0])+rangoa[0])
for ik in range(1,len(matriz)-1):
    est=list(matriz[:,ik])
    nest=[1]*len(matriz)
    for ip in range(0,len(est)):
        nest[ip]=est[ip]
        if est[ip]<abs(eps)*0.1 or 0*est[ip]!=0:
            nest[ip]=0
    noest=nonzero(nest)
    if len(noest[0])>0:   
        bifhomo[ik]=min(noest[0])*(rangoa[1]-rangoa[0])+rangoa[0]
        bifhopf[ik]=max(noest[0])*(rangoa[1]-rangoa[0])+rangoa[0]
f1=plb.figure(0,figsize=(12,8))
ax=plb.gca()
plb.pcolor(rangoa,rangob,matriz)
plb.title('Fixed point distance',fontsize=16)
plb.xlabel('a',fontsize=16)
plb.ylabel('b',fontsize=16)
plb.colorbar()
f1.savefig('STD2.eps')

f2=plb.figure(1,figsize=(12,8))
ax=plb.gca()
x2=rangoa[1:]
plb.plot(x2,bifhomo,'o',label='Homoclinic Bifurcation P')
plb.plot(x2,5/7*sqrt(x2),label='5/7* sqrt(x) ')
plb.plot(x2,bifhopf,'o',label='Hopf Bifurcation')
plb.plot(x2,sqrt(x2),label=' sqrt(x) ')
plb.title('Bifurcation lines',fontsize=16)
plb.xlabel('a',fontsize=16)
plb.ylabel('b',fontsize=16)
plb.legend()
f2.savefig('STL2.eps')

f3=plb.figure(2,figsize=(12,8))
ax=plb.gca()
plb.plot(x3,per,'o',label='Example of period')
#plb.plot(x3,(x3-x3[0])**(-1/2)*per[-1]/sqrt(1-x3[0]),label='1/sqrt(x)')
plb.title('Example of period',fontsize=16)
plb.xlabel('a',fontsize=16)
plb.ylabel('T',fontsize=16)
plb.legend()
f3.savefig('STP2.eps')
