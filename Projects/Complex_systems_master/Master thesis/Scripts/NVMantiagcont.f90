program NVMantiagcont
implicit none
integer,parameter::dp=selected_real_kind(15,307)
real(dp),parameter::Num=3000.0d0 
integer,parameter:: long=100
integer(dp),parameter::sim=100
integer(dp)::tray,i,j,nmax,cont,apasos,a2
real(dp)::n,r,xm,xm2,xm4,x,q,m,taumaj,taumin,taudif,a,tcont,conta,tconta
real(dp)::dran_u,omegat,tn,t,tmax,start,finish,mmaj,mmin
real(dp),dimension(long)::omega1,omega2,omega3,omega4,nip,nin,omegas,nmin,nmaj
real(dp),dimension(4)::subomega
call dran_ini(5000)

open(unit=90,file='NVManticonta.txt',action='write')
	
apasos=40

do a2=1,apasos
	xm=0.0d0
	xm2=0.0d0
	xm4=0.0d0
	taumin=0.0d0
	taumaj=0.0d0
	mmaj=0.0d0
	mmin=0.0d0
	do j=1,long
	nmaj(j)=0.0d0
	nmin(j)=0.0d0
	end do
	taudif=0.0d0
	a=10.0d0**(-3.0d0+3*dble(a2)/dble(apasos))
	tmax= 10.0d0**(3.0d0)
	conta=0
	tconta=0.0d0	
	do tray=1,sim
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
		tcont=0.0d0
		!M1 evolucion temporal
		cont=0
		tcont=0.0d0
		
		do while (t.lt.tmax)
		cont=cont+1
		tcont=tcont+tn
		
			
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
		tcont=tcont/cont
		tconta=tconta+tcont
		conta=conta+cont
		
		
		if (x.gt.0.0d0) then 
			do i=1,long
				nmaj(i)=nmaj(i)+nip(i)
				nmin(i)=nmin(i)+nin(i)
						
			end do
		else if (x.lt.0.0d0) then
			do i=1,long
				nmaj(i)=nmaj(i)+nin(i)
				nmin(i)=nmin(i)+nip(i)			
			end do
		end if
		xm=xm+abs(x)
		xm2=xm2+x*x
		xm4=xm4+x**(4.0d0)
	
	end do
	tconta=tconta/sim
	conta=dble(conta)/sim
	write(*,*)a,tconta,conta
	write(90,'(3f13.6)')a,tconta,conta
	do i=1,long
		nmaj(i)=nmaj(i)/dble(sim)
		nmin(i)=nmin(i)/dble(sim)		
	end do
	do i=1,long
	taumaj=taumaj+nmaj(i)*dble(i-1)
	taumin=taumin+nmin(i)*dble(i-1)
	mmaj=mmaj+nmaj(i)
	mmin=mmin+nmin(i)
	end do
	do i=1,long
		nmaj(i)=nmaj(i)/dble(sim)
		nmin(i)=nmin(i)/dble(sim)		
	end do
	do i=1,long
	taumaj=taumaj+nmaj(i)*dble(i-1)
	taumin=taumin+nmin(i)*dble(i-1)
	mmaj=mmaj+nmaj(i)
	mmin=mmin+nmin(i)
	end do
	xm=xm/dble(sim)
	xm2=xm2/dble(sim)
	xm4=xm4/dble(sim)
	taumaj=taumaj/mmaj
	taumin=taumin/mmin
	taudif=taumaj-taumin
	xm4=1.0d0-xm4/(3.0d0*xm2**2.0d0)
	xm2=(xm2-xm**2.0d0)*num
	call cpu_time(finish)
	
	
end do
close(unit=20)	
end program
