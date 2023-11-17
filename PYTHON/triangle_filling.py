import time
import numpy as np

# Function that calculates the color of each pixel, based on the distance between two known pixels.
def interpolate_color(x1,x2,x,C1,C2):
    k = np.sqrt(np.sum(np.square(np.subtract(x,x2))))/np.sqrt(np.sum(np.square(np.subtract(x2,x1))))
    value = k * C1 + (1-k) * C2
    return value


def shade_triangle(img,verts2d,vcolors,shade_t):
    Y = img

    dims = np.shape(Y)
    # Initialization of these arrays, which will store the min and max values of every edge
    xkmin = np.zeros(3)
    xkmax = np.zeros(3)
    ykmin = np.zeros(3)
    ykmax = np.zeros(3)

    # Find min and max values and store them on the above arrays
    for k in range(3):
        z1 = verts2d[k]
        z2 = verts2d[(k+1)%3]
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

    mean_color = np.mean(vcolors,axis=0)

    # Initialize y as ymin and empty arrays with active edges and active vertices
    y = ymin
    active_edges = np.zeros(3)
    active_vertices = []

    # Initialize m: pinakas me tis kliseis ka8e akmhs: Dx = m*Dy 
    m = np.zeros(3)

    # Find active edges and vertices
    for k in range(3):
        # Get vertices' pairs for each edge
        z1 = verts2d[k]
        z2 = verts2d[(k+1)%3]
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
                        # Color pixels between the pair of active vertices
                        if shade_t == 'flat':
                            Y[int(y)][int(x+0.5)] = mean_color
                        elif shade_t == 'gouraud':
                            k1 = z1[2]
                            k2 = z2[2]
                            # First find rgb color for the first active vertex
                            c1 = interpolate_color(verts2d[k1],verts2d[(k1+1)%3],z1[:2],vcolors[k1],vcolors[(k1+1)%3])
                            # Then find rgb color for the second one
                            c2 = interpolate_color(verts2d[k2],verts2d[(k2+1)%3],z2[:2],vcolors[k2],vcolors[(k2+1)%3])
                            Y[int(y)][int(x+0.5)] = interpolate_color(z1[:2],z2[:2],[int(x+0.5),y],c1,c2)
   
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
        
                    
    return Y
                
def render(verts2d,faces,vcolors,depth,shade_t):
    # verts2d (Lx2): array with L vertices
    # faces (Kx3): array with K triangles
    # vcolors (Lx3)
    # depth (Lx1)

    start = time.time()

    # Initialize image's dimensions
    M = 512
    N = 512

    # Initialize canvas' color to white
    img = np.ones((M,N,3))
    if shade_t != 'flat' and shade_t != 'gouraud':
        print('Argument shade_t must has one of the following values: flat or gouraud')
        return 
    
    # Create triangles and colors of each triangle based on arguments
    triangles = np.array(verts2d[faces])
    triangle_colors= np.array(vcolors[faces])

    # Calculate depth for each of the above triangles
    depths = np.array(depth[faces])
    depths = np.mean(depths,axis = 1)
    index=np.argsort(depths)[::-1]

    # Reorder triangles' list based on depths, in descending order
    triangles = triangles[index]
    triangle_colors = triangle_colors[index]

    # Call shade_triangle function for each triangle.
    for i in range(len(triangles)):
        print('Iteration ',i)
        img = shade_triangle(img,triangles[i],triangle_colors[i],shade_t)
    print('total time= %.2f seconds.'%(time.time() - start))
    return img




