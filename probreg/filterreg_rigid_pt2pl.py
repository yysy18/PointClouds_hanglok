import numpy as np
import transforms3d as t3d
from probreg import filterreg
from probreg import callbacks
import utils

source, target = utils.prepare_source_and_target_3d('bunny1.ply','bunny2.ply',voxel_size=0.1)

cbs = [callbacks.Open3dVisualizerCallback(source, target)]
objective_type = 'pt2pl'
tf_param, _, _ = filterreg.registration_filterreg(source, target, target.normals,
                                                  objective_type=objective_type,
                                                  sigma2=0.01,
                                                  callbacks=cbs)

print("result: ", np.rad2deg(t3d.euler.mat2euler(tf_param.rot)),
      tf_param.scale, tf_param.t)
