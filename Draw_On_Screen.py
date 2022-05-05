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
				# dpt1.append(center)
				# dpt2.append(temp_center)
				# img = draw(img)
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
