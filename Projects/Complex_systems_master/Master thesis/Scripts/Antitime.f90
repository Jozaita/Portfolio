program NVM2antiagtime
implicit none
integer,parameter::dp=selected_real_kind(15,307)
real(dp),parameter::Num=1000.0d0
integer,parameter::ncol=50	 , long=50
integer(dp),parameter::sim=15
integer(dp)::tray,i,j,nmax,cont,cont2
real(dp)::n,r,xm,xm2,x,q,m
real(dp)::a,dran_u,omegat,tn,t,tmax,start,finish
real(dp),dimension(long)::omega1,omega2,omega3,omega4,nip,nin,omegas,nipm,ninm
real(dp),dimension(4)::subomega
call dran_ini(5000)
call cpu_time(start)


open(unit=40,file='NVM2antiagtimepruebi.txt',status='replace',action='write')

do i=1,long
	nipm(i)=0.0d0
	ninm(i)=0.0d0
end do
		

a=10.0d0**(-2.0d0)
tmax=10**(3)	

	
	
	!Set initial conditions 	
	
	nip(1)=Num/1.0d0
	nin(1)=0.0d0
	
	do i=2,long
		nip(i)=0.0d0
		nin(i)=0.0d0
	end do 
	!M1 evolucion temporal
	!open(unit=90,file='NVM2antiagtime.txt',status='replace',action='write')
	do tray=1,sim-1
		cont2=0
		call cpu_time(start)
		!write(*,*)x,tray-1,a,finish-start
		!Set initial conditions 	
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
		
		do while (cont.lt.5*10**6)
		cont=cont+1
		
		
		if (mod(cont,5*10**0).eq.0) then 
		
			cont2=cont2+1
			write(*,*)cont2,t,2.0d0*(n/Num)-1.0d0
			write(40,'(i5,2f13.6)')cont2,t,2.0d0*(n/Num)-1.0d0
			
		end if		
	!Fin M1

		do i=1,long
			omegas(i)=0.0d0
			omega1(i)=0.0d0
			omega2(i)=0.0d0
			omega3(i)=0.0d0	
			omega4(i)=0.0d0
			omegas(i)=0.0d0
		end do
		
		omegat=0.0d0
		do i=1,long
			omega1(i)=nip(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(1.0d0+dble(i-1))*(m/Num))
			omega2(i)=nin(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(1.0d0+dble(i-1))*(n/Num))
			omega3(i)=nip(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*((n/Num)*(dble(i-1)+1.0d0)+1.0d0))
			omega4(i)=nin(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*((m/Num)*(dble(i-1)+1.0d0)+1.0d0))
			omegas(i)=omegat+omega1(i)+omega2(i)+omega3(i)+omega4(i) 
			omegat=omegat+omega1(i)+omega2(i)+omega3(i)+omega4(i)
		end do
		
		
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
	
	
	n=0.0d0
	m=0.0d0
	do i=1,long
		n=n+nip(i)
		m=m+nin(i)
		nipm(i)=nipm(i)+(nip(i))/Num
		ninm(i)=ninm(i)+(nin(i))/Num
			
	end do
	write(40,*)" "
	write(40,*) " "
	x=2*(n/Num)-1.0d0
	

end do	



end program
