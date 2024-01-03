program ARC1
implicit none 
integer, parameter :: dp = selected_real_kind(15, 307)	
real(dp)::g,dran_g,start,finish,time,x,a_0,a_1,s,tfinal
integer::t

!Tiempo cero
call dran_ini(5000)
call cpu_time(start)
open(unit=30,file='ARC1.txt',status='replace',action='write')
a_0=0.5
a_1=0.5
g=dran_g()
x=g*a_0
t=1
tfinal=10
!Tiempo a partir de entonces 
do while (t.lt.tfinal)
s=a_0+a_1*x**2
g=dran_g()
x=sqrt(s)*g
write(*,*) x
write(30,*) x,s
t=t+1
end do

call cpu_time(finish)
time=finish-start
write(*,*) time
close(unit=30)
end program 

