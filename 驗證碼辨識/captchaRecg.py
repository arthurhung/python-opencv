import cv2
import numpy as np
from cv2 import waitKey, matchTemplate, threshold
import os
import matplotlib
import time



tStart = time.time()

im = cv2.imread('test1.jpg', flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)
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
    roi = im[y: y + h, x: x + w]
    thresh = roi.copy() 
    try:

        if w > 8 and h > 8:
            add = True
            for i in range(0, len(arr)):

                if abs(cnts[index][1] - arr[i][0]) <= 3:
                    add = False
                    break
            if add:
                arr.append((x, y, w, h))
    except IndexError:
        pass
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



#waitKey(0)