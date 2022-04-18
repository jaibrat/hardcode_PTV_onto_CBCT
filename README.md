hardcode_PTV_onto_CBCT
============
This python script is used to hardcode contour data onto CBCT_Pixel_data_image (img)
<img src='https://raw.githubusercontent.com/jaibrat/hardcode_PTV_onto_CBCT/main/demo-imge.PNG' align='right' height='440' width='287' alt="idea in short">

Installing
==========
1. Install Anaconda (recommended, not necessary)
2. create environment  ```bash
conda create --name myenv python --no-default-packages```
4. install requierd packages ```bash
pip install dicompyler-core
dicompyler                         0.5.0
dicompyler-core                    0.5.6
```


Using (preparing CBCTs)
======
1. From your TPS: Export CT, plan & SS to disk (*.dcm)
2. Export CBCT do to disk (*.dcm)
3. Set filenames (in this python script) to point to correct files
4. Set
