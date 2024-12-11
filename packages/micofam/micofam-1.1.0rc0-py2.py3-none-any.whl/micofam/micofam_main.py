# -*- coding: utf-8 -*-
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                MiCoFaM - Classes and Functions               %
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
Main entry point of ABAQUS-PlugIn MiCoFaM. 
 
@note: ABAQUS plug-in.       
@version:  1.0    
----------------------------------------------------------------------------------------------
@requires:
       - 

@change: 
       -    
   
@author: Gordon Just
----------------------------------------------------------------------------------------------
"""

from abaqus import *
from abaqusConstants import *
from mesh import *

import amplitude #@UnresolvedImport @UnusedImport
import section #@UnresolvedImport @UnusedImport
import regionToolset #@UnresolvedImport @UnusedImport
import displayGroupMdbToolset as dgm #@UnresolvedImport @UnusedImport
import part #@UnresolvedImport @UnusedImport
import material #@UnresolvedImport @UnusedImport
import assembly #@UnresolvedImport @UnusedImport
import step #@UnresolvedImport @UnusedImport
import interaction #@UnresolvedImport @UnusedImport
import load #@UnresolvedImport @UnusedImport
import mesh #@UnresolvedImport @UnusedImport
import job #@UnresolvedImport @UnusedImport
import sketch #@UnresolvedImport @UnusedImport
import visualization #@UnresolvedImport @UnusedImport
import xyPlot #@UnresolvedImport @UnusedImport
import displayGroupOdbToolset as dgo #@UnresolvedImport @UnusedImport
import connectorBehavior #@UnresolvedImport @UnusedImport
import math
import random
import sys #@UnusedImport
import os #@UnusedImport
import time #@UnusedImport
import shutil #@UnusedImport

def main(
    # RVE settings
    rve_fvc, rve_radius, rve_lgth, rve_dpth, 
    # Fiber settings
    fib_e11, fib_e22, fib_e33, fib_g12, fib_g13, fib_g23, fib_nu12, fib_nu13, fib_nu23, 
    # Resin settings
    res_e1, res_e2,res_d, res_nu, res_yield, res_fric, res_dil, res_c1, res_c2, 
    # Interface settings
    int_e, int_g, int_tn, int_ts, int_ufrac, int_visc, int_k1, int_k2, 
    # Mesh settings
    mesh_fib, mesh_lgth, mesh_dpth, mesh_aa, 
    # Boundary control settings
    bc_h11, bc_h12, bc_h13, bc_h21, bc_h22, bc_h23, bc_h31, bc_h32, bc_h33, bc_s11, bc_s12, bc_s13, bc_s21, bc_s22, bc_s23, bc_s31, bc_s32, bc_s33, 
    # Incrementation settings
    inc_init, inc_min, inc_max, inc_maxnum, 
    # Job settings
    job_lc, job_lt, job_stab, job_fout, job_hout, job_dDmax, job_amplratio, job_freq, job_ncycl, job_dnmin, 
    # Yet unused settings
    **kwargs):  
#========================================
# Input Parameters
#========================================
    while True:
        try:
    #----------------------------------------
    # Constants
    #----------------------------------------
    
            PI = math.pi

    #----------------------------------------
    # RVE Measures
    #----------------------------------------
    
            lgth = rve_lgth # heigth=width=length
            dpth = rve_dpth
            off = -lgth/2.
            
    #----------------------------------------
    # Materials
    #----------------------------------------
    
    # Resin isotrop
            E_res1 = res_e1 #@UnusedVariable
            E_res2 = res_e2 #@UnusedVariable
            D_res = res_d #@UnusedVariable
            nu_res = res_nu #@UnusedVariable
            sig_yield_res = res_yield #@UnusedVariable
            fric_angle = res_fric #@UnusedVariable
            dil_angle = res_dil #@UnusedVariable
            c1 = res_c1 #@UnusedVariable
            c2 = res_c2 #@UnusedVariable
    
    # Fibre orthotrop
            E11_fib = fib_e11 #@UnusedVariable
            E22_fib = fib_e22 #@UnusedVariable
            E33_fib = fib_e33 #@UnusedVariable
            G12_fib = fib_g12 #@UnusedVariable
            G31_fib = fib_g13 #@UnusedVariable
            G23_fib = fib_g23 #@UnusedVariable
            nu12_fib = fib_nu12 #@UnusedVariable
            nu31_fib = fib_nu13 #@UnusedVariable
            nu23_fib = fib_nu23 #@UnusedVariable
            fib_radius = rve_radius/2.
    
    # Interface cohesive/visco-elastic
    
            dr = 0.05*fib_radius 
            E_int = int_e*dr #@UnusedVariable
            G1_int = int_g*dr #@UnusedVariable
            G2_int = int_g*dr #@UnusedVariable
            tnn = int_tn #@UnusedVariable
            tss = int_ts #@UnusedVariable
            ttt = int_ts #@UnusedVariable
            frac_en = int_ufrac #@UnusedVariable
            if int_visc=='off':
                pass
            else:
                visc = float(int_visc) #@UnusedVariable
            k1 = int_k1 #@UnusedVariable
            k2 = int_k2 #@UnusedVariable
            
    # FibreContent 
            fvc = rve_fvc/100.
            if fvc < 0.56:
                distribution = 'Random'
            else:
                distribution = 'NNA'
            maxfib = round(((lgth**2)*fvc)/(PI*(fib_radius+dr)**2))
            if maxfib < ((lgth**2)*fvc)/(PI*(fib_radius+dr)**2):
                maxfib = maxfib+1
            if maxfib>0:
                dmin = (1./100.)*(((lgth/2)**2.)*((1.-fvc)**2))/(2.*PI*(fib_radius+dr)*(1.+fvc))
                dmax = (1./10.)*(((lgth/2)**2.)*(1.-fvc)**2)/(2.*PI*(fib_radius+dr)*(1.+fvc))
    
    # Seeds         
            if mesh_aa == 'off':
                rve_seed=lgth/mesh_lgth #@UnusedVariable
            elif mesh_aa == 'on':
                rve_seed = 2.*(2.*PI*fib_radius)/mesh_fib #@UnusedVariable
            num_seed = 0 #@UnusedVariable
            seed_3d = dpth/mesh_dpth #@UnusedVariable
            
    # Load Case
            lc = job_lc
            dDmax = job_dDmax
            if dDmax > 0.25:
                try:
                    dDch = getWarningReply('Damage Tolerance is set to a very high value! Change value?',(YES,NO))  #@UndefinedVariable
                    if dDch == YES:  #@UndefinedVariable
                        inp_dD = getInputs((('Damage Tolerance:','0.1'),),label = 'Enter Damage Tolerance value!', dialogTitle = 'Damage Evolution Settings')  #@UndefinedVariable
                    dDmax = float(inp_dD)
                except:
                    pass
            if dDmax > 1.:
                dDmax = 1.
            elif dDmax < 0.:
                dDmax = 0.
            R = job_amplratio #@UnusedVariable
            lt = job_lt #@UnusedVariable
            freq = 1. / job_freq
            step = freq / 2.
            cycles = job_ncycl + 1. #@UnusedVariable
            dNmin = job_dnmin #@UnusedVariable
            
    # Boundary Conditions
            s11 = bc_s11 * ((lgth ** 2.) * dpth) #@UnusedVariable
            s22 = bc_s22 * ((lgth ** 2.) * dpth) #@UnusedVariable
            s33 = bc_s33 * ((lgth ** 2.) * dpth) #@UnusedVariable
            s12 = bc_s12 * ((lgth ** 2.) * dpth) #@UnusedVariable
            s21 = bc_s21 * ((lgth ** 2.) * dpth) #@UnusedVariable
            s13 = bc_s13 * ((lgth ** 2.) * dpth) #@UnusedVariable
            s31 = bc_s31 * ((lgth ** 2.) * dpth) #@UnusedVariable
            s23 = bc_s23 * ((lgth ** 2.) * dpth) #@UnusedVariable
            s32 = bc_s32 * ((lgth ** 2.) * dpth) #@UnusedVariable
            
            break
        except ValueError:
            print('PLEASE ENTER CORRECT VALUES!')
    
    #========================================
    # Part Creation
    #========================================
    
    InputFile = kwargs.get("JobID","INPUTFILE.inp"); 
    ElementID = kwargs.get("ElemID","C3D8"); 
    ShapeID   = kwargs.get("ShapeID","HEX_DOMINATED"); 

    isPlugin = kwargs.get("isPlugin",True);
    
    #----------------------------------------
    # Block of Resin
    #----------------------------------------
    
    m = mdb.Model(name='RVE_'+str(int(10.*float(rve_fvc)))+'_'+lc)  #@UndefinedVariable
    r = m.ConstrainedSketch(name='resin', sheetSize=100.)
    rg, rv, rd, rc = r.geometry, r.vertices, r.dimensions, r.constraints #@UnusedVariable
    r.rectangle(point1=(off,off), point2=(lgth+off, lgth+off))
    prve = m.Part(name= m.name, dimensionality=THREE_D, type=DEFORMABLE_BODY)  #@UndefinedVariable
    prve.BaseSolidExtrude(sketch = r, depth = dpth)
    cell=prve.cells
    pickedcell = cell.findAt((off,off,0.0)) #@UnusedVariable
    f = prve.faces #@UnusedVariable
    daxis1 = prve.DatumAxisByTwoPoint(point1=(off,off,0.0), point2=(off,off,dpth)).id #@UnusedVariable
    daxis2 = prve.DatumAxisByTwoPoint(point1=(off,off,0.0), point2=(lgth+off,off,0.0)).id #@UnusedVariable
    daxis3 = prve.DatumAxisByTwoPoint(point1=(off,off,0.0), point2=(off,lgth+off,0.0)).id #@UnusedVariable
    e, d = prve.edges, prve.datums #@UnusedVariable
    skued = e.findAt((off,off+0.1,0.0)) #@UnusedVariable
    
    #----------------------------------------
    # Circles for Fibres
    #----------------------------------------
    
    #trans = prve.MakeSketchTransform(sketchPlane=f[5], sketchUpEdge=skued, sketchPlaneSide=SIDE2, sketchOrientation=LEFT, origin=(0.,0.,0.))
    c = m.ConstrainedSketch(name='fibre', sheetSize=100.)#, transform=trans)
    cg, cv, cd, cc = c.geometry, c.vertices, c.dimensions, c.constraints #@UnusedVariable
    
    #----------------------------------------
    # Coordinates for Fibre Placement
    #----------------------------------------
    
    counter=0.
    reset=int(0)
    refcount=0.
    afvc = 0.
    afvc_best = 0.
    xcor=[]
    ycor=[]
    xcor_best=[]
    ycor_Best=[] #@UnusedVariable
    radius_old = []
    fvc_fib=0.
    attempt = 0 
    pos = 0
    
    while (abs(100. * fvc - afvc) > 0.25):
        if fvc==0.:
            xcor=[]
            ycor=[]
            afvc=0.
            counter=0.
            break
        elif pos==len(xcor) and attempt>0:
            reset=int(reset+1)
            print('*** ATTEMPT '+str(reset)+' OF 10: FVF NOT REACHED WITHIN TOLERANCE! REACHED: '+str(afvc)+'%! RESTARTING FIBRE PLACEMENT...! ***')
            if abs(100.*fvc-afvc)<abs(100.*fvc-afvc_best):
                xcor_best = xcor
                ycor_best = ycor
                radius_old_best = radius_old
                afvc_best = afvc
                counter_best = counter #@UnusedVariable
            if xcor!=[] and xcor_best==[]:
                xcor_best = xcor
                ycor_best = ycor
                radius_old_best = radius_old
                afvc_best = afvc
                counter_best = counter #@UnusedVariable
            xcor=[]
            ycor=[]
            radius_old = []
            counter=0.
            pos = 0
            fvc_fib= 0.
            if reset==10:
                xcor=xcor_best
                ycor=ycor_best
                radius_old = radius_old_best
                sexit = getWarningReply('FVF of ' + str(100. * fvc) + '% not reached within tolerance!\n\nContinue with ' + str(round(100.*afvc_best)/100.) + '% FVF? (YES)\nRetry? (NO)\nStop Modeling? (CANCEL)',(YES,NO,CANCEL))  #@UndefinedVariable @UnusedVariable
                if sexit == YES:  #@UndefinedVariable
                    print('*** FVF NOT REACHED WITHIN TOLERANCE! CHOOSING BEST ATTEMPT WITH '+str(afvc_best)+'% FVF! ***')
                    break
                elif sexit == NO:  #@UndefinedVariable
                    xcor_best = []
                    ycor_best = []
                    radius_old_best = []
                    afvc_best = 0.
                    counter_best = 0. #@UnusedVariable
                    xcor = []
                    ycor = []
                    radius_old = []
                    afvc = 0.
                    counter = 0.
                    reset = 0
                elif sexit == CANCEL:  #@UndefinedVariable
                    mdb.close()  #@UndefinedVariable
                    return
        else:
            pass
        check=0
        i=0 #@UnusedVariable
        counter=int(counter)
        if len(xcor) > 0:
            if attempt == 1500:
                pos = pos+1
                attempt = 0
            else:
                radius = (random.randrange(int(0.95*fib_radius*1000.),int(1.05*fib_radius*1000.)))/(1000.)
                afib = PI*(radius+dr/2.)**2
                if distribution == 'NNA':
                    dist = (random.randrange(int((2*(fib_radius+dr)+dmin)*1000.),int((2*(fib_radius+dr)+dmax)*1000.)))/(1000.)
                    phi = (random.randrange(int(0.),int((2.*PI-PI/180.)*100.)))/100.
                    xrand = xcor[pos]+dist*cos(phi)  #@UndefinedVariable
                    yrand = ycor[pos]+dist*sin(phi)  #@UndefinedVariable
                elif distribution =='Random':
                    xrand = off+(random.randrange(int(0.),int((lgth+0.65*radius)*1000.),1.))/(1000.) 
                    yrand = off+(random.randrange(int(0.),int((lgth+0.65*radius)*1000.),1.))/(1000.) 
                    
            for i1 in range(len(xcor)):
                if ((xrand-xcor[i1])**2.+(yrand-ycor[i1])**2.) >= (((radius+radius_old[i1]+2.*dr)+dmin)**2.): 
                    check=1
                else:
                    check=0
                    attempt=attempt+1
                    break
            if check==1:
                if ((xrand-radius-dr-dmin)<=off) or ((yrand-radius-dr-dmin)<=off):
                    pass
                
                else:
                    if (xrand+radius>=lgth+off+0.35*radius) and (xrand-radius<=lgth+off-0.35*radius) and (lgth+off-yrand-radius-dr>dmin) :
                        check2=0
                        for i2 in range(len(xcor)):
                            if (((xrand-lgth)-xcor[i2])**2+(yrand-ycor[i2])**2) >= ((radius+radius_old[i2]+2*dr)+dmin)**2:
                                check2=1
                            else:
                                check2=0
                                attempt=attempt+1
                                break
                        if check2==1:       
                            xcor.append(xrand)
                            xcor.append(xrand-lgth)
                            ycor.append(yrand)
                            ycor.append(yrand)
                            radius_old.append(radius)
                            radius_old.append(radius)
                            counter=counter+1.
                            fvc_fib=fvc_fib+afib
                        else:
                            pass
                    elif (yrand+radius>lgth+off+0.35*radius) and (yrand-radius<lgth+off-0.35*radius) and (lgth+off-xrand-radius-dr>dmin) :
                        check2=0
                        for i3 in range(len(xcor)):
                            if ((xrand-xcor[i3])**2+((yrand-lgth)-ycor[i3])**2) >= ((radius+radius_old[i3]+2*dr)+dmin)**2:
                                check2=1
                            else:
                                check2=0
                                attempt=attempt+1
                                break
                        if check2==1:
                            ycor.append(yrand)
                            ycor.append(yrand-lgth)
                            xcor.append(xrand)
                            xcor.append(xrand)
                            radius_old.append(radius)
                            radius_old.append(radius)
                            counter=counter+1.
                            fvc_fib=fvc_fib+afib
                        else:
                            pass
                    elif (xrand<lgth+off-radius-dr-dmin) and (yrand<lgth+off-radius-dr-dmin):
                        xcor.append(xrand)
                        ycor.append(yrand)
                        radius_old.append(radius)
                        counter = counter+1.
                        fvc_fib=fvc_fib+afib
                    elif ((yrand+radius)>=lgth+off+0.35*radius) and ((xrand+radius)>=lgth+off+0.35*radius) and ((yrand-radius)<=lgth+off-0.35*radius) and ((xrand-radius)<=lgth+off-0.35*radius) and ((xrand)**2+(yrand)**2) <= (2*(lgth+off)-0.35*radius)**2:
                        for i4 in range(len(xcor)):
                            check2=0
                            if (((xrand-xcor[i4])**2+((yrand-lgth)-ycor[i4])**2) >= ((radius+radius_old[i4]+2*dr)+dmin)**2) and ((((xrand-lgth)-xcor[i4])**2+(yrand-ycor[i4])**2) >= ((radius+radius_old[i4]+2*dr)+dmin)**2) and ((((xrand-lgth)-xcor[i4])**2+((yrand-lgth)-ycor[i4])**2) >= ((radius+radius_old[i4]+2*dr)+dmin)**2):
                                check2=1
                            else:
                                check2=0
                                attempt=attempt+1
                                break
                        if check2==1:
                            xcor.append(xrand)
                            xcor.append(xrand)
                            xcor.append(xrand-lgth)
                            xcor.append(xrand-lgth)
                            ycor.append(yrand)
                            ycor.append(yrand-lgth)
                            ycor.append(yrand)
                            ycor.append(yrand-lgth)
                            radius_old.append(radius)
                            radius_old.append(radius)
                            radius_old.append(radius)
                            radius_old.append(radius)
                            counter=counter+1.
                            fvc_fib=fvc_fib+afib
            else:
                pass
        else: 
            xrand = (random.randrange(int((off+lgth/4)*100.),int((off+(3*lgth/4))*100.)))/100.
            yrand = (random.randrange(int((off+lgth/4)*100.),int((off+(3*lgth/4))*100.)))/100.
            radius = (random.randrange(int(0.95*fib_radius*1000.),int(1.05*fib_radius*1000.)))/(1000.)
            afib = PI*(radius+dr/2.)**2 
            if ((xrand+radius)>=lgth+off+0.35*radius) and ((yrand+radius+dr+dmin)<=lgth+off) and ((yrand-radius-dr-dmin)>=off):
                xcor.append(xrand)
                xcor.append(xrand-lgth)
                ycor.append(yrand)
                ycor.append(yrand)
                radius_old.append(radius)
                radius_old.append(radius)
                counter=counter+1.
                fvc_fib=fvc_fib+afib
            elif ((yrand+radius)>=lgth+off+0.35*radius) and ((xrand+radius+dr+dmin)<=lgth+off) and ((xrand-radius-dr-dmin)>=off):
                xcor.append(xrand)
                xcor.append(xrand)
                ycor.append(yrand)
                ycor.append(yrand-lgth)
                radius_old.append(radius)
                radius_old.append(radius)
                counter=counter+1.
                fvc_fib=fvc_fib+afib
            elif (yrand+radius>=lgth+off+0.35*radius) and (xrand+radius>=lgth+off+0.35*radius) and (yrand-radius<=lgth+off-0.35*radius) and (xrand-radius<=lgth+off-0.35*radius) :
                xcor.append(xrand)
                xcor.append(xrand)
                xcor.append(xrand-lgth)
                xcor.append(xrand-lgth)
                ycor.append(yrand)
                ycor.append(yrand-lgth)
                ycor.append(yrand)
                ycor.append(yrand-lgth)
                radius_old.append(radius)
                radius_old.append(radius)
                radius_old.append(radius)
                radius_old.append(radius)
                counter=counter+1.
                fvc_fib=fvc_fib+afib
            elif (xrand > (lgth+off+0.65*radius)) or (yrand > (lgth+off+0.65*radius)):
                pass
            elif ((xrand-radius-dr-dmin)>=off) and ((yrand-radius-dr-dmin)>=off) and ((xrand+radius+dr+dmin)<=lgth+off) and ((yrand+radius+dr+dmin)<=lgth+off):
                xcor.append(xrand)
                ycor.append(yrand)
                radius_old.append(radius)
                counter = counter+1.
                fvc_fib=fvc_fib+afib
            else:
                pass
                
        refcount=refcount+1.
        afvc = (100.*fvc_fib)/(lgth**2)
    if (abs(100. * fvc - afvc) < 0.25):
        print('*** ATTEMPT '+str(reset+1)+' OF 10: FIBRE VOLUME FRACTION OF '+str(rve_fvc)+'% REACHED! ***')
        afvc_best = afvc
        counter_best = counter #@UnusedVariable
    m.setValues(description='Reached FVF: '+str(afvc_best)+' %')
    
    #----------------------------------------   
    # Partition the Block
    #----------------------------------------
    
    # Fibre Positions and Radii for FVC = 59,52%
    
    #xcor = [7.79, 13.681414157045, 13.4194072043563, 4.05541185820914, 3.92621685689787, -0.173107147678037, 20.0706441271734, 20.3487161355225, 12.8610334814747, 19.7656567551294, -2.63414182932642, -3.32759944609828, 4.00932536601241, -8.16069386701071, 26.6979770132547, -23.3020229867453, 26.9078907940907, -23.0921092059093, 11.2505808539085, 19.388210821876, 24.9402610358088, -25.0597389641912, -10.9163043378135, -11.010254201214, -3.24035602415042, 3.21422392419782, -13.6347772462738, -16.5617558516588, -18.2569679991368, -18.1133822068143, 15.6329667703737, 8.3332429946405, 26.0158326129378, -23.9841673870622, -10.1781060382881, -17.1983385485477, -3.99019571223939, 0.744828036047275, 19.2588958759622, 12.0742376469937, 26.4519854385172, -23.5480145614828, -16.113242248798, -9.94255137630726, 4.88847359945267, 4.88847359945267]
    #ycor = [-12.34, -17.2340290385499, -7.88007864110343, -18.5366181430838, -5.41954800442342, -12.0086021204067, -11.4000900271432, -21.3510644194751, 0.1755928880489, -3.81233225774677, -21.3523659055049, -2.50887711227719, 2.27800335790686, -11.0325552971752, -16.2645838155107, -16.2645838155107, -7.20813845111927, -7.20813845111927, 7.40437413625147, 5.90037061010523, 1.10587793889746, 1.10587793889746, -20.4242817589903, 1.40905498433937, 5.57165192890117, 10.266532490183, -5.37823737572117, -11.7772119496673, -21.3888302159101, -0.0967364466983023, 14.0817136273338, 15.1737074934245, 9.60758862293403, 9.60758862293403, 8.88890828737541, 6.74505096543635, 13.105427970314, 17.996688306697, 20.8666150356997, 21.2789553230397, 18.1865087596843, 18.1865087596843, 13.5072287945192, 16.5352808915073, 24.0431005854678, -25.9568994145322]
    #radius_old = [3.382, 3.399, 3.241, 3.202, 3.219, 3.139, 3.457, 3.237, 3.197, 3.195, 3.362, 3.45, 3.158, 3.283, 3.307, 3.307, 3.22, 3.22, 3.215, 3.374, 3.396, 3.396, 3.222, 3.329, 3.395, 3.277, 3.185, 3.402, 3.184, 3.197, 3.333, 3.211, 3.343, 3.343, 3.183, 3.145, 3.142, 3.142, 3.313, 3.241, 3.416, 3.416, 3.226, 3.142, 3.183, 3.183]
    
    # Fibre Positions and Radii for FVC = 66,55%
    
    #xcor = [6.02, 13.5638236744658, 3.28099960955261, -1.7004811946928, 2.58805864471581, 10.0286342569985, 10.5897634195631, 20.7914651292484, 18.1704411342975, 1.86805422738257, -4.31878153721445, -8.42167233934066, -9.47780510360323, 8.34054407083224, -2.28885011397924, 16.3617673254976, 9.18282181162837, 26.5115994386151, -23.4884005613849, 26.7618320601776, -23.2381679398224, 18.4316450816941, 24.7889944548824, -25.2110055451176, -12.248923038721, -15.485468126445, -9.21221789347171, -16.0272750109696, -16.2976528598244, 11.1341029941388, 2.62522836029391, -7.77212025204328, 23.7243041579805, -26.2756958420195, 25.321748268979, -24.678251731021, 18.7851695591362, -17.7897038713479, 6.34466703610393, 6.34466703610393, 13.9273276797183, 13.9273276797183, -1.63420559571704, -14.4583548027798, -8.96388295274925, -8.96388295274925, -18.7687061997238, -21.3383100978637]
    #ycor = [-4.97, -5.59898677932845, -11.9820368553744, -4.88049512641892, 2.3349859365977, 1.41257161288598, -12.1370958057795, -8.34580730515599, 1.57539483714368, -20.0969462416217, -14.4870978369164, -1.01797087444235, -8.43235841431307, 8.3777138323678, 9.03499563505064, -18.1181755502636, -20.2175239696742, -13.1950406964051, -13.1950406964051, -2.07420466228493, -2.07420466228493, 10.05437245817, 6.40107954944881, 6.40107954944881, -18.1087521227481, 2.94800820745993, 6.92478442374251, -4.58375381810444, -11.7977263855704, 16.2550352389129, 14.7743731424197, 14.5866222068776, -20.6662596129137, -20.6662596129137, 14.2787306423875, 14.2787306423875, 18.7151602077831, 10.3595138948564, 23.1193052805038, -26.8806947194962, 24.1314141566561, -25.8685858433439, 21.1469273692883, 18.340618948024, 23.0925391277748, -26.9074608722252, -21.1412233067528, 21.1789006321126]
    #radius_old = [3.5, 3.389, 3.378, 3.644, 3.462, 3.397, 3.37, 3.609, 3.462, 3.324, 3.492, 3.39, 3.619, 3.331, 3.379, 3.614, 3.372, 3.476, 3.476, 3.381, 3.381, 3.521, 3.379, 3.379, 3.345, 3.649, 3.371, 3.407, 3.328, 3.538, 3.572, 3.381, 3.622, 3.622, 3.66, 3.66, 3.328, 3.646, 3.436, 3.436, 3.479, 3.479, 3.594, 3.493, 3.355, 3.355, 3.393, 3.404]
    
    print('*** FIBRES PLACED! PARTITIONING...! ***')
    for isketch in range(len(xcor)):
        radius = radius_old[isketch]
        if (xcor[isketch]+radius) >= lgth+off:
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch]+radius,ycor[isketch]))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch]+radius+dr,ycor[isketch]))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch]+0.9*radius,ycor[isketch]))
            e, d, f = prve.edges, prve.datums, prve.faces #@UnusedVariable
        elif (xcor[isketch]-radius) <= off:
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch]-radius,ycor[isketch]))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch]-radius-dr,ycor[isketch]))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch]-0.9*radius,ycor[isketch]))
            e, d, f = prve.edges, prve.datums, prve.faces #@UnusedVariable
        elif (ycor[isketch]+radius) >= lgth+off:
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]+radius))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]+radius+dr))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]+0.9*radius))
            e, d, f = prve.edges, prve.datums, prve.faces #@UnusedVariable
        elif (ycor[isketch]-radius) <= off:
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]-radius))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]-radius-dr))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]-0.9*radius))
            e, d, f = prve.edges, prve.datums, prve.faces #@UnusedVariable
        else:
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]+radius))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]+radius+dr))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]+0.5*radius))
            c.CircleByCenterPerimeter(center=(xcor[isketch],ycor[isketch]), point1=(xcor[isketch],ycor[isketch]+0.9*radius))
            e, d, f = prve.edges, prve.datums, prve.faces #@UnusedVariable
    if fvc != 0.:
        skface=f.findAt((off,off,0.)) 
        pickedcell = cell.findAt((off,off,dpth/2))
        skued = e.findAt((off,off+0.1,0.)) #@UnusedVariable
        prve.PartitionFaceBySketch(faces=skface, sketch=c)#, sketchUpEdge=skued) 
        e, d = prve.edges, prve.datums
    else:
        pass
    
    
    
    for ipart in range(len(xcor)):
    # Fibre Partition   
        radius = radius_old[ipart]
        e, d, cell = prve.edges, prve.datums, prve.cells
        pickedcell = cell.getByBoundingBox(xMin = off-0.1, yMin = off-0.1, zMin = -0.1, xMax = lgth+off+0.1, yMax = lgth+off+0.1, zMax = dpth+0.1)
            
        if (xcor[ipart]==off) and (ycor[ipart]>off) and (ycor[ipart]<lgth+off):
            e_fib = e.findAt((xcor[ipart]+radius,ycor[ipart],0.))
        elif (ycor[ipart]>=off-abs(off/100.)) and (ycor[ipart]<=off+abs(off/100.)) and (xcor[ipart]>off) and (xcor[ipart]<lgth+off):
            e_fib = e.findAt((xcor[ipart],ycor[ipart]+radius,0.))
        elif (xcor[ipart]==lgth+off) and (ycor[ipart]>off) and (ycor[ipart]<lgth+off):
            e_fib = e.findAt((xcor[ipart]-radius,ycor[ipart],0.))
        elif (ycor[ipart]==lgth+off) and (xcor[ipart]>off) and (xcor[ipart]<lgth+off):
            e_fib = e.findAt((xcor[ipart],ycor[ipart]-radius,0.))
        elif xcor[ipart]>=lgth+off and ycor[ipart]>=lgth+off:
            alpha = abs(atan((ycor[ipart]-(lgth+off))/(xcor[ipart]-(lgth+off)))) #@UndefinedVariable
            e_fib = e.findAt((xcor[ipart]-radius*cos(alpha),ycor[ipart]-radius*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]>=lgth+off and ycor[ipart]<=off:
            alpha = abs(atan((off-ycor[ipart])/(xcor[ipart]-(lgth+off)))) #@UndefinedVariable
            e_fib = e.findAt((xcor[ipart]-radius*cos(alpha),ycor[ipart]+radius*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]<=off and ycor[ipart]>=lgth+off:
            alpha = abs(atan((ycor[ipart]-(lgth+off))/(off-xcor[ipart]))) #@UndefinedVariable
            e_fib = e.findAt((xcor[ipart]+radius*cos(alpha),ycor[ipart]-radius*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]<=off and ycor[ipart]<=off:
            alpha = abs(atan((off-ycor[ipart])/(off-xcor[ipart]))) #@UndefinedVariable
            e_fib = e.findAt((xcor[ipart]+radius*cos(alpha),ycor[ipart]+radius*sin(alpha),0.)) #@UndefinedVariable
        else:
            e_fib = e.findAt((xcor[ipart]+radius,ycor[ipart],0.))
            if e_fib==None:
                e_fib = e.findAt((xcor[ipart]-radius,ycor[ipart],0.))
            if e_fib==None:
                e_fib = e.findAt((xcor[ipart],ycor[ipart]+radius,0.))
            if e_fib==None:
                e_fib = e.findAt((xcor[ipart],ycor[ipart]-radius,0.))
        fib_part = prve.PartitionCellByExtrudeEdge(cells=pickedcell, edges=e_fib, line=d[daxis1], sense=FORWARD) #@UndefinedVariable @UnusedVariable
        
        # Interface Partition
        e, d, cell = prve.edges, prve.datums, prve.cells
        pickedcell = cell.getByBoundingBox(xMin = off-0.1, yMin = off-0.1, zMin = -0.1, xMax = lgth+off+0.1, yMax = lgth+off+0.1, zMax = dpth+0.1)
            
        if (xcor[ipart]>=off-abs(off/100.)) and (xcor[ipart]<=off+abs(off/100.)) and (ycor[ipart]>off) and (ycor[ipart]<lgth+off):
            e_int = e.findAt((xcor[ipart]+radius+dr,ycor[ipart],0.))
        elif (ycor[ipart]>=off-abs(off/100.)) and (ycor[ipart]<=off+abs(off/100.)) and (xcor[ipart]>off) and (xcor[ipart]<lgth+off):
            e_int = e.findAt((xcor[ipart],ycor[ipart]+radius+dr,0.))
        elif (xcor[ipart]==lgth+off) and (ycor[ipart]>off) and (ycor[ipart]<lgth+off):
            e_int = e.findAt((xcor[ipart]-radius-dr,ycor[ipart],0.))
        elif (ycor[ipart]==lgth+off) and (xcor[ipart]>off) and (xcor[ipart]<lgth+off):
            e_int = e.findAt((xcor[ipart],ycor[ipart]-radius-dr,0.))
        elif xcor[ipart]>=lgth+off and ycor[ipart]>=lgth+off:
            alpha = abs(atan((ycor[ipart]-(lgth+off))/(xcor[ipart]-(lgth+off)))) #@UndefinedVariable
            e_int = e.findAt((xcor[ipart]-(radius+dr)*cos(alpha),ycor[ipart]-(radius+dr)*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]>=lgth+off and ycor[ipart]<=off:
            alpha = abs(atan((off-ycor[ipart])/(xcor[ipart]-(lgth+off)))) #@UndefinedVariable
            e_int = e.findAt((xcor[ipart]-(radius+dr)*cos(alpha),ycor[ipart]+(radius+dr)*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]<=off and ycor[ipart]>=lgth+off:
            alpha = abs(atan((ycor[ipart]-(lgth+off))/(off-xcor[ipart]))) #@UndefinedVariable
            e_int = e.findAt((xcor[ipart]+(radius+dr)*cos(alpha),ycor[ipart]-(radius+dr)*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]<=off and (ycor[ipart]>=off-abs(off/100.) and ycor[ipart]<=off+abs(off/100.) or ycor[ipart]<off):
            alpha = abs(atan((off-ycor[ipart])/(off-xcor[ipart]))) #@UndefinedVariable
            e_int = e.findAt((xcor[ipart]+(radius+dr)*cos(alpha),ycor[ipart]+(radius+dr)*sin(alpha),0.)) #@UndefinedVariable
        else:
            e_int = e.findAt((xcor[ipart]+radius+dr,ycor[ipart],0.))
            if e_int==None:
                e_int = e.findAt((xcor[ipart]-radius-dr,ycor[ipart],0.))
            if e_int==None:
                e_int = e.findAt((xcor[ipart],ycor[ipart]+radius+dr,0.))
            if e_int==None:
                e_int = e.findAt((xcor[ipart],ycor[ipart]-radius-dr,0.))
        
        int_part = prve.PartitionCellByExtrudeEdge(cells=pickedcell, edges=e_int, line=d[daxis1], sense=FORWARD) #@UndefinedVariable @UnusedVariable
    # Inner Fibre Partition 
        e, d, cell = prve.edges, prve.datums, prve.cells
        pickedcell = cell.getByBoundingBox(xMin = off-0.1, yMin = off-0.1, zMin = -0.1, xMax = lgth+off+0.1, yMax = lgth+off+0.1, zMax = dpth+0.1)
        path = e.findAt((off,off,dpth/2.))
        
        if (xcor[ipart]==off) and (ycor[ipart]>off) and (ycor[ipart]<lgth+off):
            e_fib_in1 = e.findAt((xcor[ipart]+0.9*radius,ycor[ipart],0.))
        elif (ycor[ipart]>=off-abs(off/100.)) and (ycor[ipart]<=off+abs(off/100.)) and (xcor[ipart]>off) and (xcor[ipart]<lgth+off):
            e_fib_in1 = e.findAt((xcor[ipart],ycor[ipart]+0.9*radius,0.))
        elif (xcor[ipart]==lgth+off) and (ycor[ipart]>off) and (ycor[ipart]<lgth+off):
            e_fib_in1 = e.findAt((xcor[ipart]-0.9*radius,ycor[ipart],0.))
        elif (ycor[ipart]==lgth+off) and (xcor[ipart]>off) and (xcor[ipart]<lgth+off):
            e_fib_in1 = e.findAt((xcor[ipart],ycor[ipart]-0.9*radius,0.))
        elif xcor[ipart]>=lgth+off and ycor[ipart]>=lgth+off:
            alpha = abs(atan((ycor[ipart]-(lgth+off))/(xcor[ipart]-(lgth+off)))) #@UndefinedVariable
            e_fib_in1 = e.findAt((xcor[ipart]-0.9*radius*cos(alpha),ycor[ipart]-0.9*radius*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]>=lgth+off and ycor[ipart]<=off:
            alpha = abs(atan((off-ycor[ipart])/(xcor[ipart]-(lgth+off)))) #@UndefinedVariable
            e_fib_in1 = e.findAt((xcor[ipart]-0.9*radius*cos(alpha),ycor[ipart]+0.9*radius*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]<=off and ycor[ipart]>=lgth+off:
            alpha = abs(atan((ycor[ipart]-(lgth+off))/(off-xcor[ipart]))) #@UndefinedVariable
            e_fib_in1 = e.findAt((xcor[ipart]+0.9*radius*cos(alpha),ycor[ipart]-0.9*radius*sin(alpha),0.)) #@UndefinedVariable
        elif xcor[ipart]<=off and ycor[ipart]<=off: 
            alpha = abs(atan((off-ycor[ipart])/(off-xcor[ipart]))) #@UndefinedVariable
            e_fib_in1 = e.findAt((xcor[ipart]+0.9*radius*cos(alpha),ycor[ipart]+0.9*radius*sin(alpha),0.)) #@UndefinedVariable
        else:
            e_fib_in1 = e.findAt((xcor[ipart]+0.9*radius,ycor[ipart],0.))
            
            if e_fib_in1==None:
                e_fib_in1 = e.findAt((xcor[ipart]-0.9*radius,ycor[ipart],0.))
                
            if e_fib_in1==None:
                e_fib_in1 = e.findAt((xcor[ipart],ycor[ipart]+0.9*radius,0.))
                
            if e_fib_in1==None:
                e_fib_in1 = e.findAt((xcor[ipart],ycor[ipart]-0.9*radius,0.))
                
        fib_in_part1 = prve.PartitionCellBySweepEdge(cells = pickedcell, edges = (e_fib_in1,), sweepPath = path) #@UnusedVariable
        
        e, d, cell = prve.edges, prve.datums, prve.cells
        pickedcell = cell.getByBoundingBox(xMin = off-0.1, yMin = off-0.1, zMin = -0.1, xMax = lgth+off+0.1, yMax = lgth+off+0.1, zMax = dpth+0.1)
        path = e.findAt((off,off,dpth/2.))  
        
        if (xcor[ipart]+radius<lgth+off) and (xcor[ipart]-radius>off) and (ycor[ipart]+radius<lgth+off) and (ycor[ipart]-radius>off):
            e_fib_in2 = e.findAt((xcor[ipart]+0.5*radius,ycor[ipart],0.))
            fib_in_part2 = prve.PartitionCellBySweepEdge(cells = pickedcell, edges = (e_fib_in2,), sweepPath = path) #@UnusedVariable
            
    if afvc>afvc_best:  
        print('*** PLACED '+str(int(counter))+' FIBRE(S) - FIBRE VOLUME FRACTION: '+str(afvc)+'% !***')
        afvc_best=afvc
    elif fvc==0.:
        print('*** PLACED '+str(int(counter_best))+' FIBRE(S) - FIBRE VOLUME FRACTION: '+str(afvc)+'% !***')
    else:
        print('*** PLACED '+str(int(counter_best))+' FIBRE(S) - FIBRE VOLUME FRACTION: '+str(afvc_best)+'% !***')
    print('*** PARTITIONING FINISHED! ***')
    
    #========================================
    # Seed & Mesh Part
    #========================================
    
    print('*** MESHING...! ***\n*** SEEDING...! ***')
    dalpha = PI/360.
    
    # Seed RVE Edges except 3rd Dimension
    e = prve.edges
    
    pickededges=[] #@UnusedVariable
    pickededges=e.getByBoundingBox(xMin=off-rve_seed/1000.,yMin=off-rve_seed/1000.,zMin=0.-rve_seed/1000.,xMax=lgth+off+rve_seed/1000.,yMax=off+rve_seed/1000.,zMax=0.+rve_seed/1000.)
    prve.seedEdgeBySize(edges=pickededges, size=rve_seed, constraint=FIXED) #@UndefinedVariable
    pickededges=[]
    pickededges=e.getByBoundingBox(xMin=off-rve_seed/1000.,yMin=lgth+off-rve_seed/1000.,zMin=0.-rve_seed/1000.,xMax=lgth+off+rve_seed/1000.,yMax=lgth+off+rve_seed/1000.,zMax=0.+rve_seed/1000.)
    prve.seedEdgeBySize(edges=pickededges, size=rve_seed, constraint=FIXED) #@UndefinedVariable
    pickededges=[]
    pickededges=e.getByBoundingBox(xMin=off-rve_seed/1000.,yMin=off-rve_seed/1000.,zMin=dpth-rve_seed/1000.,xMax=lgth+off+rve_seed/1000.,yMax=off+rve_seed/1000.,zMax=dpth+rve_seed/1000.)
    prve.seedEdgeBySize(edges=pickededges, size=rve_seed, constraint=FIXED) #@UndefinedVariable
    pickededges=[]
    pickededges=e.getByBoundingBox(xMin=off-rve_seed/1000.,yMin=lgth+off-rve_seed/1000.,zMin=dpth-rve_seed/1000.,xMax=lgth+off+rve_seed/1000.,yMax=lgth+off+rve_seed/1000.,zMax=dpth+rve_seed/1000.)
    prve.seedEdgeBySize(edges=pickededges, size=rve_seed, constraint=FIXED) #@UndefinedVariable
    pickededges=[]
    pickededges=e.getByBoundingBox(xMin=off-rve_seed/1000.,yMin=off-rve_seed/1000.,zMin=0.-rve_seed/1000.,xMax=off+rve_seed/1000.,yMax=lgth+off+rve_seed/1000.,zMax=0.+rve_seed/1000.)
    prve.seedEdgeBySize(edges=pickededges, size=rve_seed, constraint=FIXED) #@UndefinedVariable
    pickededges=[]
    pickededges=e.getByBoundingBox(xMin=lgth+off-rve_seed/1000.,yMin=off-rve_seed/1000.,zMin=0.-rve_seed/1000.,xMax=lgth+off+rve_seed/1000.,yMax=lgth+off+rve_seed/1000.,zMax=0.+rve_seed/1000.)
    prve.seedEdgeBySize(edges=pickededges, size=rve_seed, constraint=FIXED) #@UndefinedVariable
    pickededges=[]
    pickededges=e.getByBoundingBox(xMin=off-rve_seed/1000.,yMin=off-rve_seed/1000.,zMin=dpth-rve_seed/1000.,xMax=off+rve_seed/1000.,yMax=lgth+off+rve_seed/1000.,zMax=dpth+rve_seed/1000.)
    prve.seedEdgeBySize(edges=pickededges, size=rve_seed, constraint=FIXED) #@UndefinedVariable
    pickededges=[]
    pickededges=e.getByBoundingBox(xMin=lgth+off-rve_seed/1000.,yMin=off-rve_seed/1000.,zMin=dpth-rve_seed/1000.,xMax=lgth+off+rve_seed/1000.,yMax=lgth+off+rve_seed/1000.,zMax=dpth+rve_seed/1000.)
    prve.seedEdgeBySize(edges=pickededges, size=rve_seed, constraint=FIXED) #@UndefinedVariable
    
    # Cut Interface & Seed Fibres/Interfaces/RVE 3rd Dimension
    e, f = prve.edges, prve.faces
    pickededges= []
    seedfaces = []
    
    # Seed Outer Edges in 3rd Dimension
    seedfaces.append(f.getByBoundingBox(xMin =off-rve_seed/1000. , yMin = off-rve_seed/1000. , zMin = 0.-rve_seed/1000. , xMax =lgth+off+rve_seed/1000. , yMax = off+rve_seed/1000., zMax = dpth+rve_seed/1000.))
    seedfaces.append(f.getByBoundingBox(xMin =off-rve_seed/1000. , yMin = off-rve_seed/1000. , zMin = 0.-rve_seed/1000. , xMax =off+rve_seed/1000. , yMax = lgth+off+rve_seed/1000., zMax = dpth+rve_seed/1000.))
    seedfaces.append(f.getByBoundingBox(xMin =off-rve_seed/1000. , yMin = lgth+off-rve_seed/1000. , zMin = 0.-rve_seed/1000. , xMax =lgth+off+rve_seed/1000. , yMax = lgth+off+rve_seed/1000., zMax = dpth+rve_seed/1000.))
    seedfaces.append(f.getByBoundingBox(xMin =lgth+off-rve_seed/1000. , yMin = off-rve_seed/1000. , zMin = 0.-rve_seed/1000. , xMax =lgth+off+rve_seed/1000. , yMax = lgth+off+rve_seed/1000., zMax = dpth+rve_seed/1000.))
    for ilen in range(4):
        for iface in range(len(seedfaces[ilen])):
            for i3rd in range(4):
                seededges = seedfaces[ilen][iface].getEdges()
                z = e[seededges[i3rd]].pointOn[0][2]
                if z != 0. and z != dpth :
                    pickededges.append(e[seededges[i3rd]])
                else:
                    pass    
    
    prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
    
    # Cut & Seed Interface  
    for iseed in range(len(xcor)):
        radius = radius_old[iseed]
        e, f, cell = prve.edges, prve.faces, prve.cells
        pickededges = []
        pickedcell= []
        if ((xcor[iseed]-radius) < off) and ((ycor[iseed]-radius) < off) :
            alpha = abs(atan((off-ycor[iseed])/(off-xcor[iseed]))) #@UndefinedVariable
            pickedcell.append(cell.findAt((xcor[iseed]+(radius+dr/2.)*cos(alpha),ycor[iseed]+(radius+dr/2.)*sin(alpha),0.0))) #@UndefinedVariable
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed]+radius*cos(alpha),ycor[iseed]+radius*sin(alpha),0.0), point2=(xcor[iseed]+(radius+dr)*cos(alpha),ycor[iseed]+(radius+dr)*sin(alpha),0.0), point3=(xcor[iseed]+radius*cos(alpha),ycor[iseed]+radius*sin(alpha),dpth)) #@UndefinedVariable @UnusedVariable
            pickededges.append(e.findAt((xcor[iseed]+radius*cos(alpha),ycor[iseed]+radius*sin(alpha),dpth/2.))) #@UndefinedVariable
            pickededges.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha),ycor[iseed]+(radius+dr)*sin(alpha),dpth/2.))) #@UndefinedVariable
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        elif ((xcor[iseed]-radius) < off) and ((ycor[iseed]+radius) > lgth+off) :
            alpha = abs(atan((ycor[iseed]-(lgth+off))/(off-xcor[iseed]))) #@UndefinedVariable
            pickedcell.append(cell.findAt((xcor[iseed]+(radius+dr/2.)*cos(alpha),ycor[iseed]-(radius+dr/2.)*sin(alpha),0.0))) #@UndefinedVariable
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed]+radius*cos(alpha),ycor[iseed]-radius*sin(alpha),0.0), point2=(xcor[iseed]+(radius+dr)*cos(alpha),ycor[iseed]-(radius+dr)*sin(alpha),0.0), point3=(xcor[iseed]+radius*cos(alpha),ycor[iseed]-radius*sin(alpha),dpth)) #@UndefinedVariable @UnusedVariable
            pickededges.append(e.findAt((xcor[iseed]+radius*cos(alpha),ycor[iseed]-radius*sin(alpha),dpth/2.))) #@UndefinedVariable
            pickededges.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha),ycor[iseed]-(radius+dr)*sin(alpha),dpth/2.))) #@UndefinedVariable
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        elif ((ycor[iseed]-radius) < off) and ((xcor[iseed]+radius) > lgth+off) :
            alpha = abs(atan((off-ycor[iseed])/(xcor[iseed]-(lgth+off)))) #@UndefinedVariable
            pickedcell.append(cell.findAt((xcor[iseed]-(radius+dr/2.)*cos(alpha),ycor[iseed]+(radius+dr/2.)*sin(alpha),0.0))) #@UndefinedVariable
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed]-radius*cos(alpha),ycor[iseed]+radius*sin(alpha),0.0), point2=(xcor[iseed]-(radius+dr)*cos(alpha),ycor[iseed]+(radius+dr)*sin(alpha),0.0), point3=(xcor[iseed]-radius*cos(alpha),ycor[iseed]+radius*sin(alpha),dpth)) #@UndefinedVariable @UnusedVariable
            pickededges.append(e.findAt((xcor[iseed]-radius*cos(alpha),ycor[iseed]+radius*sin(alpha),dpth/2.))) #@UndefinedVariable
            pickededges.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha),ycor[iseed]+(radius+dr)*sin(alpha),dpth/2.))) #@UndefinedVariable
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        elif ((xcor[iseed]+radius) > lgth+off) and ((ycor[iseed]+radius) > lgth+off) :
            alpha = abs(atan((ycor[iseed]-(lgth+off))/(xcor[iseed]-(lgth+off)))) #@UndefinedVariable
            pickedcell.append(cell.findAt((xcor[iseed]-(radius+dr/2.)*cos(alpha),ycor[iseed]-(radius+dr/2.)*sin(alpha),0.0))) #@UndefinedVariable
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed]-radius*cos(alpha),ycor[iseed]-radius*sin(alpha),0.0), point2=(xcor[iseed]-(radius+dr)*cos(alpha),ycor[iseed]-(radius+dr)*sin(alpha),0.0), point3=(xcor[iseed]-radius*cos(alpha),ycor[iseed]-radius*sin(alpha),dpth)) #@UndefinedVariable @UnusedVariable
            pickededges.append(e.findAt((xcor[iseed]-radius*cos(alpha),ycor[iseed]-radius*sin(alpha),dpth/2.))) #@UndefinedVariable
            pickededges.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha),ycor[iseed]-(radius+dr)*sin(alpha),dpth/2.))) #@UndefinedVariable
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        elif ((xcor[iseed]+radius) > lgth+off) :
            pickedcell.append(cell.findAt((xcor[iseed]-radius-dr/2.,ycor[iseed],0.0)))
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed]-radius,ycor[iseed],0.0), point2=(xcor[iseed]-radius-dr,ycor[iseed],0.0), point3=(xcor[iseed]-radius,ycor[iseed],dpth)) #@UnusedVariable
            pickededges.append(e.findAt((xcor[iseed]-radius,ycor[iseed],dpth/2.)))
            pickededges.append(e.findAt((xcor[iseed]-radius-dr,ycor[iseed],dpth/2.)))
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        elif ((xcor[iseed]-radius) < off)  :
            pickedcell.append(cell.findAt((xcor[iseed]+radius+dr/2.,ycor[iseed],0.0)))
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed]+radius,ycor[iseed],0.0), point2=(xcor[iseed]+radius+dr,ycor[iseed],0.0), point3=(xcor[iseed]+radius,ycor[iseed],dpth)) #@UnusedVariable
            pickededges.append(e.findAt((xcor[iseed]+radius,ycor[iseed],dpth/2.)))
            pickededges.append(e.findAt((xcor[iseed]+radius+dr,ycor[iseed],dpth/2.)))
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        elif ((ycor[iseed]+radius) > lgth+off) :
            pickedcell.append(cell.findAt((xcor[iseed],ycor[iseed]-radius-dr/2.,0.0)))
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed],ycor[iseed]-radius,0.0), point2=(xcor[iseed],ycor[iseed]-radius-dr,0.0), point3=(xcor[iseed],ycor[iseed]-radius,dpth)) #@UnusedVariable
            pickededges.append(e.findAt((xcor[iseed],ycor[iseed]-radius,dpth/2.)))
            pickededges.append(e.findAt((xcor[iseed],ycor[iseed]-radius-dr,dpth/2.)))
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        elif ((ycor[iseed]-radius) < off) :
            pickedcell.append(cell.findAt((xcor[iseed],ycor[iseed]+radius+dr/2.,0.0)))
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed],ycor[iseed]+radius,0.0), point2=(xcor[iseed],ycor[iseed]+radius+dr,0.0), point3=(xcor[iseed],ycor[iseed]+radius,dpth)) #@UnusedVariable
            pickededges.append(e.findAt((xcor[iseed],ycor[iseed]+radius,dpth/2.)))
            pickededges.append(e.findAt((xcor[iseed],ycor[iseed]+radius+dr,dpth/2.)))
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        elif ((xcor[iseed]-radius)>off) and ((ycor[iseed]-radius)>off) and ((xcor[iseed]+radius)<lgth+off) and ((ycor[iseed]+radius)<lgth+off):
            pickedcell.append(cell.findAt((xcor[iseed],ycor[iseed]-radius-dr/2.,0.0)))
            int_part = prve.PartitionCellByPlaneThreePoints(cells=pickedcell, point1=(xcor[iseed],ycor[iseed]-radius,0.0), point2=(xcor[iseed],ycor[iseed]-radius-dr,0.0), point3=(xcor[iseed],ycor[iseed]-radius,dpth)) #@UnusedVariable
            pickededges.append(e.findAt((xcor[iseed],ycor[iseed]+radius,dpth/2.)))
            pickededges.append(e.findAt((xcor[iseed],ycor[iseed]+radius+dr,dpth/2.)))
            pickededges.append(e.findAt((xcor[iseed],ycor[iseed]-radius,dpth/2.)))
            pickededges.append(e.findAt((xcor[iseed],ycor[iseed]-radius-dr,dpth/2.)))
            prve.seedEdgeBySize(edges=pickededges, size=seed_3d, constraint=FIXED) #@UndefinedVariable
        else:
            pass
    
    for iseed in range(len(xcor)):
    # Seed Fibres
        radius = radius_old[iseed]
        fib_seed=(2*PI*radius)/mesh_fib
        e = prve.edges
        e_fib_pick = []
        num_fib1 = 0
        num_int1 = 0
        num_fib2 = 0
        num_int2 = 0
        same = 1 #@UnusedVariable
        
        if (xcor[iseed]==off) and (ycor[iseed]-radius>off):
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(dalpha),ycor[iseed]+radius*sin(dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(dalpha),ycor[iseed]+radius*sin(dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(-dalpha),ycor[iseed]+radius*sin(-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(-dalpha),ycor[iseed]+radius*sin(-dalpha), dpth)),) #@UndefinedVariable
            
        elif (ycor[iseed]>=off-abs(off/100.)) and (ycor[iseed]<=off+abs(off/100.)) and (xcor[iseed]-radius>off):
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)+dalpha),ycor[iseed]+radius*sin((PI/2)+dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)+dalpha),ycor[iseed]+radius*sin((PI/2)+dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)-dalpha),ycor[iseed]+radius*sin((PI/2)-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)-dalpha),ycor[iseed]+radius*sin((PI/2)-dalpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]==lgth+off) and (ycor[iseed]+radius<lgth+off):
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(PI+dalpha),ycor[iseed]+radius*sin(PI+dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(PI+dalpha),ycor[iseed]+radius*sin(PI+dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(PI-dalpha),ycor[iseed]+radius*sin(PI-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(PI-dalpha),ycor[iseed]+radius*sin(PI-dalpha), dpth)),) #@UndefinedVariable
            
        elif (ycor[iseed]==lgth+off) and (xcor[iseed]+radius<lgth+off):
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((-PI/2)+dalpha),ycor[iseed]+radius*sin((-PI/2)+dalpha), 0.)),) #@UndefinedVariable   
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((-PI/2)+dalpha),ycor[iseed]+radius*sin((-PI/2)+dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((-PI/2)-dalpha),ycor[iseed]+radius*sin((-PI/2)-dalpha), 0.)),)   #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((-PI/2)-dalpha),ycor[iseed]+radius*sin((-PI/2)-dalpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]-radius<off) and (ycor[iseed]-radius<off):
            alpha = abs(atan((off-ycor[iseed])/(off-xcor[iseed]))) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(alpha+dalpha),ycor[iseed]+radius*sin(alpha+dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(alpha+dalpha),ycor[iseed]+radius*sin(alpha+dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(alpha-dalpha),ycor[iseed]+radius*sin(alpha-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(alpha-dalpha),ycor[iseed]+radius*sin(alpha-dalpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]-radius<off) and (ycor[iseed]+radius>lgth+off):
            alpha = abs(atan((ycor[iseed]-(lgth+off))/(off-xcor[iseed]))) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(alpha+dalpha),ycor[iseed]-radius*sin(alpha+dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(alpha+dalpha),ycor[iseed]-radius*sin(alpha+dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(alpha-dalpha),ycor[iseed]-radius*sin(alpha-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(alpha-dalpha),ycor[iseed]-radius*sin(alpha-dalpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]+radius>lgth+off) and (ycor[iseed]-radius<off):
            alpha = abs(atan((off-ycor[iseed])/(xcor[iseed]-(lgth+off)))) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]-radius*cos(alpha+dalpha),ycor[iseed]+radius*sin(alpha+dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]-radius*cos(alpha+dalpha),ycor[iseed]+radius*sin(alpha+dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]-radius*cos(alpha-dalpha),ycor[iseed]+radius*sin(alpha-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]-radius*cos(alpha-dalpha),ycor[iseed]+radius*sin(alpha-dalpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]+radius>lgth+off) and (ycor[iseed]+radius>lgth+off):
            alpha = abs(atan((ycor[iseed]-(lgth+off))/(xcor[iseed]-(lgth+off)))) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]-radius*cos(alpha+dalpha),ycor[iseed]-radius*sin(alpha+dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]-radius*cos(alpha+dalpha),ycor[iseed]-radius*sin(alpha+dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]-radius*cos(alpha-dalpha),ycor[iseed]-radius*sin(alpha-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]-radius*cos(alpha-dalpha),ycor[iseed]-radius*sin(alpha-dalpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]+radius<lgth+off) and (ycor[iseed]+radius<lgth+off) and (xcor[iseed]-radius>off) and (ycor[iseed]-radius>off):
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)+dalpha),ycor[iseed]+radius*sin((PI/2)+dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)+dalpha),ycor[iseed]+radius*sin((PI/2)+dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)-dalpha),ycor[iseed]+radius*sin((PI/2)-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)-dalpha),ycor[iseed]+radius*sin((PI/2)-dalpha), dpth)),) #@UndefinedVariable
            
        else:   
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(dalpha),ycor[iseed]+radius*sin(dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(dalpha),ycor[iseed]+radius*sin(dalpha), dpth)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(-dalpha),ycor[iseed]+radius*sin(-dalpha), 0.)),) #@UndefinedVariable
            e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(-dalpha),ycor[iseed]+radius*sin(-dalpha), dpth)),) #@UndefinedVariable
            
            if e_fib_pick[0]==None or e_fib_pick[2]==None or (e_fib_pick[0]==e_fib_pick[2]):
                e_fib_pick=[]
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)+dalpha),ycor[iseed]+radius*sin((PI/2)+dalpha), 0.)),) #@UndefinedVariable
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)+dalpha),ycor[iseed]+radius*sin((PI/2)+dalpha), dpth)),) #@UndefinedVariable
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)-dalpha),ycor[iseed]+radius*sin((PI/2)-dalpha), 0.)),) #@UndefinedVariable
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((PI/2)-dalpha),ycor[iseed]+radius*sin((PI/2)-dalpha), dpth)),) #@UndefinedVariable
                
            if e_fib_pick[0]==None or e_fib_pick[2]==None or (e_fib_pick[0]==e_fib_pick[2]):
                e_fib_pick=[]
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(PI+dalpha),ycor[iseed]+radius*sin(PI+dalpha), 0.)),) #@UndefinedVariable
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(PI+dalpha),ycor[iseed]+radius*sin(PI+dalpha), dpth)),) #@UndefinedVariable
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(PI-dalpha),ycor[iseed]+radius*sin(PI-dalpha), 0.)),) #@UndefinedVariable
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos(PI-dalpha),ycor[iseed]+radius*sin(PI-dalpha), dpth)),) #@UndefinedVariable
                
            if e_fib_pick[0]==None or e_fib_pick[2]==None or (e_fib_pick[0]==e_fib_pick[2]):
                e_fib_pick=[]
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((-PI/2)+dalpha),ycor[iseed]+radius*sin((-PI/2)+dalpha), 0.)),) #@UndefinedVariable
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((-PI/2)+dalpha),ycor[iseed]+radius*sin((-PI/2)+dalpha), dpth)),) #@UndefinedVariable 
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((-PI/2)-dalpha),ycor[iseed]+radius*sin((-PI/2)-dalpha), 0.)),) #@UndefinedVariable
                e_fib_pick.append(e.findAt((xcor[iseed]+radius*cos((-PI/2)-dalpha),ycor[iseed]+radius*sin((-PI/2)-dalpha), dpth)),) #@UndefinedVariable
                
        prve.seedEdgeBySize(edges=e_fib_pick, size=fib_seed, constraint=FIXED) #@UndefinedVariable
        num_fib1 = prve.getEdgeSeeds(edge = e_fib_pick[0], attribute = NUMBER) #@UndefinedVariable
        num_fib2 = prve.getEdgeSeeds(edge = e_fib_pick[2], attribute = NUMBER) #@UndefinedVariable
        
    # Seed Interfaces
        int_seed=(2*PI*(radius+dr))/mesh_fib
        e_int_pick=[]
        e_int_thick=[]
        if (xcor[iseed]==off) and (ycor[iseed]-radius>off):
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(dalpha),ycor[iseed]+(radius+dr)*sin(dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(dalpha),ycor[iseed]+(radius+dr)*sin(dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(-dalpha),ycor[iseed]+(radius+dr)*sin(-dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(-dalpha),ycor[iseed]+(radius+dr)*sin(-dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]+(radius+dr/2.),ycor[iseed], 0.)),)
            e_int_thick.append(e.findAt((xcor[iseed]+(radius+dr/2.),ycor[iseed], dpth)),)
            
        elif (ycor[iseed]>=off-abs(off/100.)) and (ycor[iseed]<=off+abs(off/100.)) and (xcor[iseed]-radius>off):
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)+dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)-dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)-dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)-dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)-dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]+(radius+dr/2.), 0.)),)
            e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]+(radius+dr/2.), dpth)),)
            
        elif (xcor[iseed]==lgth+off) and (ycor[iseed]+radius<lgth+off):
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(PI+dalpha),ycor[iseed]+(radius+dr)*sin(PI+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(PI+dalpha),ycor[iseed]+(radius+dr)*sin(PI+dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(PI-dalpha),ycor[iseed]+(radius+dr)*sin(PI-dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(PI-dalpha),ycor[iseed]+(radius+dr)*sin(PI-dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]-(radius+dr/2.),ycor[iseed], 0.)),)
            e_int_thick.append(e.findAt((xcor[iseed]-(radius+dr/2.),ycor[iseed], dpth)),)
            
        elif (ycor[iseed]==lgth+off) and (xcor[iseed]+radius<lgth+off):
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((-PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((-PI/2)+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((-PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((-PI/2)+dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((-PI/2)-dalpha),ycor[iseed]+(radius+dr)*sin((-PI/2)-dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((-PI/2)-dalpha),ycor[iseed]+(radius+dr)*sin((-PI/2)-dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]-(radius+dr/2.), 0.)),)
            e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]-(radius+dr/2.), dpth)),)
            
        elif (xcor[iseed]-radius<off) and (ycor[iseed]-radius<off):
            alpha = abs(atan((off-ycor[iseed])/(off-xcor[iseed]))) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha+dalpha),ycor[iseed]+(radius+dr)*sin(alpha+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha+dalpha),ycor[iseed]+(radius+dr)*sin(alpha+dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha-dalpha),ycor[iseed]+(radius+dr)*sin(alpha-dalpha), 0.)),) #@UndefinedVariable  
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha-dalpha),ycor[iseed]+(radius+dr)*sin(alpha-dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha),ycor[iseed]+(radius+dr)*sin(alpha), 0.)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha),ycor[iseed]+(radius+dr)*sin(alpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]-radius<off) and (ycor[iseed]+radius>lgth+off):
            alpha = abs(atan((ycor[iseed]-(lgth+off))/(off-xcor[iseed]))) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha+dalpha),ycor[iseed]-(radius+dr)*sin(alpha+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha+dalpha),ycor[iseed]-(radius+dr)*sin(alpha+dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha-dalpha),ycor[iseed]-(radius+dr)*sin(alpha-dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha-dalpha),ycor[iseed]-(radius+dr)*sin(alpha-dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha),ycor[iseed]-(radius+dr)*sin(alpha), 0.)),)  #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(alpha),ycor[iseed]-(radius+dr)*sin(alpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]+radius>lgth+off) and (ycor[iseed]-radius<off):
            alpha = abs(atan((off-ycor[iseed])/(xcor[iseed]-(lgth+off)))) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha+dalpha),ycor[iseed]+(radius+dr)*sin(alpha+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha+dalpha),ycor[iseed]+(radius+dr)*sin(alpha+dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha-dalpha),ycor[iseed]+(radius+dr)*sin(alpha-dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha-dalpha),ycor[iseed]+(radius+dr)*sin(alpha-dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha),ycor[iseed]+(radius+dr)*sin(alpha), 0.)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha),ycor[iseed]+(radius+dr)*sin(alpha), dpth)),) #@UndefinedVariable
            
        elif (xcor[iseed]+radius>lgth+off) and (ycor[iseed]+radius>lgth+off):
            alpha = abs(atan((ycor[iseed]-(lgth+off))/(xcor[iseed]-(lgth+off)))) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha+dalpha),ycor[iseed]-(radius+dr)*sin(alpha+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha+dalpha),ycor[iseed]-(radius+dr)*sin(alpha+dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha-dalpha),ycor[iseed]-(radius+dr)*sin(alpha-dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha-dalpha),ycor[iseed]-(radius+dr)*sin(alpha-dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha),ycor[iseed]-(radius+dr)*sin(alpha), 0.)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed]-(radius+dr)*cos(alpha),ycor[iseed]-(radius+dr)*sin(alpha), dpth)),) #@UndefinedVariable
            
        else:
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)+dalpha), dpth)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((3*PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((3*PI/2)+dalpha), 0.)),) #@UndefinedVariable
            e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((3*PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((3*PI/2)+dalpha), dpth)),) #@UndefinedVariable
            e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]+(radius+dr/2.), 0.)),)
            e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]+(radius+dr/2.), dpth)),)
            e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]-(radius+dr/2.), 0.)),)
            e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]-(radius+dr/2.), dpth)),)
            
            if e_int_pick[0]==None or e_int_pick[2]==None or (e_int_pick[0]==e_int_pick[2]) or e_int_thick[0]==None or e_int_thick[2]==None or (e_int_thick[0]==e_int_thick[2]):
                e_int_pick=[]
                e_int_thick=[]
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)+dalpha), 0.)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)+dalpha), dpth)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)-dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)-dalpha), 0.)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((PI/2)-dalpha),ycor[iseed]+(radius+dr)*sin((PI/2)-dalpha), dpth)),) #@UndefinedVariable
                e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]+(radius+dr/2.), 0.)),)
                e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]+(radius+dr/2.), dpth)),)
                
            if e_int_pick[0]==None or e_int_pick[2]==None or (e_int_pick[0]==e_int_pick[2]) or e_int_thick[0]==None or e_int_thick[1]==None or (e_int_thick[0]==e_int_thick[1]):
                e_int_pick=[]
                e_int_thick=[]
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(PI+dalpha),ycor[iseed]+(radius+dr)*sin(PI+dalpha), 0.)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(PI+dalpha),ycor[iseed]+(radius+dr)*sin(PI+dalpha), dpth)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(PI-dalpha),ycor[iseed]+(radius+dr)*sin(PI-dalpha), 0.)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(PI-dalpha),ycor[iseed]+(radius+dr)*sin(PI-dalpha), dpth)),) #@UndefinedVariable
                e_int_thick.append(e.findAt((xcor[iseed]-(radius+dr/2.),ycor[iseed], 0.)),)
                e_int_thick.append(e.findAt((xcor[iseed]-(radius+dr/2.),ycor[iseed], dpth)),)
                
            if e_int_pick[0]==None or e_int_pick[2]==None or (e_int_pick[0]==e_int_pick[2]) or e_int_thick[0]==None or e_int_thick[1]==None or (e_int_thick[0]==e_int_thick[1]):
                e_int_pick=[]
                e_int_thick=[]
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((-PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((-PI/2)+dalpha), 0.)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((-PI/2)+dalpha),ycor[iseed]+(radius+dr)*sin((-PI/2)+dalpha), dpth)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((-PI/2)-dalpha),ycor[iseed]+(radius+dr)*sin((-PI/2)-dalpha), 0.)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos((-PI/2)-dalpha),ycor[iseed]+(radius+dr)*sin((-PI/2)-dalpha), dpth)),) #@UndefinedVariable
                e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]-(radius+dr/2.), 0.)),)
                e_int_thick.append(e.findAt((xcor[iseed],ycor[iseed]-(radius+dr/2.), dpth)),)
                
            if e_int_pick[0]==None or e_int_pick[2]==None or (e_int_pick[0]==e_int_pick[2]) or e_int_thick[0]==None or e_int_thick[1]==None or (e_int_thick[0]==e_int_thick[1]):
                e_int_pick=[]
                e_int_thick=[]
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(dalpha),ycor[iseed]+(radius+dr)*sin(dalpha), 0.)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(dalpha),ycor[iseed]+(radius+dr)*sin(dalpha), dpth)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(-dalpha),ycor[iseed]+(radius+dr)*sin(-dalpha), 0.)),) #@UndefinedVariable
                e_int_pick.append(e.findAt((xcor[iseed]+(radius+dr)*cos(-dalpha),ycor[iseed]+(radius+dr)*sin(-dalpha), dpth)),) #@UndefinedVariable
                e_int_thick.append(e.findAt((xcor[iseed]+(radius+dr/2.),ycor[iseed], 0.)),)
                e_int_thick.append(e.findAt((xcor[iseed]+(radius+dr/2.),ycor[iseed], dpth)),)
                
        prve.seedEdgeBySize(edges=e_int_pick, size=int_seed, constraint=FIXED) #@UndefinedVariable
        prve.seedEdgeByNumber(edges=e_int_thick, number=1, constraint=FIXED) #@UndefinedVariable

    # Check if Fibre and Interface have same Number of Seeds
        num_int1 = prve.getEdgeSeeds(edge = e_int_pick[0], attribute = NUMBER) #@UndefinedVariable
        num_int2 = prve.getEdgeSeeds(edge = e_int_pick[2], attribute = NUMBER) #@UndefinedVariable
        if num_fib1 !=num_int1:
            new_edge=[]
            num_seed = num_fib1
            new_edge.append(e_fib_pick[0])
            new_edge.append(e_int_pick[0])
            new_edge.append(e_fib_pick[1])
            new_edge.append(e_int_pick[1])
            prve.seedEdgeByNumber(edges=new_edge, number=num_seed, constraint=FIXED) #@UndefinedVariable
            same = 0 #@UnusedVariable
        if num_fib2 != num_int2:
            new_edge=[]
            num_seed = num_fib2 
            new_edge.append(e_fib_pick[2])
            new_edge.append(e_int_pick[2])
            new_edge.append(e_fib_pick[3])
            new_edge.append(e_int_pick[3])      
            prve.seedEdgeByNumber(edges=new_edge, number=num_seed, constraint=FIXED) #@UndefinedVariable
            same = 0 #@UnusedVariable
    # Seed Inner Fibres
    
        e_fib_in1 = []
        fib_in_seed=0.9*fib_seed #@UnusedVariable
        if (xcor[iseed]+radius<lgth+off) and (xcor[iseed]-radius>off) and (ycor[iseed]+radius<lgth+off) and (ycor[iseed]-radius>off):
            e_fib_in1.append(e.findAt((xcor[iseed]+0.9*radius,ycor[iseed],0.)))
            e_fib_in1.append(e.findAt((xcor[iseed]+0.9*radius,ycor[iseed],dpth)))
        elif (xcor[iseed]-radius<off) and (ycor[iseed]<lgth+off) and (ycor[iseed]>off):
            e_fib_in1.append(e.findAt((xcor[iseed]+0.9*radius,ycor[iseed],0.)))
            e_fib_in1.append(e.findAt((xcor[iseed]+0.9*radius,ycor[iseed],dpth)))
        elif (xcor[iseed]+radius>lgth+off) and (ycor[iseed]<lgth+off) and (ycor[iseed]>off):
            e_fib_in1.append(e.findAt((xcor[iseed]-0.9*radius,ycor[iseed],0.)))
            e_fib_in1.append(e.findAt((xcor[iseed]-0.9*radius,ycor[iseed],dpth)))
        elif (ycor[iseed]-radius<off) and (xcor[iseed]<lgth+off) and (xcor[iseed]>off):
            e_fib_in1.append(e.findAt((xcor[iseed],ycor[iseed]+0.9*radius,0.)))
            e_fib_in1.append(e.findAt((xcor[iseed],ycor[iseed]+0.9*radius,dpth)))
        elif (ycor[iseed]+radius>lgth+off) and (xcor[iseed]<lgth+off) and (xcor[iseed]>off):
            e_fib_in1.append(e.findAt((xcor[iseed],ycor[iseed]-0.9*radius,0.)))
            e_fib_in1.append(e.findAt((xcor[iseed],ycor[iseed]-0.9*radius,dpth)))
        elif (xcor[iseed]-radius<off) and (ycor[iseed]-radius<off):
            alpha = abs(atan((off-ycor[iseed])/(off-xcor[iseed]))) #@UndefinedVariable
            e_fib_in1.append(e.findAt((xcor[iseed]+0.9*(radius)*cos(alpha),ycor[iseed]+0.9*(radius)*sin(alpha), 0.)),) #@UndefinedVariable   
            e_fib_in1.append(e.findAt((xcor[iseed]+0.9*(radius)*cos(alpha),ycor[iseed]+0.9*(radius)*sin(alpha), dpth)),) #@UndefinedVariable
        elif (xcor[iseed]-radius<off) and (ycor[iseed]+radius>lgth+off):
            alpha = abs(atan((ycor[iseed]-(lgth+off))/(off-xcor[iseed]))) #@UndefinedVariable
            e_fib_in1.append(e.findAt((xcor[iseed]+0.9*(radius)*cos(alpha),ycor[iseed]-0.9*(radius)*sin(alpha), 0.)),) #@UndefinedVariable   
            e_fib_in1.append(e.findAt((xcor[iseed]+0.9*(radius)*cos(alpha),ycor[iseed]-0.9*(radius)*sin(alpha), dpth)),) #@UndefinedVariable
        elif (xcor[iseed]+radius>lgth+off) and (ycor[iseed]+radius>lgth+off):
            alpha = abs(atan((ycor[iseed]-(lgth+off))/(xcor[iseed]-(lgth+off)))) #@UndefinedVariable
            e_fib_in1.append(e.findAt((xcor[iseed]-0.9*(radius)*cos(alpha),ycor[iseed]-0.9*(radius)*sin(alpha), 0.)),) #@UndefinedVariable   
            e_fib_in1.append(e.findAt((xcor[iseed]-0.9*(radius)*cos(alpha),ycor[iseed]-0.9*(radius)*sin(alpha), dpth)),) #@UndefinedVariable
        elif (xcor[iseed]+radius>lgth+off) and (ycor[iseed]-radius<off):
            alpha = abs(atan((off-ycor[iseed])/(xcor[iseed]-(lgth+off)))) #@UndefinedVariable
            e_fib_in1.append(e.findAt((xcor[iseed]-0.9*(radius)*cos(alpha),ycor[iseed]+0.9*(radius)*sin(alpha), 0.)),) #@UndefinedVariable  
            e_fib_in1.append(e.findAt((xcor[iseed]-0.9*(radius)*cos(alpha),ycor[iseed]+0.9*(radius)*sin(alpha), dpth)),) #@UndefinedVariable
        else:
            pass
        num_in_seed = num_fib1 + num_fib2
        prve.seedEdgeByNumber(edges = e_fib_in1, number = num_in_seed, constraint = FIXED) #@UndefinedVariable
        e_fib_in2 = []
        if (xcor[iseed]+radius<lgth+off) and (xcor[iseed]-radius>off) and (ycor[iseed]+radius<lgth+off) and (ycor[iseed]-radius>off):
            e_fib_in2.append(e.findAt((xcor[iseed]+0.5*radius,ycor[iseed],0.)))
            e_fib_in2.append(e.findAt((xcor[iseed]+0.5*radius,ycor[iseed],dpth)))
            prve.seedEdgeBySize(edges = e_fib_in2, size = 2.*fib_seed, constraint = FREE) #@UndefinedVariable
            
    print('*** SEEDING FINISHED! ***')
    
    #=====================================================
    # Material/Section/Elementtype Definition & Assignment
    #=====================================================
    print('*** ASSIGNING MATERIALS AND SECTIONS...! ***')
    d = prve.datums
    fibre_csys = prve.DatumCsysByTwoLines(coordSysType = CARTESIAN, line1 = d[daxis1], line2 = d[daxis2]).id #@UndefinedVariable
    allinterfaces = [] #@UnusedVariable
    if fvc != 0.:
    # Fibre 
        d = prve.datums
        
        fib_mat = m.Material(name = 'Fibre')
        fib_mat.Elastic(table = ((E11_fib, E22_fib, E33_fib, nu12_fib, nu31_fib, nu23_fib, G12_fib, G31_fib, G23_fib),), type = ENGINEERING_CONSTANTS) #@UndefinedVariable
        m.HomogeneousSolidSection(name = 'Fibre_Section', material = 'Fibre')
        fib_elem = mesh.ElemType(elemCode = ElementID, elemLibrary = STANDARD, secondOrderAccuracy = OFF, hourglassControl = DEFAULT) #@UndefinedVariable
        fibresection = []
        
        for ifib in range(len(xcor)):
            radius = radius_old[ifib]
            cell = prve.cells
            if xcor[ifib]-radius>=off and xcor[ifib]+radius<=lgth+off and ycor[ifib]-radius>=off and ycor[ifib]+radius<=lgth+off:
                fibresection.append(cell.findAt((xcor[ifib],ycor[ifib],0.)))
                fibresection.append(cell.findAt((xcor[ifib]+0.95*radius,ycor[ifib],0.)))
                fibresection.append(cell.findAt((xcor[ifib]+0.6*radius,ycor[ifib],0.)))
            elif xcor[ifib]-radius<off and ycor[ifib]>off and ycor[ifib]<lgth+off:
                fibresection.append(cell.findAt((xcor[ifib]+0.85*radius,ycor[ifib],0.)))
                fibresection.append(cell.findAt((xcor[ifib]+0.95*radius,ycor[ifib],0.)))
            elif xcor[ifib]+radius>lgth+off and ycor[ifib]>off and ycor[ifib]<lgth+off:
                fibresection.append(cell.findAt((xcor[ifib]-0.85*radius,ycor[ifib],0.)))
                fibresection.append(cell.findAt((xcor[ifib]-0.95*radius,ycor[ifib],0.)))
            elif ycor[ifib]-radius<off and xcor[ifib]>off and xcor[ifib]<lgth+off:
                fibresection.append(cell.findAt((xcor[ifib],ycor[ifib]+0.85*radius,0.)))
                fibresection.append(cell.findAt((xcor[ifib],ycor[ifib]+0.95*radius,0.)))
            elif ycor[ifib]+radius>lgth+off and xcor[ifib]>off and xcor[ifib]<lgth+off:
                fibresection.append(cell.findAt((xcor[ifib],ycor[ifib]-0.85*radius,0.)))
                fibresection.append(cell.findAt((xcor[ifib],ycor[ifib]-0.95*radius,0.)))
            elif xcor[ifib]<off and ycor[ifib]<off:
                alpha = abs(atan((off-ycor[ifib])/(off-xcor[ifib]))) #@UndefinedVariable
                fibresection.append(cell.findAt((off,off,0.)))
                fibresection.append(cell.findAt((xcor[ifib]+0.95*radius*cos(alpha),ycor[ifib]+0.95*radius*sin(alpha),0.))) #@UndefinedVariable
            elif xcor[ifib]>lgth+off and ycor[ifib]<off:
                alpha = abs(atan((off-ycor[ifib])/(xcor[ifib]-(lgth+off)))) #@UndefinedVariable
                fibresection.append(cell.findAt((lgth+off,off,0.)))
                fibresection.append(cell.findAt((xcor[ifib]-0.95*radius*cos(alpha),ycor[ifib]+0.95*radius*sin(alpha),0.))) #@UndefinedVariable
            elif xcor[ifib]<off and ycor[ifib]>lgth+off:
                alpha = abs(atan((ycor[ifib]-(lgth+off))/(off-xcor[ifib]))) #@UndefinedVariable
                fibresection.append(cell.findAt((off,lgth+off,0.)))
                fibresection.append(cell.findAt((xcor[ifib]+0.95*radius*cos(alpha),ycor[ifib]-0.95*radius*sin(alpha),0.))) #@UndefinedVariable
            elif xcor[ifib]>lgth+off and ycor[ifib]>lgth+off:
                alpha = abs(atan((ycor[ifib]-(lgth+off))/(xcor[ifib]-(lgth+off)))) #@UndefinedVariable
                fibresection.append(cell.findAt((lgth+off,lgth+off,0.)))
                fibresection.append(cell.findAt((xcor[ifib]-0.95*radius*cos(alpha),ycor[ifib]-0.95*radius*sin(alpha),0.))) #@UndefinedVariable
                
        prve.SectionAssignment(region = fibresection, sectionName = 'Fibre_Section')    
        prve.setElementType(regions = (fibresection,), elemTypes = (fib_elem,)) 
        prve.MaterialOrientation(region = fibresection, localCsys = d[fibre_csys], orientationType = SYSTEM) #@UndefinedVariable
        if not ShapeID.startswith("HEX"): prve.setMeshControls(regions = fibresection, elemShape = TET, technique = FREE) #@UndefinedVariable
        else: prve.setMeshControls(regions = fibresection, elemShape = HEX_DOMINATED, technique = SWEEP, algorithm = ADVANCING_FRONT) #@UndefinedVariable
        
    # Interface
        
        
        int_mat = m.Material(name = 'Interface')
        
        if lc == 'static':
            int_mat.Elastic(table = ((E_int, G1_int, G2_int),), type = TRACTION) #@UndefinedVariable
            int_mat.MaxsDamageInitiation(table = ((tnn, tss, ttt),))
            int_mat.maxsDamageInitiation.DamageEvolution(type = ENERGY, table = ((frac_en,),)) #@UndefinedVariable
            if int_visc == 'off':
                pass
            else:
                int_mat.maxsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff = visc)
            m.CohesiveSection(name = 'Interface_Section', material = 'Interface', response = TRACTION_SEPARATION, initialThicknessType = SPECIFY, initialThickness = dr, outOfPlaneThickness = dr) #@UndefinedVariable
            if not ShapeID.startswith("HEX"): int_elem = mesh.ElemType(elemCode=(COH3D6, C3D4,), elemLibrary=STANDARD) #@UndefinedVariable
            else: int_elem = mesh.ElemType(elemCode=COH3D8, elemLibrary=STANDARD) #@UndefinedVariable
            
        if lc == 'cyclic':
            ###int_mat.Elastic(table = ((E_int, G1_int, G2_int),), type = TRACTION)
            ###int_mat.MaxsDamageInitiation(table = ((tnn, tss, ttt),))
            ###int_mat.maxsDamageInitiation.DamageEvolution(type = ENERGY, table = ((frac_en,),))
            ###if int_visc == 'off':
            ### pass
            ###else:
            ### int_mat.maxsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff = visc)
            int_mat.UserMaterial(type = MECHANICAL, unsymm = OFF, mechanicalConstants = (E_res1, nu_res, E_res2, nu_res, D_res, nu_res, k1, k2, dDmax,1., freq, dNmin,)) #@UndefinedVariable
            int_mat.Depvar(n = 8)
            m.HomogeneousSolidSection(name = 'Interface_Section', material = 'Interface')
            int_elem = mesh.ElemType(elemCode=ElementID, elemLibrary=STANDARD, secondOrderAccuracy = OFF, hourglassControl=DEFAULT) #@UndefinedVariable
        
        interfacesection=[]
        dalpha = PI/360.
        
        for iint in range(len(xcor)):
            int_csys = prve.DatumCsysByThreePoints(coordSysType = CYLINDRICAL, origin = (xcor[iint], ycor[iint], 0.), point1 = (xcor[iint]+0.1, ycor[iint], 0.), point2 = (xcor[iint], ycor[iint]+0.1, 0.)).id #@UndefinedVariable
            radius = radius_old[iint]
            e, cell, d = prve.edges, prve.cells, prve.datums
            interfacesection = []
            
            if xcor[iint]-radius>off and xcor[iint]+radius<lgth+off and ycor[iint]-radius>off and ycor[iint]+radius<lgth+off:
                sweepedge = e.findAt((xcor[iint],ycor[iint]-radius-dr,dpth/2.))
                interfacesection.append(cell.findAt((xcor[iint]+radius+dr/2,ycor[iint],0.)),)
                sweepregion = cell.findAt((xcor[iint]+radius+dr/2,ycor[iint],0.))
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]-radius-dr/2,ycor[iint],0.)),)
                sweepregion = cell.findAt((xcor[iint]-radius-dr/2,ycor[iint],0.))
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
            elif xcor[iint]-radius<off and ycor[iint]-radius>off and ycor[iint]+radius<lgth+off:
                sweepedge = e.findAt((xcor[iint]+radius+dr,ycor[iint],dpth/2.))
                interfacesection.append(cell.findAt((xcor[iint]+(radius+dr/2)*cos(dalpha),ycor[iint]+(radius+dr/2)*sin(dalpha),0.)),) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]+(radius+dr/2)*cos(dalpha),ycor[iint]+(radius+dr/2)*sin(dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]+(radius+dr/2)*cos(dalpha),ycor[iint]-(radius+dr/2)*sin(dalpha),0.)),) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]+(radius+dr/2)*cos(dalpha),ycor[iint]-(radius+dr/2)*sin(dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
            elif xcor[iint]+radius>lgth+off and ycor[iint]-radius>off and ycor[iint]+radius<lgth+off:
                sweepedge = e.findAt((xcor[iint]-radius-dr,ycor[iint],dpth/2.))
                interfacesection.append(cell.findAt((xcor[iint]-(radius+dr/2)*cos(dalpha),ycor[iint]+(radius+dr/2)*sin(dalpha),0.)),) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]-(radius+dr/2)*cos(dalpha),ycor[iint]+(radius+dr/2)*sin(dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]-(radius+dr/2)*cos(dalpha),ycor[iint]-(radius+dr/2)*sin(dalpha),0.)),) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]-(radius+dr/2)*cos(dalpha),ycor[iint]-(radius+dr/2)*sin(dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
            elif ycor[iint]-radius<off and xcor[iint]-radius>off and xcor[iint]+radius<lgth+off:
                sweepedge = e.findAt((xcor[iint],ycor[iint]+radius+dr,dpth/2.))
                interfacesection.append(cell.findAt((xcor[iint]+(radius+dr/2)*cos(PI/2.+dalpha),ycor[iint]+(radius+dr/2)*sin(PI/2.+dalpha),0.)),) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]+(radius+dr/2)*cos(PI/2.+dalpha),ycor[iint]+(radius+dr/2)*sin(PI/2.+dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]-(radius+dr/2)*cos(PI/2.+dalpha),ycor[iint]+(radius+dr/2)*sin(PI/2.+dalpha),0.)),) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]-(radius+dr/2)*cos(PI/2.+dalpha),ycor[iint]+(radius+dr/2)*sin(PI/2.+dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
            elif ycor[iint]+radius>lgth+off and xcor[iint]-radius>off and xcor[iint]+radius<lgth+off:
                sweepedge = e.findAt((xcor[iint],ycor[iint]-radius-dr,dpth/2.))
                interfacesection.append(cell.findAt((xcor[iint]+(radius+dr/2)*cos(PI/2.+dalpha),ycor[iint]-(radius+dr/2)*sin(PI/2.+dalpha),0.)),) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]+(radius+dr/2)*cos(PI/2.+dalpha),ycor[iint]-(radius+dr/2)*sin(PI/2.+dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]-(radius+dr/2)*cos(PI/2.+dalpha),ycor[iint]-(radius+dr/2)*sin(PI/2.+dalpha),0.)),) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]-(radius+dr/2)*cos(PI/2.+dalpha),ycor[iint]-(radius+dr/2)*sin(PI/2.+dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
            elif xcor[iint]-radius<=off and ycor[iint]-radius<=off:
                alpha = abs(atan((off-ycor[iint])/(off-xcor[iint]))) #@UndefinedVariable
                sweepedge = e.findAt((xcor[iint]+(radius+dr)*cos(alpha),ycor[iint]+(radius+dr)*sin(alpha),dpth/2.)) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]+(radius+dr/2)*cos(alpha+dalpha),ycor[iint]+(radius+dr/2)*sin(alpha+dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]+(radius+dr/2)*cos(alpha-dalpha),ycor[iint]+(radius+dr/2)*sin(alpha-dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]+(radius+dr/2)*cos(alpha+dalpha),ycor[iint]+(radius+dr/2)*sin(alpha+dalpha),0.)),) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]+(radius+dr/2)*cos(alpha-dalpha),ycor[iint]+(radius+dr/2)*sin(alpha-dalpha),0.)),) #@UndefinedVariable
            elif xcor[iint]+radius>=lgth+off and ycor[iint]-radius<=off:
                alpha = abs(atan((off-ycor[iint])/(xcor[iint]-(lgth+off)))) #@UndefinedVariable
                sweepedge = e.findAt((xcor[iint]-(radius+dr)*cos(alpha),ycor[iint]+(radius+dr)*sin(alpha),dpth/2.)) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]-(radius+dr/2)*cos(alpha+dalpha),ycor[iint]+(radius+dr/2)*sin(alpha+dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]-(radius+dr/2)*cos(alpha-dalpha),ycor[iint]+(radius+dr/2)*sin(alpha-dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]-(radius+dr/2)*cos(alpha+dalpha),ycor[iint]+(radius+dr/2)*sin(alpha+dalpha),0.)),) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]-(radius+dr/2)*cos(alpha-dalpha),ycor[iint]+(radius+dr/2)*sin(alpha-dalpha),0.)),) #@UndefinedVariable
            elif xcor[iint]-radius<=off and ycor[iint]+radius>=lgth+off:
                alpha = abs(atan((ycor[iint]-(lgth+off))/(off-xcor[iint]))) #@UndefinedVariable
                sweepedge = e.findAt((xcor[iint]+(radius+dr)*cos(alpha),ycor[iint]-(radius+dr)*sin(alpha),dpth/2.)) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]+(radius+dr/2)*cos(alpha+dalpha),ycor[iint]-(radius+dr/2)*sin(alpha+dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]+(radius+dr/2)*cos(alpha-dalpha),ycor[iint]-(radius+dr/2)*sin(alpha-dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]+(radius+dr/2)*cos(alpha+dalpha),ycor[iint]-(radius+dr/2)*sin(alpha+dalpha),0.)),) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]+(radius+dr/2)*cos(alpha-dalpha),ycor[iint]-(radius+dr/2)*sin(alpha-dalpha),0.)),) #@UndefinedVariable
            elif xcor[iint]+radius>=lgth+off and ycor[iint]+radius>=lgth+off:
                alpha = abs(atan((ycor[iint]-(lgth+off))/(xcor[iint]-(lgth+off)))) #@UndefinedVariable
                sweepedge = e.findAt((xcor[iint]-(radius+dr)*cos(alpha),ycor[iint]-(radius+dr)*sin(alpha),dpth/2.)) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]-(radius+dr/2)*cos(alpha+dalpha),ycor[iint]-(radius+dr/2)*sin(alpha+dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                sweepregion = cell.findAt((xcor[iint]-(radius+dr/2)*cos(alpha-dalpha),ycor[iint]-(radius+dr/2)*sin(alpha-dalpha),0.)) #@UndefinedVariable
                prve.setSweepPath(region = sweepregion, edge = sweepedge, sense = FORWARD) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]-(radius+dr/2)*cos(alpha+dalpha),ycor[iint]-(radius+dr/2)*sin(alpha+dalpha),0.)),) #@UndefinedVariable
                interfacesection.append(cell.findAt((xcor[iint]-(radius+dr/2)*cos(alpha-dalpha),ycor[iint]-(radius+dr/2)*sin(alpha-dalpha),0.)),) #@UndefinedVariable
            if lc == 'cyclic':
                prve.MaterialOrientation(region = interfacesection, localCsys = d[int_csys], orientationType= SYSTEM, axis = AXIS_2, angle = 90.) #@UndefinedVariable
                prve.SectionAssignment(region = interfacesection, sectionName = 'Interface_Section')
            prve.setElementType(regions = (interfacesection,), elemTypes = (int_elem,)) 
            if not ShapeID.startswith("HEX"): prve.setMeshControls(regions = interfacesection, elemShape = TET, technique = FREE) #@UndefinedVariable
            else: prve.setMeshControls(regions = interfacesection, elemShape = HEX_DOMINATED, technique = SWEEP, algorithm = ADVANCING_FRONT) #@UndefinedVariable
            
    # Resin 
        res_mat = m.Material(name = 'Resin')
        if lc == 'static':
            res_mat.Elastic(table =((E_res1 + E_res2, nu_res),))
            #res_mat.Plastic(table=((20., 0.), (25.1825, 0.00027835), (30.27, 0.00055141), (35.3675, 0.00062095), (40.5, 0.00117252), (45.6525, 0.00171463), (50.85, 0.00273212), (56.1, 0.00421929), (61.44, 0.00664986), (64.7325, 0.00914742), (66.95, 0.01096158), (68.145, 0.01305388)), temperatureDependency = OFF, dependencies = 0, hardening = ISOTROPIC)
            res_mat.MohrCoulombPlasticity(table=((fric_angle, dil_angle), ), temperatureDependency = OFF, dependencies = 0) #@UndefinedVariable
            res_mat.mohrCoulombPlasticity.MohrCoulombHardening(table=((sig_yield_res, 0.), ), temperatureDependency = OFF, dependencies = 0) #@UndefinedVariable
            res_mat.mohrCoulombPlasticity.TensionCutOff(table=((0., 0.), ), temperatureDependency = OFF, dependencies = 0) #@UndefinedVariable
        elif lc == 'cyclic':
            res_mat.UserMaterial(type = MECHANICAL, unsymm = OFF, mechanicalConstants = (E_res1, nu_res, E_res2, nu_res, D_res, nu_res, c1, c2, dDmax,0., freq, dNmin,)) #@UndefinedVariable
            res_mat.Depvar(n = 8)
        m.HomogeneousSolidSection(name = 'Resin_Section', material = 'Resin')
        res_elem = mesh.ElemType(elemCode=ElementID, elemLibrary=STANDARD, secondOrderAccuracy = OFF, hourglassControl=DEFAULT) #@UndefinedVariable
            
        resinsection=[]
        for ires in range(len(xcor)):
            radius = radius_old[ires]
            cell = prve.cells
            if (xcor[ires]-radius)>off and (xcor[ires]+radius)<lgth+off and (ycor[ires]-radius)>off and (ycor[ires]+radius)<lgth+off :
                resinsection.append(cell.findAt((xcor[ires]+radius+dr+dmin/2,ycor[ires],0.)))
                break
            elif xcor[ires]<=off and ycor[ires]<lgth+off and ycor[ires]>off:
                resinsection.append(cell.findAt((xcor[ires]+radius+dr+dmin/2,ycor[ires],0.)))
                break
            elif xcor[ires]>=lgth+off and ycor[ires]<lgth+off and ycor[ires]>off:
                resinsection.append(cell.findAt((xcor[ires]-radius-dr-dmin/2,ycor[ires],0.)))
                break
            elif ycor[ires]<=off and xcor[ires]<lgth+off and xcor[ires]>off:
                resinsection.append(cell.findAt((xcor[ires],ycor[ires]+radius+dr+dmin/2,0.)))
                break
            elif ycor[ires]>=lgth+off and ycor[ires]<lgth+off and ycor[ires]>off:
                resinsection.append(cell.findAt((xcor[ires],ycor[ires]-radius-dr-dmin/2,0.)))
                break
            elif xcor[ires]<off and ycor[ires]<off:
                alpha = abs(atan((off-ycor[ires])/(off-xcor[ires]))) #@UndefinedVariable
                resinsection.append(cell.findAt((xcor[ires]+(radius+dr+dmin/2)*cos(alpha),ycor[ires]+(radius+dr+dmin/2)*sin(alpha),0.))) #@UndefinedVariable
                break
            elif xcor[ires]<off and ycor[ires]>lgth+off:
                alpha = abs(atan((ycor[ires]-(lgth+off))/(off-xcor[ires]))) #@UndefinedVariable
                resinsection.append(cell.findAt((xcor[ires]+(radius+dr+dmin/2)*cos(alpha),ycor[ires]-(radius+dr+dmin/2)*sin(alpha),0.))) #@UndefinedVariable
                break
            elif xcor[ires]>lgth+off and ycor[ires]<off:
                alpha = abs(atan((off-ycor[ires])/(xcor[ires]-(lgth+off)))) #@UndefinedVariable
                resinsection.append(cell.findAt((xcor[ires]-(radius+dr+dmin/2)*cos(alpha),ycor[ires]+(radius+dr+dmin/2)*sin(alpha),0.))) #@UndefinedVariable
                break
            elif xcor[ires]>lgth+off and ycor[ires]>lgth+off:
                alpha = abs(atan((ycor[ires]-(lgth+off))/(xcor[ires]-(lgth+off)))) #@UndefinedVariable
                resinsection.append(cell.findAt((xcor[ires]-(radius+dr+dmin/2)*cos(alpha),ycor[ires]-(radius+dr+dmin/2)*sin(alpha),0.))) #@UndefinedVariable
                break
        prve.SectionAssignment(region = resinsection, sectionName = 'Resin_Section')
        prve.setElementType(regions = (resinsection,), elemTypes = (res_elem,)) 
        prve.MaterialOrientation(region = resinsection, localCsys = d[fibre_csys], orientationType= SYSTEM) #@UndefinedVariable
        if not ShapeID.startswith("HEX"): prve.setMeshControls(regions = resinsection, elemShape = TET, technique = FREE) #@UndefinedVariable
        else: prve.setMeshControls(regions = resinsection, elemShape = HEX_DOMINATED, technique = SWEEP, algorithm = ADVANCING_FRONT) #@UndefinedVariable
        
    else:
        resinsection=[]
        cell = prve.cells
        res_mat = m.Material(name =  'Resin')
        if lc == 'static':
            res_mat.Elastic(table =((E_res, nu_res),)) #@UndefinedVariable
            res_mat.MohrCoulombPlasticity(table=((fric_angle, dil_angle), ), temperatureDependency = OFF, dependencies = 0) #@UndefinedVariable
            res_mat.mohrCoulombPlasticity.MohrCoulombHardening(table=((sig_yield_res, 0.), ), temperatureDependency = OFF, dependencies = 0) #@UndefinedVariable
            res_mat.mohrCoulombPlasticity.TensionCutOff(table=((0., 0.), ), temperatureDependency = OFF, dependencies = 0) #@UndefinedVariable
        elif lc == 'cyclic':
            res_mat.UserMaterial(type = MECHANICAL, unsymm = OFF, mechanicalConstants = (E_res1, nu_res, E_res2, nu_res, D_res, nu_res, c1, c2, dDmax, 0., freq, dNmin,)) #@UndefinedVariable
            res_mat.Depvar(n = 8)
        m.HomogeneousSolidSection(name = 'Resin_Section', material = 'Resin', thickness = None)
        res_elem = mesh.ElemType(elemCode=ElementID, elemLibrary=STANDARD, secondOrderAccuracy = OFF, hourglassControl=DEFAULT) #@UndefinedVariable
        resinsection.append(cell.findAt((off,off,0.)))
        prve.SectionAssignment(region = resinsection, sectionName = 'Resin_Section')
        prve.setElementType(regions = (resinsection,), elemTypes = (res_elem,)) 
        prve.MaterialOrientation(region = resinsection, localCsys = d[fibre_csys], orientationType= SYSTEM) #@UndefinedVariable
        prve.setMeshControls(regions = resinsection, elemShape = ShapeID, technique = SWEEP) #@UndefinedVariable
        
    print('*** MATERIAL AND SECTION ASSIGNMENT FINISHED! ***')
    pickedpart = cell.getByBoundingBox(xMin = off-lgth/10.,yMin = off-lgth/10.,zMin = 0.-lgth/10.,xMax = lgth+off+lgth/10.,yMax = lgth+off+lgth/10.,zMax= dpth+lgth/10.)
    prve.generateMesh(regions = pickedpart)
    print('*** MESHING FINISHED! ***')
        
    #========================================       
    # Instance the Part
    #========================================
    
    RVE_ass = m.rootAssembly
    RVE_inst = RVE_ass.Instance(name='Instance of RVE', part=prve, dependent=ON) #@UndefinedVariable
    RVE_ass.regenerate()
    #========================================
    # Create Elementsets for Cohesive Orientation
    #========================================
    if lc == 'static':
        elem = RVE_inst.elements
        for ielem in range(len(xcor)):
            int_elems = []
            all_elems = elem.getByBoundingCylinder(center1 = (xcor[ielem], ycor[ielem], -0.1), center2 = (xcor[ielem], ycor[ielem], dpth+0.1), radius = radius_old[ielem]+dr+dmin/2.)
            for isel in range(len(all_elems)):
                if all_elems[isel].type==COH3D8 or all_elems[isel].type==COH3D6: #@UndefinedVariable
                    int_elems.append(all_elems[isel].label)
                else:
                    pass
            int_elems = tuple(int_elems)
            if int_elems: 
                prve.SetFromElementLabels(name = 'int_'+str(ielem+1), elementLabels = int_elems)
                prve.SectionAssignment(region = prve.sets['int_'+str(ielem+1)], sectionName = 'Interface_Section') 
    
    #========================================
    # Equation Constraints
    #========================================
    
    # Referencepoints for Equations
    refptx = RVE_ass.ReferencePoint(point = (1.25*(lgth+off), 0., dpth/2)).id
    refpty = RVE_ass.ReferencePoint(point = (0., 1.25*(lgth+off) , dpth/2)).id
    refptz = RVE_ass.ReferencePoint(point = (0., 0., 1.25*dpth)).id
    r = RVE_ass.referencePoints
    
    RVE_ass.Set(name = 'Rfptx', referencePoints = (r[refptx],))
    RVE_ass.Set(name = 'Rfpty', referencePoints = (r[refpty],))
    RVE_ass.Set(name = 'Rfptz', referencePoints = (r[refptz],))
    
    n = RVE_inst.nodes
    
    # Nodes on Faces except Edges
    x0_nodes = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = off+rve_seed/1000., zMin = 0.+rve_seed/1000., xMax= off+rve_seed/1000., yMax  = lgth+off-rve_seed/1000., zMax = dpth-rve_seed/1000.)
    x1_nodes = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = off+rve_seed/1000., zMin = 0.+rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = lgth+off-rve_seed/1000., zMax = dpth-rve_seed/1000.)
    y0_nodes = n.getByBoundingBox(xMin = off+rve_seed/1000., yMin = off-rve_seed/1000., zMin = 0.+rve_seed/1000., xMax= lgth+off-rve_seed/1000., yMax  = off+rve_seed/1000., zMax = dpth-rve_seed/1000.)
    y1_nodes = n.getByBoundingBox(xMin = off+rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = 0.+rve_seed/1000., xMax= lgth+off-rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = dpth-rve_seed/1000.)
    z0_nodes = n.getByBoundingBox(xMin = off+rve_seed/1000., yMin = off+rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= lgth+off-rve_seed/1000., yMax  = lgth+off-rve_seed/1000., zMax = 0.+rve_seed/1000.)
    z1_nodes = n.getByBoundingBox(xMin = off+rve_seed/1000., yMin = off+rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= lgth+off-rve_seed/1000., yMax  = lgth+off-rve_seed/1000., zMax = dpth+rve_seed/1000.)
    
    RVE_ass.Set(name = 'Face_x0', nodes = x0_nodes)
    RVE_ass.Set(name = 'Face_x1', nodes = x1_nodes)
    RVE_ass.Set(name = 'Face_y0', nodes = y0_nodes)
    RVE_ass.Set(name = 'Face_y1', nodes = y1_nodes)
    RVE_ass.Set(name = 'Face_z0', nodes = z0_nodes)
    RVE_ass.Set(name = 'Face_z1', nodes = z1_nodes)
    
    #-------------------------
    # Face Constrains
    #-------------------------
    print('*** APPLYING EQUATION CONSTRAINTS...! ***')
    r = RVE_ass.referencePoints
    for i in range(len(x0_nodes)):
        y = x0_nodes[i].coordinates[1]
        z = x0_nodes[i].coordinates[2]
        RVE_ass.Set(nodes = x0_nodes[i:i+1], name = 'nset_x0_face_'+str(i) )
        opposingNode = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = y-rve_seed/1000, zMin = z-rve_seed/1000, xMax = lgth+off+rve_seed/1000, yMax = y+rve_seed/1000, zMax = z+rve_seed/1000 )
        RVE_ass.Set(nodes = opposingNode, name = 'nset_x1_face_'+str(i) )
    
        m.Equation( name='xface_x_'+str(i), terms=((-1.0, 'nset_x0_face_'+str(i), 1),(1.0, 'nset_x1_face_'+str(i), 1),(-lgth, 'Rfptx', 1),))  #Rfpt x -> delta x
        m.Equation( name='xface_y_'+str(i), terms=((-1.0, 'nset_x0_face_'+str(i), 2),(1.0, 'nset_x1_face_'+str(i), 2),(-lgth, 'Rfptx', 2),))
        m.Equation( name='xface_z_'+str(i), terms=((-1.0, 'nset_x0_face_'+str(i), 3),(1.0, 'nset_x1_face_'+str(i), 3),(-lgth, 'Rfptx', 3),))
        
    for i in range(len(y0_nodes)):
        x = y0_nodes[i].coordinates[0]
        z = y0_nodes[i].coordinates[2]
        RVE_ass.Set(nodes = y0_nodes[i:i+1], name = 'nset_y0_face_'+str(i) )
        opposingNode = n.getByBoundingBox(xMin = x-rve_seed/1000., yMin = lgth+off-rve_seed/1000, zMin = z-rve_seed/1000, xMax = x+rve_seed/1000, yMax = lgth+off+rve_seed/1000, zMax = z+rve_seed/1000 )
        RVE_ass.Set(nodes = opposingNode, name = 'nset_y1_face_'+str(i) )
    
        m.Equation( name='yface_x_'+str(i), terms=((-1.0, 'nset_y0_face_'+str(i), 1),(1.0, 'nset_y1_face_'+str(i), 1),(-lgth, 'Rfpty', 1),))  #Rfpt y -> delta y
        m.Equation( name='yface_y_'+str(i), terms=((-1.0, 'nset_y0_face_'+str(i), 2),(1.0, 'nset_y1_face_'+str(i), 2),(-lgth, 'Rfpty', 2),))
        m.Equation( name='yface_z_'+str(i), terms=((-1.0, 'nset_y0_face_'+str(i), 3),(1.0, 'nset_y1_face_'+str(i), 3),(-lgth, 'Rfpty', 3),))
    
    for i in range(len(z0_nodes)):
        x = z0_nodes[i].coordinates[0]
        y = z0_nodes[i].coordinates[1]
        RVE_ass.Set(nodes = z0_nodes[i:i+1], name = 'nset_z0_face_'+str(i) )
        opposingNode = n.getByBoundingBox(xMin = x-rve_seed/1000., yMin = y-rve_seed/1000, zMin = dpth-rve_seed/1000, xMax = x+rve_seed/1000, yMax = y+rve_seed/1000, zMax = dpth+rve_seed/1000 )
        RVE_ass.Set(nodes = opposingNode, name = 'nset_z1_face_'+str(i) )
    
        m.Equation( name='zface_x_'+str(i), terms=((-1.0, 'nset_z0_face_'+str(i), 1),(1.0, 'nset_z1_face_'+str(i), 1),(-dpth, 'Rfptz', 1),))  #Rfpt z -> delta z
        m.Equation( name='zface_y_'+str(i), terms=((-1.0, 'nset_z0_face_'+str(i), 2),(1.0, 'nset_z1_face_'+str(i), 2),(-dpth, 'Rfptz', 2),))
        m.Equation( name='zface_z_'+str(i), terms=((-1.0, 'nset_z0_face_'+str(i), 3),(1.0, 'nset_z1_face_'+str(i), 3),(-dpth, 'Rfptz', 3),))    ###
        
    #Nodes on Edges except CornerVertices
    #Nodes for x-Rotation
    n = RVE_inst.nodes
    
    x_rot1_nodes = n.getByBoundingBox(xMin = off+rve_seed/1000., yMin = off-rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= lgth+off-rve_seed/1000., yMax  = off+rve_seed/1000., zMax = 0.+rve_seed/1000.)
    x_rot2_nodes = n.getByBoundingBox(xMin = off+rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= lgth+off-rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = 0.+rve_seed/1000.)
    x_rot3_nodes = n.getByBoundingBox(xMin = off+rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= lgth+off-rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = dpth+rve_seed/1000.)
    x_rot4_nodes = n.getByBoundingBox(xMin = off+rve_seed/1000., yMin = off-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= lgth+off-rve_seed/1000., yMax  = off+rve_seed/1000., zMax = dpth+rve_seed/1000.)
    
    RVE_ass.Set(name = 'Edge_xrot1', nodes = x_rot1_nodes)
    RVE_ass.Set(name = 'Edge_xrot2', nodes = x_rot2_nodes)
    RVE_ass.Set(name = 'Edge_xrot3', nodes = x_rot3_nodes)
    RVE_ass.Set(name = 'Edge_xrot4', nodes = x_rot4_nodes)
    
    
    # Nodes for y-Rotation
    n = RVE_inst.nodes
    
    y_rot1_nodes = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = off+rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= off+rve_seed/1000., yMax  = lgth+off-rve_seed/1000., zMax = 0.+rve_seed/1000.)
    y_rot2_nodes = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = off+rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= off+rve_seed/1000., yMax  = lgth+off-rve_seed/1000., zMax = dpth+rve_seed/1000.)
    y_rot3_nodes = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = off+rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = lgth+off-rve_seed/1000., zMax = dpth+rve_seed/1000.)
    y_rot4_nodes = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = off+rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = lgth+off-rve_seed/1000., zMax = 0.+rve_seed/1000.)
    
    RVE_ass.Set(name = 'Edge_yrot1', nodes = y_rot1_nodes)
    RVE_ass.Set(name = 'Edge_yrot2', nodes = y_rot2_nodes)
    RVE_ass.Set(name = 'Edge_yrot3', nodes = y_rot3_nodes)
    RVE_ass.Set(name = 'Edge_yrot4', nodes = y_rot4_nodes)
    
    # Nodes for z-Rotation
    n = RVE_inst.nodes
    
    z_rot1_nodes = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = off-rve_seed/1000., zMin = 0.+rve_seed/1000., xMax= off+rve_seed/1000., yMax  = off+rve_seed/1000., zMax = dpth-rve_seed/1000.)
    z_rot2_nodes = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = off-rve_seed/1000., zMin = 0.+rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = off+rve_seed/1000., zMax = dpth-rve_seed/1000.)
    z_rot3_nodes = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = 0.+rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = dpth-rve_seed/1000.)
    z_rot4_nodes = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = 0.+rve_seed/1000., xMax= off+rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = dpth-rve_seed/1000.)
    
    RVE_ass.Set(name = 'Edge_zrot1', nodes = z_rot1_nodes)
    RVE_ass.Set(name = 'Edge_zrot2', nodes = z_rot2_nodes)
    RVE_ass.Set(name = 'Edge_zrot3', nodes = z_rot3_nodes)
    RVE_ass.Set(name = 'Edge_zrot4', nodes = z_rot4_nodes)
    
    #-------------------------
    # Edge Constraints
    #-------------------------
    r = RVE_ass.referencePoints
    for i in range(len(x_rot1_nodes)):
        x = x_rot1_nodes[i].coordinates[0]
        y = x_rot1_nodes[i].coordinates[1]
        z = x_rot1_nodes[i].coordinates[2]
        node2 = n.getByBoundingBox(xMin = x-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = z-rve_seed/1000., xMax = x+rve_seed/1000., yMax = lgth+off+rve_seed/1000., zMax = z+rve_seed/1000.)
        node3 = n.getByBoundingBox(xMin = x-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax = x+rve_seed/1000., yMax = lgth+off+rve_seed/1000., zMax = dpth+rve_seed/1000.)
        node4 = n.getByBoundingBox(xMin = x-rve_seed/1000., yMin = off-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax = x+rve_seed/1000., yMax = off+rve_seed/1000., zMax = dpth+rve_seed/1000.)
        #---
        RVE_ass.Set(nodes = x_rot1_nodes[i:i+1], name = 'nset_xrot_edge_1_'+str(i) )
        RVE_ass.Set(nodes = node2, name = 'nset_xrot_edge_2_'+str(i) )
        RVE_ass.Set(nodes = node3, name = 'nset_xrot_edge_3_'+str(i) )
        RVE_ass.Set(nodes = node4, name = 'nset_xrot_edge_4_'+str(i) )
        #---
        m.Equation( name='xrot_edge_12_x_'+str(i), terms=((-1.0, 'nset_xrot_edge_1_'+str(i), 1),(1.0, 'nset_xrot_edge_2_'+str(i), 1),(-lgth, 'Rfpty', 1),)) #Rfpt y -> delta y
        m.Equation( name='xrot_edge_12_y_'+str(i), terms=((-1.0, 'nset_xrot_edge_1_'+str(i), 2),(1.0, 'nset_xrot_edge_2_'+str(i), 2),(-lgth, 'Rfpty', 2),))
        m.Equation( name='xrot_edge_12_z_'+str(i), terms=((-1.0, 'nset_xrot_edge_1_'+str(i), 3),(1.0, 'nset_xrot_edge_2_'+str(i), 3),(-lgth, 'Rfpty', 3),))
        
        m.Equation( name='xrot_edge_23_x_'+str(i), terms=((-1.0, 'nset_xrot_edge_2_'+str(i), 1),(1.0, 'nset_xrot_edge_3_'+str(i), 1),(-dpth, 'Rfptz', 1),))  #Rfpt z -> delta z
        m.Equation( name='xrot_edge_23_y_'+str(i), terms=((-1.0, 'nset_xrot_edge_2_'+str(i), 2),(1.0, 'nset_xrot_edge_3_'+str(i), 2),(-dpth, 'Rfptz', 2),))
        m.Equation( name='xrot_edge_23_z_'+str(i), terms=((-1.0, 'nset_xrot_edge_2_'+str(i), 3),(1.0, 'nset_xrot_edge_3_'+str(i), 3),(-dpth, 'Rfptz', 3),))
        
        m.Equation( name='xrot_edge_34_x_'+str(i), terms=((1.0, 'nset_xrot_edge_3_'+str(i), 1),(-1.0, 'nset_xrot_edge_4_'+str(i), 1),(-lgth, 'Rfpty', 1),))  #Rfpt y -> delta y
        m.Equation( name='xrot_edge_34_y_'+str(i), terms=((1.0, 'nset_xrot_edge_3_'+str(i), 2),(-1.0, 'nset_xrot_edge_4_'+str(i), 2),(-lgth, 'Rfpty', 2),))
        m.Equation( name='xrot_edge_34_z_'+str(i), terms=((1.0, 'nset_xrot_edge_3_'+str(i), 3),(-1.0, 'nset_xrot_edge_4_'+str(i), 3),(-lgth, 'Rfpty', 3),))
    
    for i in range(len(y_rot1_nodes)):
        x = y_rot1_nodes[i].coordinates[0]
        y = y_rot1_nodes[i].coordinates[1]
        z = y_rot1_nodes[i].coordinates[2]
        node2 = n.getByBoundingBox(xMin = x-rve_seed/1000., yMin = y-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax = x+rve_seed/1000., yMax = y+rve_seed/1000., zMax = dpth+rve_seed/1000.)
        node3 = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = y-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax = lgth+off+rve_seed/1000., yMax = y+rve_seed/1000., zMax = dpth+rve_seed/1000.)
        node4 = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = y-rve_seed/1000., zMin = 0.-rve_seed/1000., xMax = lgth+off+rve_seed/1000., yMax = y+rve_seed/1000., zMax = 0.+rve_seed/1000.)
        #---
        RVE_ass.Set(nodes = y_rot1_nodes[i:i+1], name = 'nset_yrot_edge_1_'+str(i) )
        RVE_ass.Set(nodes = node2, name = 'nset_yrot_edge_2_'+str(i) )
        RVE_ass.Set(nodes = node3, name = 'nset_yrot_edge_3_'+str(i) )
        RVE_ass.Set(nodes = node4, name = 'nset_yrot_edge_4_'+str(i) )
        #---
        m.Equation( name='yrot_edge_12_x_'+str(i), terms=((-1.0, 'nset_yrot_edge_1_'+str(i), 1),(1.0, 'nset_yrot_edge_2_'+str(i), 1),(-dpth, 'Rfptz', 1),))  #Rfpt z -> delta z
        m.Equation( name='yrot_edge_12_y_'+str(i), terms=((-1.0, 'nset_yrot_edge_1_'+str(i), 2),(1.0, 'nset_yrot_edge_2_'+str(i), 2),(-dpth, 'Rfptz', 2),))
        m.Equation( name='yrot_edge_12_z_'+str(i), terms=((-1.0, 'nset_yrot_edge_1_'+str(i), 3),(1.0, 'nset_yrot_edge_2_'+str(i), 3),(-dpth, 'Rfptz', 3),))
        
        m.Equation( name='yrot_edge_23_x_'+str(i), terms=((-1.0, 'nset_yrot_edge_2_'+str(i), 1),(1.0, 'nset_yrot_edge_3_'+str(i), 1),(-lgth, 'Rfptx', 1),))  #Rfpt x -> delta x
        m.Equation( name='yrot_edge_23_y_'+str(i), terms=((-1.0, 'nset_yrot_edge_2_'+str(i), 2),(1.0, 'nset_yrot_edge_3_'+str(i), 2),(-lgth, 'Rfptx', 2),))
        m.Equation( name='yrot_edge_23_z_'+str(i), terms=((-1.0, 'nset_yrot_edge_2_'+str(i), 3),(1.0, 'nset_yrot_edge_3_'+str(i), 3),(-lgth, 'Rfptx', 3),))
        
        m.Equation( name='yrot_edge_34_x_'+str(i), terms=((1.0, 'nset_yrot_edge_3_'+str(i), 1),(-1.0, 'nset_yrot_edge_4_'+str(i), 1),(-dpth, 'Rfptz', 1),))  #Rfpt z -> delta z
        m.Equation( name='yrot_edge_34_y_'+str(i), terms=((1.0, 'nset_yrot_edge_3_'+str(i), 2),(-1.0, 'nset_yrot_edge_4_'+str(i), 2),(-dpth, 'Rfptz', 2),))
        m.Equation( name='yrot_edge_34_z_'+str(i), terms=((1.0, 'nset_yrot_edge_3_'+str(i), 3),(-1.0, 'nset_yrot_edge_4_'+str(i), 3),(-dpth, 'Rfptz', 3),)) 
    
    for i in range(len(z_rot1_nodes)):
        x = z_rot1_nodes[i].coordinates[0]
        y = z_rot1_nodes[i].coordinates[1]
        z = z_rot1_nodes[i].coordinates[2]
        node2 = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = y-rve_seed/1000., zMin = z-rve_seed/1000., xMax = lgth+off+rve_seed/1000., yMax = y+rve_seed/1000., zMax = z+rve_seed/1000.)
        node3 = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = z-rve_seed/1000., xMax = lgth+off+rve_seed/1000., yMax = lgth+off+rve_seed/1000., zMax = z+rve_seed/1000.)
        node4 = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = z-rve_seed/1000., xMax = off+rve_seed/1000., yMax = lgth+off+rve_seed/1000., zMax = z+rve_seed/1000.)
        #---
        RVE_ass.Set(nodes = z_rot1_nodes[i:i+1], name = 'nset_zrot_edge_1_'+str(i) )
        RVE_ass.Set(nodes = node2, name = 'nset_zrot_edge_2_'+str(i) )
        RVE_ass.Set(nodes = node3, name = 'nset_zrot_edge_3_'+str(i) )
        RVE_ass.Set(nodes = node4, name = 'nset_zrot_edge_4_'+str(i) )
        #---
        m.Equation( name='zrot_edge_12_x_'+str(i), terms=((-1.0, 'nset_zrot_edge_1_'+str(i), 1),(1.0, 'nset_zrot_edge_2_'+str(i), 1),(-lgth, 'Rfptx', 1),))  #Rfpt x -> delta x
        m.Equation( name='zrot_edge_12_y_'+str(i), terms=((-1.0, 'nset_zrot_edge_1_'+str(i), 2),(1.0, 'nset_zrot_edge_2_'+str(i), 2),(-lgth, 'Rfptx', 2),))
        m.Equation( name='zrot_edge_12_z_'+str(i), terms=((-1.0, 'nset_zrot_edge_1_'+str(i), 3),(1.0, 'nset_zrot_edge_2_'+str(i), 3),(-lgth, 'Rfptx', 3),))
        
        m.Equation( name='zrot_edge_23_x_'+str(i), terms=((-1.0, 'nset_zrot_edge_2_'+str(i), 1),(1.0, 'nset_zrot_edge_3_'+str(i), 1),(-lgth, 'Rfpty', 1),))  #Rfpt y -> delta y
        m.Equation( name='zrot_edge_23_y_'+str(i), terms=((-1.0, 'nset_zrot_edge_2_'+str(i), 2),(1.0, 'nset_zrot_edge_3_'+str(i), 2),(-lgth, 'Rfpty', 2),))
        m.Equation( name='zrot_edge_23_z_'+str(i), terms=((-1.0, 'nset_zrot_edge_2_'+str(i), 3),(1.0, 'nset_zrot_edge_3_'+str(i), 3),(-lgth, 'Rfpty', 3),))
        
        m.Equation( name='zrot_edge_34_x_'+str(i), terms=((1.0, 'nset_zrot_edge_3_'+str(i), 1),(-1.0, 'nset_zrot_edge_4_'+str(i), 1),(-lgth, 'Rfptx', 1),))  #Rfpt x -> delta x
        m.Equation( name='zrot_edge_34_y_'+str(i), terms=((1.0, 'nset_zrot_edge_3_'+str(i), 2),(-1.0, 'nset_zrot_edge_4_'+str(i), 2),(-lgth, 'Rfptx', 2),))
        m.Equation( name='zrot_edge_34_z_'+str(i), terms=((1.0, 'nset_zrot_edge_3_'+str(i), 3),(-1.0, 'nset_zrot_edge_4_'+str(i), 3),(-lgth, 'Rfptx', 3),))     
        
    # Corner Vertices
    n = RVE_inst.nodes
    r = RVE_ass.referencePoints
    corner_node1  = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = off-rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= off+rve_seed/1000., yMax  = off+rve_seed/1000., zMax = 0.+rve_seed/1000.)
    corner_node2  = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= off+rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = 0.+rve_seed/1000.)
    corner_node3  = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = 0.+rve_seed/1000.)
    corner_node4  = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = off-rve_seed/1000., zMin = 0.-rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = off+rve_seed/1000., zMax = 0.+rve_seed/1000.)
    corner_node5  = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = off-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= off+rve_seed/1000., yMax  = off+rve_seed/1000., zMax = dpth+rve_seed/1000.) 
    corner_node6  = n.getByBoundingBox(xMin = off-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= off+rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = dpth+rve_seed/1000.)
    corner_node7  = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = lgth+off-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = lgth+off+rve_seed/1000., zMax = dpth+rve_seed/1000.)
    corner_node8  = n.getByBoundingBox(xMin = lgth+off-rve_seed/1000., yMin = off-rve_seed/1000., zMin = dpth-rve_seed/1000., xMax= lgth+off+rve_seed/1000., yMax  = off+rve_seed/1000., zMax = dpth+rve_seed/1000.)
    
    RVE_ass.Set(name = 'corner_node_1', nodes = corner_node1)
    RVE_ass.Set(name = 'corner_node_2', nodes = corner_node2)
    RVE_ass.Set(name = 'corner_node_3', nodes = corner_node3)
    RVE_ass.Set(name = 'corner_node_4', nodes = corner_node4)
    RVE_ass.Set(name = 'corner_node_5', nodes = corner_node5)
    RVE_ass.Set(name = 'corner_node_6', nodes = corner_node6)
    RVE_ass.Set(name = 'corner_node_7', nodes = corner_node7)
    RVE_ass.Set(name = 'corner_node_8', nodes = corner_node8)
    node = []
    node.append(corner_node1)
    node.append(corner_node2)
    node.append(corner_node3)
    node.append(corner_node4)
    node.append(corner_node5)
    node.append(corner_node6)
    node.append(corner_node7)
    node.append(corner_node8)
    
    #-------------------------
    # Vertex Constraints
    #-------------------------
    
    for ieq in range(1,4):
            if ieq==1:
                vdir='x' #@UnusedVariable
            elif ieq==2:
                vdir='y' #@UnusedVariable
            elif ieq==3:
                vdir='z' #@UnusedVariable
            m.Equation(name = 'vertex_1_'+vdir, terms =((-1.0, 'corner_node_1', ieq),(node[0][0].coordinates[0], 'Rfptx', ieq),(node[0][0].coordinates[1], 'Rfpty', ieq),)) ###(node[0][0].coordinates[2], 'Rfptz', ieq),)) ###
            #if ieq==2 :
            m.Equation(name = 'vertex_2_'+vdir, terms =((-1.0, 'corner_node_2', ieq),(node[1][0].coordinates[0], 'Rfptx', ieq),(node[1][0].coordinates[1], 'Rfpty', ieq),)) ###(node[1][0].coordinates[2], 'Rfptz', ieq),)) ###
            #if ieq==1 or ieq==2:
            m.Equation(name = 'vertex_3_'+vdir, terms =((-1.0, 'corner_node_3', ieq),(node[2][0].coordinates[0], 'Rfptx', ieq),(node[2][0].coordinates[1], 'Rfpty', ieq),)) ###(node[2][0].coordinates[2], 'Rfptz', ieq),)) ###
            m.Equation(name = 'vertex_4_'+vdir, terms =((-1.0, 'corner_node_4', ieq),(node[3][0].coordinates[0], 'Rfptx', ieq),(node[3][0].coordinates[1], 'Rfpty', ieq),)) ###(node[3][0].coordinates[2], 'Rfptz', ieq),)) ###
            m.Equation(name = 'vertex_5_'+vdir, terms =((-1.0, 'corner_node_5', ieq),(node[4][0].coordinates[0], 'Rfptx', ieq),(node[4][0].coordinates[1], 'Rfpty', ieq),(node[4][0].coordinates[2], 'Rfptz', ieq),)) 
            m.Equation(name = 'vertex_6_'+vdir, terms =((-1.0, 'corner_node_6', ieq),(node[5][0].coordinates[0], 'Rfptx', ieq),(node[5][0].coordinates[1], 'Rfpty', ieq),(node[5][0].coordinates[2], 'Rfptz', ieq),)) 
            m.Equation(name = 'vertex_7_'+vdir, terms =((-1.0, 'corner_node_7', ieq),(node[6][0].coordinates[0], 'Rfptx', ieq),(node[6][0].coordinates[1], 'Rfpty', ieq),(node[6][0].coordinates[2], 'Rfptz', ieq),))
            m.Equation(name = 'vertex_8_'+vdir, terms =((-1.0, 'corner_node_8', ieq),(node[7][0].coordinates[0], 'Rfptx', ieq),(node[7][0].coordinates[1], 'Rfpty', ieq),(node[7][0].coordinates[2], 'Rfptz', ieq),))
            
    print('*** EQUATION CONSTRAINTS APPLIED! ***')
        
    #========================================
    # Step- and Outputdefinition / Boundary Conditions
    #========================================
    
    try:
        h11 = float(bc_h11)
    except ValueError:
        h11 = UNSET #@UndefinedVariable
            
    try:
        h22 = float(bc_h22)
    except ValueError:
        h22 = UNSET #@UndefinedVariable
        
    try:
        h33 = float(bc_h33)     
    except ValueError:
        h33 = UNSET #@UndefinedVariable
        
    try:    
        h12 = float(bc_h12) 
    except ValueError:
        h12 = UNSET #@UndefinedVariable
        
    try:
        h13 = float(bc_h13)
    except ValueError:
        h13 = UNSET #@UndefinedVariable
        
    try:
        h21 = float(bc_h21) 
    except ValueError:
        h21 = UNSET #@UndefinedVariable
        
    try:
        h23 = float(bc_h23)
    except ValueError: 
        h23 = UNSET #@UndefinedVariable
        
    try:
        h31 = float(bc_h31)
    except ValueError:
        h31 = UNSET #@UndefinedVariable
        
    try:
        h32 = float(bc_h32)
    except ValueError:
        h32 = UNSET #@UndefinedVariable
        
        
    bc_rfptx = RVE_ass.sets['Rfptx']
    bc_rfpty = RVE_ass.sets['Rfpty']
    bc_rfptz = RVE_ass.sets['Rfptz']
    corner_1 = RVE_ass.sets['corner_node_1'] #@UnusedVariable
    corner_2 = RVE_ass.sets['corner_node_2'] #@UnusedVariable
    corner_3 = RVE_ass.sets['corner_node_3'] #@UnusedVariable
    corner_4 = RVE_ass.sets['corner_node_4'] #@UnusedVariable
    corner_5 = RVE_ass.sets['corner_node_5'] #@UnusedVariable
    corner_6 = RVE_ass.sets['corner_node_6'] #@UnusedVariable
    corner_7 = RVE_ass.sets['corner_node_7'] #@UnusedVariable
    corner_8 = RVE_ass.sets['corner_node_8'] #@UnusedVariable
    
    if lc == 'static':
        if job_stab == 'off':
            m.StaticStep(name='RVE_DAMAGE_static', previous='Initial', timePeriod = 1.0, nlgeom = ON, initialInc = inc_init, minInc = inc_min, maxInc = inc_max, maxNumInc = inc_maxnum, stabilizationMethod = NONE) #@UndefinedVariable
            m.steps['RVE_DAMAGE_static'].control.setValues(allowPropagation = OFF, resetDefaultValues = OFF, timeIncrementation = (8.0, 10.0, 9.0, 16.0, 10.0, 4.0, 12.0, 15.0, 6.0, 3.0, 50.0), lineSearch = (5., 1., 0.0001, 0.25, 0.1)) #@UndefinedVariable
            m.FieldOutputRequest(name = 'F-Output-RVE', createStepName = 'RVE_DAMAGE_static', variables = ('S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'SDEG', 'STATUS', 'MAXSCRT'), timeMarks = OFF, timeInterval = job_fout, region = MODEL) #@UndefinedVariable
            m.HistoryOutputRequest(name = 'H-Output-RVE', createStepName = 'RVE_DAMAGE_static', variables = ('ALLIE', 'ALLSE', 'ALLSD'), timeMarks = OFF, timeInterval = job_hout, region = MODEL) #@UndefinedVariable
            m.fieldOutputRequests['F-Output-1'].suppress()
            m.historyOutputRequests['H-Output-1'].suppress()
                
        else:
            m.StaticStep(name='RVE_DAMAGE_static', previous='Initial', timePeriod = 1.0, nlgeom = ON, initialInc = inc_init, minInc = inc_min, maxInc = inc_max, maxNumInc = inc_maxnum, stabilizationMethod = DISSIPATED_ENERGY_FRACTION,  stabilizationMagnitude = float(job_stab)) #@UndefinedVariable
            m.steps['RVE_DAMAGE_static'].control.setValues(allowPropagation = OFF, resetDefaultValues = OFF, timeIncrementation = (8.0, 10.0, 9.0, 16.0, 10.0, 4.0, 12.0, 15.0, 6.0, 3.0, 50.0), lineSearch = (5., 1., 0.0001, 0.25, 0.1)) #@UndefinedVariable
            m.FieldOutputRequest(name = 'F-Output-RVE', createStepName = 'RVE_DAMAGE_static', variables = ('S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'SDEG', 'STATUS', 'MAXSCRT'), timeMarks = OFF, timeInterval = job_fout, region = MODEL) #@UndefinedVariable
            m.HistoryOutputRequest(name = 'H-Output-RVE', createStepName = 'RVE_DAMAGE_static', variables = ('ALLIE', 'ALLSE', 'ALLSD'), timeMarks = OFF, timeInterval = job_hout, region = MODEL) #@UndefinedVariable
            m.fieldOutputRequests['F-Output-1'].suppress()
            m.historyOutputRequests['H-Output-1'].suppress()
            
        # Displacement BCs
        if lt == 'strain':
            m.DisplacementBC(name = 'Rfptx', createStepName = 'RVE_DAMAGE_static', region = bc_rfptx, u1 = h11, u2 = h21, u3 = h31, ur1 = UNSET, ur2 = UNSET, ur3 = UNSET, fieldName = '', localCsys = None, distributionType = UNIFORM, amplitude = UNSET, fixed = OFF) #@UndefinedVariable
            m.DisplacementBC(name = 'Rfpty', createStepName = 'RVE_DAMAGE_static', region = bc_rfpty, u1 = h12, u2 = h22, u3 = h32, ur1 = UNSET, ur2 = UNSET, ur3 = UNSET, fieldName = '', localCsys = None, distributionType = UNIFORM, amplitude = UNSET, fixed = OFF) #@UndefinedVariable
            m.DisplacementBC(name = 'Rfptz', createStepName = 'RVE_DAMAGE_static', region = bc_rfptz, u1 = h13, u2 = h23, u3 = h33, ur1 = UNSET, ur2 = UNSET, ur3 = UNSET, fieldName = '', localCsys = None, distributionType = UNIFORM, amplitude = UNSET, fixed = OFF) #@UndefinedVariable
        elif lt == 'stress':
            if s11 !=0. or s21 !=0. or s31 != 0.:
                m.ConcentratedForce(name = 'Rfptx', createStepName = 'RVE_DAMAGE_static', region = bc_rfptx, cf1 = s11, cf2 = s21, cf3 = s31, field = '', localCsys = None, distributionType = UNIFORM, amplitude = UNSET) #@UndefinedVariable
            if s12 !=0. or s22 !=0. or s32 != 0.:
                m.ConcentratedForce(name = 'Rfpty', createStepName = 'RVE_DAMAGE_static', region = bc_rfpty, cf1 = s12, cf2 = s22, cf3 = s32, field = '', localCsys = None, distributionType = UNIFORM, amplitude = UNSET) #@UndefinedVariable
            if s13 !=0. or s23 !=0. or s33 != 0.:
                m.ConcentratedForce(name = 'Rfptz', createStepName = 'RVE_DAMAGE_static', region = bc_rfptz, cf1 = s13, cf2 = s23, cf3 = s33, field = '', localCsys = None, distributionType = UNIFORM, amplitude = UNSET) #@UndefinedVariable
        
    elif lc == 'cyclic':
        ampl_str = "(0., 0.),"
        if lc == 'cyclic':
            for iampl in range(int(cycles )):
                if float(R) < 0.0:
                    ampl_str = ampl_str + "(" + str((4 * iampl + 1) * step) + ", 1.),(" + str((4 * iampl + 2)* step) + "," + str((1.+float(R))/2.) + "),(" + str((4 * iampl + 3)* step) + ","+ str(float(R)) + "),(" + str((4 * iampl + 4)* step) + "," + str((1.+float(R))/2.) + "),"
                elif R != 'inf':
                    ampl_str = ampl_str + "(" + str((2 * iampl + 1) * step) + ", 1.),(" + str((2 * iampl + 2)* step) + "," + str(float(R)) + ")," ####(" + str((4 * iampl + 3)* step) + ",1.),(" + str((4 * iampl + 4)* step) + "," + str(float(R)) + "),"
                elif R == 'inf':
                    ampl_str = ampl_str + "(" + str((4 * iampl + 1) * step) + ", -1.),(" + str((4 * iampl + 2)* step) + "," + str(float(0.)) + "),(" + str((4 * iampl + 3)* step) + ",-1.),(" + str((4 * iampl + 4)* step) + "," + str(float(0.)) + "),"
        if R == 'inf' or R == '0':
            time = cycles * freq
        else:
            ampl_str = ampl_str + "(" + str((cycles * freq) + step) + ",0.),"
            time = cycles * freq + step
        ampl = eval(ampl_str)
        m.TabularAmplitude(name = 'ampl' , data = (ampl), timeSpan = STEP, smooth = SOLVER_DEFAULT) #@UndefinedVariable
        if job_stab == 'off':
            m.StaticStep(name='RVE_DAMAGE_cyclic', previous='Initial', timePeriod = time, nlgeom = OFF, initialInc = step / 10., minInc = inc_min, maxInc = step / 10., maxNumInc = inc_maxnum, stabilizationMethod = NONE) #@UndefinedVariable
            m.steps['RVE_DAMAGE_cyclic'].control.setValues(allowPropagation = OFF, resetDefaultValues = OFF, timeIncrementation = (8.0, 10.0, 9.0, 16.0, 10.0, 4.0, 12.0, 15.0, 6.0, 3.0, 50.0), lineSearch = (5., 1., 0.0001, 0.25, 0.1)) #@UndefinedVariable
            m.FieldOutputRequest(name = 'F-Output-RVE', createStepName = 'RVE_DAMAGE_cyclic', variables = ('S', 'PE', 'PEEQ', 'PEMAG', 'E', 'U', 'RF', 'SDV'), timeMarks = ON, timeInterval = step, region = MODEL) #@UndefinedVariable
            m.HistoryOutputRequest(name = 'H-Output-RVE', createStepName = 'RVE_DAMAGE_cyclic', variables = ('ALLIE', 'ALLSE', 'ALLSD'), timeMarks = ON, timeInterval = step, region = MODEL) #@UndefinedVariable
            m.fieldOutputRequests['F-Output-1'].suppress()
            m.historyOutputRequests['H-Output-1'].suppress()
            m.historyOutputRequests['H-Output-RVE'].suppress()
        else:
            m.StaticStep(name='RVE_DAMAGE_cyclic', previous='Initial', timePeriod = time, nlgeom = OFF, initialInc = step / 10., minInc = inc_min, maxInc = step / 10., maxNumInc = inc_maxnum, stabilizationMethod = DISSIPATED_ENERGY_FRACTION,  stabilizationMagnitude = float(job_stab)) #@UndefinedVariable
            m.steps['RVE_DAMAGE_cyclic'].control.setValues(allowPropagation = OFF, resetDefaultValues = OFF, timeIncrementation = (8.0, 10.0, 9.0, 16.0, 10.0, 4.0, 12.0, 15.0, 6.0, 3.0, 50.0), lineSearch = (5., 1., 0.0001, 0.25, 0.1)) #@UndefinedVariable
            m.FieldOutputRequest(name = 'F-Output-RVE', createStepName = 'RVE_DAMAGE_cyclic', variables = ('S', 'PE', 'PEEQ', 'PEMAG', 'E', 'U', 'RF', 'SDV'), timeMarks = ON, timeInterval = step, region = MODEL) #@UndefinedVariable
            m.HistoryOutputRequest(name = 'H-Output-RVE', createStepName = 'RVE_DAMAGE_cyclic', variables = ('ALLIE', 'ALLSE', 'ALLSD'), timeMarks = ON, timeInterval = step, region = MODEL) #@UndefinedVariable
            m.fieldOutputRequests['F-Output-1'].suppress()
            m.historyOutputRequests['H-Output-1'].suppress()
            m.historyOutputRequests['H-Output-RVE'].suppress()
        if lt == 'strain':
            m.DisplacementBC(name = 'Rfptx', createStepName = 'RVE_DAMAGE_cyclic', region = bc_rfptx, u1 = h11, u2 = h21, u3 = h31, ur1 = UNSET, ur2 = UNSET, ur3 = UNSET, fieldName = '', localCsys = None, distributionType = UNIFORM, amplitude = 'ampl', fixed = OFF) #@UndefinedVariable
            m.DisplacementBC(name = 'Rfpty', createStepName = 'RVE_DAMAGE_cyclic', region = bc_rfpty, u1 = h12, u2 = h22, u3 = h32, ur1 = UNSET, ur2 = UNSET, ur3 = UNSET, fieldName = '', localCsys = None, distributionType = UNIFORM, amplitude = 'ampl', fixed = OFF) #@UndefinedVariable
            m.DisplacementBC(name = 'Rfptz', createStepName = 'RVE_DAMAGE_cyclic', region = bc_rfptz, u1 = h13, u2 = h23, u3 = h33, ur1 = UNSET, ur2 = UNSET, ur3 = UNSET, fieldName = '', localCsys = None, distributionType = UNIFORM, amplitude = 'ampl', fixed = OFF) #@UndefinedVariable    
        elif lt == 'stress':
            if s11 !=0. or s21 !=0. or s31 != 0.:
                m.ConcentratedForce(name = 'Rfptx', createStepName = 'RVE_DAMAGE_cyclic', region = bc_rfptx, cf1 = s11, cf2 = s21, cf3 = s31, field = '', localCsys = None, distributionType = UNIFORM, amplitude = 'ampl') #@UndefinedVariable
            if s12 !=0. or s22 !=0. or s32 != 0.:
                m.ConcentratedForce(name = 'Rfpty', createStepName = 'RVE_DAMAGE_cyclic', region = bc_rfpty, cf1 = s12, cf2 = s22, cf3 = s32, field = '', localCsys = None, distributionType = UNIFORM, amplitude = 'ampl') #@UndefinedVariable
            if s13 !=0. or s23 !=0. or s33 != 0.:
                m.ConcentratedForce(name = 'Rfptz', createStepName = 'RVE_DAMAGE_cyclic', region = bc_rfptz, cf1 = s13, cf2 = s23, cf3 = s33, field = '', localCsys = None, distributionType = UNIFORM, amplitude = 'ampl') #@UndefinedVariable
    print('*** STEP- AND OUTPUTARGUMENTS SET! ***') 
    print('*** LOADS / BOUNDARY CONDITIONS CREATED! ***')
    
    #========================================
    # Job Definition
    #========================================
    # Display Part
    session.viewports['Viewport: 1'].setValues(displayedObject = prve) #@UndefinedVariable
    try:
        jobname = getInputs((('Jobname:',m.name),),label = 'Enter Jobname', dialogTitle = 'Jobname') #@UndefinedVariable
        jobname = jobname[0]
    except:
        jobname = m.name
    RVE_job = mdb.Job(name = os.path.splitext(InputFile)[0], model = m, type = ANALYSIS, numCpus = 1, memory = 90, memoryUnits = PERCENTAGE, getMemoryFromAnalysis = ON, numDomains = 1, multiprocessingMode = DEFAULT) #@UndefinedVariable @UnusedVariable
    mdb.jobs[os.path.splitext(InputFile)[0]].writeInput() #@UndefinedVariable
    print('*** JOB DEFINITION FINISHED! ***')
    
    #-------------------------
    # Edit Inputfile
    #-------------------------
    if lc == 'static':
        print('*** WRITING INPUTFILE! ***')
        mdb.jobs[os.path.splitext(InputFile)[0]].waitForCompletion() #@UndefinedVariable
        inp_data = open(InputFile, "r") 
        data = inp_data.read()
        inp_data.close()
        for irep in range(len(xcor)):
            data = data.replace("** Section: Interface_Section\n*Cohesive Section, elset=int_"+str(irep+1)+", material=Interface, response=TRACTION SEPARATION, thickness=SPECIFIED\n"+str(dr)+", "+str(dr),"*Orientation, name=int_sys_"+str(irep+1)+", DEFINITION=COORDINATES, SYSTEM=CYLINDRICAL\n          "+str(xcor[irep])+",           "+str(ycor[irep])+",           0.,           "+str(xcor[irep])+",           "+str(ycor[irep])+",           "+str(dpth)+"\n1, 90.\n** Section: Interface_Section\n*Cohesive Section, elset=int_"+str(irep+1)+", material=Interface, response=TRACTION SEPARATION, STACK DIRECTION=ORIENTATION, ORIENTATION=int_sys_"+str(irep+1)+", thickness=SPECIFIED\n"+str(dr)+", "+str(dr)) 
        inp_data = open(InputFile, "w") 
        inp_data.write(data)
        inp_data.close()
        print('*** INPUTFILE WRITTEN! ***')
    
    if not isPlugin:
        with open(InputFile, 'r') as content_file:
            content = content_file.read()
        os.remove(InputFile)
        # Terminate without creating temporary CAE file.      
        return content
    
    #-------------------------
    # Check for old Jobfiles
    #-------------------------
    ret_path = os.getcwd()
    try:
        os.chdir(jobname)
        openodb = os.path.abspath(jobname+'.odb')
        session.odbs[openodb].close() #@UndefinedVariable
        os.chdir(ret_path)
    except:
        os.chdir(ret_path)
    exists = 1
    w_del=[] #@UnusedVariable
    while exists==1:
        if not os.path.exists(jobname):
            os.makedirs(jobname)
            shutil.copyfile(InputFile, os.path.join(jobname,InputFile))  
            os.chdir(jobname)
            exists=0
        else:
            exists=1
        if exists==1:
            print('*** OLD JOBFILES EXIST! ***')
            try:
                delete = getWarningReply('Delete old Jobfiles?',(YES,NO)) #@UndefinedVariable
            except:
                delete = YES #@UndefinedVariable
            if delete == YES: #@UndefinedVariable
                os.chdir(jobname)
                try:
                    os.remove(jobname+'.dat')
                except:
                    pass
                try:    
                    os.remove(jobname+'.odb')
                except:
                    pass
                try:
                    os.remove(jobname+'.msg')
                except:
                    pass
                try:
                    os.remove(jobname+'.log')
                except:
                    pass
                try:
                    os.remove(jobname+'.prt')
                except:
                    pass
                try:
                    os.remove(jobname+'.sim')
                except:
                    pass
                try:
                    os.remove(jobname+'.sta')
                except:
                    pass
                try:
                    os.remove(jobname+'.com')
                except:
                    pass
                try:
                    os.remove(jobname+'.cae')
                except:
                    pass
                try:
                    os.remove(jobname+'.jnl')
                except:
                    pass
                try:
                    os.remove(InputFile)
                except:
                    pass
                try:
                    os.remove('lin_elastic.for')
                except:
                    pass
                os.chdir(ret_path)
                shutil.copyfile(InputFile, os.path.join(jobname,InputFile))  
                os.chdir(jobname)
                exists=0
                print('*** OLD JOBFILES DELETED! ***')
            elif delete == NO: #@UndefinedVariable
                try:
                    jobname = getInputs((('New Jobname:',jobname+'_COPY'),),label='Enter New Jobname', dialogTitle = 'New Jobname') #@UndefinedVariable
                    jobname = jobname[0]
                except:
                    jobname += "_COPY"
    
    if lc == 'cyclic':
        user_sub = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"user","visco_poynting_eulerfwd.for" )
        RVE_job = mdb.Job(name = jobname, model = m.name, userSubroutine = user_sub, type = ANALYSIS, nodalOutputPrecision = SINGLE, numCpus = 1, memory = 90, memoryUnits = PERCENTAGE, getMemoryFromAnalysis = ON, numDomains = 1, multiprocessingMode = DEFAULT) #@UndefinedVariable @UnusedVariable
    elif lc == 'static':
        RVE_job = mdb.JobFromInputFile(name = jobname, inputFileName = InputFile, type = ANALYSIS, nodalOutputPrecision = SINGLE, numCpus = 1, memory = 90, memoryUnits = PERCENTAGE, getMemoryFromAnalysis = ON, numDomains = 1, multiprocessingMode = DEFAULT) #@UndefinedVariable @UnusedVariable
    print('*** REACHED FIBRE VOLUME FRACTION: '+str(afvc_best)+'% OF '+str(100.*fvc)+'% !***')
    print('*** MODEL CREATION COMPLETED! ***')
    mdb.saveAs(pathName = jobname) #@UndefinedVariable
    try:
        submit = getWarningReply('Submit Job now?',(YES,NO)) #@UndefinedVariable
    except:
        submit = NO #@UndefinedVariable
    if submit == YES: #@UndefinedVariable
        mdb.jobs[jobname].submit(consistencyChecking = False, datacheckJob = False) #@UndefinedVariable
        print('*** JOB SUBMITTED! ***')
    elif submit == NO: #@UndefinedVariable
        print('*** JOB NOT SUBMITTED! ***\n*** YOU CAN SUBMIT THE JOB FROM THE MODEL TREE LATER! ***')
        
    # End of function
    return
        
if __name__ == '__main__':
    pass