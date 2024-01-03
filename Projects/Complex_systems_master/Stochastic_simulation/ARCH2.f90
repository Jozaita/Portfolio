program ARCH2
implicit none
integer, parameter :: dp = selected_real_kind(15, 307)
integer,parameter:: p=1,tfinal=10**7
integer,parameter::q=0
real(dp),dimension(p+1)::alpha,beta
real(dp)::suma,x,sigma,dran_gbmw,start,finish,m1,m2,m4,bts,m2t,m4t
real(dp)::ale
integer::i,t,k,k2,kfinal,k2final,j

call cpu_time(start)
call dran_ini(5000)


open(unit=35,file='ARCH1k.txt',status='replace',action='write')
open(unit=36,file='ARCH1m2.txt',status='replace',action='write')
!We perform the same operations as before but with two counters to make the heatmap
kfinal=100
k2final=100

do k=0,100
	do k2=0,100
!Definition of variables
	suma=0.d0
	m1=0.d0
	m2=0.d0
	m4=0.d0
	alpha(2)=dble(k)*0.01*1.0d0/dsqrt(3.0d0)
	beta(2)=0.0d0
	alpha(1)=1-alpha(2)-beta(2)
	beta(1)=0.0d0

	if (2*alpha(2)**2+(alpha(2)+beta(2))**2.0d0>1.0d0) then
		m2=-1
		m4=-1 
		write(35,'((3(f13.7)))') alpha(2),beta(2),m4/(m2**2.0d0)-3.0d0
		write(36,'((3(f13.7)))') alpha(2),beta(2),m2
	else
		x=dsqrt(alpha(1))*dran_gbmw()   
		do t=1,tfinal
    			sigma=alpha(1)+alpha(2)*dble(x)**dble(2.0d0)+beta(1)+beta(2)*sigma
    			ale=dran_gbmw()
    			x=dsqrt(sigma)*ale 
    			suma=suma+x   
    			m1=m1+x
    			m2=m2+x**2.0d0
    			m4=m4+x**4.0d0
    			m8=m8+x**8.0d0
!write(15,'(i10,(4(f13.7,5x)))')t,x,sigma,suma,std
		end do 	
		m1=m1/tfinal
		m2=m2/tfinal 
		m4=m4/tfinal



		write(35,'((3(f13.7)))') alpha(2),beta(2),m4/(m2**2.0d0)-3.0d0
		write(36,'((3(f13.7)))') alpha(2),beta(2),m2

	end if
	call cpu_time(finish)
	write(*,*)finish-start
	end do
end do


 
end program 



