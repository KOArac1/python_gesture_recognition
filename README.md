# 这只是一个普通的项目......
- Draw_On_Screen.py
    - 有BUG......
- main.py
    - 手势识别
- teach.py
    - 临时文件
- try.py
    - 为了修Draw_On_Screen.py的BUG建的文件......

>其实为了这次省赛,这些都是临时学的.

## Draw_On_Screen.py
``` python
import cv2
from cvzone.HandTrackingModule import HandDetector
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.75, maxHands=1)
center = [0, 0]
temp_center = [0, 0]
d_ = False
time = 0
dpt1 = dpt2 = []


def draw(img_):
	for i in range(time):
		img_ = cv2.line(img, (int(dpt1[i][0]), int(dpt1[i][1])), (int(dpt2[i][0]), int(dpt2[i][1])), (0, 0, 255), 2)

	return img_


while True:
	flag, img = cap.read()
	if not flag:
		break

	hands, img = detector.findHands(img)
	if hands:
		hand = hands[0]
		finger = detector.fingersUp(hand)
		lmList = hand["lmList"]
		x1, y1 = lmList[8][0:2]
		x2, y2 = lmList[12][0:2]
		length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
		cv2.putText(img, str(length), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
		xj = math.fabs(x1 - x2) / 2
		yj = math.fabs(y1 - y2) / 2
		temp_center = center
		if x1 > x2:
			center[0] = x2 + xj
		else:
			center[0] = x1 + xj

		if y1 > y2:
			center[1] = y2 + yj
		else:
			center[1] = y1 + yj

		print("Center: ", center)

		if length < 50:
			if not d_:
				d_ = True
				# print("Error!!!")
			else:
				time = time + 1
				cv2.putText(img, "Graffiti in progress!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
				            color=(0, 0, 255), thickness=2)
				print("D1: ", center)
				print("TEMP: ", temp_center)
				dpt1.append(center)
				dpt2.append(temp_center)
				img = draw(img)
				# print(dpt1)
				# print(dpt2)
				# print(time)
			# print(not d_)
		else:
			cv2.putText(img, "No graffiti!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255),
			            thickness=2)
			d_ = False

	cv2.imshow("Draw On Screen!", img)
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
```
>以上代码有蜜汁BUG,可能是python本身的问题.

        这里使用了opencv,mediapipe与cvzone三个包,来判断用户是否想要进行涂鸦,并用cvzone中的HandTrackingModule模块实现捕捉手指的坐标,然后且由列表储存起来.
``` python
if length < 50:
			if not d_:
				d_ = True
				# print("Error!!!")
			else:
				time = time + 1
				cv2.putText(img, "Graffiti in progress!", (50,    100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,color=(0, 0, 255), thickness=2)
				print("D1: ", center)
				print("TEMP: ", temp_center)
				dpt1.append(center)
				dpt2.append(temp_center)
				img = draw(img)
```
### **注:这里的length是食指与中指之间的距离,单位为像素.**
***
``` python
length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
		cv2.putText(img, str(length), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
		xj = math.fabs(x1 - x2) / 2
		yj = math.fabs(y1 - y2) / 2
		temp_center = center
		if x1 > x2:
			center[0] = x2 + xj
		else:
			center[0] = x1 + xj

		if y1 > y2:
			center[1] = y2 + yj
		else:
			center[1] = y1 + yj

		print("Center: ", center)
```
### **这里使用了勾股定理来计算中指与食指之间的中心点**
        xj和yj是两条直角边.
### x1,x2,y1,y2在之前已经定义了,见下:
``` python
x1, y1 = lmList[8][0:2]  
x2, y2 = lmList[12][0:2]
```

        lmList是手上各个关节对应点的坐标,是一个列表.
> **注:手上一共有21个点,8和12分别是食指尖和中指尖.**
***
## **draw函数**
``` python
def draw(img_):
	for i in range(time):
		img_ = cv2.line(img, (int(dpt1[i][0]), int(dpt1[i][1])), (int(dpt2[i][0]), int(dpt2[i][1])), (0, 0, 255), 2)

	return img_
```
        img_获取待处理的图片,time是目前用户有多少帧想要执行"涂鸦"的命令,dpt1和dpt2是每一帧需要涂鸦的起始坐标和结束坐标.
        然后这里使用了cv2包中的line函数进行画线,用众多的线来实现"涂鸦"的效果.

### **其他的,没啥好说的,看代码理解.**
***
***
# main.py
        其实也没啥好说的,和Draw_On_Screen.py差不多.
        Draw_On_Screen.py就是在main.py的基础上改的.
        放代码:
``` python
import cv2
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
lmList1 = lmList2 = []
cTime = time.time()

while True:
	success, img = cap.read()
	if not success:
		break
	img = img[:-1:]
	hands, img = detector.findHands(img, flipType=True)  # With Draw
	# hands = detector.findHands(img, draw=False)  # No Draw
	if hands:
		hand1 = hands[0]
		lmList1 = hand1["lmList"]
		fingers1 = detector.fingersUp(hand1)
		# print("Hand1:", fingers1, " Hand1 lmList:", lmList1[8][0:2], lmList1[12][0:2], end='')
		# print(hands)
	# length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
	else:
		# print("No hands!", end='')
		print("No Hands!")
		# cv2.putText(img, 'No Hands!', (0, 350), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)

	# if len(hands) == 1:
	# 	cv2.putText(img, 'Only One Hand!', (0, 350), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
	#
	# if len(hands) == 2:
	# 	hand2 = hands[1]
	# 	lmList2 = hand2["lmList"]
	# 	fingers2 = detector.fingersUp(hand2)
	# 	print(" , Hand2:", fingers2, " Hand2 lmList:", lmList2[8][0:2], lmList2[12][0:2])
	# 	# length, info, img = detector.findDistance(lmList2[8][0:2], lmList2[12][0:2], img)
	# 	length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img)
	# 	print("length:", length)
	# 	img = cv2.putText(img, str(length), (50, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75, color=(0, 0, 255), thickness=2)
	# 	img = cv2.putText(img, ('First index finger: ' + str(lmList1[8][0:2])), (0, 200), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=0.5, thickness=2)
	# 	img = cv2.putText(img, ('Second index finger: ' + str(lmList2[8][0:2])), (0, 350), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
	# else:
	# 	print()
	pTime = time.time()
	fps = 1 / (pTime - cTime)
	cv2.putText(img, str(fps), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
	cTime = pTime
	cv2.imshow("Image", img)
	# Show Image.
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
```

## 注释掉的东西多是完善以及输出一些参数,除了中间那一段是实现第二只手与第一只手之间画一条线.

## **>剩下两个文件没有用处,请无视< :)**
***
# **接下来是英文版,机翻警告!!!**

#This is just an ordinary project
- Draw_ On_ Screen. py
-There are bugs
- main. py
-Gesture recognition
- teach. py
-Temporary documents
- try. py
-To fix draw_ On_ Screen. Py bug file
>In fact, for this provincial competition, these are temporary learning
## Draw_ On_ Screen. py
``` python
import cv2
from cvzone.HandTrackingModule import HandDetector
import math

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.75, maxHands=1)
center = [0, 0]
temp_center = [0, 0]
d_ = False
time = 0
dpt1 = dpt2 = []


def draw(img_):
	for i in range(time):
		img_ = cv2.line(img, (int(dpt1[i][0]), int(dpt1[i][1])), (int(dpt2[i][0]), int(dpt2[i][1])), (0, 0, 255), 2)

	return img_


while True:
	flag, img = cap.read()
	if not flag:
		break

	hands, img = detector.findHands(img)
	if hands:
		hand = hands[0]
		finger = detector.fingersUp(hand)
		lmList = hand["lmList"]
		x1, y1 = lmList[8][0:2]
		x2, y2 = lmList[12][0:2]
		length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
		cv2.putText(img, str(length), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
		xj = math.fabs(x1 - x2) / 2
		yj = math.fabs(y1 - y2) / 2
		temp_center = center
		if x1 > x2:
			center[0] = x2 + xj
		else:
			center[0] = x1 + xj

		if y1 > y2:
			center[1] = y2 + yj
		else:
			center[1] = y1 + yj

		print("Center: ", center)

		if length < 50:
			if not d_:
				d_ = True
				# print("Error!!!")
			else:
				time = time + 1
				cv2.putText(img, "Graffiti in progress!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
				            color=(0, 0, 255), thickness=2)
				print("D1: ", center)
				print("TEMP: ", temp_center)
				dpt1.append(center)
				dpt2.append(temp_center)
				img = draw(img)
				# print(dpt1)
				# print(dpt2)
				# print(time)
			# print(not d_)
		else:
			cv2.putText(img, "No graffiti!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255),
			            thickness=2)
			d_ = False

	cv2.imshow("Draw On Screen!", img)
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
```
>The above code has honey bug, which may be the problem of Python itself
        Here, opencv, mediapipe and cvzone are used to judge whether users want to graffiti, and the handtrackingmodule in cvzone is used to capture the coordinates of fingers, which are then stored in the list.
``` python
if length < 50:
			if not d_:
				d_ = True
				# print("Error!!!")
			else:
				time = time + 1
				cv2.putText(img, "Graffiti in progress!", (50,    100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,color=(0, 0, 255), thickness=2)
				print("D1: ", center)
				print("TEMP: ", temp_center)
				dpt1.append(center)
				dpt2.append(temp_center)
				img = draw(img)
```
### **Pythagorean theorem is used here to calculate the center point between the middle finger and index finger**
``` python
length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
		cv2.putText(img, str(length), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
		xj = math.fabs(x1 - x2) / 2
		yj = math.fabs(y1 - y2) / 2
		temp_center = center
		if x1 > x2:
			center[0] = x2 + xj
		else:
			center[0] = x1 + xj

		if y1 > y2:
			center[1] = y2 + yj
		else:
			center[1] = y1 + yj

		print("Center: ", center)
```
>XJ and YJ are two right angle sides.
### X1, X2, Y1 and Y2 have been defined before, as shown below:
``` python
x1, y1 = lmList[8][0:2]  
x2, y2 = lmList[12][0:2]
```
        lmList is the coordinates of the corresponding points of each joint on the hand, which is a list
> **Note: there are 21 points on the hand. 8 and 12 are the tips of the index finger and the middle finger respectively**
``` python
def draw(img_):
	for i in range(time):
		img_ = cv2.line(img, (int(dpt1[i][0]), int(dpt1[i][1])), (int(dpt2[i][0]), int(dpt2[i][1])), (0, 0, 255), 2)

	return img_
```
***
        img_ Get the picture to be processed. Time is how many frames the user wants to execute the "graffiti" command. Dpt1 and dpt2 are the start and end coordinates of each frame
        Then the line function in CV2 package is used to draw lines, and many lines are used to achieve the effect of "graffiti"
### **for others, there's nothing to say. It depends on the code understanding**
***
***
# main. py
        Actually, there's nothing to say, and draw_ On_ Screen. Py almost
        Draw_ On_ Screen. Py is in main Based on py
        Look at the code:
``` python
import cv2
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
lmList1 = lmList2 = []
cTime = time.time()

while True:
	success, img = cap.read()
	if not success:
		break
	img = img[:-1:]
	hands, img = detector.findHands(img, flipType=True)  # With Draw
	# hands = detector.findHands(img, draw=False)  # No Draw
	if hands:
		hand1 = hands[0]
		lmList1 = hand1["lmList"]
		fingers1 = detector.fingersUp(hand1)
		# print("Hand1:", fingers1, " Hand1 lmList:", lmList1[8][0:2], lmList1[12][0:2], end='')
		# print(hands)
	# length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)
	else:
		# print("No hands!", end='')
		print("No Hands!")
		# cv2.putText(img, 'No Hands!', (0, 350), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)

	# if len(hands) == 1:
	# 	cv2.putText(img, 'Only One Hand!', (0, 350), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
	#
	# if len(hands) == 2:
	# 	hand2 = hands[1]
	# 	lmList2 = hand2["lmList"]
	# 	fingers2 = detector.fingersUp(hand2)
	# 	print(" , Hand2:", fingers2, " Hand2 lmList:", lmList2[8][0:2], lmList2[12][0:2])
	# 	# length, info, img = detector.findDistance(lmList2[8][0:2], lmList2[12][0:2], img)
	# 	length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img)
	# 	print("length:", length)
	# 	img = cv2.putText(img, str(length), (50, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75, color=(0, 0, 255), thickness=2)
	# 	img = cv2.putText(img, ('First index finger: ' + str(lmList1[8][0:2])), (0, 200), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=0.5, thickness=2)
	# 	img = cv2.putText(img, ('Second index finger: ' + str(lmList2[8][0:2])), (0, 350), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255), thickness=2)
	# else:
	# 	print()
	pTime = time.time()
	fps = 1 / (pTime - cTime)
	cv2.putText(img, str(fps), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
	cTime = pTime
	cv2.imshow("Image", img)
	# Show Image.
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
```
## Most of the things commented out are to improve and output some parameters, except that the middle paragraph is to draw a line between the second hand and the first hand.
## **> the remaining two files are useless, please ignore < :)**
