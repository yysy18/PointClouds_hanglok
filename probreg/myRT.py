import numpy as np
import transforms3d as t3d
from probreg import filterreg
from probreg import callbacks
import open3d as o3

def prepare_source_and_target_rigid_3d1(source_filename, target_filename, voxel_size=0.01):
    source = o3.io.read_point_cloud(source_filename)
    target = o3.io.read_point_cloud(target_filename)
    print(f"初始源点云大小: {len(source.points)}")
    print(f"初始目标点云大小: {len(target.points)}")
    source_down = source.voxel_down_sample(voxel_size=voxel_size)
    target_down = target.voxel_down_sample(voxel_size=voxel_size)
    print(f"下采样后源点云大小: {len(source_down.points)}")
    print(f"下采样后目标点云大小: {len(target_down.points)}")
    return source_down, target_down

if __name__ == "__main__":
    input_files = input("请输入源点云和目标点云文件路径（用英文逗号分隔）: ")
    source_filename, target_filename = input_files.split(',')
    # 去除可能的空格
    source_filename = source_filename.strip()
    target_filename = target_filename.strip()
    source, target = prepare_source_and_target_rigid_3d1(source_filename, target_filename)
    cbs = [callbacks.Open3dVisualizerCallback(source, target)]
    # 进行滤波配准
    objective_type = 'pt2pt'
    tf_param, _, _ = filterreg.registration_filterreg(
        source, target,
        objective_type=objective_type,
        sigma2=None,
        update_sigma2=True,
        callbacks=cbs
    )
    print("[旋转角度（Euler 角）]  缩放因子 [平移向量]: ", np.rad2deg(t3d.euler.mat2euler(tf_param.rot)),
          tf_param.scale, tf_param.t)
