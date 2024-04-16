# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 07:37:42 2024

@author: agentimis1
"""
#%%
from skimage import io
import os
#%% Sets the working directory input and output
dir1=os.path.realpath(__file__)
main = os.path.dirname(os.path.dirname(dir1))
input_images=main+'\Data\Processed\Soy1'
#%% Load the image
image = io.imread(input_images+'\P5290153.jpg')
#%%
def get_pixel_value(image, x, y):
    return image[y, x]
#%%
# Input coordinates from the user5
x = int(input("Enter the x coordinate of the pixel: "))
y = int(input("Enter the y coordinate of the pixel: "))
# Get the RGB values of the pixel at the specified coordinates
rgb_values = get_pixel_value(image, x, y)

print("RGB values at pixel ({}, {}): {}".format(x, y, rgb_values))

