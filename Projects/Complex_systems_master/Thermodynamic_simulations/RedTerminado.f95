program red
 


implicit none
integer, parameter :: ikind=selected_real_kind(p=15)
real (kind=ikind) :: L,V,a,random,dens,sumvx,sumvy,sumvz,Epot,E,Ecin,vmedia,m,vcel,ncel,b,nceli
real(kind=ikind):: deriv2,deriv,ecinazar,ecinp,desplazamiento
integer ::i,j,k,n,idum,indiceli,nump
character:: respuesta,s
real (kind=ikind),Dimension(:),Allocatable::rxp,ryp,rzp,vxp,vyp,vzp,fxp,fyp,fzp,axp,ayp,azp
!
!
!
!Suponemos una caja cúbica, y partimos de la distancia entre atomos sobre el esquema cubico de la red.Colocamos nuestras matrices
!y otros parámetros: 
nump=500
dens=0.5
V=nump/dens
E=-800
L=V**(1.0d0/3.0d0)
ncel=nump/4
Vcel=V/ncel
a=Vcel**(1.0d0/3.0d0)
b=1.0d0/a
nceli=L*b+0.1 !Agregamos 0,1 para evitar que en el siguiente comando tome una parte entera de 4.9999 a 4 y desequilibre todo.
indiceli=int(nceli)	
deriv=0.d0
deriv2=0.d0
Epot=0.d0
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
Allocate(axp(nump))
Allocate(ayp(nump))
Allocate(azp(nump))
!Programamos la red fcc y colocamos los atomos
!Aqui hacemos constar que dividimos nuestro esquema en 5 celdas sobre la direccion i, otras 5 en j y otras 5 en k, de tal manera 
!que disponemos de un volumen cúbico de 125 celdas. 
n=1
  do i=1,indiceli
    do j=1,indiceli
      do k=1,indiceli
  !Celda primitiva
 rxp(n)=a/2.0d0+(i-1)*a
 ryp(n)=a/2.0d0+(j-1)*a
 rzp(n)=0+(k-1)*a
 rxp(n+1)=0+(i-1)*a
 ryp(n+1)=a/2.0d0+(j-1)*a
 rzp(n+1)=a/2.0d0+(k-1)*a
 rxp(n+2)=a/2.0d0+(i-1)*a
 ryp(n+2)=0+(j-1)*a
 rzp(n+2)=a/2.0d0+(k-1)*a
 rxp(n+3)=0+(i-1)*a
 ryp(n+3)=0+(j-1)*a
 rzp(n+3)=0+(k-1)*a
 n=n+4
 end do
 end do
 end do
 
  !Colocamos velocidades aleatorias con random entre -1 y 1 
 idum=-1
 do i =1,nump
 vxp(i)=random(idum)*2.0d0-1.0d0
 vyp(i)=random(idum)*2.0d0-1.0d0
 vzp(i)=random(idum)*2.0d0-1.0d0
end do
   
!Mandamos a cero el momento lineal del centro de masas 
sumvx=0.d00
sumvy=0.d00
sumvz=0.d00
  do i =1,nump
  sumvx=vxp(i)+sumvx
  sumvy=vyp(i)+sumvy
  sumvz=vzp(i)+sumvz
  end do 
  do i=1,nump
    vxp(i)=vxp(i)-sumvx/nump
    vyp(i)=vyp(i)-sumvy/nump 
    vzp(i)=vzp(i)-sumvz/nump
    end do 
  !Calcularemos ahora las energias cinetica y potencial deseada y actual, aplicaremos un factor de escala segun nos dice el Hayle para ajustar a la energia
    !introducida por el usuario.
       
    call  Potencial (rxp,ryp,rzp,fxp,fyp,fzp,L,nump,dens,Epot,deriv,deriv2)
!Declaramos m, aunque no la utilicemos por el momento al no conocer las relaciones entre las diferentes magnitudes //
Ecin=E-Epot
Ecinp=Ecin/nump
m=1.0d0
do i=1,nump !Colocamos las aceleraciones iniciales con fuerza y masa
  axp(i)=fxp(i)/m
  ayp(i)=fyp(i)/m
  azp(i)=fzp(i)/m
    end do
vmedia=sqrt(2.0d0*Ecinp/m)

  !Colocamos velocidades aleatorias con random entre -1 y 1 
 idum=-1 
Ecinazar=0.d00
 do i =1,nump
 vxp(i)=vxp(i)*vmedia
 vyp(i)=vyp(i)*vmedia
 vzp(i)=vzp(i)*vmedia
 Ecinazar=Ecinazar+(vxp(i)**2+vyp(i)**2+vzp(i)**2)*0.5
 end do 
 do i=1,nump
   vxp(i)=vxp(i)*sqrt(Ecin/Ecinazar)
   vyp(i)=vyp(i)*sqrt(Ecin/Ecinazar)
   vzp(i)=vzp(i)*sqrt(Ecin/Ecinazar)
end do
15 format(i4,2x,f7.2,2x,f7.2,2x,f7.2)
16 format(f7.2,2x,f7.2)
17 format(1pe19.12,2x,1pe19.12,2x,1pe19.12)
18 format(1a15,f7.2)
19 format(1a25,i7)
open (10,file='Parametros.txt')
		write (10,15) nump,L
		write (10,16) V,dens
		write (10,17) ecin+epot,ecin,epot
	close (10)
close('Parametros.txt')
write(*,18)'Energia :',E
write(*,19)'Numero de particulas :',nump
write(*,18)'Densidad :',dens
write(*,*)'-------------------------------------------------------------------------------'
write(*,10)'Energia potencial inicial |','| Energia cinetica inicial |','| Velocidad media |' 
10 format(3a25)
write(*,*)'-------------------------------------------------------------------------------'
write(*,11)Epot,Ecin,vmedia
11 format(3f25.2)
open(12, file='Simulacion.txt',form='unformatted')  ! Guardamos toda la info de los arrays en un archivo
write(12) rxp,ryp,rzp,vxp,vyp,vzp,axp,ayp,azp
close(12) 
close('Simulacion.txt')


write(*,*)'Teclee cualquier tecla para cerrar la ventana'
read*,respuesta
if (respuesta==s) then
  write(*,*)'Gracias' 
  else 
    stop
    end if    
end program red
!_______________________________________________________________________________


  function random(idum)
        implicit none
        
        integer, parameter :: entero=SELECTED_INT_KIND(9)
        integer, parameter :: doblep=SELECTED_REAL_KIND(15,307)
!
!       random es real*8. idum integer*4
!       devuelve un numero alatorio entre (0,1), si el parametro
!       idum es negativo o es la primera vez que se la llama
!       inicializa el generador en base a idum.
!
        integer (kind=entero) :: idum
        real (kind=doblep), parameter :: mbig=4.d+06,mseed=1618033.d00
        real (kind=doblep), parameter :: mz=0.d00,fac=1.d00/mbig
        integer (kind=entero) :: i,iff,ii,inext,inextp,k
        real (kind=doblep) :: random,mj,mk,ma(55)
        save iff,inext,inextp,ma
        data iff/0/
!
        if (idum<=0.or.iff==0) then
           iff=1
           mj=abs(mseed-abs(idum))
           mj=mod(mj,mbig)
           ma(55)=mj
           mk=1
           do i=1,54
              ii=mod(21*i,55)
              ma(ii)=mk
              mk=mj-mk
              if (mk.lt.mz) mk=mk+mbig
              mj=ma(ii)
           end do
           do k=1,4
              do i=1,55
                 ma(i)=ma(i)-ma(1+mod(i+30,55))
                 if (ma(i).lt.mz) ma(i)=ma(i)+mbig
              end do
           end do
           inext=0
           inextp=31
           idum=1
        end if
        inext=inext+1
        if (inext==56) inext=1
        inextp=inextp+1
        if (inextp==56) inextp=1
        mj=ma(inext)-ma(inextp)
        if(mj.lt.mz) mj=mj+mbig
        ma(inext)=mj
        random=mj*fac
        return
        end function random
