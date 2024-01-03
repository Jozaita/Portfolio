program Ejercicio31_3_n2
!Simpson for two dimensions
implicit none 
integer, parameter :: dp = selected_real_kind(15, 307)	
real(kind=dp), parameter :: PI = 4 * atan (1.0_16)
real(kind=dp)::u,r,s,a,b,f0,f1,f2,h,j,x0,x1,x2,f,y0,y1,y2
integer::i,N,k,p
a=0.0d0
b=1.0d0
r=0.d0
s=0.d0
N=10
h=(b-a)/dble(N)
f0=0.d0
f1=0.d0
f2=0.d0
open(unit=2,file='Ejercicio31_3_n2.txt',status='replace',action='write')
do i=1,N/2
j=dble(i)
x0=a+2*j*h-2*h
x1=a+2*j*h-h
x2=a+2*j*h
do k=i,N/2
p=dble(k)
y0=a+2*p*h-2*h
y1=a+2*p*h-h
y2=a+2*p*h
f0=f0+f(x0,y0)
f1=f1+f(x1,y1)
f2=f2+f(x2,y2)
enddo
enddo 
r=(f0+4.0d0*f1+f2)*(h/3.0d0)
s=1.0d0/90.0d0*((b-a)/2.0d0)**5
write(*,*)r
write(2,'(f10.6)') r 
close(unit=2)
end program 

function f(x,y)
implicit none
integer, parameter :: dp = selected_real_kind(15, 307)	
real(kind=dp), intent(in)::x,y
real(kind=dp)::f
f=exp(-0.5d0*(x*x+y*y))*cos(x*y)**2
return
end function f	
