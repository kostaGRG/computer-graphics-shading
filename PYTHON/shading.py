import numpy as np
import camera_functions
import lighting
import triangle_filling

# FUNCTION THAT CALCULATES NORMAL VECTOR OF EACH VERTEX FOR EVERY TRIANGLE
def calculate_normals(vertices,face_indices):
    num_of_triangles = np.shape(face_indices)[0]
    normals = np.zeros((np.shape(vertices)))
    for i in range(num_of_triangles):
        current_vertices = vertices[face_indices[i,:]]
        A = current_vertices[0,:]
        B = current_vertices[1,:]
        C = current_vertices[2,:]
        ab = B-A
        bc = C-B
        ca = A-C
        normals[face_indices[i,0],:] = np.cross(ca,ab)/np.linalg.norm(np.cross(ca,ab))
        normals[face_indices[i,1],:] = np.cross(ab,bc)/np.linalg.norm(np.cross(ab,bc))
        normals[face_indices[i,2],:] = np.cross(bc,ca)/np.linalg.norm(np.cross(bc,ca))
    return normals

def render_object(shader,focal,eye,lookat,up,bg_color,M,N,H,W,verts,vert_colors,face_indices,ka,kd,ks,n,light_positions,light_intensities,Ia):
    # 1. Calculate normal vectors
    normals = calculate_normals(verts,face_indices)

    X = np.full((M,N,3),bg_color)

    # 2, Get 2d vertices and form the triangles in the right order
    [verts2d,depth] = camera_functions.project_cam_lookat(focal,eye,lookat,up,np.transpose(verts))
    verts2d = camera_functions.rasterize(verts2d,M,N,H,W)
    verts2d = np.transpose(verts2d)
    depths = np.array(depth[face_indices])
    depths = np.mean(depths,axis = 1)
    index=np.argsort(depths)[::-1]

    triangles = verts[face_indices]
    triangles2d = verts2d[face_indices]
    triangle_colors = vert_colors[face_indices]
    triangle_normals = normals[face_indices]

    triangles = triangles[index]
    triangles2d = triangles2d[index]
    triangle_colors = triangle_colors[index]
    triangle_normals = triangle_normals[index]

    # 3. Choose shader function and shade the triangles
    if shader == 'gouraud':
        for i in range(np.shape(triangles)[0]):
            # print('iteration ',i)
            bcoords = np.mean(triangles[i],axis=0)
            X = shade_gouraud(triangles2d[i],triangle_normals[i],triangle_colors[i],bcoords,eye,ka,kd,ks,n,light_positions,light_intensities,Ia,X)
    elif shader == 'phong':
        for i in range(np.shape(triangles)[0]):
            # print('iteration ',i)
            bcoords = np.mean(triangles[i],axis=0)
            X = shade_phong(triangles2d[i],triangle_normals[i],triangle_colors[i],bcoords,eye,ka,kd,ks,n,light_positions,light_intensities,Ia,X)

    # 4. Scale the final image after all the lightings back to [0,1]. We take care to keep the background on the same color. 
    minX = np.min(X)
    maxX = np.max(X)
    for i in range(np.shape(X)[0]):
        for j in range(np.shape(X)[1]):
            if np.array_equal(X[i,j],bg_color): 
                X[i,j] = bg_color*maxX
    X = (X-minX)/(maxX-minX)
    return X

def shade_gouraud(verts_p,verts_n,verts_c,bcoords,cam_pos,ka,kd,ks,n,light_positions,light_intensities,Ia,X):
    if kd == 0 and ks == 0:
        verts_c = verts_c + lighting.ambient_light(ka,Ia)
    elif ka == 0 and ks == 0:
        for j in range(3):
            verts_c[j] = lighting.diffuse_light(bcoords,verts_n[j],verts_c[j],kd,light_positions,light_intensities)
    elif ka == 0 and kd == 0:
        for j in range(3):
            verts_c[j] = lighting.specular_light(bcoords,verts_n[j],verts_c[j],cam_pos,ks,n,light_positions,light_intensities)
    else:    
        verts_c = verts_c + lighting.ambient_light(ka,Ia)
        for j in range(3):
            verts_c[j] = lighting.diffuse_light(bcoords,verts_n[j],verts_c[j],kd,light_positions,light_intensities)
            verts_c[j] = lighting.specular_light(bcoords,verts_n[j],verts_c[j],cam_pos,ks,n,light_positions,light_intensities)
    Y = triangle_filling.shade_triangle(X,verts_p,verts_c,'gouraud')
    return Y

def shade_phong(verts_p, verts_n, verts_c, bcoords, cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia, X):
    # Initialization of these arrays, which will store the min and max values of every edge
    xkmin = np.zeros(3)
    xkmax = np.zeros(3)
    ykmin = np.zeros(3)
    ykmax = np.zeros(3)
    dims = np.shape(X)

    # Find min and max values and store them on the above arrays
    for k in range(3):
        z1 = verts_p[k]
        z2 = verts_p[(k+1)%3]
        if z1[0] < z2[0]:
            xkmin[k] = z1[0]
            xkmax[k] = z2[0]
        else:
            xkmin[k] = z2[0]
            xkmax[k] = z1[0]
        if z1[1] < z2[1]:
            ykmin[k] = z1[1]
            ykmax[k] = z2[1]
        else:
            ykmin[k] = z2[1]
            ykmax[k] = z1[1]
    # Calculate minimum and maximum value of vertices' y coordinate
    ymin = min(ykmin)
    ymax = max(ykmax)

    # Initialize y as ymin and empty arrays with active edges and active vertices
    y = ymin
    active_edges = np.zeros(3)
    active_vertices = []

    # Initialize m: pinakas me tis kliseis ka8e akmhs: Dx = m*Dy 
    m = np.zeros(3)

    # Find active edges and vertices
    for k in range(3):
        # Get vertices' pairs for each edge
        z1 = verts_p[k]
        z2 = verts_p[(k+1)%3]
        if ykmax[k] != ykmin[k]:
            # Edge is not horizontal. Calculate gradient and check if it's active.
            active_edges[k] =  1*np.all((y >= ykmin[k], y <= ykmax[k]))
            m[k] = (z1[0]-z2[0])/(z1[1]-z2[1])
            if active_edges[k] == 1:
                # Add active vertex.
                if m[k] < 0:
                    x = xkmax[k]
                else:
                    x = xkmin[k]
                active_vertices.append([x,ymin,k])
        else:
            # Edge is horizontal, set its gradient to inf
            m[k] = np.inf
            active_edges[k] = 0

    # Scan each line, from ymin to ymax value
    for y in np.arange(ymin,ymax,1):
        if len(active_vertices) >= 2:
            # Sort active vertices by X values, in ascending order
            active_vertices = sorted(active_vertices)
            for j in range(1,len(active_vertices)):
                z1 = active_vertices[j-1]
                z2 = active_vertices[j]
                for x in range(int(z1[0]+0.5),int(z2[0]+0.5)):
                    if int(y)<0 or int(x+0.5)<0 or int(y) >= dims[0] or int(x+0.5) >= dims[1]:
                        continue
                    else:
                        final_color = 0
                        final_n = 0
                        # Color pixels between the pair of active vertices
                        k1 = z1[2]
                        k2 = z2[2]
                        # First find rgb color for the first active vertex
                        c1 = triangle_filling.interpolate_color(verts_p[k1],verts_p[(k1+1)%3],z1[:2],verts_c[k1],verts_c[(k1+1)%3])
                        # Then find rgb color for the second one
                        c2 = triangle_filling.interpolate_color(verts_p[k2],verts_p[(k2+1)%3],z2[:2],verts_c[k2],verts_c[(k2+1)%3])
                        final_color = triangle_filling.interpolate_color(z1[:2],z2[:2],[int(x+0.5),y],c1,c2)

                        # THE FOLLOWING FEW LINES ARE THE ONLY DIFFERENCE BETWEEN THIS FUNCTION AND THE triangle_filling.shade_triangle FUNCTION.
                        # HERE WE USE INTERPOLATION TO CALCULATE NORMAL VECTORS OF EACH VERTEX AND AFTER THAT WE CALCULATE THE SUITABLE LIGHTING.

                        
                        # First find normal vector for the first active vertex
                        n1 = triangle_filling.interpolate_color(verts_p[k1],verts_p[(k1+1)%3],z1[:2],verts_n[k1],verts_n[(k1+1)%3])
                        # Then find normal color for the second one
                        n2 = triangle_filling.interpolate_color(verts_p[k2],verts_p[(k2+1)%3],z2[:2],verts_n[k2],verts_n[(k2+1)%3])
                        final_n = triangle_filling.interpolate_color(z1[:2],z2[:2],[int(x+0.5),y],n1,n2)

                        if kd == 0 and ks == 0:
                            final_color = final_color + lighting.ambient_light(ka,Ia)
                        elif ka == 0 and ks == 0:
                            final_color = lighting.diffuse_light(bcoords,final_n,final_color,kd,light_positions,light_intensities)
                        elif ka == 0 and kd == 0:
                            final_color = lighting.specular_light(bcoords,final_n,final_color,cam_pos,ks,n,light_positions,light_intensities)
                        else:  
                            final_color = final_color + lighting.ambient_light(ka,Ia)
                            final_color = lighting.diffuse_light(bcoords,final_n,final_color,kd,light_positions,light_intensities)
                            final_color = lighting.specular_light(bcoords,final_n,final_color,cam_pos,ks,n,light_positions,light_intensities)

                        X[int(y)][int(x+0.5)] = final_color

    # Delete edges/vertices if ykmax = y
        for k in range(3):
            if ykmax[k] == y:
                active_edges[k] = 0
                for i in range(len(active_vertices)):
                    vertex = active_vertices[i]
                    if vertex[2] == k:
                        active_vertices.pop(i)
                        break

    # Refresh X,Y values on active vertices
        for i in range(len(active_vertices)):
            vertex = active_vertices[i]
            k = vertex[2]
            active_vertices[i][1] = y+1
            if m[k] != np.inf:
                active_vertices[i][0] = round(active_vertices[i][0] + m[k],2)
            
    # Add edges/vertices if ykmin = y + 1
        for k in range(3):        
            if ykmin[k] == y+1:
                active_edges[k] = 1
                if m[k] != np.inf:
                    if m[k] < 0:
                        x = xkmax[k]
                    else:
                        x = xkmin[k]
                    active_vertices.append([x,y+1,k])
                else:
                    pass
    return X


