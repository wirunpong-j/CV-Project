import cv2
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np



def main():
	image = cv2.imread("test.jpg")
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	f, ax = plt.subplots()
	f.canvas.set_window_title("image naja")
	ax.imshow(image, interpolation = 'none')
	plt.show()

main()
