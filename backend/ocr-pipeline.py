#!/usr/bin/python3
import cv2;
import numpy as np;
import pytesseract;
from math import sin;
from math import cos;
from math import sqrt;

# many thanks to S.O. 34981144
def correctReceipt(pic):
    parts = pic.split(".");

    img = cv2.imread(pic)
    # Fix bad-horizontal images
    if img.shape[0] < img.shape[1]:
        print("Fixing rotation")
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    # Threshold it better:
    (thresh, _) = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    del img_gray
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_bw = cv2.inRange(img_hsv, (0, 0, 145), (255, max(255-thresh*1.3, 50), 255));
    print("Threshval: %d"%thresh);
    del img_hsv



    for r in (8, 16, 32, 64):
        kernel_tuple = [];
        for i in range(1, r):
            t = []
            for j in range(1, r):
                if (j < r/4 or j > r/4*3) or (i < r/4 or i > r/4*3):
                    t.append(-1);
                else:
                    t.append(0);
            kernel_tuple.append(t);
        kernel_tuple = tuple(kernel_tuple);
        kernel = np.array(kernel_tuple, dtype="int");
        strays = cv2.morphologyEx(img_bw, cv2.MORPH_HITMISS, kernel); 
        img_bw = cv2.subtract(img_bw, strays);

    contimg, contours, hierarchy = cv2.findContours(img_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, contours, -1, (255,0,0), 3);
    c = max(contours, key = cv2.contourArea)
    rect = ((cx, cy), (w, h), ang) = cv2.minAreaRect(c)
    # Many thanks to S.O 41138000
    print ("unsimplified contour has",len(c),"points")
    epsilon = 0.1*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    print ("simplified contour has",len(approx),"points")
    # End S.O. 41138000
    visrect = cv2.boxPoints(rect)
    visrect = np.int0(visrect)

    # Build perspective matrix
    width, height = img.shape[:2]
    pts = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    #Sorry for this line but woooo thanks S.O. 952914
    approxpts = [item for sublist in approx for item in sublist]
    # Order them correctly:
    def ptmag(pt):
        return sqrt(pt[0]**2 + pt[1]**2)
    approxmags = list(map(ptmag, approxpts))
    def ptratio(pt):
        return pt[0]/pt[1]
    approxratios = list(map(ptratio, approxpts))
    far = approxpts[approxmags.index(max(approxmags))]
    near = approxpts[approxmags.index(min(approxmags))]
    xmid = approxpts[approxratios.index(max(approxratios))]
    ymid = approxpts[approxratios.index(min(approxratios))]
    approxpts = [near, xmid, ymid, far]
    approxpts = np.float32(approxpts)
    print(approxpts);
    mat = cv2.getPerspectiveTransform(approxpts, pts)
    aligned = cv2.warpPerspective(img, mat, (width, height))


    # Finally with fixed image, go rethreshold
    img_gray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY);
    img_bw = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                        cv2.THRESH_BINARY,11,5)
    del img_gray

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    img_bw = cv2.dilate(img_bw, kernel, iterations=1, borderType=cv2.BORDER_REPLICATE);
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9))
    img_bw = cv2.erode(img_bw, kernel, iterations=1, borderType=cv2.BORDER_REPLICATE);

    #Magic courtesy of S.O. 34981144
    hist = cv2.reduce(img_bw, 1, cv2.REDUCE_AVG).reshape(-1)
    hist = cv2.GaussianBlur(hist,(5,5),0)
    #find mean of hist:
    H,W = img_bw.shape[:2]
    def updateBounds(ratio):
        upd = aligned.copy();
        thresh = 0
        for val in hist:
            thresh = thresh + val[0]
        thresh = thresh//H
        thresh = thresh * 1000 // (ratio)  
        print(thresh)
        uppers = [y for y in range(H-1) if hist[y]<=thresh and hist[y+1]>thresh]
        lowers = [y for y in range(H-1) if hist[y]>thresh and hist[y+1]<=thresh]

        for y in uppers:
            cv2.line(upd, (0,y), (W, y), (255,0,0), 1)

        for y in lowers:
            cv2.line(upd, (0,y), (W, y), (0,255,0), 1)
        return (uppers, lowers)

    (uppers, lowers) = updateBounds(955)
    #End magic

    print(uppers)
    print(lowers)
    lines = []
    def processLine(i):
        subimg = img_bw[uppers[i]:lowers[i+1], 0:W]
        line = pytesseract.image_to_string(subimg)
        print(line)
        return line
    for i, _ in enumerate(lowers[:-1]):
        lines.append(processLine(i))

    return lines


print("OpenCV2 version: %s"%cv2.__version__)

