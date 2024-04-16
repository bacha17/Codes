# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:00:53 2024

@author: agentimis1
"""
#%% Packages
import os
import cv2
import numpy as np
from skimage import io, color
import pandas as pd
#%% Sets the working directory input and output
dir1=os.path.realpath(__file__)
main = os.path.dirname(os.path.dirname(dir1))
input_directory=main+'\Data\Processed\Soy1'
output_directory=main+'\Data\Processed\Soy1_Masked'
#%% Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
#%% Define the function to process each image
def process_image(image_path, output_directory):
    # Read the image
    image = io.imread(image_path)
    
    # Convert image to grayscale
    grayscale_image = color.rgb2gray(image)
    
    # Define the lower and upper bounds for the RGB range of soybeans
    lower_bound = np.array([70, 105, 65])
    upper_bound = np.array([150, 170, 130])
    
    # Create a mask based on the RGB range
    mask = cv2.inRange(image, lower_bound, upper_bound)
    
    # Invert the mask
    mask = cv2.bitwise_not(mask)
    
    # Apply the mask to the grayscale image
    masked_image = cv2.bitwise_and(grayscale_image, grayscale_image, mask=mask)
    
    # Convert the masked image to binary (black and white)
    _, binary_image = cv2.threshold(masked_image, 1, 255, cv2.THRESH_BINARY)
    
    # Count the number of white pixels (soybeans)
    soybean_pixels_count = np.sum(binary_image == 255)
    
    # Save the binary image
    #output_filename = os.path.splitext(os.path.basename(image_path))[0] + "_binary.JPG"
   #output_path = os.path.join(output_directory, output_filename)
   # io.imsave(output_path, binary_image)
    
    return soybean_pixels_count



#%% Initialize a DataFrame to store the results
results = []

#%% Process each image in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".JPG") or filename.endswith(".png"):
        image_path = os.path.join(input_directory, filename)
        soybean_pixels_count = process_image(image_path, output_directory)
        results.append({'Image Name': filename, 'Soybean Pixels Count': soybean_pixels_count})

#%% Create a DataFrame from the results and save it to a CSV file
results_df = pd.DataFrame(results)
results_df.to_csv(main+'\Results\Soybean_pixel_counts.csv', index=False)