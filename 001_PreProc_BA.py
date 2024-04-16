# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 19:19:39 2024

@author: agentimis1
"""
#%%=================== Importing libraries 
import os
#import numpy as np
from skimage import io
#from skimage.draw import rectangle_perimeter
#%% Sets the working directory input and output
dir1=os.path.realpath(__file__)
main = os.path.dirname(os.path.dirname(dir1))
input_images=main+'\Data\Raw\CRS2023'
output_images=main+'\Data\Processed\CRS2023'
#%%==================== Creating function to crop
def crop_image_center(image, width, height):
    center_row = image.shape[0] // 2
    center_col = image.shape[1] // 2
    min_row = max(0, center_row - height // 2)
    max_row = min(image.shape[0], center_row + height // 2)
    min_col = max(0, center_col - width // 2)
    max_col = min(image.shape[1], center_col + width // 2)
    cropped_image = image[min_row:max_row, min_col:max_col]
    return cropped_image
#%%======================= Reading and writing images
def main(input_folder, output_folder, width, height):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # List all files in the input folder
    image_names = [f for f in os.listdir(input_folder) if f.endswith('.JPG') or f.endswith('.png') or f.endswith('.jpeg')]
    
    # Output list of filenames
    print("List of Image Filenames:")
    for filename in image_names:
        print(filename)
    print("\n")
    
    # Process each image
    for filename in image_names:
        try:
            # Read the image
            image = io.imread(os.path.join(input_folder, filename))
            
            # Crop the image
            cropped_image = crop_image_center(image, width, height)
            
            # Save the cropped image
            io.imsave(os.path.join(output_folder, filename), cropped_image)
            
            print(f"Processed {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
#%% Executing everything
if __name__ == "__main__":
    input_folder = input_images
    output_folder = output_images
    width = 2700  # Width of the rectangle
    height = 450  # Height of the rectangle
    main(input_folder, output_folder, width, height)