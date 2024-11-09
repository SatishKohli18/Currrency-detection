import cv2
import pyttsx3
def display(window_name, image):
	screen_res = 700, 350	# MacBook Air
	
	scale_width = screen_res[0] / image.shape[1]
	scale_height = screen_res[1] / image.shape[0]
	scale = min(scale_width, scale_height)
	window_width = int(image.shape[1] * scale)
	window_height = int(image.shape[0] * scale)

	# reescale the resolution of the window
	cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
	cv2.resizeWindow(window_name, window_width, window_height)

	# display image
	cv2.imshow(window_name, image)

	# wait for any key to quit the program
	cv2.waitKey(0)
	cv2.destroyAllWindows()
max_val = 0
max_pt = -1
max_kp = 0

orb = cv2.ORB_create()
# orb is an alternative to SIFT

#test_img = read_img('files/test_100_2.jpg')
test_img = cv2.imread('dataset/10/01.jpg')
#cam=test_img1 =cv2.VideoCapture(0)
#test_img = cv2.imread('files/2.jpg')
#ret,frame =test_img1.read()
#cam.release() 
#cv2.destroyAllWindows() 
original=cv2.resize(test_img, None, fx=0.4, fy=0.4, interpolation = cv2.INTER_AREA)
display('original', original)

# keypoints and descriptors
# (kp1, des1) = orb.detectAndCompute(test_img, None)
(kp1, des1) = orb.detectAndCompute(test_img, None)

training_set = ['files/20.jpg', 'files/50.jpg', 'files/100.jpg','files/200.jpg', 'files/500.jpg','files/10.jpg','files/2000.jpg']

for i in range(0, len(training_set)):
	# train image
	train_img = cv2.imread(training_set[i])

	(kp2, des2) = orb.detectAndCompute(train_img, None)

	# brute force matcher
	bf = cv2.BFMatcher()
	all_matches = bf.knnMatch(des1, des2, k=2)

	good = []
	# give an arbitrary number -> 0.789
	# if good -> append to list of good matches
	for (m, n) in all_matches:
		if m.distance < 0.789 * n.distance:
			good.append([m])

	if len(good) > max_val:
		max_val = len(good)
		max_pt = i

	print(i, ' ', training_set[i], ' ', len(good))
engine=pyttsx3.init()
if max_val >= 15:
    print(training_set[max_pt])
    print('good matches ', max_val)
    note = str(training_set[max_pt])[6:-4]
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