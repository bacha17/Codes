# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 07:15:35 2024

@author: agentimis1
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import os
#%% Sets the working directory input and output
dir1=os.path.realpath(__file__)
main = os.path.dirname(os.path.dirname(dir1))
input_images=main+'\Data\Processed\Soy1'
#%% Load the image
image = io.imread(input_images+'\P5290155.jpg')
#%% Mask creating function. Just run it to load the funtion
def mask_soybeans(image, soybean_range):
    # Convert image to numpy array
    image_array = np.array(image)

    # Create a mask based on the provided soybean range
    mask = np.all((image_array >= soybean_range[0]) & (image_array <= soybean_range[1]), axis=-1)

    # Convert the mask to 3 channels to use as a mask
    mask = np.stack([mask]*3, axis=-1)

    # Apply the mask to the original image
    isolated_soybeans = np.where(mask, 255, 0).astype(np.uint8)

    return isolated_soybeans


#%% Format: [lower_bound, upper_bound], where each bound is a 3-element list [R, G, B]
soybean_range = [[72, 108, 65], [145, 170, 130]]  # Adjust these values based on your soybean color

#%% Apply mask to isolate soybeans
isolated_soybeans = mask_soybeans(image, soybean_range)

#%% Create a figure and axes
fig, axes = plt.subplots(2, 1, figsize=(8, 10))

# Plot the original image in the first subplot
axes[0].imshow(image)
axes[0].set_title('Original Image')
axes[0].axis('on')

# Plot the isolated soybeans image in the second subplot
axes[1].imshow(isolated_soybeans)
axes[1].set_title('Isolated Soybeans')
axes[1].axis('on')
#add_pixel_labels(axes[1], isolated)

# Adjust layout to reduce white space between subplots
plt.subplots_adjust(wspace=0, hspace=0)

# Save and show the plot
plt.savefig(main+'\Results\Combined_images.png', bbox_inches='tight')
plt.show()

