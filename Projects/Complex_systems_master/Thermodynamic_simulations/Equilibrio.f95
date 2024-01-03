program equilibrio
implicit none

 integer, parameter :: ikind=selected_real_kind(p=15)
real (kind=ikind) ::L,V,dens,deriv,deriv2,ecin,epot,E,dt,dt2,dpaso,dtotal,invcin
real(kind=ikind)::ecinacumulada,invcinacumulada,epotacumulada,Eacumulada,tiempo
real(kind=ikind)::derivacumulada,deriv2acumulada,invcinderivacumulada,invcinderiv2acumulada
real(kind=ikind)::alfae,invalfae,alfap,alfas,cp,kt,invkt,invks,ks,gamma
real(kind=ikind)::alfa,invalfa,cv,invcv,pres,temp,gradlib,invcinderiv2media,invcinderivmedia
real(kind=ikind)::deriv2media,derivmedia,emedia,epotmedia,invcinmedia,ecinmedia,dnump
integer ::nump,i,paso,total,coincidencia,n
real (kind=ikind),Dimension(:),Allocatable::rxp,ryp,rzp,vxp,vyp,vzp,fxp,fyp,fzp




!Recuperamos todos los datos de la situacion inicial abriendo los respectivos archivos
open (10,file='Parametros10.txt')
        	read (10,*) nump,L
			read (10,*) V,dens
			read (10,*) E,ecin,epot
            close(10)
            
            !Colocamos nuestras matrices
Allocate(rxp(nump))
Allocate(ryp(nump))
Allocate(rzp(nump))
Allocate(vxp(nump))
Allocate(vyp(nump))
Allocate(vzp(nump))
Allocate(fxp(nump))
Allocate(fyp(nump))
Allocate(fzp(nump))
            open (12,file='Vectoresfinal9.txt',form='unformatted')
               read(12)rxp,ryp,rzp,vxp,vyp,vzp,fxp,fyp,fzp
      close(12)
!Calculamos los valores temporales para la simulacion 
total=500000
paso=100
coincidencia=0
dt=10.0d0**(-4.0d0)
 dpaso=dble(paso)
 dtotal=dble(total)
dnump=dble(nump)
!Definimos el valor (nulo) de las variables acumuladas iniciales
	ecinacumulada=0.d0	
			invcinacumulada=0.d0
			epotacumulada=0.d0
			Eacumulada=0.d0
			derivacumulada=0.d0
			deriv2acumulada=0.d0
			invcinderivacumulada=0.d0
			invcinderiv2acumulada=0.d0


!Comenzamos la dinamica molecular y, para ello, abrimos un archivo de grabacion de resultados
	do i=1,total
  call verlet(rxp,ryp,rzp,vxp,vyp,vzp,fxp,fyp,fzp,L,nump,ecin,Epot,dens,deriv,deriv2)
!Definimos todas las variables necesarias para calcular los promedios
E=ecin+epot 
invcin=1.0d0/ecin



!Construimos las variables acumuladas de las cuales obtendremos las medias
			ecinacumulada=ecinacumulada+ecin
			invcinacumulada=invcinacumulada+invcin
			epotacumulada=epotacumulada+epot
			Eacumulada=Eacumulada+E
			derivacumulada=derivacumulada+deriv
			deriv2acumulada=deriv2acumulada+deriv2
			invcinderivacumulada=invcinderivacumulada+deriv*invcin
			invcinderiv2acumulada=invcinderiv2acumulada+deriv*deriv*invcin

!Programamos para que grabe a cada paso 
			if (mod(i,paso)==0) then
           
 	coincidencia=coincidencia+1
                tiempo=dble((coincidencia-1)*paso)*dt
				open (10,file='Resultados10.txt',access='append')
                21 format(f7.2,2x,1pe13.6,2x,1pe13.6,2x,1pe13.6)
					write (10,21) tiempo,Epot,Ecin,E
		        	
close (10)
open(14,file='Matriz10.txt',form='unformatted',access='append')
do n=1,nump
 write(14)rxp(n),ryp(n),rzp(n),vxp(n),vyp(n),vzp(n)
  end do
             close(14)  
			end if

		end do
!Procedemos a calcular las medias a partir de los valores acumulados 
            ecinmedia=ecinacumulada/dtotal
			invcinmedia=invcinacumulada/dtotal
            epotmedia=epotacumulada/dtotal
			Emedia=Eacumulada/dtotal
			derivmedia=derivacumulada/dtotal
			deriv2media=deriv2acumulada/dtotal
			invcinderivmedia=invcinderivacumulada/dtotal
			invcinderiv2media=invcinderiv2acumulada/dtotal
!A continuacion, empleamos estas variables medias para obtener las propiedades macroscopicas
! a partir de las definiciones de la mecanica estadistica 
gradlib=dble(3.0d0*nump)-3.0d0 !Dado que tenemos las tres ligaduras de la colectividad 
!Comenzamos a calcular magnitudes termodinamicas, teniendo en cuenta que la cte de Boltzmann=1 

temp=2*ecinmedia/gradlib
pres=dnump*temp/V-derivmedia
invcv=1+(2/gradlib-1)*ecinmedia*invcinmedia
cv=1.0d0/invcv
invalfa=V*((1-2/gradlib)*ecinmedia*invcinderivmedia-derivmedia)
alfa=1.0d0/invalfa
gamma=dnump*invcv+V*(gradlib/2-1)*(derivmedia*invcinmedia-invcinderivmedia)
invks=(dnump*temp/V)*(1+2*gamma-dnump*invcv)+V*deriv2media &
-V*(gradlib/2-1)*(invcinderiv2media-2*derivmedia*invcinderivmedia+derivmedia*derivmedia*invcinmedia)
ks=1.0d0/invks
invkt=invks-temp*cv*gamma*gamma/V
kt=1.0d0/invkt
cp=cv*kt*invks
alfas=-1/(gamma*temp)
alfap=cv/V*gamma*kt
invalfae=pres*V/cv-gamma*temp
alfae=1.0d0/invalfae
open(23,file='Resumen10.txt',access='append')
write(23,1000)'*******Resumen de los parametros*****'
write(23,1001)nump,L,V,dens,'nump,L,V,dens'
write(23,1002)dt,paso,total,'dt,paso,total'
write(23,1003)ecinmedia,epotmedia,Emedia, 'ecinmedia,epotmedia,Emedia'
write(23,1004)alfa,alfas,alfae,alfap,ks,kt,'alfa,alfas,alfae,alfap,ks,kt'
write(23,1005)temp,pres,gamma,cp,cv,'temp,pres,gamma,cp,cv'
1000 format(a50)
1001 format(i5,2x,f7.2,2x,f7.2,2x,f7.2,2x,a50)
1002 format(f10.5,2x,i9,2x,i9,2x,a50)
1003 format(1pe13.6,2x,1pe13.6,2x,1pe13.6,2x,a50)
1005 format(f13.6,2x,f13.6,2x,f13.6,2x,f13.6,2x,f13.6,2x,a50)
1004 format(f13.6,2x,f13.6,2x,f13.6,2x,f13.6,2x,f13.6,2x,f13.6,2x,a50)
close(23)



open(26,file='Vectoresfinal10.txt',form='unformatted',access='append')
write(26) rxp,ryp,rzp,vxp,vyp,vzp,fxp,fyp,fzp
close(26)
end program equilibrio            