import csv
import random
import os
from PIL import Image
import sys
import numpy as np

def combine_images_pixelwise(image_paths, output_path="combined_image.png"):
    """
    Combines 2 or 3 images by averaging their pixels.

    All images are resized to the dimensions of the first image in the list
    to allow for pixel-by-pixel operations. The output image will have the
    same size as the first input image.

    Args:
        image_paths (list): A list of paths to the images.
                            Should contain 2 or 3 image paths.
        output_path (str): The path to save the combined image.
    """
    if not 2 <= len(image_paths) <= 3:
        print("Error: Please provide 2 or 3 image paths.")
        return

    try:
        # Open images and convert to grayscale ('L')
        images = [Image.open(path).convert("L") for path in image_paths]
    except FileNotFoundError:
        print(f"Error: One or more image paths are invalid: {image_paths}")
        return
    except Exception as e:
        print(f"Error opening images: {e}")
        return

    # --- Image Resizing ---
    # All images must be the same size for pixel math.
    # We will use the size of the first image as the target size.
    target_size = images[0].size
    resized_images = [img.resize(target_size) for img in images]

    # --- Pixel Averaging using NumPy for efficiency ---
    # Convert images to NumPy arrays. We use a float type for calculations
    # to avoid data overflow issues when summing pixel values.
    arrays = [np.array(img, dtype=np.float32) for img in resized_images]

    # Sum the arrays element-wise
    summed_array = np.sum(arrays, axis=0)

    # Divide by the number of images to get the average
    average_array = summed_array / len(images)

    # Convert the resulting float array back to an 8-bit integer array for image saving
    final_array = average_array.astype(np.uint8)

    # Create a new PIL image from the final array
    combined_image = Image.fromarray(final_array)

    try:
        combined_image.save(output_path)
        print(f"Images combined successfully and saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")

def stack_images_vertically(image_paths, output_path="stacked_image.png"):
    """
    Stacks 2 or 3 single-channel images vertically.

    The stacking order is from top to bottom corresponding to the end of the
    list to the beginning (e.g., for 3 images, image 3 is on top, 2 in the
    middle, and 1 at the bottom).

    Args:
        image_paths (list): A list of paths to the images.
                            Should contain 2 or 3 image paths.
        output_path (str): The path to save the stacked image.
    """
    if not 2 <= len(image_paths) <= 3:
        print("Error: Please provide 2 or 3 image paths.")
        return

    try:
        # Convert all images to grayscale ('L')
        images = [Image.open(path).convert("L") for path in image_paths]
    except FileNotFoundError:
        print("Error: One or more image paths are invalid.")
        print(image_paths)
        return
    except Exception as e:
        print(f"Error opening images: {e}")
        return

    # To stack images vertically, they must have the same width.
    # We'll resize them to the width of the smallest image to avoid
    # upscaling, while maintaining the aspect ratio for each.
    min_width = min(img.width for img in images)
    
    resized_images = []
    for img in images:
        if img.width > min_width:
            aspect_ratio = img.height / img.width
            new_height = int(aspect_ratio * min_width)
            resized_images.append(img.resize((min_width, new_height)))
        else:
            resized_images.append(img)

    # The heights of the individual resized images
    widths, heights = zip(*(i.size for i in resized_images))

    # The final image will have the common minimum width and the sum of all heights
    total_height = sum(heights)
    max_width = min_width

    # Create a new blank image
    stacked_image = Image.new('L', (max_width, total_height))

    # Reverse the list to paste from top to bottom (img3, img2, img1)
    resized_images.reverse()

    y_offset = 0
    for img in resized_images:
        stacked_image.paste(img, (0, y_offset))
        y_offset += img.height

    try:
        stacked_image.save(output_path)
        print(f"Images stacked successfully and saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")


def join_images_side_by_side(image_paths, output_path="joined_image.png"):
    """
    Joins 2 or 3 single-channel images side by side.

    Args:
        image_paths (list): A list of paths to the images.
                            Should contain 2 or 3 image paths.
        output_path (str): The path to save the joined image.
    """
    if not 2 <= len(image_paths) <= 3:
        print("Error: Please provide 2 or 3 image paths.")
        return

    try:
        images = [Image.open(path).convert("L") for path in image_paths]  # Convert to grayscale
    except FileNotFoundError:
        print(f"Error: One or more image paths are invalid.")
        print(image_paths)
        return
    except Exception as e:
        print(f"Error opening images: {e}")
        return

    # Assuming all images should have the same height for side-by-side joining.
    # We'll resize them to the height of the smallest image to avoid distortion
    # or black bars, while maintaining aspect ratio.
    # If you want a different behavior (e.g., resize to largest, or a fixed height),
    # you can adjust this part.
    #print(image_paths)

    min_height = min(img.height for img in images)
    resized_images = []
    for img in images:
        if img.height > min_height:
            aspect_ratio = img.width / img.height
            new_width = int(aspect_ratio * min_height)
            resized_images.append(img.resize((new_width, min_height)))
        else:
            resized_images.append(img)

    images = resized_images
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights) # Should be min_height if resizing as above

    # Create a new blank image with the combined width and max height
    joined_image = Image.new('L', (total_width, max_height)) # 'L' for grayscale

    x_offset = 0
    for img in images:
        joined_image.paste(img, (x_offset, 0))
        x_offset += img.width

    try:
        joined_image.save(output_path)
        print(f"Images joined successfully and saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")

FILE_PREFIX=f"/home/guilherme/Documents/SEE-Dataset/"
a=0
file_list_imgs=[]
file_list_masks=[]
if __name__ == "__main__":
    missions=[1,3]
    #missions=[1]
    sonar_model="P900"
    for m in missions:
        with open(f"{FILE_PREFIX}mission{m}.csv", newline='') as f:
            reader = csv.reader(f)
            mission_metadata = list(reader)
            mission_metadata.pop(0)
        #mission_met=mission_metadata[0:1]    
        for mission in mission_metadata:
            a=0
            #if (int(mission[6])-1)%3>0:
            #    file_list.clear()
            #    file_list=[f"{FILE_PREFIX}Sonar-Dataset-mission-{m}-{sonar_model}-pitch/auv-{mission[0]}/GT-images/{int(mission[6])-2}.png",
            #        f"{FILE_PREFIX}Sonar-Dataset-mission-{m}-{sonar_model}-pitch/auv-{mission[0]}/GT-images/{int(mission[6])-3}.png",
            #        f"{FILE_PREFIX}Sonar-Dataset-mission-{m}-{sonar_model}-pitch/auv-{mission[0]}/GT-images/{int(mission[6])-4}.png"]
            #    stack_images_vertically(file_list,f"masks/{m}-{sonar_model}-{mission[0]}-{int((int(mission[6])-1)/3)+1}.png")
            #a=0
            #file_list.clear()

            for i in range(3*(int(mission[6]))):
                #for a in range(3):
                file_img=f"{FILE_PREFIX}Sonar-Dataset-mission-{m}-{sonar_model}-pitch/auv-{mission[0]}/Cartesian-images/{i}.png"
                file_list_imgs.append(file_img)
                file_mask=f"{FILE_PREFIX}Sonar-Dataset-mission-{m}-{sonar_model}-pitch/auv-{mission[0]}/GT-images/{i}.png"
                file_list_masks.append(file_mask)
                if len(file_list_imgs)==3:
                    combine_images_pixelwise(file_list_imgs,f"imgs_combined/{m}-{sonar_model}-{mission[0]}-{a}.png")
                    combine_images_pixelwise(file_list_masks,f"masks_combined/{m}-{sonar_model}-{mission[0]}-{a}.png")
                    stack_images_vertically(file_list_imgs,f"imgs_stack/{m}-{sonar_model}-{mission[0]}-{a}.png")
                    stack_images_vertically(file_list_masks,f"masks_stack/{m}-{sonar_model}-{mission[0]}-{a}.png")
                    file_list_imgs.clear()
                    file_list_masks.clear()
                    a=a+1