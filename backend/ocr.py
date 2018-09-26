#!/usr/bin/python3
import cv2;
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

def correctReceipt(pic):
    img = cv2.imread(pic, cv2.IMREAD_GRAYSCALE);
    (ignore, img_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU);
    #ret = cv2.minAreaRect(cv2.findNonZero(img_bw));
    #testing:
    parts = pic.split(".");
    print("name :\t" + '.'.join(parts[0:-1])+".bw."+parts[-1]);
    cv2.imwrite('.'.join(parts[0:-1])+".bw.png", img_bw);


#harvestLine("test/helloworld.png");
correctReceipt("test-receipts/IMG_20180926_112137.jpg");

