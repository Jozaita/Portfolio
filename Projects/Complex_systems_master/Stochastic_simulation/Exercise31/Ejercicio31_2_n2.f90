program Ejercicio31_2_n2
!Uniform Sampling for one dimension
implicit none 
integer, parameter :: dp = selected_real_kind(15, 307)	
real(dp), parameter :: PI = 4 * atan (1.0_16)
real(dp)::dran_u,u,r,s,g,a,b,u2
integer::i,M

call dran_ini(5000)
a=0.0d0
b=1.0d0
r=0.d0
s=0.d0
M=10**7
open(unit=2,file='Ejercicio31_2_n2.txt',status='replace',action='write')
do i=1,M
u=dran_u()/(b-a)
u2=dran_u()/(b-a)
g=(b-a)*exp(-0.5d0*(u*u+u2*u2))*cos(u*u2)*cos(u*u2)
r=r+g
s=s+g*g
end do
r=r/dble(M)
s=s/dble(M)
s=sqrt((s-r*r)/dble(M))

write(*,'(f10.6,a,f10.6)') r, '+/-',s
write(2,'(f10.6,a,f10.6)') r, '+/-',s


close(unit=2)
end program 
