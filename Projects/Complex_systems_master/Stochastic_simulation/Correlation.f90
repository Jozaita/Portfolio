program correlation
implicit none 
integer,parameter::dp=selected_real_kind(15,307)
integer::im,ij,i,j,ib,i_dran,k,iw,tau
integer::m0,Measure,L
real(dp),dimension(-4:4):: h
real(dp)::dran_u,cm,ce,errorm,errore,finish,start,e0,eini,e,contador
real(dp)::rm0,rm1,e1,taummc,tauemc,corr,pa,mc
real(dp),dimension(117)::Temp,Tred,u4,rm,rm2,e2
real(dp),dimension(100)::corr2
real(dp),dimension(10**5)::mtemp2
open(unit=32,file='Corr.txt',action='read')
do i=1,10**9
read(32,*,END=99) mtemp2(i)

enddo
99 continue

do tau=1,10**2
do i =1,int(10**4-10**2)
corr2(tau)=corr2(tau)+mtemp2(i)*mtemp2(i+tau)
!write(*,*)corr2(tau),mtemp2(i),mtemp2(i+tau)
end do
write(*,*)corr2(tau), tau
end do





end program correlation 
