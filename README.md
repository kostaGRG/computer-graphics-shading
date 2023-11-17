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
### Functions
#### Function: Ambient Light
Create the function:

ambient_light(ka, Ia)

which calculates the illumination of a point P belonging to a surface with Phong-type material due to diffuse lighting from the environment, and:
* ka is the coefficient of diffuse light from the environment.
* Ia=[Ir,Ig,Ib] is the 3x1 vector with the components of the intensity of diffuse radiation from the environment. Each component belongs to the interval [0, 1].
The function calculates the intensity of trichromatic radiation I=[Ir,Ig,Ib] that is reflected from point P. The intensity contributes cumulatively to the color of the pixel.

#### Function: Diffuse Light
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

## Implementations
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
