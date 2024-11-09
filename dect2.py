import cv2
import glob
import pyttsx3
def get_files(emotion): #Define function to get file list, randomly shuffle it and split 80/20
    files = glob.glob("dataset\\%s\\*" %emotion)
    #print(files)
    return files
def display(window_name, image):
	screen_res = 700, 350
	scale_width = screen_res[0] / image.shape[1]
	scale_height = screen_res[1] / image.shape[0]
	scale = min(scale_width, scale_height)
	window_width = int(image.shape[1] * scale)
	window_height = int(image.shape[0] * scale)
	cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
	cv2.resizeWindow(window_name, window_width, window_height)
	cv2.imshow(window_name, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
max_val = 0
max_pt = -1
max_kp = 0

orb = cv2.ORB_create()
# orb is an alternative to SIFT

#test_img = read_img('files/test_100_2.jpg')
#frame = cv2.imread('files/2000.jpg')
cam=test_img1 =cv2.VideoCapture(0)
#test_img = cv2.imread('files/2.jpg')
ret,frame =test_img1.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cam.release() 
cv2.destroyAllWindows() 
original=cv2.resize(frame, None, fx=0.4, fy=0.4, interpolation = cv2.INTER_AREA)
'''image = cv2.imread("files/50.jpg", flags = cv2.IMREAD_GRAYSCALE)
cv2.namedWindow(winname = "original", flags = cv2.WINDOW_NORMAL)
cv2.imshow(winname = "original", mat = image)
cv2.waitKey(delay = 0)
edges = cv2.Canny(image = image, threshold1 = 1,threshold2 = 1)
cv2.namedWindow(winname = "edges", flags = cv2.WINDOW_NORMAL)
cv2.imshow(winname = "edges", mat = edges)
cv2.waitKey(delay = 0)'''
display('original', original)

# keypoints and descriptors
# (kp1, des1) = orb.detectAndCompute(test_img, None)
(kp1, des1) = orb.detectAndCompute(frame, None)
file=["10","20","50","100","200","500","2000"]
for note in file:
    train=get_files(note)
    for i in train:
        train_img = cv2.imread(i)
        train_img=cv2.cvtColor(train_img, cv2.COLOR_BGR2GRAY)
        #original=cv2.resize(train_img, None, fx=0.4, fy=0.4, interpolation = cv2.INTER_AREA)
        #display('hi',original)
        (kp2, des2) = orb.detectAndCompute(train_img, None)
        #brute force matche
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        all_matches = bf.match(des1, des2)
        all_matches = sorted(all_matches , key=lambda x:x.distance)
        res= cv2.drawMatches(frame,kp1,train_img,kp2,all_matches,None)
        good = []
        
    	# give an arbitrary number -> 0.789
    	# if good -> append to list of good matches
        for m in all_matches:
            if m.distance < 50:
                good.append(m)
        if len(good) > max_val:
            max_val = len(good)
            max_pt = note
        
    print(note, len(good))
cv2.imshow('',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
engine=pyttsx3.init()
if max_val >= 50:
    print(note)
    print('good matches ', max_val)
    note = max_pt
    print('\nDetected denomination: Rs. ', note)
    s="It is "+note+" ruppess"
    engine.say(s)
    
    
    engine.setProperty('rate',100)
    engine.setProperty('volume',0.9)
    engine.runAndWait()

else:
    print('No Matches')
    engine.say('No Matches')
    engine.setProperty('rate',100)
    engine.setProperty('volume',0.9)
    engine.runAndWait()