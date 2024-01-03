program Ejercicio48
implicit none
integer, parameter :: dp = selected_real_kind(15, 307)	
real(kind=dp)::u,alpha,x,dran_u,plt1,r,s,p,v
integer::i,M,n,n1,nbins,j,o
real(kind=dp),dimension(:),allocatable::suc,x0,x1
integer::AllocateStatus
call dran_ini(5000)
alpha=0.5d0
n=1
M=10**3
r=0.d0
s=0.d0
open(unit=7,file='Ejercicio48.txt',status='replace',action='write')
allocate(suc(1))
do i=1,M
u=dran_u()
v=dran_u()
plt1=(1.0d0+alpha)
p=plt1*u
if (p<1.0d0) then 
x=p**(1.0d0/alpha)
if (v<exp(-x)) then
suc(n)=x
n=n+1
deallocate(suc)
allocate(suc(n+1))
end if 
end if
if (p<1.0d0) then 
x=-log((plt1-p)/alpha)
if (v<x**(alpha-1.0d0)) then
suc(n)=x
n=n+1
deallocate(suc)
allocate(suc(n+1))
end if
end if
end do
nbins=10
!allocate(x0(nbins+1))
!allocate(x1(nbins))
!do i=1,size(x0)
!x0(i)=(maxval(suc)-minval(suc))*i/(nbins*size(suc))
!end do
!do i=0,size(suc)
!o=0
!do j=0,size(x0)
!if (suc(i)>x0(j)) then 
!o=o+1
!else
!end if
!end do
!x1(o)=x1(o)+1 
!end do
!r=dble(n)/dble(M)

write(7,'(1f10.8)')suc
end program 
