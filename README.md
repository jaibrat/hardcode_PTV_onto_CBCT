hardcode_PTV_onto_CBCT
============
This python script is used to hardcode contour data onto CBCT_Pixel_data_image (img)
Quick-Start Use:
============
1. prepare CBCT.dcm in an "in-folder" (DICOM)
2. set all parameter values in a script (ISO-coordinates, setup-shift, filenames, and desired contour nubers)
3. run the script and as a result you have your "out-folder" filled 

<img src='https://raw.githubusercontent.com/jaibrat/hardcode_PTV_onto_CBCT/main/demo-imge.PNG' align='right' height='440' width='287' alt="idea in short">

Installing
==========
1. Install Anaconda (recommended, not necessary)
2. Create environment  ```conda create --name myenv python --no-default-packages```
4. Install requierd packages
```
pip install dicompyler-core
```
```
git clone https://github.com/bastula/dicompyler.git
#suggested versions are:
#dicompyler                         0.5.0
#dicompyler-core                    0.5.6
```
**Now, here comes an important part:**
comment out every "wx"_involvemnt
#and any other modules that might not be needed
#from matplotlib ...
Like this:
a. imports
```
#...
#from wx.lib.pubsub import pub
#...
```
b. class
```
class plugin2DView():#wx.Panel  #don't allow to inherit from wx
```
c. constructor
```
#in constructor: def __init__(self):  
	#wx.Panel.__init__(self)
        pass    
```
it's either that or installing suited wx version (to me, much harder job)
(third option is to copy-paste (rewrite) function that is being called
We just want to use one of class'es methods.


