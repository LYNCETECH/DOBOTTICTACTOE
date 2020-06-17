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



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())
gamestate = [["-","-","-"],["-","-","-"],["-","-","-"]]
tabcords = []
board =["-"]*9
class Point:
    def __init__(self, x, y,posx,posy):
        self.x = x
        self.y = y
        self.posx_plateau=posx
        self.posy_plateau=posy
        self.couleur=" "

def filter_min_area(contours,min_area):
	return list(filter(lambda cnt:cv2.contourArea(cnt)>=min_area,contours))

def ajouterPoint(point):
    tabcords.append(point)

def remplirTableauPiecesDetectees(contours,ratio):
	for index,c in enumerate(contours):
		M = cv2.moments(c)
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
		col=-1
		row=-1
		if cX < 170 :
			row=0
		elif cX < 334 :
			row=1
		else:
			row=2

		if cY < 187 :
			col=2
		elif cY < 337 :
			col	=1
		else :
			col=0

		p = Point(cX,cY,row,col)

		ajouterPoint(p)
		
# Charge l'image et diminue la taille en taille plus petite pour que les formes
#soit mieux représentées

image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
img_width = resized.shape[0]
img_height = resized.shape[1]
#flouter légèrement l'image redimensionnée, puis la convertir en deux
# niveaux de gris et les espaces colorimétriques L * a * b *
blurred = cv2.GaussianBlur(resized, (5,5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
hue,sat,val = cv2.split(gray)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
thresh = cv2.threshold(val,0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
cv2.imshow("Thresh", thresh)

#Trouver des contours dans l'image seuil
cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

cnts=filter_min_area(cnts,100)
# Initialiser le détecteur de forme et de couleurs
sd = ShapeDetector()
cl = ColorLabeler()

#Remplissage du tableau des pièces détectées
remplirTableauPiecesDetectees(cnts,ratio)
#n_ctns=filter_min_area(cnts,150)
# Parcours les contours
i=0
counter=0
print("w:"+str(img_width))
print("h:"+str(img_height))
for index, c in enumerate(cnts):
	
	M = cv2.moments(c)
	#position de chaque contour dans l'image
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)		

	
	# detection des formes et couleur
	shape = sd.detect(c)
	color = cl.label(lab, c)
	
	#attribue à chaque point sa couleur
	tabcords[index].couleur=color
	
	# multiplier les coordonnées de contour (x, y) par le rapport de redimensionnement,
	# puis dessinez les contours et le nom de la forme et étiquetés
	# couleur sur l'image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	text = "{},{},{},i=>{}".format(cX,cY,color,index)
	cv2.drawContours(image, [c], -1, (0, 255, 0), 3)
	cv2.putText(image, text, (cX, cY),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#remplissage du plateau par les points
for index,point in enumerate(tabcords):
	if point.couleur=="blue":
		print("=====blue=====")
		print("xb:"+str(point.posx_plateau)+" xb:"+str(point.x))
		print("yb:"+str(point.posy_plateau)+" yb:"+str(point.y))
		gamestate[point.posx_plateau][point.posy_plateau] = "O"

	if point.couleur=="orange":
		print("=====orange=====")
		print("xo:"+str(point.posx_plateau)+" xo:"+str(point.x))
		print("yo:"+str(point.posy_plateau)+" yo:"+str(point.y))
		gamestate[point.posx_plateau][point.posy_plateau] = "X"
		
counter=0
#affichage de l'état du plateau
print("Gamestate:")
for line in gamestate:
        linetxt = ""
        for cel in line:
                linetxt = linetxt + "|" + cel
                #print('cel:'+str(cel))
                board[counter]=cel
                counter=counter+1
        print(linetxt)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)