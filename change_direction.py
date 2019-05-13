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

# cap = cv2.VideoCapture(0)

# i= 0
# while (True):
#     i = i +1
#     if i > 100:
#         break

#     ret, frame = cap.read()
#     frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
#     people = people  + np.array([1,1])
    

#     direction = change_direction(fish,people)
#     fish = fish + direction 
#     #change_direction(fish, people)

#     cv2.circle(frame,(int(people[0]),int(people[1])),2,(255,0,0))
#     cv2.circle(frame,(int(fish[0]),int(fish[1])),2,(0,0,255))
    
#     print(fish)
#     cv2.imshow('MotionDetected Area Frame', frame)

#     # キー入力を1ms待って、kが27(ESC)だったらBreakする
#     k = cv2.waitKey(1)
#     if k == 27:
#         break
# # キャプチャーをリリースしてウィンドウ全て閉じる
# cap.release()

# cv2.destroyAllWindows()
    


    


