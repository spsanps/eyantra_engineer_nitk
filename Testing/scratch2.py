## Color Tracking v1.0
## Copyright (c) 2013-2014 Abid K and Jay Edry
## You may use, redistribute and/or modify this program it under the terms of the MIT license (https://github.com/abidrahmank/MyRoughWork/blob/master/license.txt).


''' v 0.1 - It tracks two objects of blue and yellow color each '''

from time import time

import cv2
import numpy as np


def getthresholdedimg(hsv):
    yellow = cv2.inRange(hsv, np.array((19, 137, 123)), np.array((30, 255, 255)))
    # blue = cv2.inRange(hsv,np.array((100,100,100)),np.array((120,255,255)))
    # both = cv2.add(yellow,blue)
    return yellow


c = cv2.VideoCapture(0)
width, height = c.get(3), c.get(4)
print "frame width and height : ", width, height

t = 0
i = 0

while (1):
    i += 1
    _, f = c.read()
    t1 = time()
    f = cv2.flip(f, 1)
    blur = cv2.medianBlur(f, 5)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    both = getthresholdedimg(hsv)
    erode = cv2.erode(both, None, iterations=3)
    dilate = cv2.dilate(erode, None, iterations=10)

    image, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w / 2, y + h / 2

        if 20 < hsv.item(cy, cx, 0) < 30:
            cv2.rectangle(f, (x, y), (x + w, y + h), [0, 255, 255], 2)
            print "yellow :", x, y, w, h
        elif 100 < hsv.item(cy, cx, 0) < 120:
            cv2.rectangle(f, (x, y), (x + w, y + h), [255, 0, 0], 2)
            print "blue :", x, y, w, h

    cv2.imshow('img', f)

    if cv2.waitKey(25) == 27:
        break

    t2 = time()

    t += t2 - t1

print t / i

cv2.destroyAllWindows()
c.release()
