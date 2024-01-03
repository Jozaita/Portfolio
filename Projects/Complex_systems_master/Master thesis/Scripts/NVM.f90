program NVM
implicit none
integer,parameter::dp=selected_real_kind(15,307)
real(dp),parameter::Num=1000.0d0
integer(dp),parameter::sim=10*Num
integer(dp)::apasos,a2,i
real(dp)::n,r,xm,xm2,x,xm4
real(dp)::a,dran_u,omegap,omegan,omegat,omega1,omega2,tn,t,tmax



call dran_ini(5000)
open(unit=15,file='NVM.txt',status='replace',action='write')

apasos=50
tmax=10**6.0d0
do a2=1,apasos
	xm=0.0d0
	xm2=0.0d0
	xm4=0.0d0
	a=10.0d0**(-3+3*dble(a2)/dble(apasos))
	do i=1,sim	
	n=Num/2
	t=0.0d0

		do while (t.lt.tmax)
			omegap=(a/2.0d0+(1.0d0-a)*(n/Num))*(Num-n)/Num
			omegan=(a/2.0d0+(1.0d0-a)*(Num-n)/Num)*(n/Num)
			omegat=omegap+omegan
			tn=-log(dran_u())/omegat
			t=t+tn
			r=dran_u()*omegat
			if (r.lt.omegap) then
				n=n+1
			else 
				n=n-1
			end if
		end do
		x=2*(n/Num)-1.0d0
		xm=xm+abs(x)
		xm2=xm2+x*x
		xm4=xm4+x**(4.0d0)
		!write(*,*)a,x,xm2/i,xm4/i,i
	end do
	xm=xm/dble(sim)
	xm2=xm2/dble(sim)
	xm4=xm4/dble(sim)
	xm4=1.0d0-xm4/(3.0d0*xm2**2.0d0)
	xm2=(xm2-xm**2.0d0)*num
	write(15,'(4e13.6)')a,xm,xm2,xm4
	
	write(*,*)a,xm,xm2,xm4
end do
close(unit=20)	
end program
