import cv2
import numpy as np

capture_point_1 =np.array([0,0])
capture_point_2 =np.array([0,600])
capture_point_3 =np.array([800,0])
capture_point_4 =np.array([800,600])


def get(x,fish):
    bod1 = [abs(x[0]),abs(600-x[0])]
    bod2 = [abs(x[1]),abs(800-x[1])]
    m1 = min(bod1)
    m2 = min(bod2)

    if m1 < 70 and m2< 160:
        fish[:,:,3]= 0
        print("Success")
        return True
    # r1 = np.linalg.norm(x-capture_point_1)
    # r2 = np.linalg.norm(x-capture_point_2)
    # r3 = np.linalg.norm(x-capture_point_3)
    # r4 = np.linalg.norm(x-capture_point_4)
    # R = 90
    # if r1 < :
    #     fish[:,:,3]= 0
    #     print("Success")
    #     return True
    # if r2 < 100:
    #     fish[:,:,3]= 0
    #     return True
    # if r3 < 100:
    #     fish[:,:,3]= 0
    #     return True
    # if r4 < 100:
    #     fish[:,:,3]= 0
    #     return True
    # else:
    #     print("Failed")
    #     return False