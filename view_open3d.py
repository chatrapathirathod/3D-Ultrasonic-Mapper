import open3d as o3d
import pickle
import numpy as np

# LOAD DOTS
with open("points.pkl", "rb") as f:
    points = pickle.load(f)

points_np = np.array(points)

# CREATE POINT CLOUD
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points_np)

# SHOW MAP
o3d.visualization.draw_geometries([pcd])
