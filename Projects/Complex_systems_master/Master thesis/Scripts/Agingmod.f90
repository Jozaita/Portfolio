

subroutine neighbors(n1,n2,n3,n4)

implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter::  L=64
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




program Agingmod
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=32,ncol=51
integer,parameter:: N=L*L,sim=10*N
real,parameter:: a=10.0d0**(-4.0d0)
integer::i_dran,tray,i,al1,al3,a2
integer(dp)::t,mc
integer,dimension(N)::s
integer,dimension(N)::n1,n2,n3,n4,age
integer,dimension(4)::neigh
real(dp)::xm,xm2,xmin,xmax,pas,q,pas2,xmin2
real(dp),dimension(ncol)::histo,centre,histo2,centre2
real(dp),dimension(3000)::agemaj,agemin
real(dp)::dran_u,start,al2,al4,al5,x,finish
real(dp),dimension(3000)::nip,nin,omegas,nipm,ninm
real(dp)::mtemp,m,m2,m4,taumaj,taumin


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

do i=1,3000
	nipm(i)=0.0d0
	ninm(i)=0.0d0
end do


open(unit=20,file='Agingmodtime.txt',status='replace',action='write')
mc=1000
m=0.0d0
m2=0.0d0
m4=0.0d0
do i=1,size(agemaj)
	agemaj(i)=0.0d0
	agemin(i)=0.0d0
end do
call cpu_time(start)
do tray=1,sim
		
	do i =1,N
  		if (dran_u().lt.0.5d0)then 
    			s(i)=1
  		else
  			s(i)=0
		end if
  		age(i)=0
	end do
!Empieza la dinamica
	do t=1,mc*N
		!Escoger agente 
		al1=i_dran(N)
		!Escoger free will o social interaction 	
		al2=dran_u()
		if (al2.gt.a) then !social interaction
			al5=dran_u()
			neigh(1)=n1(al1)
			neigh(2)=n2(al1)
			neigh(3)=n3(al1)
			neigh(4)=n4(al1)
			al3=i_dran(4)
			if (al5.lt.dble(age(neigh(al3)))/(dble(age(al1))+dble(age(neigh(al3))))) then
			
				if (s(al1).eq.s(neigh(al3))) then 
					age(al1)=age(al1)+1
				else 
					age(al1)=0
				end if
				s(al1)=s(neigh(al3))
			else 	
				age(al1)=age(al1)+1
			end if
		else !free will
			al4=dran_u()
			if (al4.gt.0.5d0) then 
				age(al1)=age(al1)+1	
			else 
			age(al1)=0
			s(al1)=abs(1-s(al1))
			end if
		end if
		if ((mod(t,N).eq.0).and.(tray.eq.1)) then 
			write(20,'(i13,f13.6)')t,sum(s)/dble(N)
			!write(*,*)t,sum(s)/dble(N)
		end if
		
	end do
	x=dble(sum(s))
	mtemp=2*x/dble(N)-1.0d0
	m=m+abs(mtemp)
	m2=m2+mtemp**2.0d0
	m4=m4+mtemp**4.0d0	
	if (mtemp.gt.0.0d0) then 
		do i=1,N
			if (s(i).eq.1) agemaj(age(i)+1)=agemaj(age(i)+1)+1.0d0
			if (s(i).eq.0) agemin(age(i)+1)=agemin(age(i)+1)+1.0d0
		end do			
	else if (mtemp.lt.0.0d0) then
		do i=1,N 
			if (s(i).eq.0) agemaj(age(i)+1)=agemaj(age(i)+1)+1.0d0
			if (s(i).eq.1) agemin(age(i)+1)=agemin(age(i)+1)+1.0d0
		end do	
	end if
		call cpu_time(finish)
		x=2*(x/N)-1.0d0
		write(*,*)tray,a,mtemp,finish-start
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
	taumaj=0.0d0
	taumin=0.0d0
	do i=1,size(agemaj)	
		taumaj=taumaj+agemaj(i)*dble(i-1)/sum(agemaj)
		taumin=taumin+agemin(i)*dble(i-1)/sum(agemin)
	end do
	m=m/dble(sim)
	m2=m2/dble(sim)
	m4=m4/dble(sim)
	

	m4=1.0d0-m4/(3.0d0*m2**2.0d0)
	m2=(m2-m**2.0d0)*N
	write(*,*)m,m2,m4,taumaj,taumin,taumaj-taumin	
	

open(unit=50,file='Agingp01.txt',status='replace',action='write')
open(unit=70,file='Agingp201.txt',status='replace',action='write')
write(50,'(4f13.6)')centre(1),centre2(1),histo(1)/((centre(1)-xmin)*dble(sim-1)),histo2(1)/(centre(1)*dble(sim-1))
do i=2,ncol-1
	write(50,'(4f13.6)')centre(i),centre2(i),histo(i)/((centre(i)-centre(i-1))*dble(sim-1)),& 
	histo2(i)/((centre2(i)-centre2(i-1))*dble(sim-1))
	
end do
write(50,'(4f13.6)')centre(ncol),centre2(ncol),histo(ncol)/((xmax-centre(ncol))*dble(sim-1)),histo2(ncol)/(centre(ncol)*dble(sim-1))

do i=1,3000
	write(70,'(i5,3f13.6)')i,nipm(i)/dble(sim-1),ninm(i)/dble(sim-1),(nipm(i)+ninm(i))/dble(sim-1)
end do
close(unit=50)
	
	
	
end program 


