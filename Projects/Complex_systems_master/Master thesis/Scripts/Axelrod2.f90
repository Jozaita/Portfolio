integer function iran_poisson(q)
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer:: q
real(dp) :: u,dran_u

u=dran_u()
iran_poisson=0
do while(u > exp(-dble(q)))
u=u*dran_u()
iran_poisson=iran_poisson+1
enddo
end function iran_poisson







recursive subroutine addtocluster(used,i,t,n1,n2,n3,n4,atr)
!integer,parameter::dp=selected_real_kind(15,307)
implicit none
integer,parameter:: L=64,N=L*L,F=10
integer::k,i,j,t,p,comun
integer,dimension(N)::used
integer,dimension(N,F)::atr
integer,dimension(L*L)::n1,n2,n3,n4
integer,dimension(4)::neigh

used(i)=1
neigh(1)=n1(i)
neigh(2)=n2(i)
neigh(3)=n3(i)
neigh(4)=n4(i)

do k=1,4
	p=neigh(k)
	if (used(p).eq.0) then
	comun=0
	do j=1,F
		if (atr(i,j).eq.atr(p,j)) comun=comun+1 
	end do	
	if (comun.eq.F) then
		t=t+1
			
		call addtocluster(used,p,t,n1,n2,n3,n4,atr)	
	end if	
	end if
	
  
      
end do

end


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

subroutine density(n1,n2,n3,n4,atr,dens)
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter::  L=64, N=L*L,F=10
integer,dimension(4)::neigh
integer,dimension(N)::n1,n2,n3,n4
integer,dimension(N,F)::atr
integer::comun,k,i,j,p
real(dp)::dens
dens=0
do i=1,N
	
	neigh(1)=n1(i)
	neigh(2)=n2(i)
	neigh(3)=n3(i)
	neigh(4)=n4(i)
	do k=1,4
		p=neigh(k)
		comun=0
		do j=1,F
			if (atr(i,j).eq.atr(p,j)) comun=comun+1 
		end do	
		if ((comun.ne.0).and.(comun.ne.F)) dens=dens+1.0d0/dble(4*N)	
	end do
end do

end subroutine density


program Axelrod2
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=64, F=10
integer,parameter:: N=L*L
integer::i_dran,i,j,q,comun,p,contador,k,suj,obj,o,o2,t,tmax,interr,qmax,t2,sim
integer::iran_poisson,vec
integer,dimension(N,F)::atr
integer,dimension(N)::n1,n2,n3,n4,used
integer,dimension(4)::neigh
real(dp)::start,dens,finish,act,tmaxprom
real(dp),dimension(100)::smax 

call dran_ini(5000)
open(unit=20,file='AxelrodL64i2.txt',status='replace',action='write')

!GLOBAL
qmax=500

!Initial condition
call neighbors(n1,n2,n3,n4)
do q=2,102,5
tmaxprom=0
call cpu_time(start)
do t2=1,N
!Set conditions to nodes 
do i=1,N
	do j=1,F
	atr(i,j)=i_dran(q)
	end do
end do
!Measure the active links

call density(n1,n2,n3,n4,atr,dens)


contador=0
!Dynamics
do while (dens.gt.0.0d0)
	suj=i_dran(N)
	neigh(1)=n1(suj)
	neigh(2)=n2(suj)
	neigh(3)=n3(suj)
	neigh(4)=n4(suj)
	vec=i_dran(4)
	obj=neigh(vec)
	comun=0
	do i=1,F
		if (atr(suj,i).eq.atr(obj,i)) comun=comun+1
	end do
	if (comun.ne.F) then
	
	o=i_dran(F) 
	if (atr(suj,o).eq.atr(obj,o)) then
		o2=i_dran(F)
		do while (atr(suj,o2).eq.atr(obj,o2))
			o2=i_dran(F)
			
		end do
	
	atr(suj,o2)=atr(obj,o2)
		
	end if	
	end if
	contador=contador+1
	if (mod(contador,N).eq.0) then
		contador=0
		call density(n1,n2,n3,n4,atr,dens)
		
	end if
end do

do i=1,N
used(i)=0
end do
tmax=0
do i=1,N
	t=1	
	call addtocluster(used,i,t,n1,n2,n3,n4,atr)
	if (tmax.lt.t) then
		tmax=t
	end if

				
end do
tmaxprom=tmaxprom+dble(tmax)
if (mod(dble(t2),dble(N)/100.0d0).eq.0) write(*,*)t2,N**2
end do
		
call cpu_time(finish)
tmaxprom=tmaxprom/dble(N*N)
write(*,*)tmaxprom,q,finish-start
write(20,'(i5,f13.6)')q,tmaxprom
end do
call cpu_time(finish)
write(*,*)finish-start
end program Axelrod2
