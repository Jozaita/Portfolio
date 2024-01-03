




program MFag3
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: N=1000,sim=1000
integer::i_dran,tray,i,al1,al3,a2,rho2
integer(dp)::t,mc,b,cont
integer,dimension(N)::s,eti 
integer,dimension(N)::age,lista
real(dp),dimension(20000)::agemaj,agemin
real(dp)::dran_u,start,al2,al4,al5,a,sumaj,sumin,finish
real(dp)::mtemp,m,m2,m4,taumaj,taumin,x,rho


call dran_ini(5000)
open(unit=42,file='Pruebe3.txt',status='replace',action='write')

 close(unit=42)
mc=2*10**3

!Initial condition

do rho2=1,10,1
	rho=dble(rho2)*0.01d0+0.2d0
	
	do a2=1,20
		call cpu_time(start)
		a=0.005d0*a2
		m=0.0d0
		m2=0.0d0
		m4=0.0d0
		
		do i=1,size(agemaj)
			agemaj(i)=0.0d0
			agemin(i)=0.0d0
		end do
		do tray=1,sim


			do i=1,N
  				if (dran_u().lt.0.5d0)then 
  				else
    					s(i)=1
  					s(i)=0
  				end if
				age(i)=0
  				
			end do
			
			do i=1,N			
				lista(i)=i
			end do
			cont=0
			do while(cont.lt.int((1.0d0-rho)*N))
				b=i_dran(N)
				if (0.ne.lista(b)) then 
					age(b)=-1
					lista(b)=0
					cont=cont+1
				end if
			end do
			
		!Empieza la dinamica
			do t=1,mc*N
		!Escoger agente 
			al1=i_dran(N)
			
		!Escoger free will o social interaction 	
			al2=dran_u()
			if (al2.gt.a) then !social interaction
				al5=dran_u()
				if (al5.lt.1.0d0/(dble(age(al1))+2.0d0)) then
					al3=i_dran(N)
					if (age(al1).gt.-1) then 
						if (s(al1).eq.s(al3)) then 
							age(al1)=age(al1)+1		
						else 
							age(al1)=0
						end if
					end if
					s(al1)=s(al3)
				else 	
					if (age(al1).gt.-1) age(al1)=age(al1)+1
				end if
			else !free will
				al4=dran_u()
				if (al4.gt.0.5d0) then 
					if (age(al1).gt.-1) age(al1)=age(al1)+1 
				else 
					if (age(al1).gt.-1) age(al1)=0
				s(al1)=abs(1-s(al1))
				end if
			end if
			!if ((mod(t,10**2*N).eq.0).and.(tray.eq.1)) then 
			!	write(20,'(i13,f13.6)')t,2*sum(s)/dble(N)-1.0d0
			!end if	
			end do
			x=dble(sum(s))
			mtemp=2*x/dble(N)-1.0d0
			m=m+abs(mtemp)
			m2=m2+mtemp**2.0d0
			m4=m4+mtemp**4.0d0	
			if (mtemp.gt.0.0d0) then 
				do i=1,N
					if (age(i).gt.0) then
						if (s(i).eq.1) agemaj(age(i)+1)=agemaj(age(i)+1)+1.0d0
						if (s(i).eq.0) agemin(age(i)+1)=agemin(age(i)+1)+1.0d0
					end if
				end do			
			else if (mtemp.lt.0.0d0) then
				do i=1,N 
					if (age(i).gt.0) then
						if (s(i).eq.0) agemaj(age(i)+1)=agemaj(age(i)+1)+1.0d0
						if (s(i).eq.1) agemin(age(i)+1)=agemin(age(i)+1)+1.0d0
				        end if 
				end do	
			end if
		
		!write(*,*)tray,a,mtemp,finish-start
		
		end do
	taumaj=0.0d0
	taumin=0.0d0
	m=m/dble(sim)
	m2=m2/dble(sim)
	m4=m4/dble(sim)
	sumaj=sum(agemaj)
	sumin=sum(agemin)
	do i=1,size(agemaj)	
	taumaj=taumaj+agemaj(i)*dble(i-1)/sumaj
	taumin=taumin+agemin(i)*dble(i-1)/sumin
	end do
	
	m4=1.0d0-m4/(3.0d0*m2**2.0d0)
	m2=(m2-m**2.0d0)*N
	
	call cpu_time(finish)
	open(unit=42,file='Pruebe3.txt',status='old',position='append',action='write')
	write(42,'(8f13.6)')a,rho,m,m2,m4,taumaj,taumin,taumaj-taumin
	write(*,*)a,rho,m,m2,m4,taumaj,taumin,taumaj-taumin
	write(*,*)finish-start
	close(unit=42)
	
	end do
write(42,'(a5)')" "	
end do

end program 


