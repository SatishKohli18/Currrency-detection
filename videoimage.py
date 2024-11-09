import cv2 
import os 
  
# Read the video from specified path 
cam = test_img1 =cv2.VideoCapture(0)
  
try: 
      
    # creating a folder named data 
    if not os.path.exists('data'): 
        os.makedirs('data') 
  
# if not created then raise error 
except OSError: 
    print ('Error: Creating directory of data') 
currentframe = 0
ret,frame = cam.read() 
  
if ret:
    name = './data/frame' + str(currentframe) + '.jpg'
    print ('Creating...' + name) 
    cv2.imwrite(name, frame) 
# Release all space and windows once done 
