# ParkingSpacePicker.py
# Description: Used to generate the rectangles onto a single frame of the video (aka snapshot)
#              that will be tested for parking spot availability.
#              This will be done manually since the camera bird eye view does slightly wiggle from
#              left to right.


# Import cv2 and pickle libraries
import cv2
import pickle

# Trial and error to determine the correct width and height of each space
width, height = 107, 48

# try/except for pickle file in order to edit rectangle locations without losing its position once the
# image is closed
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


# Function: mouseClick
# Description: Action item for when the mouse is clicked
def mouseClick(events, x, y, flags, params):
    # add rectangle when left button clicked
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        # remove rectangle when right button clicked and is within an existing rectangle
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    # dump (add) into pickle file
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


# beginning image stream
while True:
    # reading image
    img = cv2.imread('carParkImg.png')
    # adding rectangles
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), thickness=2)
    # displaying image
    cv2.imshow('image', img)
    # calling mouse click function for every click
    cv2.setMouseCallback('image', mouseClick)
    # wait key for image
    cv2.waitKey(1)
