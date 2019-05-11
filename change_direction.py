import cv2
import numpy as np

fish =np.array([0,0])
people =np.array([40,40])
np.linalg.norm(fish - people) 

r = 20

direction = np.array([1,1])

def change_direction(fish,people):
    if np.linalg.norm(fish - people) < r:
        new_direction = (fish -people) / np.linalg.norm(fish - people)
        return new_direction 
    else:
        return np.array([1,1]) 

i= 0
while (True):
    i = i +1
    if i > 40:
        break
    direction = change_direction(fish,people)
    fish = fish + direction 
    change_direction(fish, people)
    
    print(fish)
    


    


