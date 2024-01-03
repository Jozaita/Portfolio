program correlation 
implicit none
integer, parameter :: dp = selected_real_kind(15, 307)
integer,parameter:: p=1,tfinal=10**8
integer,parameter::q=0
real(dp),dimension(p+1)::alpha,beta
real(dp)::ale,cov1,cov2,cov3
real(dp),dimension(10**2)::cov
real(dp),dimension(:),allocatable::t,x,sigma,suma
integer::i,n,t1,contador


open(unit=12,file='ARCH5example.txt',action='read')
open(unit=42,file='Corr3example.txt',action='write')

allocate(t(10**8))
allocate(x(10**8))
allocate(sigma(10**8))
allocate(suma(10**8))

do i=1,10**8
    read(12,*) t(i),x(i),sigma(i),suma(i)

enddo

do n=1,10**2
    cov1=0.d0
    cov2=0.d0
    cov3=0.d0
    contador=0
    do t1=1,10**8-10**2 
        cov1=cov1+x(t1)**2.0d0*x(t1+n)**2.0d0
        cov2=cov2+x(t1)**2.0d0
        cov3=cov3+x(t1+n)**2.0d0
        contador=contador+1

    end do
    cov1=cov1/dble(contador)
    cov2=cov2/dble(contador)
    cov3=cov3/dble(contador)
    cov(n)=cov1-cov2*cov3
    write(42,'((i10,f13.7))')n,cov(n)
end do

end program correlation 

