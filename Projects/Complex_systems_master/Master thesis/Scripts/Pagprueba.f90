

subroutine neighbors(n1,n2,n3,n4)

implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter::  L=32
integer::ix,iy,ix1,iy2,ix3,iy4,i
integer, dimension(L*L)::n1,n2,n3,n4
do ix=1,L
  do iy=1,L
    i=(iy-1)*L+ix
    ix1=ix+1
    iy2=iy+1
    ix3=ix-1
    iy4=iy-1
    if(ix1==L+1) ix1=1
    n1(i)=(iy-1)*L+ix1
    if(iy2==L+1) iy2=1
    n2(i)=(iy2-1)*L+ix
    if (ix3==0) ix3=L
    n3(i)=(iy-1)*L+ix3
     if(iy4==0) iy4=L
    n4(i)=(iy4-1)*L+ix
  end do
end do
end subroutine neighbors




program Pagcuadrado
implicit none
integer,parameter::dp=selected_real_kind(15,307)
integer,parameter:: L=32,sim=1
integer,parameter:: N=L*L
integer::i_dran,tray,i,al1,al3,a2,rho2,rho
integer(dp)::t,mc,b
integer,dimension(N)::s,eti 
integer,dimension(N)::n1,n2,n3,n4,age
integer,dimension(4)::neigh
real(dp)::dran_u,start,al2,al4,al5,a
real(dp)::mtemp,m,m2,m4

call cpu_time(start)
call dran_ini(5000)

open(unit=20,file='PagL8time.txt',status='replace',action='write')

mc=2*10**5

!Initial condition
call neighbors(n1,n2,n3,n4)
rho=N/16
a=0.03
		do tray=1,sim


			do i=1,N
  				if (dran_u().lt.0.5d0)then 
					s(i)=1
  				else
    					
  					s(i)=0
  				end if
				age(i)=0
  				
			end do
			do i=1,N-rho 
				b=i_dran(N)
				age(b)=-1
			end do
			
		!Empieza la dinamica
			do t=1,mc*N
		!Escoger agente 
			al1=i_dran(N)
		!Escoger free will o social interaction 	
			al2=dran_u()
			if (al2.gt.a) then !social interaction
				al5=dran_u()
				if (al5.lt.1.0d0/(dble(age(al1))+2.0d0)) then
					neigh(1)=n1(al1)
					neigh(2)=n2(al1)
					neigh(3)=n3(al1)
					neigh(4)=n4(al1)
					al3=i_dran(4)
					if (age(al1).gt.-1) then 
						if (s(al1).eq.s(neigh(al3))) then 
							age(al1)=age(al1)+1		
						else 
							age(al1)=0
						end if
					end if
					s(al1)=s(neigh(al3))
				else 	
					age(al1)=age(al1)+1
				end if
			else !free will
				al4=dran_u()
				if (al4.gt.0.5d0) then 
					age(al1)=age(al1)+1	
				else 
				age(al1)=0
				s(al1)=abs(1-s(al1))
				end if
			end if
			
			if (mod(t,100*N).eq.0) then 
				write(20,'(i13,f13.6)')t,2*sum(s)/dble(N)-1.0d0
				
			end if	
			end do
			mtemp=2*sum(s)/dble(N)-1.0d0
			write(*,*)mtemp
			
		end do

end program 


