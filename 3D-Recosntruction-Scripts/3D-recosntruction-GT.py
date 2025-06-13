import numpy as np
from PIL import Image
import json
import tqdm
import csv
import os

def GT2xyz(GT_folder,output_xyz_filepath,mission,auv,mission_metadata):
        sonar_configuration = json.load(open('sonar-configuration.json'))
        sonar_model=sonar_configuration["P900"]
        try:
            with open(output_xyz_filepath, 'w') as outfile:
                for i,file in enumerate(os.listdir(GT_folder)):
                    filename=(f"{i+1}.xyz")
                    matrix=np.load(f"SEE-Dataset/Sonar-Dataset-mission-{mission}-P900/auv-{auv}/GT-bin/{i+1}.npy")
                    theta,phi=matrix.shape
                    #if filename.endswith(".xyz"):
                    filepath = os.path.join(GT_folder, filename)
                    try:
                        #with open(filepath, 'r') as infile:
                            for t in range(theta):
                                for p in range(phi): 
                                    #parts = line.strip().split() #split each line by space.
                                    auv_metadata=json.load(open(f"SEE-Dataset/Sonar-Dataset-mission-{mission}-P900/auv-{auv}/Meta-data/{i+1}.json"))

                                    r=matrix[t][p]
                                    theta_=((t*(sonar_model["Azimuth"])/theta)-sonar_model["Azimuth"]/2) + auv_metadata["yaw"]
                                    if mission%2==0:
                                        phi_=((p*(sonar_model["Elevation"])/phi)-sonar_model["Elevation"]/2) -45
                                    else:
                                        phi_=((p*(sonar_model["Elevation"])/phi)-sonar_model["Elevation"]/2)
                
                
                                    x=r*np.cos(np.deg2rad(theta_))*np.cos(np.deg2rad(phi_))+(auv_metadata["x"]-float(mission_metadata[2]))
                                    y=r*np.sin(np.deg2rad(theta_))*np.cos(np.deg2rad(phi_))+(auv_metadata["y"]+float(mission_metadata[3]))
                                    z=r*np.sin(np.deg2rad(phi_)) + auv_metadata["z"]
                                
                                    outfile.write(f"{x} {y} {z}\n")
                                    

                            print(f"Merged and offset {filename}")
                    except FileNotFoundError:
                            print(f"Error: File not found: {filepath}")
                    except Exception as e:
                            print(f"Error processing {filename}: {e}")

            print(f"Successfully merged all .xyz files into {output_xyz_filepath}")

        except Exception as e:
            print(f"An error occurred: {e}")





if __name__ == "__main__":
    # Replace with your actual XYZ file paths


    missions=[1,2,3,4]
    auvs=[12,18,33]

    for auv in auvs:
        for mission in missions:
        
            GT_folder=(f"SEE-Dataset/Sonar-Dataset-mission-{mission}-P900/auv-{auv}/Point-cloud")
            output_xyz_filepath=(f"gt-{mission}-auv-{auv}.xyz")

        with open(f"SEE-Dataset/mission{mission}.csv", newline='') as f:
            reader = csv.reader(f)
            mission_metadata = list(reader)
            mission_metadata.pop(0)

        mission_met=mission_metadata[auv]

        GT2xyz(GT_folder,output_xyz_filepath,mission,auv,mission_met)