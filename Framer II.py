# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 12:39:26 2025

@author: Uporabnik
version with plain brown frames
"""

import os
import random
from PIL import Image
from PIL import ImageDraw
import time

VERSION = "0.1.0"

# Directories
PICS_DIR = "Pics"      # Directory containing pictures to be framed
OUTPUT_DIR = "Output"  # Directory to save framed pictures

FILENAME = "RetroGames"
counter = 1000
JPG_QUALITY = 80
BORDER_WIDTH = 20

MIN_BROWN = (60, 30, 0)
MAX_BROWN = (150, 100, 60)
TOLERANCE = 20

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clamp(value, min_val, max_val):
    return max(min(value, max_val), min_val)

def random_brown(seed_rgb=(101, 67, 33)):
    r, g, b = seed_rgb
    channel = random.choices([0, 1, 2], weights=[0.6, 0.2, 0.2])[0]
    rgb = [r, g, b]
    original_value = rgb[channel]
    rgb[channel] = random.randint(original_value - TOLERANCE, original_value + TOLERANCE)
    rgb[channel] = clamp(rgb[channel], MIN_BROWN[channel], MAX_BROWN[channel])
    return tuple(rgb)

# main
def frame_pictures(counter):
    print(f"\n************** FramerII v{VERSION}**************")
    start_time = time.time()
    
    pictures = [f for f in os.listdir(PICS_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    
    for picture_file in pictures:
        # Load picture
        picture_path = os.path.join(PICS_DIR, picture_file)
        picture = Image.open(picture_path)
        W, H = picture.size
        M = max(W,H)
        
        if (M <=512):
            BORDER_WIDTH = 10
        else:
            BORDER_WIDTH = 20
        
        newW = W + 2 * BORDER_WIDTH
        newH = H + 2 * BORDER_WIDTH
        new_size = (newW, newH)
        combined_image = Image.new("RGBA", new_size)
        combined_image.paste(picture, (BORDER_WIDTH, BORDER_WIDTH)), picture.convert("RGBA")
        
        # drawing the randomized brown frame
        draw = ImageDraw.Draw(combined_image)
        seed_rgb = (101, 67, 33)
        for i in range(BORDER_WIDTH):
            seed_rgb = random_brown(seed_rgb)
            draw.rectangle((0 + i, 0 + i,  newW-i, newH - i), fill=None, outline=seed_rgb, width=1)
        
        
        # Save the combined image to the output directory
        filename = f"{FILENAME}_{str(counter).zfill(3)}"
        output_path = os.path.join(OUTPUT_DIR, f"{filename}.jpg")
        combined_image = combined_image.convert("RGB")  
        combined_image.save(output_path, "JPEG", quality=JPG_QUALITY)
        counter += 1


        print(f"Pic {picture_file} --> {filename}")
    
    print("************** DONE **************")
    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")




# Execute the main workflow
if __name__ == "__main__":
    frame_pictures(counter)