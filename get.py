import cv2
import numpy as np

capture_point =np.array([189,189]) #追い込む場所

def get(x,fish):
    r = np.linalg.norm(x-capture_point)
    print(r)
    if r < 1:
        fish[:,:,3]= 0
        print("Success")
        return True
    else:
        print("Failed")
        return False