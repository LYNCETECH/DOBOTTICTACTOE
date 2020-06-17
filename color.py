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



ca=MyCapture()

tabpos = []

class Point:
    def __init__(self, x, y,posx,posy):
        self.x = x
        self.y = y
        self.posx_plateau=posx
        self.posy_plateau=posy
        self.couleur=" "
        
        
        
class ImageRecognition(object):

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#help="path to the input image")
#args = vars(ap.parse_args())
    def __init__(self):
        self.tabcords=[]

    def shoot(self):
        ca.captureImage()
        return True

    def ajouterPoint(self,point):
        self.tabcords.append(point)

    def remplirTableauPiecesDetectees(self,cX,cY,couleur):

        col=-1
        row=-1

        if cX>50 :
            if cX < 307 :
                row=2
            elif cX < 466 :
                row=1
            else:
                row=0

            if cY < 187 :
                col=0
            elif cY < 337 :
                col =1
            else :
                col=2

        p = Point(cX,cY,row,col)
        p.couleur=couleur
        self.ajouterPoint(p)
    

    def filter_min_area(self,contours,min_area):
        return list(filter(lambda cnt:cv2.contourArea(cnt)>=min_area,contours))

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better

    def recongnition(self):
        board =["-"]*9
        gamestate=[["-","-","-"],["-","-","-"],["-","-","-"]]
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
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts=self.filter_min_area(cnts,50)
    # initialize the shape detector and color labeler
        sd = ShapeDetector()
        cl = ColorLabeler()
        
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

            #Remplissage du tableau des pièces détectées
            self.remplirTableauPiecesDetectees(cX,cY,color)  
            
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
        for index,point in enumerate(self.tabcords):
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
                        board[counter]=cel
                        counter=counter+1
                print(linetxt)
        # show the output image
        cv2.imwrite("output.png", image)
        counter=0
       
        return board