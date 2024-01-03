program neighbors

implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer(dp),parameter::  L=4
integer(dp)::ix,iy,ix1,iy2,ix3,iy4,i
integer(dp), dimension(L*L)::n1,n2,n3,n4
do ix=1,L
  do iy=1,L
    i=(iy-1.0d0)*L+ix
    ix1=ix+1.0d0
    iy2=iy+1.0d0
    ix3=ix-1.0d0
    iy4=iy-1.0d0
    if(ix1==L+1.0d0) ix1=1.0d0
    n1(i)=(iy-1.0d0)*L+ix1
    if(iy2==L+1.0d0) iy2=1.0d0
    n2(i)=(iy2-1.0d0)*L+ix
    if (ix3==0.d0) ix3=L
    n3(i)=(iy-1.0d0)*L+ix3
    if(iy4==0.0d0) iy4=L
    n4(i)=(iy4-1.0d0)*L+ix
  end do
end do
do i=1,L*L
write(*,*)n1(i),n2(i)

end do
end program

