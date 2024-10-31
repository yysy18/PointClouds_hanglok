import numpy as np
import open3d as o3
import transforms3d as t3d
from probreg import bcpd
from probreg import callbacks
import utils

source, target = utils.prepare_source_and_target_3d('bunny1.ply','bunny2.ply',voxel_size=0.1)
cbs = [callbacks.Open3dVisualizerCallback(source, target)]
tf_param = bcpd.registration_bcpd(source, target,
                                  callbacks=cbs)

print("result: ", np.rad2deg(t3d.euler.mat2euler(tf_param.rigid_trans.rot)),
      tf_param.rigid_trans.scale, tf_param.rigid_trans.t)
