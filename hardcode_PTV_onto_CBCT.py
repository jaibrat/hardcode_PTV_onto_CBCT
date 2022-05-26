# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 18:50:57 2022

@author: Lovro
version 0.0.3
"""
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("plugin2DView", r"/home/ubuntu2/Downloads/dicompyler/dicompyler/baseplugins/2dview.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)       
#from dicompylercore import dicomparser as dd
from dicompylercore import dicomparser056 as dd
import pydicom as dd2
klasa1=foo.plugin2DView     #from 2dview import plugin2dview as plugin
import glob
import os

def REFIZO(corrC):
    #this function makes setup correction in real_space coordinates
    #corrC is array of x,y,z cooridnates of a structure (of each of its points)
    gama2=[]
    for ii in corrC:
        c0=ii[0]-Jizo[0]-shift6apr[0] #see "Some explanation"
        c1=ii[1]-Jizo[1]+shift6apr[1] #(+,-) convention is used for script that takes couch coord. from Mosaiq
        c2=ii[2] #Z-direction (longitudinal) is transformed in "find postition" part
        gama2.append([type_org(c0),type_org(c1),type_org(c2)])
        #return shifted array (& preserve object-type)
    return gama2
    
#works only for Head-First Supine!!!!!
print("works only for Head-First Supine!!!!!")
#works only for Head-First Supine!!!!!
#also:
#(0020, 0037) Image Orientation (Patient) must be:        DS: [1.00, 0.00, 0.00, 0.00, 1.00, 0.00]
filename2='/home/ubuntu2/ftp2/J672/CT.rtp1.0.J210672.08Dec2021.T.-1159.CT.dcm'
#any slice from planning CT is requiered to take Z-position (lognitude)
filePlan='/home/ubuntu2/ftp2/J672/RTXPLAN.J210672.199_J210672b.dcm'
#necessary for ISO coord. (just that)
fileS='/home/ubuntu2/ftp2/J672/SS.rtp1.0.J210672.199.dcm'
#file that contains structures

dS=dd.DicomParser(fileS)
#dp02=dd2.dcmread(filename2,force=True) #this is redundant
beta=dS.GetStructures()
structure=beta #each structure has its number *1, and a name
ctv=dS.GetStructureCoordinates(8) #that number us usedd here *1
ptv=dS.GetStructureCoordinates(9) #and here
mandibula=dS.GetStructureCoordinates(1) #and here

#print(ctv) #dS.GetStructures() #(IZO dicom-tag 300a, 012c)
strukture3=[ctv,ptv,mandibula]
#PTV & CTV are mandatory, while it can be usfull to put some other anatom.struc.
#mandibula-10
#12-ptv1
#8 -ctv1
#lat,vert,long: mm
#Kizo=[-8.9,22.7,-889]
#Jizo=[0.1, 18.7, -889.0]
Jizo=[85.1, -65.2, -1321.0]#[9.4, 12.7, -1215.0]
#isocenter manualy entered in mm, (it can be read from RTplan.dcm)
# shift6apr=[1.3,-1.6,0.5]
shift6apr=[-10.5,1,-3.8]
mm=4000 #CT-number white color in grayscele CT image
type_org=dd2.valuerep.DSfloat
#this data type behaves like as both str and float, I want to keep it that way


#load CBCT-slice
in_folder=r'/home/ubuntu2/ftp2/inCBCT'
#glob needs trailing slash e.g. c:\path\
#out_folder must be created before running: E:\ftp2\CBCTfolder\Export0000\SR0000Out\\'
for filename in glob.iglob(in_folder+'**/*.dcm',recursive=True):
    head, tail = os.path.split(filename)
    dp1=dd.DicomParser(filename) #load in-file
    dp1b=dp1 #prepare for out-file
    print(filename)
    structurepixlut=dp1.GetPatientToPixelLUT()   
    #find postition
    #position='-1216.50'
    izoCBCT=dp1.ds['0x00200032'] #CBCT
    # izoXiO=dp02['0x00200032'] #CT #this is redundant
    #some arithmetics is needet to calculate according slice Z-position
    # pomakREFIZO=Jizo[2]  #redundant
    p_float=float(izoCBCT[2])+Jizo[2]+shift6apr[2]
    #applied couch shift has opposite direct. of IZO-movement (see "Some explanation")
    position=str(p_float )
    print("slice_position mm: ", position) #now we have it
    #position='-1216.50' mm
    # Some explanation (on coordinate transformations):
    # couch_shift=def= Couch_coord_new - Couch_coord_old
    # couch_coord system: e.g.: (+)-direction means couch is going up
    #    notice: that is opposite of (Head_First_Supine) DICOM coord sys
    #DICOM coord systemm (axes, and direction) can be seen: google: "DICOM coord."
    # the function "REFIZO" that converts coordinate of StructureSet
    #     takes Coordinates, and subtracts IZO-coord from them
    #     because in CBCT slices, coord (0,0,0) is the (ISO)centar of LINAC
    #
    # Some explanation (#2):
    # try and see (on yourself)
    count=0 #count of curves in a slice
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
            #if a contour coordinates are further away from according CBCT slice
            #==>skip that
            #print('skip.zmin:',zmin)
            continue #skip drawning, continue with next one
        else:
            for contour in structure['planes'][list(structure['zkeys'])[index]]:
                if (contour['type'] == u"CLOSED_PLANAR"):
                    # Convert the structure data to pixel data
                    corrC=contour['data']   
                    #contour['data'] is in dimensions (x,y,z)
                    #contour curve pre-correction(shift) at XVI
                    corrC2=REFIZO(corrC)
                    #contour curve post-correction
                    pixeldata = klasa1.GetContourPixelData(klasa1,
                        structurepixlut, corrC2)
                    #pixelLUT is a transformation from real space (x,y,z)
                    #to pixel coordinates (ix, iy)                                       
                    #pixeldata is in dimensions PixelX, PixelY
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
    dp1b.ds.save_as(head+'Out2'+'/'+tail)
    #write to out-folder, you create before running the script
print('Finished')
