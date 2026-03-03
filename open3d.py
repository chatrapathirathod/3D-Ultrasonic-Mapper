import open3d as o3d
import numpy as np

# Create random 3D points
points = np.random.rand(200, 3) * 100

# Create point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Show the points
o3d.visualization.draw_geometries(
    [pcd],
    window_name="Open3D Test - If you see this, Open3D works",
    width=800,
    height=600
)
