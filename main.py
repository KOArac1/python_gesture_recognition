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
