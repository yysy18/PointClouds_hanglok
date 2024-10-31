import numpy as np
import transforms3d as t3d
from probreg import l2dist_regs
from probreg import callbacks
import utils

source, target = utils.prepare_source_and_target_3d('bunny1.ply','bunny2.ply',voxel_size=0.1)

cbs = [callbacks.Open3dVisualizerCallback(source, target)]

tf_param = l2dist_regs.registration_svr(source, target,callbacks=cbs)
print("result: ", np.rad2deg(t3d.euler.mat2euler(tf_param.rot)),
      tf_param.scale, tf_param.t)
