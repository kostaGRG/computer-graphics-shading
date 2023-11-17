import numpy as np
import triangle_filling

# This function is responsible for calculating the rotation matrix,
# given the angle in rads (theta) and the axis of the rotation (u)
def calculateRotMatrix(theta,u):
    # Case that we dont apply rotation
    if theta is None or np.mod(theta,360) == 0:
        R = np.eye(3)

    # Otherwise, calculate the rotation matrix based on the theory
    else:
        k1 = 1 - np.cos(theta)
        k2 = np.cos(theta)
        k3 = np.sin(theta)
        ux = u[0]
        uy = u[1]
        uz = u[2]

        R = np.array([
            [k1*np.power(ux,2)+k2, k1*ux*uy - k3*uz, k1*ux*uz + k3*uy],
            [k1*ux*uy + k3*uz, k1*np.power(uy,2)+k2, k1*uy*uz - k3*ux],
            [k1*ux*uz - k3*uy, k1*uy*uz + k3*ux, k1*np.power(uz,2) + k2]
            ])

    return R

# FUNCTION A
def affine_transform(c_p, theta, u, t):
    # First get rotation matrix
    R = calculateRotMatrix(theta,u)

    # we use homogeneous coordinates, so even if there is not
    # shift operation, we add one more column.
    if t is None:
        t = np.array(np.append([0,0,0],1))[:,None]
    else:
        t = np.array(np.append(t,1))[:,None]

    # add one more row, due to homogeneous coords
    R = np.concatenate((R,np.zeros(3)[:,None].T),axis=0)
    R = np.concatenate((R,t),axis=1)
    c_q = np.matmul(R,np.concatenate((c_p,np.ones(np.shape(c_p)[1])[:,None].T),axis=0))

    return c_q[:3]

# FUNCTION B
# again we follow the methodology as before, but in this case we have to
# change some details, because it's about system transform.
def system_transform(c_p,R,c_o):
    if c_o is None:
        c_o = np.array(np.append([0,0,0],1))[:,None]
    else:
        c_o = - np.matmul(R,c_o)
        c_o = np.array(np.append(c_o,1))[:,None]
    
    R = np.concatenate((R,np.zeros(3)[:,None].T),axis=0)
    R = np.concatenate((R,c_o),axis=1)
    d_p = np.matmul(R,np.concatenate((c_p,np.ones(np.shape(c_p)[1])[:,None].T),axis=0))
    return d_p[:3]

# FUNCTION C
def project_cam(f,c_v,c_x,c_y,c_z,p):
    N = np.shape(p)[1]
    verts2d = np.zeros((2,N))
    depth = np.zeros((1,N))

    # rotation matrix, given that c_x, c_y, c_z are the cords of the 3 camera axes.
    R = np.array([c_x,c_y,c_z])
    verts3d = system_transform(p,np.transpose(R),c_v)
    # depth is equal with value of third coordinate
    depth = verts3d[2,:]
    verts2d = f*verts3d[0:2,:]/depth

    return [verts2d, depth]

def project_cam_lookat(f,c_org,c_lookat,c_up,verts3d):
    # apply theory to calculate c_x,c_y and c_z from c_lookat and c_up
    ck = c_lookat - c_org
    c_z = ck/np.linalg.norm(ck)
    t = c_up - np.dot(c_up,c_z)*c_z
    c_y = t/np.linalg.norm(t)
    c_x = np.cross(c_y,c_z)

    return project_cam(f,c_org,c_x,c_y,c_z,verts3d)


def rasterize(verts2d,img_h,img_w,cam_h,cam_w):
    verts_rast = np.zeros(np.shape(verts2d))
    # constant k used for mapping from camera coordinates (x,y) to image coordinates
    k = [img_h/cam_h,img_w/cam_w]

    # center of the camera
    center = [cam_h/2,cam_w/2]

    # coordinates transform and return the new one
    verts2d[0,:] = verts2d[0,:] + center[0]
    verts2d[1,:] = verts2d[1,:] + center[1]

    verts_rast[0,:] = np.floor(k[0]*verts2d[0,:]) 
    verts_rast[1,:] = np.floor(k[1]*verts2d[1,:]) 
    return verts_rast


def render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up):
    I = np.ones((img_h, img_w, 3))
    [verts2d,depth] = project_cam_lookat(f,c_org,c_lookat,c_up,verts3d)
    verts2d = rasterize(verts2d,img_h,img_w,cam_h,cam_w)
    I = triangle_filling.render(verts2d.T, faces, vcolors)

    return I