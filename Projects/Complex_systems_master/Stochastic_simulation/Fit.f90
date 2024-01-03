program fit
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer::im,ij,i,j,ib,i_dran,k,iw
integer::m0,Measure,L
real(dp),dimension(-4:4):: h
real(dp)::dran_u,cm,ce,errorm,errore,finish,start,e0,eini,e,contador
real(dp)::rm0,rm1,e1,taummc,tauemc,corr,pa,mc
real(dp),dimension(117)::Temp,Tred,u4,rm,rm2,e2
open(unit=11,file='IsingL64.txt',action='read')
open(unit=21,file='Fit64.txt',status='replace',action='write')


L=64
write(*,*)L
do i=1,10000
read(int(11),*,END=99)Temp(i),rm(i),rm2(i),e,e2(i),errorm,taummc,cm,errore,tauemc,ce,corr,u4(i)
enddo
99 continue
do i=1,117
Tred(i)=(1.0d0-Temp(i)/2.268d0)
write(*,*)Tred(i)
if ((Tred(i))<-0.05d0)  then 
if ((Tred(i))>-0.17d0)  then 
write(int(21),'(5(f20.7,5x))')abs(Tred(i)),u4(i),rm(i),rm2(i),e2(i)
end if
end if
end do

end program

