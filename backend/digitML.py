#!/usr/bin/python3

from PIL import Image;
import numpy as np
import os;
from sklearn import svm, metrics
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.utils import shuffle


def loadDataset(path):
    classes = []
    images = []
    for dire in os.listdir(path):
        if not os.path.isdir(os.path.join(path, dire)):
            continue
        if dire == ' ':
            continue #these are 'bad' anyway
        for f in os.listdir(os.path.join(path, dire)):
            i = Image.open(os.path.join(path, dire, f))
            images.append(np.asarray(i, dtype="int32"))
            classes.append(dire)
    return (classes, images)

(classes, images) = loadDataset("chars")

print("Number of samples:", len(images))
images = np.array(images)
classes = np.array(classes)
n = len(images)
ind = images.reshape((n, -1)) #features are 1D arrays
#ind = images

ind, classes = shuffle(ind, classes, random_state=42)

splt = n//4*3 # train-test split


classifier = DecisionTreeClassifier()
classifier.fit(ind[:splt], classes[:splt])

expected = classes[splt:]
predicted = classifier.predict(ind[splt:])
for i, (e, p) in enumerate(list(zip(expected, predicted))):
    print("\t",  e, "&", p, "\\\\")

print("Accuracy:", accuracy_score(expected, predicted))
print("Classification report for classifier %s:\n%s\n"
              % (classifier, metrics.classification_report(expected, predicted)))
#print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
print("Kappa score: ", cohen_kappa_score(expected, predicted))
