      SUBROUTINE SDVINI(STATEV,COORDS,NSTATV,NCRDS,NOEL,NPT,
     & LAYER,KSPT)
C
      INCLUDE 'ABA_PARAM.INC'
C   
      DIMENSION STATEV(NSTATV),COORDS(NCRDS)
C*** SET INITIAL CONDITIONS FOR STATE VARIABLES ***C
      STATEV(1) = 0.0
      STATEV(2) = 0.0
      STATEV(3) = 0.0
      STATEV(4) = 0
      STATEV(5) = 0.0
      STATEV(6) = 0.0
      STATEV(7) = 0.0
      STATEV(8) = 0
C
      RETURN
      END
      subroutine umat(stress, statev, ddsdde, sse, spd, scd, rpl, 
     & ddsddt, drplde, drpldt, stran, dstran, time, dtime, temp,
     & dtemp, predef, dpred, materl, ndi, nshr, ntens, nstatv,
     & props, nprops, coords, drot, pnewdt, celent, dfgrd0,
     & dfgrd1, noel, npt, kslay, kspt, kstep, kinc)
      include 'ABA_PARAM.INC'
C     
      character*80 materl, path
      character*30 outdir
C
      integer ntens, nstatv, noel, npt, step, counter, kinc
      double precision
     & stress(ntens), statev(nstatv), tch,
     & ddsdde(ntens,ntens), stran(ntens), dstran(ntens), time(2),
     & predef(1), dpred(1), props(nprops), coords(3), drot(3,3),
     & delta, strain_per(6)
C
      double precision
     & strant(6), tstrant(6), cfull(6,6), cfulln(6,6)
C
      integer 
     & N, ELSTAT
      double precision
     & E, G, nu, dU, dN, dD, dDdN, NG, D, N0, atemp,
     & S11, S22, S33, S12, S13, S23, SEQ, C1, C2, C3, C4, CEL,
     & p, SP1, SP2, SP3, UDIL, UROT, UGES, mat
      logical writesdvflg 
C*** GET MATERIAL PROPERTIES, STRESSES AND STRAINS ***C
      E = props(1)
      nu = props(2)
      C1 = props(3) 
      C2 = props(4) 
      C3 = props(5) 
      C4 = props(6)
      dN = props(7)
      mat = props(8)
      CEL = celent
      N0 = STATEV(1)
      NG = STATEV(2)
      D = STATEV(3)
      N = STATEV(4)
      dD = STATEV(7)
      ELSTAT = STATEV(8)
      S11 = stress(1)
      S22 = stress(2)
      S33 = stress(3)
      S12 = stress(4)
      S13 = stress(5)
      S23 = stress(6)
      p = (2.0 / 3.0)
C*** MISES EQUIVALENT STRESS ***C
C      SEQ = sqrt(0.5 * ((S11 - S22) ** 2.0 + (S22 - S33) ** 2.0 + (S33
C     & - S11) ** 2.0) + 3.0 * (S12 ** 2.0 + S13 ** 2.0 + S23 ** 2.0))
C*** CALCULATE ENERGY DENSITY AND DAMAGE EVOLUTION ***C
      IF ((TIME(1).GT.((2 * N + 1) * 0.02 - 0.005)).AND.(TIME(1).LT.
     & ((2 * N + 1) * 0.02 + 0.005))) THEN 
C
      dU = 2.0 * ((1.0 - 2.0 * nu) / (6.0 * (1.0 - D ** p)  
     & * E)) * (S11 + S22 + S33) ** 2.0
      N0 = C1 * dU ** C2
      STATEV(1) = N0
C
      IF (mat.EQ.0.0) THEN
      dU = 2.0 * ((1.0 - 2.0 * nu) / (6.0 * (1.0 - D ** p)  
     & * E)) * (S11 + S22 + S33) ** 2.0
C      dU = 1.0 / ((1.0 - D ** p) * E) * (S11 ** 2.0 + S22 ** 2.0 + 
C     & S33 ** 2.0) - (2.0 * nu) / ((1.0 - D ** p) * E) * (S11 * S22 + 
C     & S11 * S33 + S22 * S33) + ((1.0 + nu) * 2.0) / 
C     & ((1.0 - D ** p) * E) * (S12 ** 2.0 +  S13 ** 2.0 + S23 ** 2.0)
      ENDIF
      IF (mat.EQ.1.0) THEN
      IF (S33.LT.0.0) THEN
      S33 = 0.0
      ENDIF
      dU = 2.0 * ((1.0 - 2.0 * nu) / (6.0 * (1.0 - D ** p) 
     & * E)) * (S11 + S22 + S33) ** 2.0
C      dU = 1.0 / ((1.0 - D ** p) * E) * (S11 ** 2.0 + S22 ** 2.0 + 
C     & S33 ** 2.0) - (2.0 * nu) / ((1.0 - D ** p) * E) * (S11 * S22 + 
C     & S11 * S33 + S22 * S33) + ((1.0 + nu) * 2.0) / 
C     & ((1.0 - D ** p) * E) * (S12 ** 2.0 +  S13 ** 2.0 + S23 ** 2.0)
      ENDIF
      NG = STATEV(2) + dN
      STATEV(2) = NG
      IF (STATEV(2).GT.STATEV(1)) THEN
      dDdN = (C3 * dU ** C4) 
      dD = dDdN * dN
      IF (dD.LT.0.0) THEN
      dD = 0.0
      ENDIF
      ENDIF
      ENDIF
      IF ((TIME(1).GT.((2 * N + 2) * 0.02 - 0.005)).AND.(TIME(1).LT.
     & ((2 * N + 2) * 0.02 + 0.005))) THEN
      D = (STATEV(3) + dD) 
      N = STATEV(4) + 1
      IF ((D ** p).GT.1.0) THEN
      D = 0.99999
      ELSTAT = 1
      ELSEIF (D.LT.0.0) THEN
      D = 0.0
      ENDIF
      ENDIF
C
C*** CALCULATE STIFFNESS MATRIX OF DAMAGED MATERIAL ***C
C*** CURRENT STRAINS, STRESSES, AND DAMAGE VARIABLES  ***C
C
C*** STIFFNESS OF DAMAGED MODEL ***C
      cfull = 0.0
      atemp = (1.0 + nu) * (1.0 - 2.0 * nu)
      cfull(1,1) = (1.0 - D ** p) * (1.0 - nu) * E / atemp
      cfull(2,2) = (1.0 - D ** p) * (1.0 - nu) * E / atemp
      cfull(3,3) = (1.0 - D ** p) * (1.0 - nu) * E / atemp
      cfull(1,2) = (1.0 - D ** p) * nu * E / atemp
      cfull(2,1) = (1.0 - D ** p) * nu * E / atemp
      cfull(1,3) = (1.0 - D ** p) * nu * E / atemp
      cfull(3,1) = (1.0 - D ** p) * nu * E / atemp
      cfull(2,3) = (1.0 - D ** p) * nu * E / atemp
      cfull(3,2) = (1.0 - D ** p) * nu * E / atemp
      cfull(4,4) = (1.0 - D ** p) * E / (2.0 * (1.0 + nu))
      cfull(5,5) = (1.0 - D ** p) * E / (2.0 * (1.0 + nu))
      cfull(6,6) = (1.0 - D ** p) * E / (2.0 * (1.0 + nu))
C
C*** SET STATE VARIABLES ***C 
      STATEV(1) = N0
      STATEV(3) = D 
      STATEV(4) = N
      STATEV(5) = D ** p
      STATEV(6) = dU
      STATEV(7) = dD
      STATEV(8) = ELSTAT
C      IF (NOEL.EQ.1) THEN
C      CALL URDFIL(0, 0, KSTEP, KINC, DTIME, TIME)
C      END IF
C
C*** STRAIN CALCULATION FROM ABAQUS ***C
      strant = stran + dstran
C
C*** PRESENT STRESSES FOR DAMAGED MATERIAL ***C
      stress = matmul(cfull, strant)
C
C*** CALCULATE TANGENT STIFFNESS MATRIX ***C
      ddsdde = cfull
      return
C*** ENERGY ***C
C      UGES = 0.5 / E * (S11 ** 2.0 + S22 ** 2.0 + S33 ** 2.0) - nu / E * 
C     & (S11 * S22 + S11 * S33 + S22 * S33) + (1.0 + nu) / E * 
C     & (S12 ** 2.0 +  S13 ** 2.0 + S23 ** 2.0)
C      UROT = (1.0 + nu) / (6.0 * E) * ((S11 - S22) ** 2.0 
C     & + (S22 - S33) ** 2.0 + (S11 - S33) ** 2.0 
C     & + 6.0 * (S12 ** 2.0 + S13 ** 2.0 + S23 ** 2.0))
C      UDIL = 2.0 * ((1.0 - 2.0 * nu) / (6.0 * E))  
C     &  * (S11 + S22 + S33) ** 2.0
      end
C*** DETERMINE MINIMUM CYCLEJUMP ***C
C      SUBROUTINE URDFIL(LSTOP,LOVRWRT,KSTEP,KINC,DTIME,TIME)
CC
C      INCLUDE 'ABA_PARAM.INC'
CC
C      DIMENSION ARRAY(513),JRRAY(NPRECD,513),TIME(2)
C      EQUIVALENCE (ARRAY(1),JRRAY(1,1))
CC
C      CALL POSFIL(KSTEP, KINC, ARRAY, JRCD)
C      PRINT 1
C      DO K1 = 1, 999999
C      CALL DBFILE(0, ARRAY, JRCD)
C      IF (JRCD.NE.0) GO TO 110
C      KEY = JRRAY(1,2)
C      IF  (KEY.EQ.5) THEN
C      PRINT ARRAY(1)
C      ENDIF
C      END DO
C 110   CONTINUE
CC
C      RETURN
C      END
