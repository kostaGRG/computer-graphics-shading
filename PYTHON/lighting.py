import numpy as np

def ambient_light(ka,Ia):
    return ka*Ia

# IN THE FOLLOWING 2 FUNCTIONS WE CONSTRUCT THE MATHEMATICAL EQUATIONS OF THE THEORY 
def diffuse_light(P,N,color,kd,light_positions,light_intensities):
    num_of_lights = np.shape(light_positions)[0]
    I = 0
    for i in range(num_of_lights):
        light_position = light_positions[i]
        light_intensity = light_intensities[i]
        L = light_position - P
        distance = np.linalg.norm(L)
        L = L/distance
        # f = 1/np.power(distance,2)
        f = 1
        I = I + light_intensity*kd*f*np.dot(N,L)
    return color+I

def specular_light(P,N,color,cam_pos,ks,n,light_positions,light_intensities):
    num_of_lights = np.shape(light_positions)[0]
    I = 0
    for i in range(num_of_lights):
        light_position = light_positions[i]
        light_intensity = light_intensities[i]
        L = light_position - P
        L = L/np.linalg.norm(L)

        V = cam_pos - P
        V = V/np.linalg.norm(V)

        R = 2*N*np.dot(N,L) - L
        R = R/np.linalg.norm(R)
        I = I + light_intensity*ks*np.power(np.dot(R,V),n)
    return color + I