recursive subroutine addtocluster(used2,i,cl,n1,n2,n3,n4,atr)
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=32,N=L*L,F=5
integer::k,i,j,p,comun,cl
integer,dimension(N)::used2
integer,dimension(N,F)::atr
integer,dimension(L*L)::n1,n2,n3,n4
integer,dimension(4)::neigh

used2(i)=1
neigh(1)=n1(i)
neigh(2)=n2(i)
neigh(3)=n3(i)
neigh(4)=n4(i)

do k=1,4
	p=neigh(k)
	if ((used2(p).eq.0).and.(p.ne.0)) then
	comun=0
	do j=1,F
		if (atr(i,j).eq.atr(p,j)) comun=comun+1 
	end do	
	if (comun.eq.F) then
		cl=cl+1
			
		call addtocluster(used2,p,cl,n1,n2,n3,n4,atr)	
	end if	
	end if
	
  
      
end do

end







recursive subroutine clusternum(used,i,n1,n2,n3,n4,atr)
!integer,parameter::dp=selected_real_kind(15,307)
implicit none
integer,parameter:: L=32,N=L*L,F=5
integer::k,i,j,p,comun
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
		call clusternum(used,p,n1,n2,n3,n4,atr)	
	end if	
	end if
      
end do

end


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

subroutine density(n1,n2,n3,n4,atr,dens)
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter::  L=32, N=L*L,F=5
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

	




program AxelrodMM3_3
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=32, F=5,sim=150
integer,parameter:: N=L*L
integer::i_dran,i,j,q,comun,p,contador,k,suj,obj,o,o2,t,tmax,interr,qmax,t2,j2
integer::i2,cl,lmax,L1,ik,contador2
integer::iran_poisson,vec,m,ma,p2
integer,dimension(N,F)::atr
integer,dimension(F)::media
integer,dimension(:),allocatable::freq
integer,dimension(:),allocatable::chosen
integer,dimension(N)::n1,n2,n3,n4,used,used2
integer,dimension(4)::neigh
real(dp)::start,dens,finish,act,tmaxprom,b,dran_u,mu,tmaxvar,lmaxprom,lmaxvar,rho,tmaxvar2
real(dp),dimension(100)::smax 

call dran_ini(5000)
open(unit=70,file='AxelrodMM3Nall.txt',status='replace',action='write')

!GLOBAL
b=0.5d0
do L1=2,N-22,50
call cpu_time(start)
rho=dble(L1)/(dble(N))

allocate(chosen(L1))


!Initial condition
tmaxvar2=0.0d0
tmaxvar=0.0d0
q=25
call neighbors(n1,n2,n3,n4)


tmaxvar2=tmaxvar
tmaxprom=0.0d0
lmaxprom=0.0d0
tmaxvar=0.0d0
lmaxvar=0.0d0
allocate(freq(q))	

do t2=1,sim

do i=1,L1
	chosen(i)=0
end do

do i=1,L1
	contador2=0	
	mu=i_dran(N)
	do j=1,L1
		if (chosen(j).ne.mu) contador2=contador2+1
	end do 
	if (contador2.eq.L1) chosen(i)=mu	
end do

!Set conditions to nodes 
do i=1,N
	do j=1,F
	atr(i,j)=i_dran(q)
	end do
end do
!Set conditions to media, most frequent in nodes

do j=1,F
	do i2=1,int(q)
		freq(i2)=0
	end do
	do i=1,L1
		j2=atr(chosen(i),j)
		freq(j2)=freq(j2)+1
	end do	
		ma=0	
		do p=1,int(q)
			m=freq(p)
			if (m.gt.ma) then 
				ma=m
				p2=p
			end if
		end do
		media(j)=p2
		
end do



!Measure the active links

call density(n1,n2,n3,n4,atr,dens)


contador=0
!Dynamics

do while (dens.gt.0.0d0)
	suj=i_dran(N)
	contador2=0
	!Solo si pertenecen a chosen interaccionan con el mass media 
	do ik=1,L1
	contador2=contador2+1
	if (suj.eq.chosen(ik)) then
		mu=dran_u()
		if (mu.lt.b) then !Interaction with mass media  
			comun=0
			do i=1,F
				if (atr(suj,i).eq.media(i)) comun=comun+1
			end do
			if (comun.ne.F) then
				o=i_dran(F) 
				if (atr(suj,o).eq.media(o)) then
					o2=i_dran(F)
					do while (atr(suj,o2).eq.media(o2))
						o2=i_dran(F)
					end do
					atr(suj,o2)=media(o2)
		
				end if	
			end if
			contador=contador+1
		else 	
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
		end if
	else if (contador2.eq.L1) then 
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
	end if
	end do	
	!El mass media se tiene que actualizar
	do j=1,F
		do i2=1,int(q)
			freq(i2)=0
		end do
		do i=1,L1
			j2=atr(chosen(i),j)
			freq(j2)=freq(j2)+1
		end do	
		ma=0	
		do p=1,int(q)
			m=freq(p)
			if (m.gt.ma) then 
				ma=m
				p2=p
			end if
		end do
		media(j)=p2
		
	end do
 

			
	if (mod(contador,N).eq.0) then
		contador=0
		call density(n1,n2,n3,n4,atr,dens)
		
	end if
	
end do

do i=1,N
used(i)=0
used2(i)=0
end do
t=0
lmax=0
do i=1,N
	if (used(i).eq.0) then 
		t=t+1	
		call clusternum(used,i,n1,n2,n3,n4,atr)
	end if 
	cl=1
	if (used2(i).eq.0) then 	
		call addtocluster(used2,i,cl,n1,n2,n3,n4,atr)
		if (lmax.lt.cl) then
			lmax=cl
		end if
	end if			
end do
lmaxprom=lmaxprom+dble(lmax)
lmaxvar=lmaxvar+dble(lmax)**2.0d0
tmaxprom=tmaxprom+dble(t)
tmaxvar=tmaxvar+dble(t)**2.0d0

end do
		

tmaxprom=tmaxprom/dble(N*sim)
tmaxvar=sqrt(tmaxvar/(dble(N)**2.0d0*dble(sim))-tmaxprom**2.0d0)
lmaxprom=lmaxprom/dble(N*sim)
lmaxvar=lmaxvar/(dble(N)**2.0d0*dble(sim))
lmaxvar=sqrt(lmaxvar-lmaxprom**2.0d0)

deallocate(freq)

call cpu_time(finish)
write(70,'(5f13.6)')rho,tmaxprom,tmaxvar,lmaxprom,lmaxvar
write(*,*)rho,finish-start
write(*,*)tmaxprom,tmaxvar,lmaxprom,lmaxvar
deallocate(chosen)
!write(*,*)rho,q,lmaxvar,tmaxvar2

end do
end program AxelrodMM3_3
