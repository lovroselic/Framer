# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 22:15:06 2024

@author: lovro
"""
import os
from PIL import Image, ImageStat
import time

VERSION = "0.2.0"

# Directories
INPUT_DIR = "input"  # Directory containing input PNG files
OUTPUT_DIR = "Output"  # Directory to save output images


# Configurable parameters
CENTER_REGION_SIZE = 768  # Size of the central region (square)
COLOR_TOLERANCE = 100  # Tolerance for matching canvas color
EXPECTED_RESOLUTION = 1024

FILENAME = "GenericFrame"
counter = 65

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_dominant_color(image, region_size):
    """
    Get the dominant color in the center of the image.
    Args:
        image (PIL.Image): The image to analyze.
        region_size (int): Size of the central region for analysis.
    Returns:
        tuple: Dominant RGB color.
    """
    width, height = image.size
    left = (width - region_size) // 2
    top = (height - region_size) // 2
    right = left + region_size
    bottom = top + region_size

    # Crop the central region
    cropped = image.crop((left, top, right, bottom))
    # Calculate average color
    stat = ImageStat.Stat(cropped)
    return tuple(int(x) for x in stat.mean[:3])  # Return RGB values

def is_similar_color(pixel_color, dominant_color, tolerance):
    """
    Check if a pixel color is similar to the dominant color within a tolerance.
    """
    return all(abs(pixel_color[i] - dominant_color[i]) <= tolerance for i in range(3))

def find_canvas_edges(image, dominant_color):
    """
    Find the top, bottom, left, and right edges of the canvas.
    Args:
        image (PIL.Image): The input image.
        dominant_color (tuple): The dominant color of the canvas.
    Returns:
        tuple: (top_left, bottom_right) coordinates of the rectangular canvas.
    """
    width, height = image.size
    pixels = image.load()

    # Initialize edges with the center region
    center_x, center_y = width // 2, height // 2
    half_region = CENTER_REGION_SIZE // 2

    # Start with safe defaults
    top_edge = center_y - half_region
    bottom_edge = center_y + half_region
    left_edge = center_x - half_region
    right_edge = center_x + half_region

    # Search for the top edge
    for y in range(center_y - half_region, -1, -1):  # Upward
        if any(not is_similar_color(pixels[center_x, y][:3], dominant_color, COLOR_TOLERANCE) for x in range(width)):
            top_edge = y + 1  # Set the first valid row
            break

    # Search for the bottom edge
    for y in range(center_y + half_region, height):  # Downward
        if any(not is_similar_color(pixels[center_x, y][:3], dominant_color, COLOR_TOLERANCE) for x in range(width)):
            bottom_edge = y - 1  # Set the last valid row
            break

    # Search for the left edge
    for x in range(center_x - half_region, -1, -1):  # Leftward
        if any(not is_similar_color(pixels[x, center_y][:3], dominant_color, COLOR_TOLERANCE) for y in range(height)):
            left_edge = x + 1  # Set the first valid column
            break

    # Search for the right edge
    for x in range(center_x + half_region, width):  # Rightward
        if any(not is_similar_color(pixels[x, center_y][:3], dominant_color, COLOR_TOLERANCE) for y in range(height)):
            right_edge = x - 1  # Set the last valid column
            break

    # Construct the rectangle from the detected edges
    print(f"..top edge: {top_edge}, bottom edge: {bottom_edge}, left edge: {left_edge}, right edge: {right_edge}")
    top_left = (max(0, left_edge), max(0, top_edge))
    bottom_right = (min(width - 1, right_edge), min(height - 1, bottom_edge))

    print(f"...top left color {pixels[left_edge-1, top_edge-1][:3]}")
    print(f"...bottom right color {pixels[right_edge+1, bottom_edge+1][:3]}")
    return top_left, bottom_right

def apply_transparency(image, top_left, bottom_right):
    pixels = image.load()
    width, height = image.size
    for x in range(max(0, top_left[0]), min(width, bottom_right[0] + 1)):
        for y in range(max(0, top_left[1]), min(height, bottom_right[1] + 1)):
            pixels[x, y] = (0, 0, 0, 0)  # Set to fully transparent
    return image


def process_image(image_path, output_path):
    """
    Process a single image to remove the inner canvas and save the result.
    """
    image = Image.open(image_path).convert("RGBA")
    
    if image.size != (EXPECTED_RESOLUTION, EXPECTED_RESOLUTION):
        print(f"Skipping {os.path.basename(image_path)}: Image size is {image.size}, not 1024x1024.")
        return
    
    dominant_color = get_dominant_color(image, CENTER_REGION_SIZE)
    print(f"Dominant color: {dominant_color}")

    top_left, bottom_right = find_canvas_edges(image, dominant_color)
    print(f"Canvas edges detected: Top-Left: {top_left}, Bottom-Right: {bottom_right}")

    result_image = apply_transparency(image, top_left, bottom_right)
    result_image.save(output_path, "PNG")
    print(f"Saved: {output_path}")

def process_images(counter):
    """
    Process all PNG files in the input directory and save the results to the output directory.
    """
    print(f"\n************** Framer Canvas Remover v{VERSION}**************")
    start_time = time.time()
    
    
    for file_name in os.listdir(INPUT_DIR):
        if file_name.lower().endswith(".png"):
            input_path = os.path.join(INPUT_DIR, file_name)
            output_path = os.path.join(OUTPUT_DIR, f"{FILENAME}_{str(counter).zfill(3)}.png")
            print(f"\nProcessing image: {file_name}")
            process_image(input_path, output_path)
            counter += 1
    print("\n************** DONE **************")
    print("All images processed.")
    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")


# Execute the script
if __name__ == "__main__":
    process_images(counter)
