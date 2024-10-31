import numpy as np
import open3d as o3
use_cuda = True
if use_cuda:
    import cupy as cp
    to_cpu = cp.asnumpy
    cp.cuda.set_allocator(cp.cuda.MemoryPool().malloc)
else:
    cp = np
    to_cpu = lambda x: x
from probreg import cpd
import utils
import time

source, target = utils.prepare_source_and_target_3d('cloud18.ply','cloud21.ply',voxel_size=0.02)
source_pt = cp.asarray(source.points, dtype=cp.float32)
target_pt = cp.asarray(target.points, dtype=cp.float32)


acpd = cpd.AffineCPD(source_pt, use_cuda=use_cuda)
start = time.time()
tf_param, _, _ = acpd.registration(target_pt)
elapsed = time.time() - start
print("time: ", elapsed)

print("result: ", to_cpu(tf_param.b), to_cpu(tf_param.t))

result = tf_param.transform(source_pt)
pc = o3.geometry.PointCloud()
pc.points = o3.utility.Vector3dVector(to_cpu(result))
pc.paint_uniform_color([0, 0, 1])
o3.visualization.draw_geometries([pc,source,target])