# p2p-bridge说明
服务器文件夹路径： /home/hanglok/Desktop/HXJ/code/P2P-Bridg   
[p2p-bridge源代码](https://github.com/matvogel/P2P-Bridge)  
## 环境配置
[p2p-bridge环境配置](https://github.com/matvogel/P2P-Bridge?tab=readme-ov-file#%EF%B8%8F-requirements)  

在4090机器上，已经激活了p2pb，如命令行显示未激活p2pb，可运行以下代码激活  
```
conda activate p2pb
```  
## 代码修改
纯3D文件输入，代码参考
```
python denoise_room.py --room_path <ROOM PATH> --model_path <MODEL PATH> --out_path <OUTPUT PATH>
```  
实际运行
```
python denoise_room.py  
--room_path  /home/hanglok/Desktop/HXJ/code/P2P-Bridge/data/hxj/data/cloud.ply   
--model_path /home/hanglok/Desktop/HXJ/code/P2P-Bridge/pretrained/PVDL_ARK_RGB/step_100000.pth 
--out_path   /home/hanglok/Desktop/HXJ/code/P2P-Bridge/data/hxj/output/denoised_cloud.ply
--overwrite
```   
--overwrite（可选）当out_path 已经存在输出的点云时，再运行代码会报错，--overwrite可以直接覆盖原来输出的去噪点云，如果之前没有存在，也可以生成新的，--overwrite最好写上去。  

/home/hanglok/Desktop/HXJ/code/P2P-Bridge/pretrained 下面有model_path，在xyzrgb输入时只能选PVDL_ARK_RGB或PVDL_SNPP_RGB文件夹下的step_100000.pth  
PVDL_SNPP_RGB_DINO文件夹的权重文件需要点云含dino，PVDS_PUNet需要点云是XYZ形式的，不符合要求XYZRGB的形式。

