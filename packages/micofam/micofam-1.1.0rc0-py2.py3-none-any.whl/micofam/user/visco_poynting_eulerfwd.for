      subroutine sdvini(statev,coords,nstatv,ncrds,noel,npt,
     & layer,kspt)
c
      include 'ABA_PARAM.INC'
c   
      dimension statev(nstatv),coords(ncrds)
c
c Set initial Conditions for State Variables
c
      statev(1) = 0.0
      statev(2) = 0
      statev(3) = 0.0
      statev(4) = 0.0
      statev(5) = 0.0
      statev(6) = 0.0
      statev(7) = 0.0
      statev(8) = 0.0
c
      return
      end
c
c
c Forward difference time discretization at TIME
c
c      
       subroutine umat(stress, statev, ddsdde, sse, spd, scd, rpl, 
     & ddsddt, drplde, drpldt, stran, dstran, time, dtime, temp,
     & dtemp, predef, dpred, materl, ndi, nshr, ntens, nstatv,
     & props, nprops, coords, drot, pnewdt, celent, dfgrd0,
     & dfgrd1, noel, npt, kslay, kspt, kstep, kinc)
      include 'ABA_PARAM.INC'

      
      character*80 materl, path, filepath
      character*30 outdir
c      character(len=100), dimension(2) :: filepath
      integer i, j, ntens, nstatv, noel, npt, kinc, errflg, n, elstat
c
      double precision
     & stress(ntens), statev(nstatv),
     & ddsdde(ntens,ntens), stran(ntens), dstran(ntens), time(2),
     & predef(1), dpred(1), props(nprops), coords(3), drot(3,3),
     & dtime, sm, smvec(6), e1, e2, e3, evec(6)
c    
      double precision
     & sig_m(6), sig(6), sig_p(6), eps_m(6), eps(6), eps_p(6),
     & dtg, c1, c2, Dmg, dilUs, dilUe, dilU, mstress(6),
     & mstress_old(6), eps_per(6), sig_per(6), delta, mat,
     & old_stress(6), dstress(6), dU, dD, dN, dDdN, Nges,
     & dDmax, dNmaxi, dNmax, dNmin, frq, dilU_old
c
      double precision
     & D(6,6), K(6,6), Kinv(6,6), C(6,6), A0(6,6), B0(6,6), B1(6,6),
     & lambda, mu
c 
c Set path to file to save dNmax in every cycle
c
      filepath = 'D:/just_go/Skript/dNmax.txt'
c     &'C:/SIMULIA/Abaqus/6.12-1/code/python/lib/
c     &abaqus_plugins/rve_simulation/dNmax.txt'
c
c Set Cyclejump to an arbitrary high number in first increment
c
      if (Kinc.eq.1) then
       open(25, file=filepath)
      write (25,*) 1.+9
      close(25)
      endif
c
c Recover stresses, strains, and time increment from previous increment
c
      do i = 1, ntens
        sig_m(i) = stress(i)
        old_stress(i) = stress(i)
      end do
      do i = 1, ntens
        eps_m(i) = stran(i)
      end do
      eps = stran
      eps_p = stran + dstran
      sig = stress
      dtg = dtime
c
c calculate hydrostatic stress state at beginning of increment
c
      do i = 1, 3
      mstress_old(i) = (old_stress(1) + old_stress(2) + old_stress(3)) / 
     & 3.0
      end do
      mstress_old(4) = 0.
      mstress_old(5) = 0.
      mstress_old(6) = 0.
c
c get material properties and constants for subroutine
c
      c1 = props(7)
      c2 = props(8)
      dDmax = props(9)
      mat = props(10)
      freq = props(11)
      dNmin = props(12)
      dDdN = statev(1)
      n = statev(2)
      dNmaxi = statev(3)
      Nges = statev(4)
      Dmg = statev(5)
      elstat = statev(6)
      dilU = statev(7)
      dilU_old = statev(8)
c
c calculate element damage
c
      if ((time(2).gt.((n + 1) * freq - (dtime / 10.))).and.
     & (time(2).lt.((n + 1) * freq + (dtime / 10.)))) then
c
c read dNmax from file
c
        open(25, file=filepath)
        read (25,*) dNmax
        close(25)
c
c calculate damage for allowed cyclejump
c
c set allowed cyclejump to dNmin < dNmax < 100000 cycles
c
        if (n.eq.0) dNmax = 0.
        if (n.gt.0) then
        if ((dNmax.lt.dNmin).and.(dNmax.gt.0.)) dNmax = dNmin
        if (dNmax.gt.1.e+5) dNmax = 1.e+5
        endif
c
c avoid negative damage growth (healing)
c
        if (dDdN.le.0.) dDdN = 0.
c
c calculate damage after cyclejump
c
        Dmg = statev(5) + dDdN * (dble(int(dNmax)))
        if (Dmg.ge.1.) then  
          Dmg = 0.99999999
          elstat = 1
        endif
c
c count number of total cycles
c
      Nges = statev(4) + dble(int(dNmax))
      endif
c
c reset dNmax
c
      if ((time(2).gt.((n + 1) * freq + (0.9 * dtime))).and.
     & (time(2).lt.((n + 1) * freq + (1.1 * dtime)))) then
       open(25, file=filepath)
       write (25,*) 1.e+5
       close(25)
       n = statev(2) + 1
      endif
c
c calculate material tetrads from input parameters via "Lame"-constants
c
c props(1) : E1
c props(2) : nu1
c props(3) : E2
c props(4) : nu2
c props(5) : D3
c props(6) : nu3
c
      lambda = props(2) * props(1) / 
     & ((1.+props(2)) * (1.-2.*props(2)))
      mu = props(1) / (2. * (1. + props(2)))
      do i=1,ntens
        do j=1,ntens
          C(i,j) = 0.
        end do
      end do
      C(1,1) = lambda + 2. * mu
      C(2,2) = lambda + 2. * mu
      C(3,3) = lambda + 2. * mu
      C(4,4) = mu
      C(5,5) = mu
      C(6,6) = mu
      C(1,2) = lambda
      C(1,3) = lambda
      C(2,1) = C(1,2)
      C(2,3) = lambda
      C(3,1) = C(1,3)
      C(3,2) = C(2,3)
      
      lambda = props(4) * props(3) / 
     & ((1.+props(4)) * (1.-2.*props(4)))
      mu = props(3) / (2. * (1. + props(4)))
      do i=1,ntens
        do j=1,ntens
          K(i,j) = 0.
        end do
      end do
      K(1,1) = lambda + 2. * mu
      K(2,2) = lambda + 2. * mu
      K(3,3) = lambda + 2. * mu
      K(4,4) = mu
      K(5,5) = mu
      K(6,6) = mu
      K(1,2) = lambda
      K(1,3) = lambda
      K(2,1) = K(1,2)
      K(2,3) = lambda
      K(3,1) = K(1,3)
      K(3,2) = K(2,3)
      
      lambda = props(6)* props(5) / 
     & ((1.+props(6))*(1.-2.*props(6)))
      mu = props(5) / (2. * (1. + props(6)))
      do i=1,ntens
        do j=1,ntens
          D(i,j) = 0.
        end do
      end do
      D(1,1) = lambda + 2. * mu
      D(2,2) = lambda + 2. * mu
      D(3,3) = lambda + 2. * mu
      D(4,4) = mu
      D(5,5) = mu
      D(6,6) = mu
      D(1,2) = lambda
      D(1,3) = lambda
      D(2,1) = D(1,2)
      D(2,3) = lambda
      D(3,1) = D(1,3)
      D(3,2) = D(2,3)
c
c apply damage to stiffness and damping matrices
c
      C = (1.0 - Dmg) * C
      K = (1.0 - Dmg) * K
      D = (1.0 - Dmg) * D
c
c calculate matrix inverses
c
      call FINDInv(K, Kinv, 6, errflg)
      call FINDInv((matmul(D, Kinv)), A0, 6, errflg)
c      
c calculate factors for DGL
c
      B0 = matmul(C, A0)
      B1 = matmul(matmul(D, matmul( (C+K) ,Kinv)),A0)
c
c explanation of factors A0, B0 and B1 in DGL 
c
c     A0 = K/D
c     B0 = C*K/D
c     B1 = D(C+K)/K*(K/D)
c     
c calculate and update stresses
c
      call material(eps_m, eps, eps_p, sig_m, sig, sig_p, A0, B0, B1,
     & dtg, noel, npt)
c
      stress = sig_p
c
c set stresses to zero if element has failed
c
c      if (elstat.ge.1) stress(:) = 0.
c
c calculate DDSDDE
c
      delta = 1.d-6
      do j = 1, ntens
        eps_per = stran + dstran
        eps_per(j) = stran(j) + dstran(j) + delta
      call material(eps_m, eps, eps_per, sig_m, sig,
     & sig_per, A0, B0, B1, dtg, noel, npt) !!! A1 <--> A0
      ddsdde(:,j) = (sig_per - sig_p) / delta !!! sig_m <--> sig_p ?!?!
      end do
c      ddsdde = C + K  !!! Ausgeschaltet !!!
c
c damage increment calculation
c
c calculate hysteresis energy
c
c calculate hydrostatic stress state
c
      do i = 1, 3
      mstress(i) = (stress(1) + stress(2) + stress(3)) / 3.0
      end do
      mstress(4) = 0.
      mstress(5) = 0.
      mstress(6) = 0.
c      dstress = old_stress + stress
c
c calculate energy fraction
c 
      dilU = 0.5 * dot_product((mstress + mstress_old), dstran) 		! dilatational energy
c      dilU = 0.5 * dot_product(dstran,dstress)					 		! all energy
c      dilU = 0.5 * dot_product(dstran,(old_stress - mstress_old) + 	! deviatoric energy 
c     & (stress - mstress))
      dilU = statev(7) + dilU
c
c get maximum cyclejump for given damage tolerance
c
      if ((time(2).gt.((n + 1) * freq - (1.1 * dtime))).and.
     & (time(2).lt.((n + 1) * freq - (0.9 * dtime)))) then
c
      dilU = abs(dilU) 
c
c skip damage and cyclejump calculation in first cycle
c
      if (n.eq.0) then 
      dilU_old = dilU
c
c determine whether cycle is stabilized or not and calculate damage increment
c
      elseif ((abs(dilU_old - dilU)).lt.(abs(dDmax * dilU_old))) then
      dDdN  = (c1 * (dilU ** c2)) 
c      if ((Dmg + dDmax - 1.).gt.(dDmax / 2.)) dDmax = dDmax / 2. 
      dNmaxi = dDmax / dDdN
      dilU_old = dilU
      else
c
c set cyclejump to zero if no stabilized cycle has been obtained
c
      dilU_old = dilU
      dNmaxi = 0.
      endif
c
c set cyclejump to ridiculous high value for failed elements
c
      if (elstat.eq.1) dNmaxi = 1.e+9

c
c read current dNmax from file
c
        open(25, file=filepath)
        read (25,*) dNmax
        close(25)
c
c set dNmaxi as new dNmax if dNmaxi<dNmax
c
        if (dNmaxi.lt.dNmax) then
         open(25, file=filepath)
         write (25,*) dNmaxi
         close(25)
        endif
c
c reset hysteresis energy for next cycle
c
      dilU = 0.0
      endif
c
c write state variables
c
      statev(1) = dDdN
      statev(2) = n
      statev(3) = dNmaxi
      statev(4) = Nges
      statev(5) = Dmg
      statev(6) = elstat
      statev(7) = dilU
      statev(8) = dilU_old
c
c end of subroutine     
c     
      return
      end 
      
      
c###########################################################################
c
c Subroutine 'material' calculates stresses from given strains, strain increments,
c time, time increments, and old stresses
c
c###########################################################################      
      subroutine material(eps_m, eps, eps_p, sig_m, sig, sig_p,
     & A0, B0, B1, dtg, noel, npt)
     
      integer
     & i, errflg
     
      double precision
     & eps_m(6), eps(6), eps_p(6), sig_m(6), sig(6), sig_p(6),
     & A0(6,6), B0(6,6), B1(6,6), dtg, dteps(6),
     & eqn_lhs(3,3), eqn_lhs_inv(3,3), eqn_rhs(3), eqn_sol(3)
      
c Calculate strain rates
      dteps = ( eps_p - eps ) / dtg
      sig_p = sig+dtg*(matmul(B1, dteps) + matmul(B0,eps)
     & - matmul(A0, sig))
      return
      end
c      
c      
c      
      subroutine FINDInv(matrix, inverse, n, errorflag)
c
      integer n, errorflag, i, j, k, l
! errorflag: Return error status. -1 for error, 0 for normal
      double precision matrix(n,n), inverse(n,n), augmatrix(n,2*n), m
      integer FLAG = 1
     
      !Augment input matrix with an identity matrix
      do i = 1, n
        do j = 1, 2*n
          if (j .le. n ) then
            augmatrix(i,j) = matrix(i,j)
          else if ((i+n) .eq. j) then
            augmatrix(i,j) = 1
          else
            augmatrix(i,j) = 0
          endif
        end do
      end do
     
      !Reduce augmented matrix to upper traingular form
      do k =1, n-1
        if (augmatrix(k,k) .eq. 0) then
          FLAG = 0
          do i = k+1, n
            if (augmatrix(i,k) .ne. 0.) then
              do j = 1,2*n
                augmatrix(k,j) = augmatrix(k,j)+augmatrix(i,j)
              end do
              FLAG = 1
              exit
            endif
            if (FLAG .eq. 0) then
              inverse = 0
              errorflag = -1
              return
            endif
          end do
        endif
        do j = k+1, n                       
          m = augmatrix(j,k)/augmatrix(k,k)
          do i = k, 2*n
            augmatrix(j,i) = augmatrix(j,i) - m*augmatrix(k,i)
          end do
        end do
      end do
     
      !Test for invertibility
      do i = 1, n
        if (augmatrix(i,i) .eq. 0) then
          inverse = 0
          errorflag = -1
          return
        endif
      end do
     
      !Make diagonal elements as 1
      do i = 1 , n
        m = augmatrix(i,i)
        do j = i , (2 * n)                               
          augmatrix(i,j) = (augmatrix(i,j) / m)
        end do
      end do
     
      !Reduced right side half of augmented matrix to identity matrix
      do k = n-1, 1, -1
        do i =1, k
        m = augmatrix(i,k+1)
          do j = k, (2*n)
            augmatrix(i,j) = augmatrix(i,j) -augmatrix(k+1,j) * m
          end do
        end do
      end do                               
     
      !store answer
      do i =1, n
        do j = 1, n
          inverse(i,j) = augmatrix(i,j+n)
        end do
      end do
      errorflag = 0
      
      return
      end

