# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
	def __init__(self):
		
		self.lower = {
         'blue':(71,83,200),
         'orange':(20,100,10)
         }

		self.upper = {
		         'blue':(255,100,100),
		         'orange':(30,255,255)

		         }

		# define standard colors for circle around the object
		self.colors = {
		          'blue':(240,100,100),
		          'orange':(0,128,255),
		          }

		# allocate memory for the L*a*b* image, then initialize
		# the color names list
		self.lab = np.zeros((len(self.colors), 1, 3), dtype="uint8")
		self.colorNames = []

		# loop over the colors dictionary
		for (i, (name, rgb)) in enumerate(self.colors.items()):
			# update the L*a*b* array and the color names list
			self.lab[i] = rgb
			self.colorNames.append(name)

		# convert the L*a*b* array from the RGB color space
		# to L*a*b*
		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_BGR2HSV)

	def label(self, image, c):
		# construct a mask for the contour, then compute the
		# average L*a*b* value for the masked region
		# initialize the minimum distance found thus far
		minDist = (np.inf, None)
		for key, value in self.upper.items():
	# find the colors within the specified boundaries and apply
	# the mask
			mask = cv2.inRange(image,self.lower[key],self.upper[key])
			cv2.drawContours(mask, [c], -1, 255, -1)
			mask = cv2.erode(mask, None, iterations=2)
			mean = cv2.mean(image, mask=mask)[:3]
			output = cv2.bitwise_and(image, image, mask = mask)
			
			# loop over the known L*a*b* color values
			for (i, row) in enumerate(self.lab):
				# compute the distance between the current L*a*b*
				# color value and the mean of the image
				d = dist.euclidean(row[0], mean)

				# if the distance is smaller than the current distance,
				# then update the bookkeeping variable
				if d < minDist[0]:
					minDist = (d, i)

		# return the name of the color with the smallest distance
		return self.colorNames[minDist[1]]
