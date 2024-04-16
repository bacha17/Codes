# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 17:00:53 2024

@author: agentimis1
"""
#%% Packages
import os
import pandas as pd
import numpy as np
from skimage import io, morphology, feature
# Suppress low contrast warning
import warnings
warnings.filterwarnings("ignore")

#%%=======================  Sets the working directory input and output
dir1 = __file__ if '__file__' in locals() else os.getcwd()
main_dir = os.path.dirname(os.path.dirname(dir1))
input_images = os.path.join(main_dir, 'Data', 'Processed', 'Soy1')
output_images = os.path.join(main_dir, 'Data', 'Processed', 'Soy1_Counted')

#%%=======================  Create output folder if it doesn't exist
if not os.path.exists(output_images):
    os.makedirs(output_images)

#%%======================= Set erosion and dilation
erode_width = 8  # Adjusted to more realistic values
dilate_width = 12  # Adjusted to more realistic values

#%%=======================  Format: [lower_bound, upper_bound], where each bound is a 3-element list [R, G, B]
soybean_range = [[75, 120, 70], [125, 175, 130]]  # Adjust these values based on your soybean color
results = []  # Initialize results list

#%%=======================  Mask creating, erosion, dilation, and blob detection function.
def process_image(image, soybean_range, erode_width, dilate_width):
    # Convert image to numpy array
    image_array = np.array(image)

    # Create a mask based on the provided soybean range
    mask = np.all((image_array >= soybean_range[0]) & (image_array <= soybean_range[1]), axis=-1)

    # Apply morphological erosion and dilation
    selem = morphology.square(erode_width)
    mask_eroded = morphology.erosion(mask, selem)
    mask_dilated = morphology.dilation(mask_eroded, morphology.square(dilate_width))

    # Convert the mask to 3 channels to use as a mask
    mask_dilated_3d = np.stack([mask_dilated]*3, axis=-1)

    # Apply the mask to the original image
    isolated_soybeans = np.where(mask_dilated_3d, image_array, 0).astype(np.uint8)

    # Blob detection
    blobs = feature.blob_log(mask_dilated, max_sigma=100, num_sigma=10, threshold=.1)
    blob_count = len(blobs)

    return isolated_soybeans, blob_count

#%%======================= Reading, processing, and writing images
def main(input_folder, output_folder, erode_width, dilate_width):
    # List all files in the input folder
    image_names = [f for f in os.listdir(input_folder) if f.endswith('.JPG') or f.endswith('.png') or f.endswith('.jpeg')]
    
    # Process each image
    for filename in image_names:
        try:
            # Read the image
            image = io.imread(os.path.join(input_folder, filename))
            
            # Process the image (including erosion, dilation, and blob detection)
            isolated_image, blob_count = process_image(image, soybean_range, erode_width, dilate_width)
            
            # Count soybean pixels
            soybean_pixels = np.sum(isolated_image > 0) // 3  # Adjusted for the isolated image
            
            # Save the processed image
            io.imsave(os.path.join(output_folder, filename), isolated_image)
            
            print(f"Processed {filename}")
            
            # Append results to the results list
            results.append([filename, soybean_pixels, blob_count])
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
#%% Executing everything
if __name__ == "__main__":
    main(input_images, output_images, erode_width, dilate_width)
#%% Returning the results as a csv file
resultsdf = pd.DataFrame(results, columns=['Image Name', 'Soybean Pixels', 'Blob Count'])
resultsdf.to_csv(os.path.join(main_dir, 'Results', 'Pixel_Blob_Counts.csv'), index=False)

print("Processing complete. Results saved to Pixel_Blob_Counts.csv.")