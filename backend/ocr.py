#!/usr/bin/python3
import cv2;
import numpy as np;
import pytesseract;

def harvestLine(pic):
    img = cv2.imread(pic, cv2.IMREAD_GRAYSCALE);
    (ignore, img_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU);
    line = pytesseract.image_to_string(img_bw);
    # testing purposes:
    print(line);
    parts = pic.split(".");
    cv2.imwrite('.'.join(parts[0:-1])+".bw."+parts[-1], img_bw);
    return line;

# many thanks to S.O. 34981144
def correctReceipt(pic):
    img = cv2.imread(pic)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    # Threshold it better:
    (thresh, _) = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    del img_gray
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_bw = cv2.inRange(img_hsv, (0, 0, 145), (255, max(255-thresh*1.3, 40), 255));
    print("Threshval: %d"%thresh);
    del img_hsv



    parts = pic.split(".");
    #img_bw = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #        cv2.THRESH_BINARY_INV, 5, 0);
    #(threshval, img_bw) = cv2.threshold(img,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    # default OTSU thresholding is a liiiiitttle to agressive on receipts.
    #(threshval2, img_bw) = cv2.threshold(img,threshval*1.1,255,cv2.THRESH_BINARY)
    

    # remove lone pixels
#    kernel = np.array((
#        [0, 1, 0],
#        [1, -1, 1],
#        [0, 1, 0],
#        ), dtype="int");
    
    kernel_tuple = [];
    r = 64
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
#    kernel = np.array((
#        [-1, -1, -1, -1],
#        [-1,  0,  0, -1],
#        [-1,  0,  0, -1],
#        [-1, -1, -1, -1],
#        ), dtype="int");
#    kernel = np.array((
#        [1, 1, 1],
#        [1,-1, 1],
#        [1, 1, 1],
#        ), dtype="int");
    strays = cv2.morphologyEx(img_bw, cv2.MORPH_HITMISS, kernel); 
    #cv2.imshow("strays", strays);
    #cv2.waitKey();
    #cv2.imshow("orig", img_bw);
    #cv2.waitKey();
    img_bw = cv2.subtract(img_bw, strays);
    #cv2.imshow("result", img_bw);
    #cv2.waitKey();

    #cv2.imwrite('.'.join(parts[0:-1])+".aabefore.png", img_bw);
    #cv2.imwrite('.'.join(parts[0:-1])+".aafter.png", img_bw);
    ((cx, cy), (w, h), ang) = cv2.minAreaRect(cv2.findNonZero(img_bw));
    if(w > h):
        w, h = h, w
        ang += 90
    mat = cv2.getRotationMatrix2D((cx, cy), ang, 1)
    aligned = cv2.warpAffine(img_bw, mat, (img.shape[0], img.shape[1]))

    edges = cv2.Canny(aligned, 75, 100);

    #testing:
    print("name :\t" + '.'.join(parts[0:-1])+".edges."+parts[-1]);
    cv2.imwrite('.'.join(parts[0:-1])+".edges.png", edges);
    print("name :\t" + '.'.join(parts[0:-1])+".bw."+parts[-1]);
    cv2.imwrite('.'.join(parts[0:-1])+".bw.png", img_bw);
    print("name :\t" + '.'.join(parts[0:-1])+".aligned."+parts[-1]);
    cv2.imwrite('.'.join(parts[0:-1])+".aligned.png", aligned);


print("OpenCV2 version: %s"%cv2.__version__);
#harvestLine("test/helloworld.png");
correctReceipt("test-receipts/IMG_20180926_111127.jpg");
correctReceipt("test-receipts/IMG_20180926_112137.jpg");
correctReceipt("test-receipts/IMG_20181023_200121.jpg");

