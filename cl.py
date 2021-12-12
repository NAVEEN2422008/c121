import cv2
import numpy as np
import time

#to save the output in a file output.avi

fourcc= cv2.VideoWriter_fourcc(*'XVID')
output_file=cv2.VideoWriter('output.avi',fourcc,20.0,(64,48))

#to save the video from wedcamar from our system

cap=cv2.VideoCapture(0)
time.sleep(2)
bg=0

#capthuring background for 60 frames

for i  in range(60):
    ret,bg=cap.read()
    bg=np.flip(bg,axis=1)

#reading the captured frame untell camar open

while (cap.isOpened()) :
    ret,img=cap.read()
    if not ret :
        break
    img=np.flip(img,axis=1)

#conveting the color from bgr to hsv

hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#genreating mask to  decet red  color

low_red=np.array([0,120,50])
upper_red=np.array([10,255,255])
m1=cv2.inRange(hsv,low_red,upper_red)

low_red=np.array([170,120,70])
upper_red=np.array([180,255,255])
m2=cv2.inRange(hsv,low_red,upper_red)
m1=m1+m2

# open and expand thr commend to m1
m1=cv2.morphologyEx(m1,cv2.MORPH_OPEN,np.ones(3,3),np.uint8)
m1=cv2.morphologyEx(m1,cv2.MORPH_DILATE,np.ones(3,3),np.uint8)

#select only part he dos not has m1 and saving in m2 

m2=cv2.bitwise_not(m1)
#keeping only thre part of image with out red color

res1=cv2.bitwise_and(img,img,mask=m2)
res2=cv2.bitwise_and(bg,bg,mask=m1)

#genrateing the output with res1 and rs2

final=cv2.addWeighted(res1,1,res2,1,0)
output_file.write(final)
cv2.imshow("magic",final)
cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()