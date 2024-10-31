# PCL说明
服务器文件夹路径(非4090)： D:\HXJ\code\pcl-learning\mypcl_segmentation\bulid\cloud_viewer.sln  
双击即可打开,代码只需要把txt文件的内容复制到本地的mypcl_segmentation.cpp里,点击运行即可 
## 环境配置及学习文档
参考文档  
[学习文档+环境配置(win/ubuntu)](https://www.yuque.com/huangzhongqing/pcl/lnilhi)  
[Win10下 pcl1.9.1 +vs2017配置教程](https://blog.csdn.net/WXG1011/article/details/126779692?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522172287791716800186516374%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=172287791716800186516374&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~times_rank-6-126779692-null-null.nonecase&utm_term=windows%20%E5%AE%89%E8%A3%85PCL%E5%BA%931.9.1&spm=1018.2226.3001.4450)  
[cmake创建visual studio工程](https://blog.csdn.net/m0_46384757/article/details/121753149?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522172288104516800182710894%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=172288104516800182710894&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-121753149-null-null.142^v100^control&utm_term=cmake%E5%88%9B%E5%BB%BAVS%E9%A1%B9%E7%9B%AE&spm=1018.2226.3001.4187)  

## 代码修改
特别提醒：PCL运行的时候不能含中文名的路径
### 滤波去噪
修改路径，代码不长，具体参数修改可问chatgpt
```
StatisticalOutlierRemoval filter.txt
noise_filter.txt
均匀采样滤波器.txt
离群点移除滤波器.txt
高斯滤波.txt
```  
### 分割机械壁支座
【半人工分割-去除mesh.txt】如没进行Manual cutting stage不报错  
【半人工分割.txt】如果没有进行Manual cutting stage报错，需要进行这个操作。（如果需要修改该问题可以参考半【人工分割-去除mesh.txt】进行修改）  

* 颜色区域生长分割，如果部件分割效果不好可以调整此参数  
```
    int MinClusterSize = 1000, KN_normal = 20;
    float DistanceThreshold = 10.0, ColorThreshold =4.3, RegionColorThreshold =3.5, SmoothnessThreshold = 30.0, CurvatureThreshold = 0.05;
```  
* 计算法面信息，mls_radius越大运行速度会越慢，polynomial_order可不用调
```
    double mls_radius = 0.05;
    int polynomial_order = 2;
```  
* 控制mesh之后的平滑效果的，数字越大越平滑。
```
 pcl::PolygonMesh smoothedMesh = smoothMesh(mesh, 3);  // 迭代3次
``` 
* 滤波参数，可以通过观察输出的点数来看看滤波多少
```
    sor_stat.setMeanK(20);
    sor_stat.setStddevMulThresh(0.01);
``` 
* Mesh阶段三角网格参数，一般调整setSearchRadius，setMu，setMaximumNearestNeighbors
```
    gp3.setSearchRadius(0.05);                          // 设置搜索半径
    gp3.setMu(20.0);                                     // 设置内侧点搜索距离
    gp3.setMaximumNearestNeighbors(100);                // 设置最大邻居点数
    gp3.setMaximumSurfaceAngle(M_PI / 4);               // 设置最大表面角（45度）
    gp3.setMinimumAngle(M_PI / 18);                     // 设置最小角度（10度）
    gp3.setMaximumAngle(2 * M_PI / 3);                  // 设置最大角度（120度）
    gp3.setNormalConsistency(true);                     // 设置法线一致性
``` 
*在mesh阶段的三角化之后进行拉普拉斯平滑
```
    laplacianVtk.setConvergence(0.5f);
    laplacianVtk.setRelaxationFactor(0.25f);
    laplacianVtk.setFeatureAngle(360.f);
    laplacianVtk.setEdgeAngle(180.f);
``` 

### 平面分割
设置RANSAC算法在平面分割时的距离阈值。这个阈值决定了哪些点被视为“内点”（即属于平面的点）
```
seg.setDistanceThreshold(0.06);
```  
判断当前剩余点云中点的数量是否大于原始点云数量的30%
```
 while (cloud_copy->points.size() > 0.3 * nr_points) 
```  
根据点云数据的特点（如密集度、颜色差异等）进行调整
```
        // 设置颜色聚类参数
        reg.setInputCloud(planes[i]);
        reg.setDistanceThreshold(1);           // 空间距离阈值
        reg.setPointColorThreshold(5);          // 点颜色差异阈值
        reg.setRegionColorThreshold(5);         // 区域颜色差异阈值
        reg.setMinClusterSize(0.06 * nr_points); // 最小聚类大小
```  
### 其他分割
修改路径，代码不长，具体参数修改可问chatgpt
``` 
cluster_extraction.txt
conditional_euclidean_clustering.txt
cylinder_segmentation.txt
min_cut_segmentation.txt
region_growing_rgb_segmentation.txt
region_growing_segmentation.txt
supervoxel_clustering.txt
``` 
### mesh
修改路径，代码不长，具体参数修改可问chatgpt
``` 
Greedy+MLS+Laplacian3.txt
GreedyTriangulation+MLS.txt
泊松曲面重建.txt
移动最小二乘法（MLS).txt
移动立方体.txt
贪心三角化.txt
``` 