import matplotlib
matplotlib.use('TkAgg')

from transform import four_point_transform
import imutils
from skimage.filters import threshold_adaptive
import numpy as np
import argparse
import cv2

ratioRate = 500.0

def increaseContrast(image):
	"""Increase Contrast Of The Image"""
	lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(lab)

	clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
	cl = clahe.apply(l)

	limg = cv2.merge((cl,a,b))

	image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
	return image


def refineEdge(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 75, 200)
	return edged


def getContour(image):
	(_, cnts, _) = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	 
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		if len(approx) == 4:
			screenCnt = approx
			return screenCnt


def transformImage(image, contour,  mode, ratio):
	warped = four_point_transform(image, contour.reshape(4, 2) * ratio)

	if mode == 0 :
		return warped

	elif mode == 1 :
		warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
		return warped

	elif mode == 2 :
		warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
		warped = threshold_adaptive(warped, 251, offset = 10)
		warped = warped.astype("uint8") * 255
		return warped


def scanImage(path, mode):
	"""Read Image from path and display transformed Image"""

	#Read Image
	image = cv2.imread(path)
	ratio = image.shape[0] / ratioRate
	orig = image.copy()
	image = imutils.resize(image, height = 500)

	cv2.imshow("Original", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	image = increaseContrast(image)

	cv2.imshow("Contrast", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	edged = refineEdge(image)

	cv2.imshow("Edge", edged)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	screenCnt = getContour(edged)
	cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

	cv2.imshow("Contour", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	result = transformImage(orig, screenCnt, mode, ratio)

	cv2.imshow("Result", result)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
