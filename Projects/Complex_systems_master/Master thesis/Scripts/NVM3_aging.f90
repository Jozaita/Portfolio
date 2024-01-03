program NVM2ag
implicit none
integer,parameter::dp=selected_real_kind(15,307)
real(dp),parameter::Num=1000.0d0 , a=10.0d0**(-3.0d0)
integer,parameter::ncol=51	 , long=3000
integer(dp),parameter::sim=10*Num
integer(dp)::tray,i,j,nmax,cont,maximo
real(dp)::n,r,xm,xm2,x,xmin,xmax,pas,q,pas2,xmin2,m
real(dp)::dran_u,omegat,tn,t,tmax,start,finish,taup,taun
real(dp),dimension(ncol)::histo,centre,histo2,centre2
real(dp),dimension(long)::omega1,omega2,omega3,omega4,nip,nin,omegas,nipm,ninm
real(dp),dimension(4)::subomega
call dran_ini(5000)


xmin=-1
xmin2=0
xmax=1
pas=(xmax-xmin)/ncol
pas2=(xmax-xmin2)/ncol
do i=1,ncol
	histo(i)=0.0d0
	histo2(i)=0.0d0
	centre(i)=xmin+i*pas-(pas/2.0d0)
	centre2(i)=xmin2+i*pas2-(pas2/2.0d0)			
enddo

do i=1,long
	nipm(i)=0.0d0
	ninm(i)=0.0d0
end do
		


tmax=2*10**(3)	
do tray=1,sim
	call cpu_time(finish)
	!Set initial conditions 
	nmax=1	
	nip(1)=Num/2.0d0
	nin(1)=Num/2.0d0
	n=Num/2.0d0
	m=Num/2.0d0
	do i=2,long
		nip(i)=0.0d0
		nin(i)=0.0d0
	end do 
	t=0.0d0
	!M1 evolucion temporal
	cont=0
	call cpu_time(start)
	!open(unit=90,file='NVM2agtime.txt',status='replace',action='write')
	do while (t.lt.1*10**3)
		cont=cont+1
		!if ((cont.eq.1000).and.(tray.eq.1)) then 
		!	cont=0
		!write(*,*)t,n
		!	write(90,'(2f13.6)')t,n
		!end if
		
			
	!Fin M1

		do i=1,nmax+1
			omegas(i)=0.0d0
			omega1(i)=0.0d0
			omega2(i)=0.0d0
			omega3(i)=0.0d0	
			omega4(i)=0.0d0
			omegas(i)=0.0d0
		end do
		
		omegat=0.0d0
		taup=0.0d0
		taun=0.0d0	
		do i=1,nmax+1
			omega1(i)=nip(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(m/Num))
			omega2(i)=nin(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(n/Num))
			omega3(i)=nip(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(n/Num+1.0d0+dble(i-1)))
			omega4(i)=nin(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(m/Num+1.0d0+dble(i-1)))
			omegas(i)=omegat+omega1(i)+omega2(i)+omega3(i)+omega4(i) 
			omegat=omegat+omega1(i)+omega2(i)+omega3(i)+omega4(i)
			
		end do
		
		!write(*,*)omegat,nmax
		tn=-log(dran_u())/omegat
				
		r=dran_u()*omegat
		
		
		if (r.lt.omegas(1)) then !borrar, construir unvector para todos
			j=1
		else if (r.gt.omegas(1)) then  
			j=1
			do while (r.gt.omegas(j))
				j=j+1
			end do
		end if
		
		subomega(1)=omega1(j)
		subomega(2)=subomega(1)+omega2(j)
		subomega(3)=subomega(2)+omega3(j)
		subomega(4)=subomega(3)+omega4(j)
		if (j.gt.nmax) nmax=j			
		if (j.gt.1) then		
			r=r-omegas(j-1)
		end if
		
		

		if (r.lt.subomega(1)) then 
			nip(j)=nip(j)-1.0d0
			nin(1)=nin(1)+1.0d0
			n=n-1.0d0
			m=m+1.0d0
			t=t+tn
		
		else if (r.lt.subomega(2)) then 
			nin(j)=nin(j)-1.0d0
			nip(1)=nip(1)+1.0d0
			n=n+1.0d0
			m=m-1.0d0
			t=t+tn
			
			
		else if (r.lt.subomega(3)) then 
			nip(j)=nip(j)-1.0d0
			nip(j+1)=nip(j+1)+1.0d0
			t=t+tn
			
			
		else if (r.lt.subomega(4)) then 
			nin(j)=nin(j)-1.0d0
			nin(j+1)=nin(j+1)+1.0d0
			t=t+tn
			
			
		end if
		
		
	end do
	
	maximo=1
	do i=1,nmax+1
		nipm(i)=nipm(i)+(nip(i))/Num
		ninm(i)=ninm(i)+(nin(i))/Num
		if ((nip(maximo)+nin(maximo)).lt.(nip(i)+nin(i))) maximo=i		
	end do
	
	x=2*(n/Num)-1.0d0
	call cpu_time(finish)
	write(*,*)tray,x,finish-start,maximo	
	if (x.lt.centre(1)) histo(1)=histo(1)+1.0d0
	if (x**2.lt.centre2(1)) histo2(1)=histo2(1)+1.0d0 
	do i=1,ncol-2
		if ((x.gt.centre(i)).and.(x.lt.centre(i+1))) then 
			histo(i+1)=histo(i+1)+1.0d0
		end if
		if ((x**2.gt.centre2(i)).and.(x**2.lt.centre2(i+1))) then 
			histo2(i+1)=histo2(i+1)+1.0d0
		end if				
	end do
	if (x.gt.centre(ncol-1)) histo(ncol)=histo(ncol)+1.0d0
	if (x**2.gt.centre2(ncol-1)) histo2(ncol)=histo2(ncol)+1.0d0
end do	

	
open(unit=20,file='NVM2aga01.txt',status='replace',action='write')
open(unit=80,file='NVM2ag2a01.txt',status='replace',action='write')
write(20,'(4f13.6)')centre(1),centre2(1),histo(1)/((centre(1)-xmin)*dble(sim-1)),histo2(1)/(centre(1)*dble(sim-1))
do i=2,ncol-1
	write(20,'(4f13.6)')centre(i),centre2(i),histo(i)/((centre(i)-centre(i-1))*dble(sim-1)),& 
	histo2(i)/((centre2(i)-centre2(i-1))*dble(sim-1))
	
end do
write(20,'(4f13.6)')centre(ncol),centre2(ncol),histo(ncol)/((xmax-centre(ncol))*dble(sim-1)),histo2(ncol)/(centre(ncol)*dble(sim-1))

do i=1,long
	write(80,'(i5,3f13.6)')i,nipm(i)/dble(sim-1),ninm(i)/dble(sim-1),(nipm(i)+ninm(i))/dble(sim-1)
end do
close(unit=50)


	
end program
