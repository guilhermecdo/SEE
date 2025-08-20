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

        return numpy_array

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def matrix2xyz(matrix,output_xyz_filepath,index,mission,auv,mission_metadata):
        sonar_configuration = json.load(open('/home/guilherme/Documents/SEE-Dataset/SEE-Synthetic-Data/sonar-configuration.json'))
        sonar_model=sonar_configuration["P900"]
        auv_metadata=json.load(open(f"/home/guilherme/Documents/SEE-Dataset/SEE-Synthetic-Data/Sonar-Dataset-mission-{mission}-P900/auv-{auv}/Meta-data/{index}.json"))
        radius, theta = matrix.shape
        try:
            with open(output_xyz_filepath, 'a') as outfile:
                for t in range(theta):
                    for r in range(radius):
                        if matrix[r][t]>0:
                            
                            rad = (r*sonar_model["RangeMax"])/sonar_model["RangeBins"] + sonar_model["RangeMin"]
                            phi_= (matrix[r][t]-(sonar_model["Elevation"]/2))
                            theta_= ((t*(sonar_model["Azimuth"])/theta)-sonar_model["Azimuth"]/2) +auv_metadata["yaw"]
                            
                            
                            x=(rad*np.cos(np.deg2rad(theta_))*np.cos(np.deg2rad(phi_)))+(auv_metadata["x"]-float(mission_metadata[2]))
                            y=(rad*np.sin(np.deg2rad(theta_))*np.cos(np.deg2rad(phi_)))+(auv_metadata["y"]+float(mission_metadata[3]))
                            z=(rad*np.sin(np.deg2rad(phi_))) + auv_metadata["z"]
                            outfile.write(f"{x} {y} {z}\n")
        except:
            pass

if __name__ == "__main__":

    missions=[1]
    auvs=[12,18,33]
    for m in missions:
        with open(f"/home/guilherme/Documents/SEE-Dataset/SEE-Synthetic-Data/mission{m}.csv", newline='') as f:
            reader = csv.reader(f)
            mission_metadata = list(reader)
            mission_metadata.pop(0)
        for auv in auvs:
            mission=mission_metadata[auv]
            output_xyz_filepath=(f"unet-multiview-{m}-auv-{auv}.xyz")
            for i in tqdm.tqdm(range(int(mission[-1])-1)):
                image_file_path = (f"/home/guilherme/Documents/Pytorch-UNet/Multiview-SEE/{m}-{auv}/{i}.png")
                matrix2xyz(matrix=png2matrix(image_file_path),output_xyz_filepath=output_xyz_filepath,index=i,mission=m,auv=auv,mission_metadata=mission)