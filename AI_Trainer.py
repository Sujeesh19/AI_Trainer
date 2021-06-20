import cv2
import numpy as np
import time
import poseModule as pm

cap = cv2.VideoCapture(0)

detector = pm.PoseDetector()
count = 0
dir = 0
bar = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread('bicep6.jpg')
    img = detector.findPose(img, False)
    lm = detector.findPosition(img, False)
    if len(lm) != 0:
        # right arm
        angle = detector.findAngle(img, 12, 14, 16)
        # left arm
        # detector.findAngle(img, 11, 13, 15)

        per = np.interp(angle, (60, 160), (0, 100))
        bar = np.interp(angle, (60, 160), (650, 100))
        # print(per, angle)

        # check for the dumbbell curl result
        color = (255, 0, 0)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1

        if per == 0:
            color = (0, 0, 255)
            if dir == 1:
                count += 0.5
                dir = 0

        # print(count)

        # draw bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (1160, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # showing curl count

        # cv2.rectangle(img, (0, 0), (300, 200), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, f'Angle Detection: ', (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 4)
        # cv2.putText(img, f'{str(int(angle))}', (10, 150), cv2.FONT_HERSHEY_PLAIN, 7, (255, 255, 255), 12)
        cv2.rectangle(img, (0, 450), (250, 720), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f'Counting Curls', (5, 490), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 4)
        cv2.putText(img, f'{str(int(count))}', (50, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 255, 255), 20)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
