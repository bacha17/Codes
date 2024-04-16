# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:00:53 2024

@author: agentimis1
"""
#%% Packages
import os
import pandas as pd
import numpy as np
from skimage import io, morphology
# Suppress low contrast warning
import warnings
warnings.filterwarnings("ignore")

#%%=======================  Sets the working directory, input, and output
dir1 = __file__ if '__file__' in locals() else os.getcwd()  # Handles environments where __file__ might be undefined
main_dir = os.path.dirname(os.path.dirname(dir1))
input_images = r'F:\02_Thesis_Projects\Soybean_Project\Data\01_Raw_Data\03_PointData\crs2022_test'
output_images = r"F:\02_Thesis_Projects\Soybean_Project\Data\02_Processed_Data\crs_2022_masked"
#%%=======================  Create output folder if it doesn't exist
if not os.path.exists(output_images):
    os.makedirs(output_images)
#%%======================= Set erosion and dilation
erode_width = 1 # Adjusted for demonstration; you might need to tweak it
dilate_width = 30  # Adjusted for demonstration; you might need to tweak it
#%%=======================  Format: [lower_bound, upper_bound], where each bound is a 3-element list [R, G, B]
soybean_range = [[80, 125, 70], [112, 148, 102]]  # Adjust these values based on your soybean color
results = []  # Initialize results list
#%%=======================  Mask creating function. Just run it to load the function
def mask_soybeans(image, soybean_range, erode_width, dilate_width):
    # Convert image to numpy array
    image_array = np.array(image)

    # Create a mask based on the provided soybean range
    mask = np.all((image_array >= soybean_range[0]) & (image_array <= soybean_range[1]), axis=-1)

    # Apply erosion and dilation
    if erode_width > 0:
        mask = morphology.binary_erosion(mask, morphology.disk(erode_width))
    if dilate_width > 0:
        mask = morphology.binary_dilation(mask, morphology.disk(dilate_width))

    # Convert the mask to 3 channels to use as a mask
    mask = np.stack([mask] * 3, axis=-1)

    # Apply the mask to the original image
    isolated_soybeans = np.where(mask, 255, 0).astype(np.uint8)

    return isolated_soybeans
#%%======================= Reading, processing and writing images
def main(input_folder, output_folder, erode_width, dilate_width):
    
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
            
            # Isolate the soybeans in the image
            isolated_image = mask_soybeans(image, soybean_range, erode_width, dilate_width)
            
            # Count soybean pixels
            soybean_pixels = np.sum(isolated_image == 255) // 3  # Divide by 3 for 3 channels
           
            # Save the isolated image
            io.imsave(os.path.join(output_folder, filename), isolated_image)
            
            print(f"Processed {filename}")
            # Append results to the results list
            results.append([filename, soybean_pixels])
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # Create DataFrame from results list and save it
    resultsdf = pd.DataFrame(results, columns=['Image Name', 'Soybean Pixels'])
    results_file_path = r"F:\02_Thesis_Projects\Soybean_Project\Results\Pixel_Counts.csv"
    resultsdf.to_csv(results_file_path)
    print(f"Results saved to {results_file_path}")

#%% Executing everything
if __name__ == "__main__":
    main(input_images, output_images, erode_width, dilate_width)

