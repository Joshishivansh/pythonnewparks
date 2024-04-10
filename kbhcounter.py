import cv2
import pickle
import cvzone
import numpy as np
cap = cv2.VideoCapture('171257439764228 (1).mp4')

with open('kbhposn', 'rb') as f:
    posList = pickle.load(f)

width, height = 200,200
def rescaleframe(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)


        if count < 4500:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img_r, pos, (pos[0] + width, pos[1] + height), color, thickness)
        # cvzone.putTextRect(img_r, str(count), (x, y + height - 3), scale=1,
        #                    thickness=2, offset=0, colorR=color)

    # cvzone.putTextRect(img_r, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
    #                        thickness=5, offset=20, colorR=(0,200,0))
while True:
    success, img = cap.read()
    img_r=rescaleframe(img)
    imgGray = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img_r)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    if cv2.waitKey(5) &0xFF==ord("q"):
        break