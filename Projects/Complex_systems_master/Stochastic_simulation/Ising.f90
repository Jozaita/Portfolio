recursive subroutine addtocluster(i,s,pa,n1,n2,n3,n4)
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=8
integer::k,i,j
integer,dimension(L*L)::n1,n2,n3,n4,s
integer,dimension(4)::neigh
real(dp)::pa,dran_u
s(i)=-s(i)
neigh(1)=n1(i)
neigh(2)=n2(i)
neigh(3)=n3(i)
neigh(4)=n4(i)

do k=1,4
  j=neigh(k)
  if(s(j)==-s(i)) then
    if (dran_u()<pa) then 
      call addtocluster(j,s,pa,n1,n2,n3,n4)
      
    end if
  endif

end do

end



subroutine neighbors(n1,n2,n3,n4)

implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter::  L=8
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




program Ising
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=8
integer,parameter:: N=L*L
integer::im,ij,i,j,ib,i_dran,k,iw
integer::m0,Measure
integer,dimension(N)::s
integer,dimension(N)::n1,n2,n3,n4
real(dp),dimension(-4:4):: h
real(dp)::dran_u,cm,ce,errorm,errore,finish,start,e0,eini,e,e2
real(dp)::rm0,rm1,e1,rm,rm2,taum,taue,Temp,corr,pa,u4,mc
call cpu_time(start)
call dran_ini(5000)
open(unit=10,file='IsingL8.txt',status='replace',action='write')
M0=1000

Measure=10**4
!Initial condition
call neighbors(n1,n2,n3,n4)

do i =1,N
  if (dran_u()<0.5d0)then 
    s(i)=+1
  else
  s(i)=-1
  end if
end do


!Core
write(10,'(13(a13,5x))')'Temp','rm','rm2','e','e2','errorm','mc*taum','cm','errore','mc*taue','ce','corr','u4'
Temp=5.0d0
do while(Temp>0.0d0)
write(*,*) Temp
  do j=-4,4,2
    h(j)=min(1.0,exp(dble(-2*j)/Temp))
  end do
  do ij=1,M0*N
    i=i_dran(N)
    ib=s(i)*(s(n1(i))+s(n2(i))+s(n3(i))+s(n4(i)))
    if (ib <= 0) then
      s(i)=-s(i)
    else if (dran_u() < h(ib)) then 
    s(i)=-s(i) 
    endif
  end do
  corr=0.d0
  cm=0.d0
  ce=0.d0
  rm=0.d0
  rm2=0.d00
  e=0.d0
  u4=0.d0
  e2=0.d0
  rm1=(abs(sum(s))/dble(N))
  e1=0.d0
  do i=1,N
    e1=e1-dble(s(i)*(s(n1(i))+s(n2(i))+s(n3(i))+s(n4(i))))/dble(N)
  end do
  do im=1,Measure
    if (abs((Temp-2.26)).lt.(0.4d0)) then
       mc=0.25
    else 
       mc=1
    end if
  
      do ij=1,int(mc*N)
        i=i_dran(N)
        if (abs((Temp-2.26)).lt.(0.4d0)) then
          pa=1.0d0-exp(-2.0d0/Temp)
          call addtocluster(i,s,pa,n1,n2,n3,n4)
        else		
        ib=s(i)*(s(n1(i))+s(n2(i))+s(n3(i))+s(n4(i)))
        if (ib <= 0) then
          s(i)=-s(i)
        else if(dran_u()< h(ib)) then   
          s(i)=-s(i)
         end if
        end if
      end do
   
    e0=0.d0
    do i=1,N
      e0=e0-dble(s(i)*(s(n1(i))+s(n2(i))+s(n3(i))+s(n4(i))))/dble(N)
    end do
    
    e=e+e0
    e2=e2+e0*e0
    rm0=(abs(sum(s))/dble(N)) 
    rm=rm+rm0
    rm2=rm2+rm0*rm0
    u4=u4+rm0**4
    cm=cm+rm0*rm1
    ce=ce+e0*e1
    rm1=rm0
    e1=e0
    do i=1,N
      corr=corr+(s(i)-rm0)*(s(n1(i))+s(n2(i))+s(n3(i))+s(n4(i))-4.0d0*rm0)
    end do
    
  end do
  
  
  

  corr=abs(1.0d0/log(corr/dble(Measure)))
  e=e/dble(Measure)
  e2=(e2/dble(Measure)-e*e)
  rm=rm/dble(Measure)
  u4=u4/dble(Measure)
  rm2=(rm2/dble(Measure))
  u4=1.0d0-u4/(3.0d0*rm2**2)
  rm2=rm2-rm*rm
  cm=(cm/dble(Measure)-rm*rm)/rm2 
  ce=(ce/dble(Measure)-e*e)/e2
  if (cm.ne.1.0d0) taum=cm/(1.0d0-cm)
  if (ce.ne.1.0d0) taue=ce/(1.0d0-ce)
  errore=sqrt(e2*(2*taue+1)/dble(Measure))
  errorm=sqrt(rm2*(2*taum+1)/dble(Measure))  
  
  rm2=N*rm2/Temp
  e2=N*e2/(Temp*Temp)
  
  write(10,'(13(f13.7,5x))')Temp,rm,rm2,e,e2,errorm,mc*taum,cm,errore,mc*taue,ce,corr,u4


if (abs(Temp-2.269)<0.4d0) then 
  Temp=Temp-0.01 
else
  Temp=Temp-0.1
end if
end  do
call cpu_time(finish)
write(*,*)finish-start
end program Ising



