import cv2
import numpy as np

capture_point =np.array([100,130]) #追い込む場所

def get(x,fish):
    r = np.linalg.norm(x-capture_point)
    print(r)
    if r < 1e-4:
        fish[:,:,3]= 0
        
        print("Success")
    else:
        print("Failed")