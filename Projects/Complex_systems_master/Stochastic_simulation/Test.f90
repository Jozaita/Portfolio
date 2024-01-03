
implicit double precision (a-h,o-z)

xm=0.0
xm2=0.0
M=10000000
ii=5000
   call dran_ini(ii)
do i=1,M
   u=dran_u()
   print*, u 
   xm=xm+u
   xm2=xm2+u*u
enddo
xm=xm/M
xm2=xm2/M-xm*x
write(6,*) xm, xm2
end

