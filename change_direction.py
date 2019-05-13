import cv2
import numpy as np

fish = np.array([40,40])
people =np.array([0,0])

r = 20

direction = np.array([1,1])

def change_direction(fish,people):
    if np.linalg.norm(fish - people) < r:
        new_direction = 3*(fish -people) / (np.linalg.norm(fish - people)+1e-9)
        return new_direction 
    else:
        return np.array([0,0]) 

    


    


