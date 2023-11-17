import numpy as np
import matplotlib.pyplot as plt
import shading

# READ DATA FROM .NPY FILE 
data = np.load('h3.npy',allow_pickle=True).item()
verts = data['verts']
vertex_colors = data['vertex_colors']
face_indices = data['face_indices']
depth = data['depth']
cam_eye = data['cam_eye']
cam_up = data['cam_up']
cam_lookat = data['cam_lookat']
ka = data['ka']
kd = data['kd']
ks = data['ks']
n = data['n']
light_positions = data['light_positions']
light_intensities = data['light_intensities']
Ia = data['Ia']
M = data['M']
N = data['N']
W = data['W']
H = data['H']
bg_color = data['bg_color']

# WE USE THIS VALUE FOR FOCAL, WHICH WE GET FROM THE PREVIOUS EXERCISE
focal = 70

# GET IMAGES WITH 2 DIFFERENT SHADERS AND 4 DIFFERENT MODES: TOTAL 8 IMAGES
for shader in ['gouraud','phong']:
    for mode in ['ambient','diffusion','specular','all']:
        if mode=='ambient':
            X = shading.render_object(shader,focal,cam_eye,cam_lookat,cam_up,bg_color,M,N,H,W,verts,vertex_colors,face_indices,ka,0,0,n,light_positions,light_intensities,Ia)
        elif mode =='diffusion':
            X = shading.render_object(shader,focal,cam_eye,cam_lookat,cam_up,bg_color,M,N,H,W,verts,vertex_colors,face_indices,0,kd,0,n,light_positions,light_intensities,Ia)
        elif mode == 'specular':
            X = shading.render_object(shader,focal,cam_eye,cam_lookat,cam_up,bg_color,M,N,H,W,verts,vertex_colors,face_indices,0,0,ks,n,light_positions,light_intensities,Ia)
        else:
            X = shading.render_object(shader,focal,cam_eye,cam_lookat,cam_up,bg_color,M,N,H,W,verts,vertex_colors,face_indices,ka,kd,ks,n,light_positions,light_intensities,Ia)
        print('Shader = '+shader+', mode = '+mode)
        fig=plt.figure(0)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(X)
        plt.savefig(shader+'_'+mode+'.jpg')
