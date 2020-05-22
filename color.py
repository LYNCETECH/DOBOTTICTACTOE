# USAGE
# python detect_color.py --image example_shapes.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import argparse
import imutils
import cv2
from capture import MyCapture
# construct the argument parse and parse the arguments

gamestate =["?"]*9
ca=MyCapture()
        
class ImageRecognition(object):

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#help="path to the input image")
#args = vars(ap.parse_args())
    

    def filter_min_area(contours,min_area):
        return list(filter(lambda cnt:cv2.contourArea(cnt)>=min_area,contours))

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better

    def recongnition(self):
        	ca.captureImage()
        	image = cv2.imread("saved.png")
        	resized = imutils.resize(image, width=300)
        	ratio = image.shape[0] / float(resized.shape[0])
        	img_width = resized.shape[0]
        	img_height = resized.shape[1]
        	# blur the resized image slightly, then convert it to both
        	# grayscale and the L*a*b* color spaces
        	blurred = cv2.GaussianBlur(resized, (5, 5), 0)
        	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        	hue,sat,val = cv2.split(gray)
        	lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        	thresh = cv2.threshold(val,0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        	#cv2.imshow("Thresh", thresh)
        
        	# find contours in the thresholded image
        	cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
        		cv2.CHAIN_APPROX_SIMPLE)
        	cnts = imutils.grab_contours(cnts)
        
        	# initialize the shape detector and color labeler
        	sd = ShapeDetector()
        	cl = ColorLabeler()
        
        	#n_ctns=filter_min_area(cnts,150)
        	# loop over the contours
        	i=0
        	for c in cnts:
        		# compute the center of the contour
        		M = cv2.moments(c)
        		cX = int((M["m10"] / M["m00"]) * ratio)
        		cY = int((M["m01"] / M["m00"]) * ratio)
        
        		x,y,w,h = cv2.boundingRect(c)
        		tileX = round((cX/img_width)*3)-1
        		tileY = round((cY/img_height)*3)-1
        		#tileX=2 if tileX>=3 else tileX
        		#tileY=2 if tileY>=3 else tileY
        		
        		
        		# detect the shape of the contour and label the color
        		shape = sd.detect(c)
        		color = cl.label(lab, c)
        		
        		
        		if color=="blue":
        			 i=i+1
        			 print("blue:"+str(i))
        			 print("x:"+str(tileX))
        			 print("y:"+str(tileY))
        			 gamestate[tileX][tileY] = "O"
        		if color=="orange":
        			gamestate[tileX][tileY] = "X"
        		if color!="orange" and color!="blue":
        			color=" "
        		
        		
        		# multiply the contour (x, y)-coordinates by the resize ratio,
        		# then draw the contours and the name of the shape and labeled
        		# color on the image
        		c = c.astype("float")
        		c *= ratio
        		c = c.astype("int")
        		text = "{},{}".format(cX,cY)
        		cv2.drawContours(image, [c], -1, (0, 255, 0), 3)
        		
        		cv2.putText(image, text, (cX, cY),
        			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        	#print the gamestate
        	print("Gamestate:")
        	for line in gamestate:
        	        linetxt = ""
        	        for cel in line:
        	                linetxt = linetxt + "|" + cel
        	        print(linetxt)
        	# show the output image
        	#cv2.imshow("Image", image)

        	return gamestate;