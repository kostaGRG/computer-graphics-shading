# computer-graphics-shading
## Intro
This project is created for the university class named Computer Graphics at Aristotle University of Thessaloniki (AUTh). It's the third out of three repositories referenced on the same class.

## General
In this assignment, we are tasked with combining the functions from previous assignments with those developed in this one, which concern the lighting of objects. The uploaded folder named PYTHON contains the following Python files:
* Demo.py
* Camera_functions.py
* Triangle_filling.py
* Lighting.py
* Shading.py
  
The first file, demo.py, is the one that calls the functions to perform the requested operations. Initially, we read the data from the available h3.npy file and store it in the corresponding variables. We also initialize some constants defined in the assignment statement. Immediately after, we capture the object successively with the four types of lighting requested, for the two types of shaders, by calling the render_object function located in the shading.py file with the appropriate arguments. The images are automatically saved by the program.

The file camera_functions.py is the one created in the second assignment without any changes. The functions project_cam_lookat and rasterize from the shading.py file are used here. The file triangle_filling.py is also used without any changes, exactly as it was in the second deliverable. The functions shade_triangle and interpolate_color from the shading.py file are used here.

## Tasks: Lighting
### Function: Ambient Light
Create the function:

ambient_light(ka, Ia)

which calculates the illumination of a point P belonging to a surface with Phong-type material due to diffuse lighting from the environment, and:
* ka is the coefficient of diffuse light from the environment.
* Ia=[Ir,Ig,Ib] is the 3x1 vector with the components of the intensity of diffuse radiation from the environment. Each component belongs to the interval [0, 1].
The function calculates the intensity of trichromatic radiation I=[Ir,Ig,Ib] that is reflected from point P. The intensity contributes cumulatively to the color of the pixel.

### Function: Diffuse Light
Implement the function:

I = diffuse_light(P, N, color, kd, light_positions, light_intensities)

which calculates the illumination of a point P due to diffuse reflection, and:
* P is a 3x1 column vector with the coordinates of point P.
* N is a 3x1 column vector with the coordinates of the normal vector of the surface at point P (i.e., the vector perpendicular to the surface). The vector points outward from the surface, towards the observer.
* color=[cr,cg,cb] is the 3x1 vector with the color components of point P. Each component belongs to the interval [0, 1].
* kd is the coefficient of diffuse reflection of the Phong model.
* light_positions is a list of 3x1 vectors containing the positions of light sources.
* light_intensities is a list of 3x1 vectors containing the intensities of the light sources (corresponding to the light_positions).
  
The function calculates the intensity of trichromatic radiation I=[Ir,Ig,Ib] that is reflected from point P. The intensity contributes cumulatively to the final color of the pixel.

### Function: Specular Light
Implement the function:

I = specular_light(P, N, color, cam_pos, ks, n, light_positions, light_intensities)

which calculates the illumination of a point P due to specular reflection, and:
* P is a 3x1 column vector with the coordinates of point P.
* N is a 3x1 column vector with the coordinates of the normal vector of the surface at point P (i.e., the vector perpendicular to the surface). The vector points outward from the surface, towards the observer.
* color=[cr,cg,cb] is the 3x1 vector with the color components of point P. Each component belongs to the interval [0, 1].
* cam_pos is a 3x1 column vector with the coordinates of the observer (i.e., the camera).
* ks is the coefficient of specular reflection of the Phong model.
* n is the Phong exponent.
* light_positions is a list of 3x1 vectors containing the positions of light sources.
* light_intensities is a list of 3x1 vectors containing the intensities of the light sources (corresponding to the light_positions).
  
The function calculates the intensity of trichromatic radiation I=[Ir,Ig,Ib] that is reflected from point P. The intensity contributes cumulatively to the final color of the pixel.

## Implementations: Lighting
### Function: Ambient Light
ambient_light(ka,Ia)

It calculates the illumination caused by ambient light in the environment and returns the result.

### Function: Diffuse Light
diffuse_light(P,N,color,kd,light_positions,light_intensities)

The function calculates the illumination of a point due to diffuse reflection. For each light source, it calculates the unit vector L between the source and point P, and the final result is calculated using the well-known formula from theory:

![Diffuse light formula](/images/diff_light.png)

For the following images, it was assumed that f_att=1, but in the code, there is also the option to take distance into account, in the form of a comment. The final color returned is the sum of the original input color and the calculated I.

### Function: Specular Light
specular_light(P,N,color,cam_pos,ks,n,light_positions,light_intensities)

The function calculates the illumination of a point due to specular reflection. For each light source, the unit vectors L and V are calculated. The final result is then computed using the formula

![Specular light formula](/images/spec_light.png)

It returns as the final color the sum of the original input color with the calculated I.

## Tasks: Shading
### Function: Calculation of surface's normal vectors
Consider a 3D object composed exclusively of N_T triangles. Implement the function:

normals = calculate_normals(vertices, face_indices)

where:
* vertices is a 3×Nv array with the coordinates of the object's vertices.
* face_indices is a 3×NT array describing the triangles. The k-th column of face_indices contains the ascending numbers of the vertices of the k-th triangle of the object, 1≤k≤NT. The order of vertex listing follows the right-hand rule, indicating the direction of the normal vector and, therefore, the outward side of the object.

The function calculates the 3×Nv array with the coordinates of the normal vectors at each point (vertex) on the surface defined by the object.

### Function: Object Rendering
Implement the function:

img = render_object(shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors, face_indices, ka, kd, ks, n, light_position, light_intensities, Ia)

which creates the colored image img of a 3D object by calculating the color based on the lighting models from section A. Specifically, it implements the following process:
1. Calculate the normal vectors of the object's vertices using the calculate_normals function.
2. Project the vertices of the triangles into an orthogonal camera projection using the project_cam_ku() function from assignment #2. Triangles with vertices outside the projection will not be colored.
3. Repeatedly call the shading function selected based on the value of the shader variable to color each triangle of the object, starting from those with the greatest depth (as in previous assignments).

The arguments it accepts are as follows:
* shader is a binary control variable used to select the function (described below) to be used for shading the triangles. Consider that shader = "gouraud" corresponds to Gouraud shading, and shader = "phong" corresponds to Phong shading.
* focal is the distance from the projection to the camera center (in the units of measurement used in the camera's coordinate system).
* eye is the 3 × 1 vector with the coordinates of the camera center.
* lookat is the 3 × 1 vector with the coordinates of the camera's target point.
* up is the 3 × 1 unit up vector of the camera.
* bg_color is the 3 × 1 vector with the color components of the background.
* M and N are the dimensions of the generated image in pixels (i.e., M × N pixels).
* H and W describe the physical dimensions of the camera's projection in length units identical to those used in the camera's coordinate system.
* verts is a 3 × Nv array with the coordinates of the object's vertices.
* verts_colors is a 3 × Nv array with the color components of each vertex of the object.
* face_indices as defined for the calculate_normals function.
* ka, kd, ks, and n are the coefficients that define the surface texture.
* light_positions is a list of 3 × 1 vectors containing the position components of the light sources.
* light_intensities is a list of 3 × 1 vectors containing the intensities of the light sources (corresponding to light_positions).
* Ia = [Ir, Ig, Ib]T is the 3 × 1 vector with the components of the intensity of ambient radiation. Each component belongs to the interval [0, 1].

For a given triangle, calculate the vectors V and L of the lighting models once, using the center of gravity of the triangle as point P (before projection), and consider them constant for all points of the triangle.

### Function: Gouraud Shading
Implement the function:

Y = shade_gouraud(vertsp, vertsn, vertsc, bcoords, cam_pos, ka, kd, ks, n, light_positions, light_intensities, Ia, X)

which calculates the color at the vertices of the given triangle based on the full lighting model (i.e., using the functions from section A) and then uses linear interpolation of colors to find the color at the interior points of the triangle, using the interpolate_color function from assignment #1. More specifically:
* The vertsp array, of dimensions 2 × 3, contains the coordinates of the triangle's vertices after projection into the camera's view.
* The vertsn array, of dimensions 3 × 3, contains the normal vectors of the triangle's vertices in its columns.
* The vertsc array, of dimensions 3 × 3, contains the color components for each point of the triangle.
* The bcoords vector, of dimensions 3 × 1, contains the barycenter of the triangle before projection.
* cam_pos is a 3 × 1 column vector with the coordinates of the observer (i.e., the camera).
* ka, kd, ks, and n are the coefficients that define the surface texture.
* light_positions is a list of 3 × 1 vectors containing the position components of the light sources.
* light_intensities is a list of 3×1 vectors containing the intensities of the light sources (corresponding to light_positions).
* Ia = [Ir, Ig, Ib]T is the 3 × 1 vector with the components of the intensity of ambient radiation in the environment. Each component belongs to the interval [0, 1].
* X is an image (a 3D array of dimensions M × N × 3) with any pre-existing triangles.
* Y is an array of dimensions M × N × 3, which, for the points inside the triangle, will contain the corresponding color components (Ri, Gi, Bi) as well as any pre-existing triangles from input X (overlapping any common colored points that existed from other triangles)

### Function: Phong Shading
Implement the function:

Y = shade_phong(vertsp, vertsn, vertsc, bcoords, campos, ka, kd, ks, n, light_position, light_intensities, Ia, X)

which calculates the color of the points within the triangle by interpolating both the normal vectors and vertex colors. Specifically:
1. For the given triangle, it will calculate the normal vectors of the initial points (i.e., before projection) along the active edges by performing linear interpolation on the normal vectors of the vertices of the edge.
2. For each interior point, it will calculate the normal vector along the scan line by performing linear interpolation on the normal vectors corresponding to the active points of the edge.
3. A similar process will be performed for the colors of the points.
4. Once the normal vector and color for a point have been calculated, its color will be determined using the functions ambient_light(), diffuse_light(), and specular_light().

The arguments of the function are the same as those of the shade_gouraud() function

## Implementations: Shading
### Function: Calculation of surface's normal vectors
The function returns the normal vector at that point for each available vertex. Iteratively, the function performs the following operation:

For each triangle, it finds the three vectors formed by its sides. To calculate the normal vector at the vertex, it calculates the cross product of the two vectors associated with that vertex. For example, in triangle ABC, to find the normal vector N at vertex A, it calculates the cross product between vectors CA and AB. The resulting cross product is then normalized, and this process continues iteratively for all triangles in the image.

### Function: Object Rendering
This is the function that coordinates all the operations. Initially, it calls the "calculate_normals" function to calculate the normal vectors at each vertex. Immediately after, the functions from the "camera_functions" file are called to find the coordinates of the three-dimensional points in the two dimensions, as projected by the camera. We calculate the depths of each triangle as in previous tasks and change the order of the triangles based on these depths (a known procedure). Depending on the value of the "shader" argument, we call the respective function, either "shader_gouraud" or "shader_phong," for each of the triangles. After obtaining the values of the final image, we scale them to the range [0, 1]. We check which of these values remained unchanged throughout the lighting and coloring process: they belong to the background. Therefore, we ensure that they are maintained proportionally to their original values.

### Function: Gouraud Shading
This function is called by the "render_object" function, which has already been analyzed. It performs linear interpolation on the triangle after first calculating the colors of the three vertices, taking into account the lighting they are subjected to. Depending on the values of the coefficients k, it selects which types of lighting to consider, calling the corresponding functions defined in the "lighting.py" file. More specifically, if there is only one non-zero value of k, it chooses that type of lighting, while in all other cases, it uses all three types of lighting. After calculating the final colors for the three vertices of the triangle, it calls the "shade_triangle" function from the "triangle_filling.py" file with shading = gouraud, which, as we know, will perform the coloring of the triangle using linear interpolation.

### Function: Phong Shading
This function is similar in most of its parts to the "shade_triangle" function, as it is a copy of it. However, the change it makes is that it performs interpolation not only for the colors of each point but also for the unit normal vector of the triangle at that point. So, after calculating the color of this point through interpolation, the color value is updated, taking into account the lighting, with the type of lighting being influenced by the values of the coefficients ka, kd, ks, just like in the "shade_gouraud" function.

## Results
At this point in the report, I present the results from running the "demo.py" program. The same results can be obtained by anyone who chooses to run the program without the need to use any external arguments. Since the process of capturing the 8 images is time-consuming, the program reports in the console which image it is currently processing, providing information about the shader type and lighting method used.

1. Shading: Gouraud, Lighting: Ambient

![Gouraud Ambient](/images/gouraud_ambient.jpg)

2. Shading: Gouraud, Lighting: Diffuse

![Gouraud Diffuse](/images/gouraud_diffusion.jpg)

3. Shading: Gouraud, Lighting: Specular

![Gouraud Specular](/images/gouraud_specular.jpg)

4. Shading: Gouraud, Lighting: All

![Gouraud All](/images/gouraud_all.jpg)

5. Shading: Phong, Lighting: Ambient

![Phong Ambient](/images/phong_ambient.jpg)

6. Shading: Phong, Lighting: Diffuse

![Phong Diffuse](/images/phong_diffusion.jpg)

7. Shading: Phong, Lighting: Specular

![Phong Specular](/images/phong_specular.jpg)

4. Shading: Phong, Lighting: All

![Phong All](/images/phong_all.jpg)
