# main.py
# Description: Inputs the video of a parking lot and calculates if a parking spot is available or not
#              depending on the pixels within each rectangle. This also includes am available spot tracker.

# import libraries used
import cv2
import pickle
import cvzone
import numpy as np

# Video Feed
cap = cv2.VideoCapture('carPark.mp4')

# loading pickle file previously generated that has the rectangle displayed
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

# assigning heigth and width of these rectangles that box out a parking space
width, height = 107, 48


# Function: checkParkingSpace
# Description: Keeps track of available spaces. crops each space individually, counts non zeros of pixels, and
#              adds a text of the sum of the pixels within the rectangle per frame. Finally, adjusts the rectangle
#              to mimic availability. Green = available, and Red = unavailable
def checkParkingSpace(imgPro):
    space_counter = 0
    for pos in posList:
        x, y = pos
        # cropping img
        img_crop = imgPro[y:y + height, x:x + width]
        # counts nonzero pixels within the cropped image
        count = cv2.countNonZero(img_crop)
        # displays pixel count
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=(0, 0, 255))

        # if pixel count is less than 950 then adjust color to green
        if count < 950:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        # else keep it red
        else:
            color = (0, 0, 255)
            thickness = 2
        # draw rectangle around parking spot with adjusted themes
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    # total available spots counter
    cvzone.putTextRect(img, f'Available: {space_counter} / {len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))


# loop video feed
while True:
    # resets the video upon reaching the end
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # reading video stream collecting the frame
    success, img = cap.read()
    # grayscale the video
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur the video
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # Adding an adaptive threshold to make the video binary
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    # adding median blue to threshold in order to remove excessive noise.
    imgMedianBlur = cv2.medianBlur(imgThreshold, 5)
    # implementing kernel size with a numpy array to use as the kernel size for dilation
    kernel = np.ones((3, 3), np.uint8)
    # dilating the median blur to fill in the blanks created by the image processing above
    imgDilate = cv2.dilate(imgMedianBlur, kernel, iterations=1)

    # calling checkParkingspace function
    checkParkingSpace(imgDilate)

    # display video
    cv2.imshow('Image', img)

    # displaying video with a 10 frame per min speed
    cv2.waitKey(10)
