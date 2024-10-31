# -*- coding: utf-8 -*-
import os
import torch
import argparse
import numpy as np
import open3d as o3d

from segment import seg_point, seg_box, seg_mask
import sam2point.dataset as dataset
import sam2point.configs as configs
from sam2point.voxelizer import Voxelizer
from sam2point.utils import cal
from show import render_scene, render_scene_outdoor
torch.autocast(device_type="cuda", dtype=torch.bfloat16).__enter__()

if torch.cuda.get_device_properties(0).major >= 8:
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

def create_box(prompt):
   x_min, y_min, z_min, x_max, y_max, z_max = tuple(prompt)
   bbox_points = np.array([
       [x_min, y_min, z_min],
       [x_max, y_min, z_min],
       [x_max, y_max, z_min],
       [x_min, y_max, z_min],
       [x_min, y_min, z_max],
       [x_max, y_min, z_max],
       [x_max, y_max, z_max],
       [x_min, y_max, z_max]
   ])
   edges = [
       (0, 1), (1, 2), (2, 3), (3, 0), # Bottom face
       (4, 5), (5, 6), (6, 7), (7, 4), # Top face
       (0, 4), (1, 5), (2, 6), (3, 7)  # Vertical edges
   ]
   bbox_lines = []
   f = 1
   for start, end in edges:
       bbox_lines.append(go.Scatter3d(
           x=[bbox_points[start, 0], bbox_points[end, 0]],
           y=[bbox_points[start, 1], bbox_points[end, 1]],
           z=[bbox_points[start, 2], bbox_points[end, 2]],
           mode='lines',
           line=dict(color='rgb(220, 20, 60)', width=6),  
           name="Box Prompt" if f == 1 else "",
           showlegend=True if f == 1 else False
       ))
       f = 0
   return bbox_lines


import plotly.graph_objs as go
import subprocess
import webbrowser
import random
def visualize_point_cloud(points, colors,prompt_box, title="Point Cloud Visualization"):
    if points.shape[0] > 400000:
           indices = np.random.choice(points.shape[0], 400000, replace=False)
           points = points[indices]
           colors = colors[indices]

    scatter = go.Scatter3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2],
        mode='markers',
        marker=dict(
            size=1,  # 点的大小
            color=colors,  # 使用RGB颜色
            opacity=1
        )
    )

    scatter = [scatter]+ create_box(prompt_box)
    # scatter = [scatter]
    
    layout = go.Layout(
        title=title,
        scene=dict(
            xaxis=dict(visible=True),  # 将坐标轴设置为可见
            yaxis=dict(visible=True),
            zaxis=dict(visible=True),
            aspectmode='data'  ,
            bgcolor='rgb(30, 30, 40)'  
        )
    )

    # layout = go.Layout(
    #     title=title,
    #     scene=dict(
    #         xaxis=dict(visible=False),  # 将坐标轴设置为可见
    #         yaxis=dict(visible=False),
    #         zaxis=dict(visible=False),
    #         aspectmode='data'  ,
    #         bgcolor='rgb(30, 30, 40)'  
    #     )
    # )

    fig = go.Figure(data=scatter, layout=layout)

    # 保存为 HTML 文件，确保路径正确
    file_path = os.path.join(os.getcwd(), "point_cloud_visualization.html")
    fig.write_html(file_path)

    print(f"HTML file saved at: {file_path}")  # 调试输出

    return file_path

def start_server(file_path):
    """使用 subprocess 启动带随机端口的 HTTP 服务器"""
    # 随机选择一个端口号，避免端口占用冲突
    port = random.randint(1024, 65535)

    # 改变当前工作目录到 HTML 文件所在的目录
    os.chdir(os.path.dirname(file_path))

    # 使用 subprocess 启动服务器
    try:
        subprocess.Popen(["python", "-m", "http.server", str(port)])
        print(f"Serving at http://localhost:{port}/")
        return port  # 返回生成的端口号
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    args.dataset = 'S3DIS'
    args.prompt_type='box'
    args.sample_idx=5
    args.prompt_idx =0

    args.voxel_size =0.02
    args.theta =0.
    args.mode='bilinear'  
    
    info = configs.S3DIS_samples[args.sample_idx]
    point, color,point0= dataset.load_S3DIS_sample(info['path'])
  
    print(args)
    point_color = np.concatenate([point, color], axis=1)
    voxelizer = Voxelizer(voxel_size=args.voxel_size, clip_bound=None)
    
    labels_in = point[:, :1].astype(int)
    locs, feats, labels, inds_reconstruct = voxelizer.voxelize(point, color, labels_in)

    if args.prompt_type == 'point':
        mask = seg_point(locs, feats, info['point_prompts'], args)
        point_prompts = np.array(info['point_prompts'])
        prompt_point = list(point_prompts[args.prompt_idx])
        prompt_box = None
    elif args.prompt_type == 'box':
        mask = seg_box(locs, feats, info['box_prompts'], args)
        box_prompts = np.array(info['box_prompts'])
        prompt_point = None
        prompt_box = list(box_prompts[args.prompt_idx])
    else:
        print("Wrong prompt type! Please select prompt type from {point, box}. Mask prompt will be released soon. Please be patient. :))")
    
    point_locs = locs[inds_reconstruct]
    point_mask = mask[point_locs[:, 0], point_locs[:, 1], point_locs[:, 2]]
    
    point_mask = point_mask.unsqueeze(-1)
    point_mask_not = ~point_mask
    
    point, color = point_color[:, :3], point_color[:, 3:]
    new_color = color * point_mask_not.numpy() + (color * 0 + np.array([[0., 1., 0.]])) * point_mask.numpy()

    point=point*(point0.max(axis=0)-point0.min(axis=0))+point0.min(axis=0)
    prompt_box=np.array([-4.0, 0.7,-0.19,    -3.7, 1.5, 0.23])
    file_path = visualize_point_cloud(point,new_color,prompt_box, title="Segmented Point Cloud")

    # 检查 file_path 是否有效
    if not file_path:
        print("Error: No file path returned for visualization.")
        return

    # 启动 HTTP 服务器并获取随机端口号
    port = start_server(file_path)

    if port:
        # 打开浏览器显示点云文件
        webbrowser.open(f"http://localhost:{port}/{os.path.basename(file_path)}")
    else:
        print("Failed to start the server.")

if __name__=='__main__':
    main()
