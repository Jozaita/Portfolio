program NVM
implicit none
integer,parameter::dp=selected_real_kind(15,307)
real(dp),parameter::Num=100.0d0 
integer,parameter::ncol=100
integer(dp),parameter::sim=10*Num
integer(dp)::tray,i
real(dp)::n,r,xm,xm2,x,xmin,xmax,pas
real(dp)::a,dran_u,omegap,omegan,omegat,omega1,omega2,tn,t,tmax
real(dp),dimension(ncol)::histo,centre


call dran_ini(5000)

a=0.001
xmin=-1
xmax=1
pas=(xmax-xmin)/ncol
do i=1,ncol
	histo(i)=0.0d0 !elements a cada columna
	centre(i)=xmin+i*pas-(pas/2.0d0) !posicio cada columna
	
enddo



tmax=10**5.0d0
do tray=1,10**3
	xm=0.0d0
	xm2=0.0d0
	
		
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

		 !if write(60,'(2f13.6)')t,n
	end do
	x=2*(n/Num)-1.0d0
	xm=xm+x
	xm2=xm2+x*x
	do i=1,ncol-1
		if ((xm.gt.centre(i)).and.(xm.lt.centre(i+1))) then 
			histo(i)=histo(i)+1.0d0
		end if				
	end do
	if (xm.gt.centre(ncol-1)) histo(ncol)=histo(ncol)+1.0d0
end do	
	
write(*,*)maxval(histo)
open(unit=50,file='NVM3.txt',status='replace',action='write')
do i=1,ncol
	write(50,'(2f13.6)')centre(i),histo(i)/dble(tray)
end do
close(unit=50)


	
end program
