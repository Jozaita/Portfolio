
subroutine Potencial(rxp,ryp,rzp,fxp,fyp,fzp,L,nump,dens,Epot,deriv,deriv2)
implicit none
integer, parameter :: ikind=selected_real_kind(p=15), pi=3.14159265
real (kind=ikind) :: dx,dy,dz,r2,epsilon,sigma,sigma2,fr6,fmod,fxi,fyi,fzi,rcorte,rcorte2,L
real (kind=ikind),Dimension(nump),intent(in)::rxp,ryp,rzp
real (kind=ikind),Dimension(nump),intent(out)::fxp,fyp,fzp
integer :: i,j
integer,intent(in)::nump
real (kind=ikind), intent(in):: dens
real (kind=ikind) , intent(out):: Epot,deriv,deriv2
epsilon=1.0d0
sigma=1.0d0
sigma2=sigma*sigma
rcorte=5.0d0*sigma
rcorte2=rcorte*rcorte
!Colocamos las fuerzas  iniciales a 0 y apagamos el potencial
Epot=0.d0
      deriv=0.d0
      deriv2=0.d0
  do i=1,nump
  fxp(i)=0.d0
  fyp(i)=0.d0
  fzp(i)=0.d0
  
  end do
  !Colocamos el algoritmo que sume fuerzas a cada distancia y potenciales. Tener en cuenta la condicion radio de corte 
  do i=1,nump-1
  do  j=i+1,nump
    dx=rxp(i)-rxp(j)
    dy=ryp(i)-ryp(j)
    dz=rzp(i)-rzp(j)
            dx=dx-L*dnint(dx/L)	 
			dy=dy-L*dnint(dy/L)	
			dz=dz-L*dnint(dz/L)	

    r2=dx*dx+dy*dy+dz*dz
    if (r2<rcorte2) then 
      fr6=(sigma2/r2)**3.0d0
          fmod=48.d0*epsilon*fr6*(fr6-0.5d0)/r2
          deriv=-fmod
          deriv2=(24.d0*epsilon/r2)*(26.d0*fr6**2.d0-7.d0*fr6)
      fxi=fmod*dx
      fyi=fmod*dy
      fzi=fmod*dz
      !Sumamos las fuerzas sobre cada particula y aplicamos accion reaccion 
      fxp(i)=fxp(i)+fxi
      fxp(j)=fxp(j)-fxi
      fyp(i)=fyp(i)+fyi
      fyp(j)=fyp(j)-fyi
      fzp(i)=fzp(i)+fzi
      fzp(j)=fzp(j)-fzi
      Epot=Epot+4.0d0*epsilon*fr6*(fr6-1.0d0)
          
  end if
  end do
  end do
  !Introducimos la correccion de largo alcance para la energia potencial 
   Epot=Epot-nump*(8.0d0*pi*dens)/(3.d0*rcorte**3.0d0)
end subroutine Potencial




































