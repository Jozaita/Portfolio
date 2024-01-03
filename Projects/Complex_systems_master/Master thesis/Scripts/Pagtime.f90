program NVMptime 
implicit none
integer,parameter::dp=selected_real_kind(15,307)
real(dp),parameter::Num=1000.0d0 , a=5.0d0*10.0d0**(-2.0d0), rho=0.05d0
integer,parameter::ncol=51	 , long=10000
integer(dp),parameter::sim=15
integer(dp)::tray,i,j,nmax,cont
real(dp)::n,r,xm,xm2,x,xmin,xmax,pas,q,pas2,xmin2,m,omega5,omega6,nxp,nxpm,nxn,nxnm,omegat2
real(dp)::dran_u,omegat,tn,t,tmax,start,finish,taup,taun,taumin,taumaj
real(dp),dimension(ncol)::histo,centre,histo2,centre2
real(dp),dimension(long)::omega1,omega2,omega3,omega4,nip,nin,omegas,nipm,ninm
real(dp),dimension(4)::subomega
call dran_ini(5000)
call cpu_time(start)

	
open(unit=90,file='NVM2pagtimea.txt',status='replace',action='write')
	
do tray=1,sim
	call cpu_time(finish)
	!write(*,*)x,tray-1,a,finish-start
	!Set initial conditions 	
	nmax=0
	nip(1)=rho*Num/2.0d0
	nin(1)=rho*Num/2.0d0
	nxp=(1.0d0-rho)*Num/2.0d0
	nxn=(1.0d0-rho)*Num/2.0d0
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
		if (mod(cont,5*10**4).eq.0) then 
			
			taup=0.0d0
			taun=0.0d0
			do i=1,long
				taup=taup+dble(i-1)*nip(i)
				taun=taun+dble(i-1)*nin(i)	
			end do
			taup=taup/(n-nxp)
			taun=taun/(m-nxn)
			!write(*,*)t,cont,n,taup,taun,nmax
			write(90,'(5f20.5)')dble(cont),t,2.0d0*(n/N)-1.0d0,taup,taun
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
		taup=0.0d0
		taun=0.0d0
		do i=1,long
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
			if (j.gt.nmax) nmax=j
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
	
	
write(90,*)" "
write(90,*)" "	
end do
	
end program
