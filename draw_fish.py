import cv2
import numpy as np
import get
import change_direction as cd

color = (0,0,255)
r = 20
people =np.array([0,0])


img = cv2.imread("sea.jpg",cv2.IMREAD_UNCHANGED)
zero = np.zeros((img.shape[0],img.shape[1]),img.dtype)
img = cv2.merge((img,zero))
fish = cv2.imread("18438.png",cv2.IMREAD_UNCHANGED)
fish_scale_inv = 4
orgHeight = fish.shape[0]
orgWidth = fish.shape[1]
resized = (orgWidth//fish_scale_inv, orgHeight//fish_scale_inv)
fish = cv2.resize(fish,resized)
mask = fish[:,:,3]
fish_lb = [100,100]
flag = False
flag1 = False

i=0

def move_fish(img,fish,fish_lb):
    out = img.copy()
    left = int(fish_lb[0])
    right = left + fish.shape[0]
    bottom = int(fish_lb[1])
    top = bottom + fish.shape[1]

    roi = img[left:right, bottom:top]

    mask = fish[:, :, 3]
    ret, mask_inv = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY_INV)
    img2_fg = cv2.bitwise_and(fish, fish, mask=mask)
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    diff = cv2.add(img1_bg, img2_fg)
    out[left:right, bottom:top] = diff
    return out

while(True):
    # out = img.copy()
    # left = int(fish_lb[0])
    # right = left+fish.shape[0]
    # bottom = int(fish_lb[1])
    # top = bottom+fish.shape[1]
    # center = (int((left+right)/2.0),int((bottom+top)/2.0))
    #
    # roi = img[left:right,bottom:top]
    #
    # mask = fish[:,:,3]
    # ret, mask_inv = cv2.threshold(mask,50, 255, cv2.THRESH_BINARY_INV)
    # img2_fg = cv2.bitwise_and(fish, fish, mask=mask)
    # img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    # diff = cv2.add(img1_bg,img2_fg)
    # out[left:right,bottom:top] = diff
    out = move_fish(img,fish,fish_lb)
    #cv2.circle(out,center,2,color)
    cv2.circle(out,(int(fish_lb[1]),int(fish_lb[0])),2,color) #魚の位置

    i = i +1
    if i > 300:
        break
    print(np.linalg.norm(np.array(fish_lb) - np.array(people)))

    people = people  + np.array([1,1])
    cv2.circle(out,(int(people[0]),int(people[1])),2,color) #人の位置

    direction = cd.change_direction(np.array(fish_lb), np.array(people))
    fish_lb = fish_lb + direction 
    cd.change_direction(np.array(fish_lb), np.array(people))
    print(fish_lb)

    
    
    if flag:    
        cv2.putText(out, 'GET!!', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow("test", out)

    flag1 = get.get(fish_lb,fish)

    k = cv2.waitKey(1)

    if flag1:
        color = (255,100,0)
        flag = True


    if k == 27:
        break
cv2.destroyAllWindows()