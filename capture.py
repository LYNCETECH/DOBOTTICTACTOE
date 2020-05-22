import cv2 

class MyCapture(object):
    

    def captureImage(self):
        webcam = cv2.VideoCapture(1)
        try:
            check, frame = webcam.read()
            print(check) #prints true as long as the webcam is running
            print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(5)
            
            cv2.imwrite(filename='saved.png', img=frame)
            webcam.release()
            img_new = cv2.imread('saved.png', cv2.IMREAD_GRAYSCALE)
            img_new = cv2.imshow("Captured Image", img_new)
            cv2.waitKey(1650)
            cv2.destroyAllWindows()
            
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            