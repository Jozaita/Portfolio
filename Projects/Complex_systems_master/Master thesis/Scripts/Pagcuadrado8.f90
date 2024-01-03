

subroutine neighbors(n1,n2,n3,n4)

implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter::  L=32
integer::ix,iy,ix1,iy2,ix3,iy4,i
integer, dimension(L*L)::n1,n2,n3,n4
do ix=1,L
  do iy=1,L
    i=(iy-1)*L+ix
    ix1=ix+1
    iy2=iy+1
    ix3=ix-1
    iy4=iy-1
    if(ix1==L+1) ix1=1
    n1(i)=(iy-1)*L+ix1
    if(iy2==L+1) iy2=1
    n2(i)=(iy2-1)*L+ix
    if (ix3==0) ix3=L
    n3(i)=(iy-1)*L+ix3
     if(iy4==0) iy4=L
    n4(i)=(iy4-1)*L+ix
  end do
end do
end subroutine neighbors




program Pagcuadrado8
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=32
integer,parameter:: N=L*L,sim=N
integer::i_dran,tray,i,al1,al3,a2,rho2,rho
integer(dp)::t,mc,b,cont
integer,dimension(N)::s,eti 
integer,dimension(N)::n1,n2,n3,n4,age,lista
integer,dimension(4)::neigh
real(dp),dimension(5000)::agemaj,agemin
real(dp)::dran_u,start,al2,al4,al5,a,sumaj,sumin,finish
real(dp)::mtemp,m,m2,m4,taumaj,taumin,x

call cpu_time(start)
call dran_ini(5000)
open(unit=47,file='PagL328.txt',status='replace',action='write')
!open(unit=20,file='PagL8time.txt',status='replace',action='write')
 close(unit=47)
mc=2*10**5

!Initial condition
call neighbors(n1,n2,n3,n4)
do rho2=8,8
	rho=16*rho2+160
	do a2=1,10
		a=0.0015d0*a2
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
			do while(cont.lt.(N-rho))
				b=i_dran(N)
				if (b.eq.lista(b)) then 
					age(b)=-1
					lista(b)=0
					cont=cont+1
				end if
			end do
			
		!Empieza la dinamica
			do t=1,mc*N
		!Escoger agente 
			al1=i_dran(N)
			!write(*,*)age(i)
		!Escoger free will o social interaction 	
			al2=dran_u()
			if (al2.gt.a) then !social interaction
				al5=dran_u()
				if (al5.lt.1.0d0/(dble(age(al1))+2.0d0)) then
					neigh(1)=n1(al1)
					neigh(2)=n2(al1)
					neigh(3)=n3(al1)
					neigh(4)=n4(al1)
					al3=i_dran(4)
					if (age(al1).gt.-1) then 
						if (s(al1).eq.s(neigh(al3))) then 
							age(al1)=age(al1)+1		
						else 
							age(al1)=0
						end if
					end if
					s(al1)=s(neigh(al3))
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
			!if (mod(t,10**2*N).eq.0) then 
			!	write(20,'(i13,f13.6)')t,sum(s)/dble(N)
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
	open(unit=47,file='PagL328.txt',status='old',position='append',action='write')
	write(47,'(8f13.6)')a,dble(rho)/dble(N),m,m2,m4,taumaj,taumin,taumaj-taumin
	close(unit=47)
	write(*,*)a,rho/N,m,m2,m4,taumaj,taumin,taumaj-taumin
	write(*,*)finish-start	
	end do	
end do

end program 


