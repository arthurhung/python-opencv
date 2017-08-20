# -*- coding: utf-8 -*-
import cv2
import numpy as np
from cv2 import waitKey, matchTemplate, threshold
import os
import matplotlib
import time



tStart = time.time()

im = cv2.imread('test2.jpg', flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)
retval, im = cv2.threshold(im, 115, 255, cv2.THRESH_BINARY_INV)

for i in xrange(len(im)):
    for j in xrange(len(im[i])):
        if im[i][j] == 255:
            count = 0 
            for k in range(-2, 3):
                for l in range(-2, 3):
                    try:
                        if im[i + k][j + l] == 255:
                            count += 1
                    except IndexError:
                        pass
            if count <= 4:
                im[i][j] = 0

im = cv2.dilate(im, (2, 2), iterations=1)


contours, hierarchy = cv2.findContours(im.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])

arr = []

for index, (c, _) in enumerate(cnts):
    (x, y, w, h) = cv2.boundingRect(c)

    try:
        # 只將寬高大於 8 視為數字留存
        if w > 8 and h > 8:
            add = True
            for i in range(0, len(arr)):
                # 這邊是要防止如 0、9 等，可能會偵測出兩個點，當兩點過於接近需忽略
                if abs(cnts[index][1] - arr[i][0]) <= 3:
                    add = False
                    break
            if add:
                arr.append((x, y, w, h))
    except IndexError:
        pass


for index, (x, y, w, h) in enumerate(arr):
    roi = im[y: y + h, x: x + w]
    thresh = roi.copy() 
    
    angle = 0
    smallest = 999
    row, col = thresh.shape

    for ang in range(-60, 61):
        M = cv2.getRotationMatrix2D((col / 2, row / 2), ang, 1)
        t = cv2.warpAffine(thresh.copy(), M, (col, row))

        r, c = t.shape
        right = 0
        left = 999

        for i in xrange(r):
            for j in xrange(c):
                if t[i][j] == 255 and left > j:
                    left = j
                if t[i][j] == 255 and right < j:
                    right = j

        if abs(right - left) <= smallest:
            smallest = abs(right - left)
            angle = ang

    M = cv2.getRotationMatrix2D((col / 2, row / 2), angle, 1)
    thresh = cv2.warpAffine(thresh, M, (col, row))
    # resize 成相同大小以利後續辨識
    thresh = cv2.resize(thresh, (50, 50))

    cv2.imwrite('tmp/' + str(index) + '.png', thresh)

def mse(im1, im2):
    err = np.sum((im1.astype('float') - im2.astype('float')) ** 2)
    err /= float(im1.shape[0] * im1.shape[0])
    
    return err

arr = []
for tmp_png in [f for f in os.listdir('tmp') if not f.startswith('.')]:
    min_a = 9999999999
    min_png = None
    pic = cv2.imread('tmp/' + tmp_png)
    
    for directory in [f for f in os.listdir('templates') if not f.startswith('.')]:
        for png in [f for f in os.listdir('templates/' + directory) if not f.startswith('.')]:
            ref = cv2.imread('templates/' + directory + '/' + png)
            if mse(ref, pic) < min_a:
                min_a = mse(ref, pic)
                min_png = directory

    arr.append(min_png)

print ''.join(arr)

tEnd = time.time()

print "Running Time : %f sec" % (tEnd - tStart)

# cv2.imshow('image',im)
# cv2.waitKey(0)

#waitKey(0)