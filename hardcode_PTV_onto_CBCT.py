# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 18:50:57 2022

@author: Lovro
version 0.0.1
"""
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("plugin2DView", r"E:\progs3\Anaconda3\Lib\site-packages\dicompyler\baseplugins\2dview.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)       
from dicompylercore import dicomparser as dd
import pydicom as dd2
klasa1=foo.plugin2DView     #from 2dview import plugin2dview as plugin
import glob
import os

def REFIZO(corrC):
    #this function makes setup correction in real_space coordinates
    #corrC is array of x,y,z cooridnates of a structure (of each of its points)
    gama2=[]
    for ii in corrC:
        c0=ii[0]-Jizo[0]-shift6apr[0] #I guess (-) sign shoud be her :-)
        c1=ii[1]-Jizo[1]-shift6apr[1]
        c2=ii[2]
        gama2.append([type_org(c0),type_org(c1),type_org(c2)])
        #return shifted array (& preserve object-type)
    return gama2
    
    
#works only for Head-First Supine!!!!!
#works only for Head-First Supine!!!!!
#works only for Head-First Supine!!!!!
filename2=r'E:\ftp2\XiO\CT.rtp1.0.J220156.25mar2022.T.-1326.CT.dcm'
#any slice from planning CT is requiered to take Z-position (lognitude)
filePlan=r'E:\ftp2\XiO\RTXPLAN.J220156.198_J220156.dcm'
#necessary for ISO coord. (just that)
fileS=r'E:\ftp2\XiO\SS.rtp1.0.J220156.198.dcm'
#file that contains structures

dS=dd.DicomParser(fileS)
dp02=dd2.dcmread(filename2,force=True)
beta=dS.GetStructures()
structure=beta #each structure has its number *1, and a name
ctv=dS.GetStructureCoordinates(5) #that number us usedd here *1
ptv=dS.GetStructureCoordinates(8) #and here
mandibula=dS.GetStructureCoordinates(6) #and here

strukture3=[ctv,ptv,mandibula]
#PTV & CTV are mandatory, while it can be usfull to put some other anatom.struc.
#mandibula-10
#12-ptv1
#8 -ctv1
#lat,vert,long: mm
#Kizo=[-8.9,22.7,-889]
#Jizo=[0.1, 18.7, -889.0]
Jizo=[9.4, 12.7, -1215.0]
#isocenter manualy entered in mm, (it can be read from RTplan.dcm)
shift6apr=[1.3,-1.6,0.5]
mm=4000 #CT-number white color in grayscele CT image
type_org=dd2.valuerep.DSfloat



#load CBCT-slice
in_folder=r'E:\ftp2\CBCTfolder\Export0000\SR0000\\'
#glob needs trailing slash e.g. c:\path\
#out_folder must be created before running: E:\ftp2\CBCTfolder\Export0000\SR0000Out\\'
for filename in glob.iglob(in_folder+'**/*.dcm',recursive=True):
    head, tail = os.path.split(filename)
    dp1=dd.DicomParser(filename)
    dp1b=dp1
    print(filename)
    structurepixlut=dp1.GetPatientToPixelLUT()   
    #find postition
    #position='-1216.50'
    izoCBCT=dp1.ds['0x00200032'] #CBCT
    izoXiO=dp02['0x00200032'] #CT
    #some arithmetics is needet to calculate according slice Z-position
    pomakREFIZO=Jizo[2]-izoXiO[2]
    p_float=float(izoCBCT[2])+pomakREFIZO+izoXiO[2]
    position=str(p_float )
    print(position) #now we have it
    #position='-1216.50'
    
    count=0#count of curves in a slice
    pixArr=[]
    for odabrana in strukture3:
        structure['planes']=odabrana#PTV,ctv,...
        if 1==1 or not "zarray" in structure:
            structure['zarray'] = np.array(
                    list(structure['planes'].keys()), dtype=np.float32)
            structure['zkeys'] = structure['planes'].keys()
        zmin = np.amin(np.abs(structure['zarray'] - float(position)))
        index = np.argmin(np.abs(structure['zarray'] - float(position)))
        if abs(zmin)>3: #3 milimeters
            #if a contour coordinates ar further away from according CBCT slice
            #==>skip that
            #print('skip.zmin:',zmin)
            continue #skip drawning, continue with next one
        else:
            for contour in structure['planes'][list(structure['zkeys'])[index]]:
                if (contour['type'] == u"CLOSED_PLANAR"):
                    # Convert the structure data to pixel data
                    corrC=contour['data']
                    #contour curve pre-correction(shift) at XVI
                    corrC2=REFIZO(corrC)
                    #contour curve post-correction
                    pixeldata = klasa1.GetContourPixelData(klasa1,
                        structurepixlut, corrC2)
                    #pixelLUT is a transformation from real space (x,y,z)
                    #to pixel coordinates (ix, iy)                                       
                    count+=1
                    pixArr.append(pixeldata)
        #print(pixeldata)    #plt.plot(pixeldata) #matplotlib or seaborn modules
    picture2=dp1.get_pixel_array
    for pixII in pixArr:
        #hardcode in slice-pixel-array
        for jj,ii in pixII:
            picture2[ii,jj]=mm
            #note thet x & y are inverted, that's how pixData is represented in picture

    #picture2[10,240]=mm
    #    picture2[ii-1,jj-1]=mm
    #    picture2[ii+1,jj+1]=mm
    #thick lines
    #plt.imshow(picture2, cmap='gray')
    dp1b.ds.PixelData=picture2
    dp1b.ds.save_as(head+'Out'+'\\'+tail)
    #write to out-folder
print('Finished')

