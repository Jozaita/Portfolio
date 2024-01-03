program Ejercicio28
implicit none 
integer, parameter :: dp = selected_real_kind(15, 307)	
real(dp), parameter :: PI = 4 * atan (1.0_16)
real(dp)::dran_u,fx,dx,u,x,xn,a,y,aver,var,g,s,ref,sigma,start,finish,time,ef,refef

integer::i,sim

call dran_ini(5000)
a=1.0d0
open(unit=2,file='Ejercicio28.txt',status='replace',action='write')
do while (a.gt.0)
call cpu_time(start)
sim=10**7
aver=0.d0
var=0.d0
do i=1,sim
u=dran_u()
x=u
xn=x-(fx-u)/dx
do while (abs(xn-x)>0.000001)
fx=6.0d0/(3.0d0+a)*(1.0d0*x+x*x*(a-1.0d0)/2.0d0-(a/3.0d0)*x*x*x)
dx=6.0d0/(3.0d0+a)*(1.0d0+x*(a-1.d0)-a*x*x)
xn=x
x=x-(fx-u)/dx
enddo
y=dble(x)
g=cos(0.5*(PI*y))/(6.0d0/(3.0d0+a)*(1.0d0+y*(a-1.d0)-a*y*y))
aver=aver+g
var=var+g*g
enddo
aver=aver/dble(sim)
var=var/dble(sim)
s=sqrt((var-aver*aver)/dble(sim))
if (a==1) then 
ref=s
end if 
sigma=s/ref
call cpu_time(finish)
time=finish-start
ef=var*time
if(a==1) then
refef=ef
end if
ef=refef/ef
write(*,'(f10.7,5x,a,5x,a,f6.3)') sigma,'s/s(a(0))','a=',a
write(2,'(f10.7,5x,f3.2,5x,f10.7,5x,f10.7)') sigma,a,aver,s,ef,refef

a=a-0.01d0
end do
close(unit=2)
end program 





