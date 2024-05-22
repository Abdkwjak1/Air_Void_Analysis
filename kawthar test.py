#!/usr/bin/env python
# coding: utf-8

# In[23]:


from skimage.transform import resize
import SimpleITK as sitk
import cv2
import pydicom
import numpy as np
import os
from matplotlib import pyplot as plt 
from skimage.measure import label, regionprops
from skimage.morphology import remove_small_objects


# In[6]:


# imagedata= pydicom.dcmread(r"C:\Users\kawthar\Downloads\Hossz (1)\Hossz\s_0005.dcm")
# img =imagedata.pixel_array



#Reading the whole dicom series 
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(os.path.join(os.getcwd(),"Downloads","Hossz","Hossz"))
reader.SetFileNames(dicom_names)
image = reader.Execute()
image.GetSize()
image.GetSpacing()
image_np = sitk.GetArrayFromImage(image)
# sitk_img = sitk.ReadImage(r"C:\Users\kawthar\Downloads\Hossz (1)\Hossz\s_0005.dcm")
plt.imshow(image_np[15,:,:])


# In[15]:


# Trimming the volume
binary_mask = (image_np>0).astype(np.uint8)
labeled_mask = label(binary_mask)
regions = regionprops(labeled_mask)
max_region = max(regions,key=lambda region: region.area)
min_slice, min_row, min_col, max_slice, max_row, max_col = max_region.bbox
cropped = image_np[min_slice:max_slice+1,min_row:max_row+1,min_col:max_col+1]


ran_slice = np.random.randint(0,cropped.shape[0])
plt.imshow(cropped[ran_slice,:,:])


# In[26]:


# labeling and counting the holes.

hole_mask = (cropped >= -1000) & (cropped <= 0)
hole_mask = hole_mask.astype(np.uint8)
labeled_holes, num_holes = label(hole_mask, connectivity=2, return_num=True)

min_size = 100  # Adjust this value based on your specific case
filtered_holes = remove_small_objects(labeled_holes, min_size=min_size)

# Measure circularity of detected objects and label circular holes
circular_holes = np.zeros_like(filtered_holes)
for label_value in range(1, num_holes + 1):
    region = filtered_holes == label_value
    props = regionprops(region)
    circularity = props[0].perimeter ** 2 / (4 * np.pi * props[0].area)
    if 0.8 <= circularity <= 1.2:  # Adjust circularity threshold as needed
        circular_holes[region] = label_value

# Count the circular holes
num_circular_holes = len(np.unique(circular_holes)) - 1 
print(f"Number of holes: {num_circular_holes}")


# In[219]:


os.path.join(os.getcwd(),"Downloads","Hossz","Hossz")


# In[188]:


# name = imagedata.split('/')[-1][:-4]
img = resize(img,(512,512)) 


# In[191]:


cv2.imwrite('output1.png', img * 255)


# In[192]:


print(imagedata.BitsAllocated) 
print(imagedata.PhotometricInterpretation)


# In[172]:


smallerimage= img [0:455 , 0:420]
img2= smallerimage [120:480 , 100:420]


# In[200]:


plt.imshow(img)


# In[180]:


plt.imshow (img)


# In[182]:


plt.imshow(img2)


# In[ ]:





# In[181]:


for y in range(200):
    for x in range(200):
        if (img[y,x]>1000):
            print("y="+str(y)+" x="+str(x))
            break

