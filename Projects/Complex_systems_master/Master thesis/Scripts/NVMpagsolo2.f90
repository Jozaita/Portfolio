program NVMpagsolo2
implicit none
integer,parameter::dp=selected_real_kind(15,307)
real(dp),parameter::Num=1000.0d0,rho=0.20d0
integer,parameter:: long=5000
integer(dp),parameter::sim=Num
integer(dp)::tray,i,j,cont,apasos,a2,rho2,nmax
real(dp)::n,r,xm,xm2,xm4,x,q,m,taumaj,taumin,iprom,ivar,a
real(dp)::dran_u,omegat,tn,t,tmax,start,finish,mmaj,mmin,taup,taun,nxp,nxpm
real(dp)::nxn,nxnm,omegat2,omega5,omega6
real(dp),dimension(long)::omega1,omega2,omega3,omega4,nip,nin,omegas,nmaj,nmin
real(dp),dimension(4)::subomega
call dran_ini(5000)

open(unit=72,file='NVMpag022.txt',status='new',action='write')
 close(unit=72)
	
apasos=20
do a2=1,10
a=dble(a2)*2.5d0*10.0d0**(-3.0d0)+2.5d0*10.0d0**(-2.0d0)

	call cpu_time(start)
	xm=0.0d0
	xm2=0.0d0
	xm4=0.0d0
	nmax=1
	taumin=0.0d0
	taumaj=0.0d0
	mmaj=0.0d0
	mmin=0.0d0
	do j=1,long
	nmaj(j)=0.0d0
	nmin(j)=0.0d0
	end do
	
	tmax=2*10**(3)	
	do tray=1,sim
	call cpu_time(finish)
	!write(*,*)x,tray-1,a,finish-start
	!Set initial conditions 	
	
	nip(1)=int(rho*Num/2.0d0+0.1)
	nin(1)=int(rho*Num/2.0d0+0.1)
	nxp=int((1.0d0-rho)*Num/2.0d0)
	nxn=int((1.0d0-rho)*Num/2.0d0)
	
	n=Num/2.0d0
	m=Num/2.0d0
	do i=2,long
		nip(i)=0.0d0
		nin(i)=0.0d0
	end do 
	
	t=0.0d0
	!M1 evolucion temporal
	  cont=0
	!open(unit=90,file='NVM2pagtime.txt',status='replace',action='write')
	do while (cont.lt.2*10**6)
		cont=cont+1
		!if ((cont.eq.1000).and.(tray.eq.1)) then 
		!	cont=0
		!	write(*,*)t,n
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
			omega1(i)=rho*nip(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(m/Num))
			omega2(i)=rho*nin(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(n/Num))
			omega3(i)=rho*nip(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(n/Num+1.0d0+dble(i-1)))
			omega4(i)=rho*nin(i)*(a/2.0d0+(1.0d0-a)/(2.0d0+dble(i-1))*(m/Num+1.0d0+dble(i-1)))
			omegas(i)=omegat+omega1(i)+omega2(i)+omega3(i)+omega4(i) 
			omegat=omegat+omega1(i)+omega2(i)+omega3(i)+omega4(i)
			
		end do
		omega5=(1.0d0-rho)*nxp*(a/2.0d0+(1.0d0-a)*m)
		omega6=(1.0d0-rho)*nxn*(a/2.0d0+(1.0d0-a)*n)
		omegat2=omega5+omega6
		r=dran_u()
		!write(*,*)omegat,nmax
		
				
		
		if (rho.gt.r) then 
			r=dran_u()*omegat
			tn=-log(dran_u())/omegat
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
		else if(rho.lt.r) then 
			r=dran_u()*omegat2
			tn=-log(dran_u())/omegat2
			if (r.lt.omega5) then
				nxp=nxp-1.0d0
				nxn=nxn+1.0d0 
				n=n-1.0d0
				m=m+1.0d0
				t=t+tn
			else 
				nxp=nxp+1.0d0
				nxn=nxn-1.0d0
				n=n+1.0d0
				m=m-1.0d0
				t=t+tn
			end if
		end if 
		end do
	
	
	
		
		
		x=2*(n/Num)-1.0d0
		!write(*,*)rho,tray,x
		
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
	do i=1,nmax+1
		nmaj(i)=nmaj(i)/dble(sim)
		nmin(i)=nmin(i)/dble(sim)		
	end do
	do i=1,nmax+1
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
	
	xm4=1.0d0-xm4/(3.0d0*xm2**2.0d0)
	xm2=(xm2-xm**2.0d0)*num
	call cpu_time(finish)
	open(unit=72,file='NVMpag022.txt',status='old',position='append',action='write')
	write(72,'(8e13.6)')a,rho,xm,xm2,xm4,taumaj,taumin,taumaj-taumin
	close(unit=72)
	!write(*,*)a,rho,xm,xm2,xm4,taumaj,taumin,taumaj-taumin,finish-start
end do


!Entre el primer y el sgundo bucle, '' ''
	
end program		
