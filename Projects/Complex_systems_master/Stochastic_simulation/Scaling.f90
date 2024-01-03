program scaling 
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer::im,ij,i,j,ib,i_dran,k,iw
integer::m0,Measure,L
real(dp),dimension(-4:4):: h
real(dp)::dran_u,cm,ce,errorm,errore,finish,start,e0,eini,e,contador
real(dp)::rm0,rm1,e1,taummc,tauemc,corr,pa,mc
real(dp),dimension(117)::Temp,Tred,u4,rm,rm2,e2
open(unit=11,file='IsingL64.txt',action='read')
open(unit=12,file='IsingL32.txt',action='read')
open(unit=13,file='IsingL16.txt',action='read')
open(unit=14,file='IsingL8.txt',action='read')
open(unit=15,file='IsingL4.txt',action='read')

open(unit=21,file='Scaling64.txt',status='replace',action='write')
open(unit=22,file='Scaling32.txt',status='replace',action='write')
open(unit=23,file='Scaling16.txt',status='replace',action='write')
open(unit=24,file='Scaling8.txt',status='replace',action='write')
open(unit=25,file='Scaling4.txt',status='replace',action='write')



do j=1,5
L=2**(7-j)
write(*,*)L
do i=1,10000
read(int(10+j),*,END=99)Temp(i),rm(i),rm2(i),e,e2(i),errorm,taummc,cm,errore,tauemc,ce,corr,u4(i)
enddo
99 continue
do i=1,117
Tred(i)=dble(L)**(1.0d0)*(1.0d0-Temp(i)/2.268d0)
e2(i)=dble(L)**(0.0d0)*e2(i)
write(int(20+j),'(5(f20.7,5x))')Tred(i),u4(i),rm(i),rm2(i),e2(i)
end do
end do
end program


