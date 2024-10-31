import open3d as o3
import numpy as np
def prepare_source_and_target_3d(source_filename,target_filename,voxel_size=0.01):
    source = o3.io.read_point_cloud(source_filename)
    source = source.voxel_down_sample(voxel_size=voxel_size)
    print(source)
    target = o3.io.read_point_cloud(target_filename)
    target = target.voxel_down_sample(voxel_size=voxel_size)
    print(target)
    return source, target
