import cv2
import glob
import pyttsx3
def get_files(emotion): 
    files = glob.glob("dataset\\%s\\*" %emotion)
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
#test_img = read_img('files/test_100_2.jpg')
#frame = cv2.imread('files/201.jpg')
cam=test_img1 =cv2.VideoCapture(0)
count=0
while True:
    ret,frame =test_img1.read()
    if count==100:
        break;
    count+=1
        
#test_img = cv2.imread('files/2.jpg')

#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cam.release() 
cv2.destroyAllWindows()
original=cv2.resize(frame, None, fx=0.4, fy=0.4, interpolation = cv2.INTER_AREA)
display('original', original)
(kp1, des1) = orb.detectAndCompute(frame, None)
file=["10","20","50","100","200","500","2000"]
for note in file:
    train=get_files(note)
    for i in train:
        train_img = cv2.imread(i)
        (kp2, des2) = orb.detectAndCompute(train_img, None)
         
        #brute force matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        all_matches = bf.match(des1, des2)
        all_matches = sorted(all_matches , key=lambda x:x.distance)
        res= cv2.drawMatches(frame,kp1,train_img,kp2,all_matches,None)
        good = []
        for m in all_matches:
            if m.distance < 50:
                good.append(m)
        if len(good) > max_val:
            max_val = len(good)
            k=res
            max_pt = note
        
        print(note, len(good))
display('comp',k)
cv2.waitKey(0)
cv2.destroyAllWindows()
engine=pyttsx3.init()
if max_val >= 60:
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