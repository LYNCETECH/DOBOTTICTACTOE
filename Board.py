
import argparse
import imutils
import cv2

class Board(object):
    def __init__(self, board,tabpos):
        self.board=board
        self.tabpos=tabpos