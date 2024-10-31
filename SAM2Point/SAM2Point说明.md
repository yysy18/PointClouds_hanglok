# SAM2Point说明
服务器文件夹路径： /home/hanglok/Desktop/HXJ/code/SAM2Point 
[SAM2Point源代码](https://github.com/ZiyuGuo99/SAM2Point)  
## 环境配置
[SAM2Point环境配置](https://github.com/ZiyuGuo99/SAM2Point?tab=readme-ov-file#-get-started)  

在4090机器上，已经激活了sam2point，如命令行显示未激活sam2point，可运行以下代码激活  
```
conda activate sam2point
```  
## 代码修改
用data.py进行归一化，需要填入点云的XYZ范围min_vals、max_vals，以及框选框的范围box_prompts
```
box_prompts = np.array([0.424, 0.51, -0.232,    -3.7, 1.5, 0.23]  )
#x_min, y_min, z_min,    x_max, y_max, z_max

min_vals = np.array([-5.04356, -2.40746, -1.69578])# x_min, y_min, z_min
max_vals = np.array([2.02347, 6.00956, 2.21511])# x_max, y_max, z_max
```  

/home/hanglok/Desktop/HXJ/code/SAM2Point/sam2point/configs.py
需要填入归一化之后的点,修改点云路径
```
...
sample_my = {'path': 'data/S3DIS/d_cloud.txt',
       'point_prompts': [ [0.77367154,0.34661436,0.37428309]],
       'box_prompts': [[0.14766599,0.36918767,0.38502234,0.19011664,0.46423318,0.49241477]],
}
S3DIS_samples = [sample_2, sample_3, sample_4, sample_1, sample_0,sample_my ]
...
```
box.py 和 point.py 需要修改在 configs.py 里面 sample_my 的位置，并且填入（未归一化前）原始box和point的位置 

box.py
```
...
    args.sample_idx=5
    args.prompt_idx =0
...
    prompt_box=np.array([-4.0, 0.7,-0.19,    -3.7, 1.5, 0.23])
...
```  
point.py
```
...
    args.sample_idx=5
    args.prompt_idx =0
...
    prompt_point=np.array([0.424, 0.51, -0.232])
...
```  
只需要点击运行即可，或者python	box.py/python	point.py
```
python	box.py
```  
```
python	point.py
```  