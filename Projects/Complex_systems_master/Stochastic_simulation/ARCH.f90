program GARCH
implicit none
integer, parameter :: dp = selected_real_kind(15, 307)
integer,parameter:: p=1,tfinal=10**8
real(dp),dimension(p+1)::alpha,beta
real(dp)::suma,x,sigma,dran_g,start,finish,m1,m2,m4,s2,s3,bts,m2t,m4t
real(dp)::ale,m8,std
integer::i,t
call cpu_time(start)
call dran_ini(5000)

open(unit=18,file='ARCH5example.txt',status='replace',action='write')
!open(unit=28,file='ARCH1ac.txt',status='replace',action='write')


!Definition of variables and parameters
beta(1)=0.d0
suma=0.d0
m1=0.d0
m2=0.d0
m4=0.d0
!!!!!!!!!!!!
alpha(1)=0.1d0
alpha(2)=0.2d0
beta(2)=0.7d0
x=dsqrt(alpha(1))*dran_g()   
do t=1,tfinal
    sigma=alpha(1)+alpha(2)*dble(x)**dble(2.0d0)+beta(1)+beta(2)*sigma !Recursive relation
    ale=dran_g()
    x=dsqrt(sigma)*ale   !Generation of return price
    std=dsqrt(sigma) 
    suma=suma+x   
    m1=m1+x
    m2=m2+dble(x)**2.0d0
    m4=m4+dble(x)**4.0d0
    m8=m8+dble(x)**8.0d0
!Depending on the quantity of data we want to extract, the if can be activated.
!if (mod(t,10**5).eq.0.0d0) then
write(18,'(i10,(4(f13.7,5x)))')t,x,sigma,suma,std
!end if
end do 	
m1=m1/tfinal
m2=m2/tfinal 
m4=m4/tfinal
!Theoretical quantities
m2t=alpha(1)/(1.0d0-alpha(2)-beta(2))
m4t=(3.0d0-3.0d0*(alpha(2)+beta(2))**2.0d0)/(1.0d0-3.0d0*alpha(2)**2.0d0&
&-2.0d0*alpha(2)*beta(2)-beta(2)**2.0d0)*m2t**2.0d0
bts=m4t/m2t**2.0d0-3.0d0

!Depending on the data we want to extract, we can activate this
!write(28,'((7(f13.7,5x)))')m1,m2,m2t,m4,m4t,m4/(m2**2.0d0)-3.0d0,bts


call cpu_time(finish)
write(*,*)finish-start
end program 



