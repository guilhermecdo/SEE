import numpy as np
from scipy.spatial import cKDTree

def load_xyz(filename):
    """Loads a point cloud from an XYZ file.

    Args:
        filename (str): Path to the XYZ file.
        use_gpu (bool): If True, loads the data onto the GPU.

    Returns:
        cupy.ndarray or numpy.ndarray: Nx3 array representing the point cloud, or None if an error occurs.
    """
    try:
        data = np.loadtxt(filename)
        return data
    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        return None
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None


def hausdorff_distance_cpu(point_cloud1, point_cloud2):
    """Calculates the mean and RMS Hausdorff distance between two point clouds using CPU.

    Args:
        point_cloud1 (numpy.ndarray): Nx3 array representing the first point cloud (on CPU).
        point_cloud2 (numpy.ndarray): Mx3 array representing the second point cloud (on CPU).

    Returns:
        tuple: (mean_hausdorff, rms_hausdorff)
    """
    if point_cloud1 is None or point_cloud2 is None:
        return None, None

    tree1 = cKDTree(point_cloud1)
    tree2 = cKDTree(point_cloud2)

    distances1_to_2, _ = tree2.query(point_cloud1)
    distances2_to_1, _ = tree1.query(point_cloud2)

    mean_hausdorff = (np.mean(distances1_to_2) + np.mean(distances2_to_1)) / 2.0
    rms_hausdorff = np.sqrt((np.mean(distances1_to_2**2) + np.mean(distances2_to_1**2)) / 2.0)

    return mean_hausdorff, rms_hausdorff

if __name__ == "__main__":
    
    missions=[1]
    objs=[12,18,33]

    for obj in objs:
        for  m in missions:
            # Replace with your actual XYZ file paths
            file1 = (f"gt-{m}-auv-{obj}.xyz")
            file2 = (f"{m}-auv-{obj}.xyz")

            point_cloud1 = load_xyz(file1,use_gpu=True)
            point_cloud2 = load_xyz(file2,use_gpu=True)

            if point_cloud1 is not None and point_cloud2 is not None:
                mean_h, rms_h = hausdorff_distance_cpu(point_cloud1, point_cloud2)
                print(f"Mean {m} {obj}: {mean_h}")
                print(f"RMS {m} {obj}: {rms_h}")