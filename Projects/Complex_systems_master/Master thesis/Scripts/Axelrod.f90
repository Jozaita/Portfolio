recursive subroutine addtocluster(used,cluster,i,linki,linko,linkd)
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=10,N=L*L
integer::k,i,j,cluster,suj,obj,ij,i2,obj2
integer,dimension(2*N)::linki,linko,linkd,used
integer,dimension(4)::neigh


used(i)=1

suj=linko(i)
obj=linkd(i)

do ij=1,2*N
	obj2=linkd(ij)
	
	if (suj.eq.obj2) then	
	i2=ij
	
	end if
end do

neigh(1)=i
neigh(2)=i2
neigh(3)=mod(i+N,2*N+1)
neigh(4)=mod(i2+N,2*N)

do k=1,4
	j=neigh(k)
	
  		if (linki(j).eq.1) then
			if (used(j).eq.0) then
    				cluster=cluster+1 
							
      				call addtocluster(used,cluster,j,linki,linko,linkd)
			end if
		end if  
end do
end



subroutine neighbors(n1,n2,n3,n4)

implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter::  L=10
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




program Axelrod
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=10, F=10
integer,parameter:: N=L*L
integer::i_dran,i,j,q,comun,suj,obj,o,o2,k,cluster,lustermax,ik,indice
integer,dimension(N,F)::atr
integer,dimension(2*N)::linko,linkd,linka,linki,used
integer,dimension(N)::n1,n2,n3,n4
real(dp)::start,dens,finish
real(dp),dimension(100)::smax
call cpu_time(start)
call dran_ini(5000)
open(unit=10,file='AxelrodL4.txt',status='replace',action='write')


indice=0	
do q=2,102
indice=indice+1

!Initial condition
call neighbors(n1,n2,n3,n4)

!Set conditions to nodes 
do i=1,N
	do j=1,F
	atr(i,j)=i_dran(q)
  
	end do
end do

!Measure the active links 
do i=1,N
	linko(i)=i
	linkd(i)=n1(i)
end do
do j=1,N
	linko(j+N)=j
	linkd(j+N)=n2(j)
end do
do i=1,2*N,1
	comun=0
	do j=1,F
		if (atr(linko(i),j).eq.atr(linkd(i),j)) then
			comun=comun+1
		end if
	end do
			
	if (comun.eq.0) then 
		linka(i)=0
		linki(i)=0
	else if (comun.eq.F) then
		linki(i)=1
		linka(i)=0
	else 
		linki(i)=0
		linka(i)=1
	
	end if
	
end do

dens=dble(sum(linka))/dble(2*N) 
!write(*,*)dens
!Enable the dynamics
do while (dens.gt.0.0d0)
	k=i_dran(2*N)
	if (linka(k).eq.1) then
		suj=linko(k)
		obj=linkd(k)
		!if (q.gt.22) write(*,*)k,suj,obj,linka(k)
		o=i_dran(F)
		if (atr(suj,o).eq.atr(obj,o)) then
			o2=i_dran(F)
			do while (atr(suj,o2).eq.atr(obj,o2))
				o2=i_dran(F)
				!write(*,*)atr(suj,o2),atr(obj,o2),o2
			end do
			atr(suj,o2)=atr(obj,o2)
		end if
	end if
	do i=1,2*N 
		comun=0
		do j=1,F
			if (atr(linko(i),j).eq.atr(linkd(i),j)) then
				comun=comun+1
			end if
		end do	
		if (comun.eq.0) then 
			linka(i)=0
			linki(i)=0
		else if (comun.eq.F) then
			linka(i)=0
			linki(i)=1
		else 
			linka(i)=1
			linki(i)=0
		end if
	end do
	dens=dble(sum(linka))/dble(2*N) 
	write(*,*)sum(linka)	

end do

write(*,*)dens
lustermax=0

do ik=1,2*N
used(ik)=0
end do

do ik=1,2*N
	if (linki(ik).eq.1) then
		if (used(ik).eq.0) then
			cluster=1	
			call addtocluster(used,cluster,ik,linki,linko,linkd)
			if (lustermax.lt.cluster) then
				lustermax=cluster
			end if
		end if 
				
	end if
end do	
call cpu_time(finish)
smax(indice)=dble(lustermax)/dble(2*N)
write(*,*)smax(indice),q,finish-start

end do



end program Axelrod2
