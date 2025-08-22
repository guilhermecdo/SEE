import numpy as np
from PIL import Image
import json
import tqdm
import csv

def png2matrix(image_path):
    """
    Opens a PNG image, converts it to grayscale, and returns its pixel data as a NumPy array.

    Args:
        image_path (str): The path to the PNG image file.

    Returns:
        numpy.ndarray: A 2D NumPy array representing the grayscale pixel data, or None if an error occurs.
    """
    try:
        # Open the image using Pillow (PIL)
        img = Image.open(image_path)
        img=img.rotate(180)

        # Convert the image to grayscale
        img_gray = img.convert("L")  # "L" mode for grayscale

        # Convert the grayscale image to a NumPy array
        numpy_array = np.array(img_gray)
        #print(numpy_array.max())
        return numpy_array

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def matrix2xyz(matrix,output_xyz_filepath,mission_metadata):

        radius, theta = matrix.shape
        #try:
        with open(output_xyz_filepath, 'a') as outfile:
                for t in range(theta):
                    for r in range(radius):
                        if matrix[r][t]>0:
                            
                            rad = (r*4.5)/radius
                            if rad<3.3:
                                phi_= (matrix[r][t]-(10)) + float(mission_metadata[-2])
                                theta_= ((t*(130)/theta)-65) + float(mission_metadata[-1])
                            
                            
                                x=(rad*np.cos(np.deg2rad(theta_))*np.cos(np.deg2rad(phi_)))
                                y=(rad*np.sin(np.deg2rad(theta_))*np.cos(np.deg2rad(phi_)))
                                z=(rad*np.sin(np.deg2rad(phi_))) + float(mission_metadata[-4])
                                outfile.write(f"{x} {y} {z}\n")
        #except:
        #    pass

if __name__ == "__main__":

    #file_path=f""
    file_path=f"/home/guilherme/Documents/SEE-Dataset/SEE-Real-Data/single-view/imgs_elevateNET/"

    with open(f"/home/guilherme/Documents/SEE-Dataset/SEE-Real-Data/single-view/synchronized_summary.csv", newline='') as f:
        reader = csv.reader(f)
        mission_metadata = list(reader)
        mission_metadata.pop(0)

    output_xyz_filepath=(f"elevateNET-realData.xyz")
    #output_xyz_filepath=(f"elevateNETR-realData-singleView.xyz")
    
    for i in tqdm.tqdm(range(len(mission_metadata))):
        image_file_path =f"{file_path}{mission_metadata[i][0]}"
        #print(mission_metadata[i][0])
        matrix2xyz(matrix=png2matrix(image_file_path),output_xyz_filepath=output_xyz_filepath,mission_metadata=mission_metadata[i])