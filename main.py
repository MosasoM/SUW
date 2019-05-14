import cv2
import others
import detect_move
import numpy as np
import get
import change_direction as cd


print(cv2.__version__)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600) 

ok = False
detected_frame = None
bbox = (0,0,0,0)
center =(0,0)
avg = others.init_avg(cap)
color = (0,0,255)


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
fish_lb = np.random.randint(200,500,2)
flag = False
flag1 = False

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

while (True):
    bboxes = []
    people =[]
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contours,hierarchy = detect_move.detect(gray,avg)
    
    out = move_fish(img,fish,[100,100])
    out = move_fish(img,fish,fish_lb)
    fish_center = fish_lb +np.array([resized[1],resized[0]-30])/2
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= 1500:
            areaframe = frame
            cv2.putText(areaframe, 'motion', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
            x, y, w, h = cv2.boundingRect(cnt)
            bbox = (x, y, w, h)
            bboxes.append(bbox)
            detected_frame = frame.copy()
            center = (int(x + w / 2.0), int(y + h / 2.0))
            people.append([center[1],center[0]])
            out = cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)
            out = cv2.circle(out, center , 4, (0, 0, 255),-1)

    
    #cv2.circle(out,(int(fish_center[1]),int(fish_center[0])),2,color) #魚の位置


    
    if fish_lb[1] > 800-resized[0]-5 :
        direction = np.array([0,-10])
        fish_lb = fish_lb + direction 

    if fish_lb[1] < 10:
        direction = np.array([0,10])
        fish_lb = fish_lb + direction  

    
    if fish_lb[0] > 600-resized[1]-5:
        direction = np.array([-10,0])
        fish_lb = fish_lb + direction 
    
    if fish_lb[0] < 10:
        direction = np.array([10,0])
        fish_lb = fish_lb + direction  

    
    else:
        direction = cd.change_direction_multi(np.array(fish_center), people)
        fish_lb = fish_lb + direction 

    
    if flag:    
        cv2.putText(out, 'GET!!', (0, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, cv2.LINE_AA)
   
    flag1 = get.get(fish_center,fish)

    if flag1:
        color = (255,100,0)
        flag = True

    cv2.imshow('Fish hunt', out)

    # キー入力を1ms待って、kが27(ESC)だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break
# キャプチャーをリリースしてウィンドウ全て閉じる
cap.release()

cv2.destroyAllWindows()