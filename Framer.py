# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 09:18:04 2024

@author: lovro
"""

import os
import random
from PIL import Image
import time

VERSION = "0.2.0"
# Directories
FRAMES_DIR = "Frames"  # Directory containing frame images
PICS_DIR = "Pics"      # Directory containing pictures to be framed
OUTPUT_DIR = "Output"  # Directory to save framed pictures

FILENAME = "UnusedEdtitiesFramed"

resizeW = 768
counter = 1
JPG_QUALITY = 80

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to get the inner width of the frame
def get_inner_width(frame_image):
    """
    Calculate the width of the transparent inner area of the frame.
    Assumes the frame's transparent area is uniform.
    """
    # Convert frame to RGBA for transparency detection
    frame_rgba = frame_image.convert("RGBA")
    # Get pixels as a 2D array
    pixels = frame_rgba.load()
    width, height = frame_image.size

    # Detect the inner width by scanning horizontally for transparent pixels
    for x in range(width):
        for y in range(height):
            if pixels[x, y][3] == 0:  
                return width - (2 *x),x, y 
    return None  

# Main workflow
def frame_pictures(counter):
    print(f"\n************** Framer v{VERSION}**************")
    start_time = time.time()
    
    # Get lists of pictures and frames
    pictures = [f for f in os.listdir(PICS_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    frames = [f for f in os.listdir(FRAMES_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    for picture_file in pictures:
        # Load picture
        picture_path = os.path.join(PICS_DIR, picture_file)
        picture = Image.open(picture_path)
        
        # Select a random frame
        frame_file = random.choice(frames)
        frame_path = os.path.join(FRAMES_DIR, frame_file)
        frame = Image.open(frame_path)

        # Get the inner width of the frame
        inner_width, SX, SY = get_inner_width(frame)

        # Resize the picture to fit within the frame's inner width
        aspect_ratio = picture.height / picture.width
        new_width = inner_width
        new_height = int(new_width * aspect_ratio)
        resized_picture = picture.resize((new_width, new_height), Image.Resampling.LANCZOS)


        # Create a blank canvas for combining
        combined_image = Image.new("RGBA", frame.size)
        # Paste the resized picture and frame
        combined_image.paste(resized_picture, (SX, SY), resized_picture.convert("RGBA"))
        combined_image.paste(frame, (0, 0), frame.convert("RGBA"))
        
        
        #resize
        resizedFinalImage = combined_image.resize((resizeW, int(resizeW * frame.height / frame.width)), 
                                                  Image.Resampling.LANCZOS);

        # Save the combined image to the output directory
        filename = f"{FILENAME}_{str(counter).zfill(3)}"
        output_path = os.path.join(OUTPUT_DIR, f"{filename}.jpg")
        resizedFinalImage = resizedFinalImage.convert("RGB")  
        resizedFinalImage.save(output_path, "JPEG", quality=JPG_QUALITY)
        counter += 1


        print(f"Pic {picture_file} , frame:{frame_file} --> {filename}")
        
    print("************** DONE **************")
    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")

# Execute the main workflow
if __name__ == "__main__":
    frame_pictures(counter)
