import cv2
import numpy as np
import random
import math

fish = np.array([40,40])
people =np.array([0,0])

r = 10000

direction = np.array([1,1])
angle = 0

def change_direction(fish,people):
    global angle
    if np.linalg.norm(fish - people) < r:
        new_direction = 10*(fish -people) / (np.linalg.norm(fish - people)+1e-9)
        return new_direction 
        
    else:
        angle = angle + 20*(random.randrange(7) - 3)
        #return np.array([2.0*math.cos(angle * 3.14/180),2.0*math.sin(angle * 3.14 /180)])
        return np.array([0,0])

def change_direction_multi(fish,people):
    global angle
    new_direction = [0,0]
    flag = False
    for p in people:
        d = np.linalg.norm(fish - p)
        if d < r:
            new_direction += 1.5*(fish -p) / (np.linalg.norm(fish - p)+1e-9)
            flag = True

    if flag:
        #new_direction = new_direction / (np.linalg.norm(fish - p)+1e-9)
        return new_direction
    else:
        angle = angle + 20 * (random.randrange(7) - 3)
        return np.array([2.0 * math.cos(angle * 3.14 / 180), 2.0 * math.sin(angle * 3.14 / 180)])
        #return np.array([0,0])


    


    


