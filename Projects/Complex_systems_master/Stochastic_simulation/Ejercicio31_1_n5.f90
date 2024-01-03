program Ejercicio31_1_n5
!Hit and miss for five dimensions
implicit none 
integer, parameter :: dp = selected_real_kind(15, 307)	
real(dp), parameter :: PI = 4 * atan (1.0_16)
real(dp)::dran_u,a,b,d,p,v,x1,u,r,s,w,u2,u3,u4,u5
integer::i,M,n

call dran_ini(5000)
n=0
a=0.0d0
b=1.0d0
M=10**7
open(unit=2,file='Ejercicio31_1_n5.txt',status='replace',action='write')
do i=1,M
u=dran_u()
u2=dran_u()
u3=dran_u()
u4=dran_u()
u5=dran_u()
v=dran_u()
x1=exp(-0.5d0*(u*u+u2*u2+u3*u3+u4*u4+u5*u5))*cos(u*u2+u2*u3+u3*u4+u4*u5+u5*u)**2
d=10.d0
if (x1>d*v) then
n=n+1
end if
end do
p=dble(n)/dble(M)
r=(b-a)*d*p
s=sqrt(p*(1.0d0-p)/M)*d*(b-a)

write(*,'(f10.5,a,f10.5)') r, '+/-',s
write(2,'(f10.5,a,f10.5)') r, '+/-',s


close(unit=2)
end program 
