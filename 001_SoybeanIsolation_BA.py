# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 09:19:46 2024

@author: agentimis1
"""
#%% Packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage import io
import os
#%% Square generating image (just run it to create the function)
def generate_square(image, center_x, center_y, width):
    # Create a copy of the image to avoid modifying the original
    square_image = np.copy(image)
    
    # Calculate the coordinates of the square corners
    x_min = max(0, center_x - width // 2)
    x_max = min(image.shape[1], center_x + width // 2)
    y_min = max(0, center_y - width // 2)
    y_max = min(image.shape[0], center_y + width // 2)
    
    # Draw a white square on the image
    square_image[y_min:y_max, x_min:x_max] = [255, 255, 255]
    
    # Create a DataFrame to store pixel coordinates and RGB values
    pixel_data = []
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            pixel_data.append({'X': x, 'Y': y, 'R': image[y, x, 0], 'G': image[y, x, 1], 'B': image[y, x, 2]})
    
    df = pd.DataFrame(pixel_data)
    
    return square_image, df

#%% Sets the working directory input and output
dir1=os.path.realpath(__file__)
main = os.path.dirname(os.path.dirname(dir1))
input_images=main+'\Data\Processed\Soy1'
#%% Load the image, you can choose anyone in the directory Soy1
image = io.imread(input_images+'\P5290153.jpg')

#%% Display the image
plt.imshow(image)
plt.title('Original Image')
plt.xlabel('X (pixels)')
plt.ylabel('Y (pixels)')
plt.grid(True)
plt.show()

#%% Input coordinates from the user and width
#x = int(input("Enter the x coordinate of the center point: "))
#y = int(input("Enter the y coordinate of the center point: "))
#width = int(input("Enter the width of the square: "))
x=1000
y=120
width=20

#%% Generate the square and get the pixel data
square_image, pixel_df = generate_square(image, x, y, width)

#%% Display the image with the square
plt.imshow(square_image)
plt.title('Image with Square')
plt.axis('off')
plt.show()

#%% Calculate summary statistics and save to CSV
summary_statistics = pixel_df.describe()
summary_statistics.to_csv(main+'\Results\SampleSquare_SumSats.csv')
print(summary_statistics)
