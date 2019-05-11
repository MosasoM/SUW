import cv2
import numpy as np

import get

color = (0,0,255)

img = np.zeros((512,512,4), np.uint8)
fish = cv2.imread("18438.png",cv2.IMREAD_UNCHANGED)
fish_scale_inv = 4
orgHeight = fish.shape[0]
orgWidth = fish.shape[1]
resized = (orgWidth//fish_scale_inv, orgHeight//fish_scale_inv)
fish = cv2.resize(fish,resized)
mask = fish[:,:,3]
fish_lb = [256,256]
cv2.imshow("test",fish)

flag = False

while(True):
    out = img.copy()
    left = resized[0]
    right = left+fish.shape[0]
    bottom = resized[1]
    top = bottom+fish.shape[1]
    center = (int((left+right)/2.0),int((bottom+top)/2.0))

    roi = img[left:right,bottom:right]

    mask = fish[:,:,3]
    ret, mask_inv = cv2.threshold(mask,50, 255, cv2.THRESH_BINARY_INV)
    img2_fg = cv2.bitwise_and(fish, fish, mask=mask)
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    diff = cv2.add(img1_bg,img2_fg)
    out[left:right,bottom:right] = diff
    cv2.circle(out,center,2,color)
    if flag:    
        cv2.putText(out, 'Get', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow("test", out)
    k = cv2.waitKey(1)

    if k == ord('s'):
        center = (100,130)
        color = (0,0,0)
        print("s")
        get.get(center,fish)
        flag = True


    if k == 27:
        break
cv2.destroyAllWindows()