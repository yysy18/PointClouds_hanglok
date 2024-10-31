# probreg说明
服务器文件夹路径： D:\HXJ\code\probreg-master  
[probreg源代码](https://github.com/neka-nat/probreg)  
## 环境配置
[probreg环境配置](https://github.com/neka-nat/probreg?tab=readme-ov-file#installation)  

在我的电脑上(非4090)，已经激活了base，如命令行显示未激活base，可运行以下代码激活  
```
conda activate base
```  
## 代码修改
修改D:\HXJ\code\probreg-master\probreg\callbacks.py，这样源点云和目标点云保持原来的颜色，配准后的结果点云显示蓝色。
conda activate base
```
        # if not self._result.has_colors():
        #     self._result.paint_uniform_color([0, 0, 1])
        self._result.paint_uniform_color([0, 0, 1])
```  
每个代码只需要修改这一行代码，修改源点云和目标点云的路径，voxel_size根据点云的数量来调整。
```
source, target = prepare_source_and_target_3d(source_filename, target_filename,0.01)
```  