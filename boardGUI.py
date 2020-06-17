# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'board.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import imutils
import sys
import pdb
import random
from datetime import datetime
from time import sleep

from random import randint
from color import ImageRecognition
from Board import Board
from scipy.spatial import distance as dist
from PIL import Image, ImageDraw,ImageFont
import numpy

PLAYERS = ["X","O"]



class Ui_board(object):
    
    def __init__(self,diff, level,_dobot):
        #self._dm = dobot_manager
        self.gameboard = ['-']*9
        self.currentbuffer = 0
        self.moves = []
        self.diff = diff
        self.turn=False
        self.checked=False
        self.currentPos=-1
        self.active=[0]*9
        self.score_ia = 0
        self.score_player=0
        self.end=False
        self.level=level
        self.dfcolor="color: #333;\n"
        "    border: 2px solid #555;\n"
        "    border-radius: 50px;\n"
        "    border-style: outset;\n"
        "    background: qradialgradient(\n"
        "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
        "        );\n"
        "    padding: 5px;"
        self._winning_combinations = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])
        self.player="O"
        self.enemy = "X"
        self.currentplayer = "O"
     
        
        self.dobot = _dobot
        self.dobot.connectDobot()
        self.dobot.initDobot()
        
    
    #Vérifie si le plateau est vide
    #Pas de parametre d'entrée
    def _is_board_empty(self):
        unique = list(set(self._gameboard.status()))
        if (len(unique) == 1) and unique[0] == "-":
            return True
        return False
        
    #Vérifie si le jeu est terminé sans vainqueur
    def _is_game_won(self):
        for player in PLAYERS:
            for combos in self._winning_combinations:
                if (self.gameboard[combos[0]] == player and self.gameboard[combos[1]] == player and self.gameboard[combos[2]] == player):
                    return player
                
        if "-" not in self.gameboard:
            return "tie"
        return None
    #Vérifie le joueur a gagné ou pas
    def _is_game_won_player(self, player, board):
        for combos in self._winning_combinations:
            if (board[combos[0]] == player and board[combos[1]] == player and board[combos[2]] == player):
                return True

        return False
        
    #retourne les positions non occupée par les joueurs
    def _get_all_free_pos(self, board):
        free = [i for i, pos in enumerate(board) if pos == "-"]
        return free
        
    #Vérifie si le mouvement est valide (position correcte)
    def _is_move_valid(self, move):
        pos = -1
        try:
            pos = int(move)
        except:
            return None
        if self.gameboard[pos] == "-":
            return pos
        return None
    
    #Mise à jour du plateau par les donnés du joueur
    def _update_board(self, pos, player):
        self.gameboard[pos] = player
        #self._gameboard.positions[pos].draw_symbol_on_position(player, pos)
    
    #Mise à jour du plateau par les donnés de l'ia
    def update_ai_board(self,pos,player, board):
        board[pos] = player
        return board
    
    
    ##191970 p ,ia:#DE310C
    #Mise à jour du plateau virtuel par les donnés du joueur ou de l'ia
    def _define_color(self,pos,color):
        self.tabBtn[pos].setStyleSheet("color: #333;\n"
                "border: 2px solid #555;\n"
                "border-radius: 50px;\n"
                "border-style: outset;\n"
                "background: qradialgradient(\n"
                "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                "        radius: 1.35, stop: 0 #fff, stop: 1 "+color+"\n"
                "        );\n"
                "padding: 5px;")  

    
    
        
    #initialise le plateau
    def init_gameboard_ai(self):
        #board = ["X", "-", "-", "O", "-", "O", "-", "X", "-"]
        board = ["-"]*9
        self.gameboard = board
        return board

    #permet de changer de joueur
    def _change_player(self,player):
        if player == "X":
            return "O"
        else:
            return "X"
    
    #efface le plateau
    def clear(self):   
        self.btnplat1.setStyleSheet(self.dfcolor)
        self.btnplat2.setStyleSheet(self.dfcolor)
        self.btnplat3.setStyleSheet(self.dfcolor)
        self.btnplat4.setStyleSheet(self.dfcolor)
        self.btnplat5.setStyleSheet(self.dfcolor)         
        self.btnplat6.setStyleSheet(self.dfcolor)
        self.btnplat7.setStyleSheet(self.dfcolor)        
        self.btnplat8.setStyleSheet(self.dfcolor)        
        self.btnplat9.setStyleSheet(self.dfcolor)
        #self.__init__(False,self.diff)#need btn recommencer
    
    #vérifie s'il y'a un gagnant        
    def winner(self):
        return self._is_game_won()
        
                 
    #algo min max
    def minimax(self, newBoard, player):
        available_pos = self._get_all_free_pos(newBoard)
        if self._is_game_won_player("X", newBoard):
            score = 0
            return score
        elif self._is_game_won_player("O", newBoard):
            score = 100
            return score
        elif len(available_pos) == 0:
            score = 50
            return score
            
        if player == "O":
            bestVal = 0
            for var in available_pos:
                # print("Making move: " + str(var))
                newBoard = self.update_ai_board(var, player, newBoard)
                moveVal = self.minimax(newBoard, "X")
                newBoard = self.update_ai_board(var, "-", newBoard)
                bestVal = max(bestVal, moveVal)
            return bestVal


        if player == "X":
            bestVal = 100
            for var in available_pos:
                # print("Making move: " + str(var))
                newBoard = self.update_ai_board(var, player, newBoard)
                moveVal = self.minimax(newBoard, "O")
                newBoard = self.update_ai_board(var, "-", newBoard)
                bestVal = min(bestVal, moveVal)
            return bestVal
            
    def make_best_move(self, board, player,difficulty):
        if difficulty == 0:
            diff_random = 25
        elif difficulty == 1:
            diff_random = 75
        elif difficulty == 2:
            diff_random = 100
        
        # Generate random
        rnum = randint(0, 100)
        # Find available moves
        initValue = 50
        best_choices = []

        available_pos = self._get_all_free_pos(board)
        if len(available_pos)==9 and diff_random == 500:
            return 4
        if rnum > diff_random and len(available_pos)>0:
            move = random.choice(available_pos)
            return move

        else:
            if player == "O":
                for move in available_pos:
                    board = self.update_ai_board(move, player, board)
                    moveVal = self.minimax(board, self._change_player(player))
                    board = self.update_ai_board(move, "-", board)

                    if moveVal > initValue:
                        best_choices = [move]
                        return move
                    elif moveVal == initValue:
                        best_choices.append(move)
            else:
                for move in available_pos:
                    board = self.update_ai_board(move, player, board)
                    moveVal = self.minimax(board, self._change_player(player))
                    board = self.update_ai_board(move, "-", board)

                    if moveVal < initValue:
                        best_choices = [move]
                        return move
                    elif moveVal == initValue:
                        best_choices.append(move)

            if len(best_choices)>0:
                return random.choice(best_choices)
            elif len(available_pos)>0:
                return random.choice(available_pos)

    
    
    def setupUi(self, level):
        level.setObjectName("level")
        level.resize(1689, 1112)
        level.setMaximumSize(QtCore.QSize(1800, 2581))
        level.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        self.keepwindow=level
        icon.addPixmap(QtGui.QPixmap("71UU+enQH9L._AC_SY355_.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        level.setWindowIcon(icon)
        level.setLayoutDirection(QtCore.Qt.LeftToRight)
        level.setStyleSheet("background-color: rgb(0, 85, 127);")
        self.centralwidget = QtWidgets.QWidget(level)
        self.centralwidget.setObjectName("centralwidget")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(20, 300, 491, 501))
        self.logo.setMaximumSize(QtCore.QSize(5000, 5000))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("pb.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
    
        font = QtGui.QFont()
        font.setFamily("PMingLiU-ExtB")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        
        font = QtGui.QFont()
        font.setFamily("PMingLiU-ExtB")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        
        font = QtGui.QFont()
        font.setFamily("PMingLiU-ExtB")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        
        self.lbscore_2 = QtWidgets.QLabel(self.centralwidget)
        self.lbscore_2.setGeometry(QtCore.QRect(730, 20, 191, 111))
        font = QtGui.QFont()
        font.setFamily("PMingLiU-ExtB")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.lbscore_2.setFont(font)
        self.lbscore_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbscore_2.setObjectName("lbscore_2")
        self.btnplat3 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat3.setGeometry(QtCore.QRect(350, 360, 111, 101))
        self.btnplat3.setStyleSheet("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;")
        self.btnplat3.setText("")
        self.btnplat3.setObjectName("btnplat3")
        self.btnplat2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat2.setGeometry(QtCore.QRect(210, 360, 111, 101))
        self.btnplat2.setStyleSheet("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;")
        self.btnplat2.setText("")
        self.btnplat2.setObjectName("btnplat2")
        self.btnplat1 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat1.setGeometry(QtCore.QRect(70, 360, 111, 101))
        self.btnplat1.setStyleSheet("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;")
        self.btnplat1.setText((""))
        self.btnplat1.setObjectName(("btnplat1"))
        self.btnplat4 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat4.setGeometry(QtCore.QRect(70, 500, 111, 101))
        self.btnplat4.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat4.setText((""))
        self.btnplat4.setObjectName(("btnplat4"))
        self.btnplat5 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat5.setGeometry(QtCore.QRect(210, 500, 111, 101))
        self.btnplat5.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat5.setText((""))
        self.btnplat5.setObjectName(("btnplat5"))
        self.btnplat6 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat6.setGeometry(QtCore.QRect(350, 500, 111, 101))
        self.btnplat6.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat6.setText((""))
        self.btnplat6.setObjectName(("btnplat6"))
        self.btnplat7 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat7.setGeometry(QtCore.QRect(70, 640, 111, 101))
        self.btnplat7.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat7.setText((""))
        self.btnplat7.setObjectName(("btnplat7"))
        self.btnplat8 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat8.setGeometry(QtCore.QRect(210, 640, 111, 101))
        self.btnplat8.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat8.setText((""))
        self.btnplat8.setObjectName(("btnplat8"))
        self.btnplat9 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat9.setGeometry(QtCore.QRect(350, 640, 111, 101))
        self.btnplat9.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat9.setText((""))
        self.btnplat9.setObjectName(("btnplat9"))
        self.btnValid = QtWidgets.QPushButton(self.centralwidget)
        self.btnValid.setGeometry(QtCore.QRect(180, 830, 141, 111))
        font = QtGui.QFont()
        font.setFamily(("NSimSun"))
        font.setPointSize(12)
        self.btnValid.setFont(font)
        self.btnValid.setStyleSheet(("color: rgb(255, 255, 255);\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    \n"
"background-color: rgb(85, 170, 127);\n"
"    padding: 5px;"))
        self.btnValid.setObjectName(("btnValid"))
        self.lbnotification = QtWidgets.QLabel(self.centralwidget)
        self.lbnotification.setGeometry(QtCore.QRect(100, 180, 311, 71))
        font = QtGui.QFont()
        font.setFamily("PMingLiU-ExtB")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.lbnotification.setFont(font)
        self.lbnotification.setStyleSheet("color: rgb(255, 255, 255);")
        self.lbnotification.setObjectName("lbnotification")
        self.imageia1 = QtWidgets.QLabel(self.centralwidget)
        self.imageia1.setGeometry(QtCore.QRect(590, 190, 521, 391))
        self.imageia1.setScaledContents(True)
        font = QtGui.QFont()
        font.setFamily(("PMingLiU-ExtB"))
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.imageia1.setFont(font)
        self.imageia1.setStyleSheet(("color: rgb(255, 255, 255);\n"
"gridline-color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);"))
        self.imageia1.setText((""))
        self.imageia1.setObjectName(("imageia1"))
        self.imageia2 = QtWidgets.QLabel(self.centralwidget)
        self.imageia2.setGeometry(QtCore.QRect(1120, 190, 521, 391))
        self.imageia2.setScaledContents(True)
        font = QtGui.QFont()
        font.setFamily(("PMingLiU-ExtB"))
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.imageia2.setFont(font)
        self.imageia2.setStyleSheet(("color: rgb(255, 255, 255);"))
        self.imageia2.setText((""))
        
        self.imageia2.setObjectName(("imageia2"))
        self.imageia2_2 = QtWidgets.QLabel(self.centralwidget)
        self.imageia2_2.setGeometry(QtCore.QRect(600, 690, 301, 291))
        self.imageia2_2.setScaledContents(True)
        font = QtGui.QFont()
        font.setFamily(("PMingLiU-ExtB"))
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.imageia2_2.setFont(font)
        self.imageia2_2.setStyleSheet(("color: rgb(255, 255, 255);"))
        self.imageia2_2.setText((""))
        self.imageia2_2.setScaledContents(True)
        self.imageia2_2.setObjectName(("imageia2_2"))
        self.btnplat1_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat1_2.setGeometry(QtCore.QRect(520, 130, 111, 101))
        self.btnplat1_2.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat1_2.setObjectName(("btnplat1_2"))
        self.btnplat1_3 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat1_3.setGeometry(QtCore.QRect(1110, 120, 111, 101))
        self.btnplat1_3.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat1_3.setObjectName(("btnplat1_3"))
        self.btnplat1_4 = QtWidgets.QPushButton(self.centralwidget)
        self.btnplat1_4.setGeometry(QtCore.QRect(580, 620, 111, 101))
        self.btnplat1_4.setStyleSheet(("color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;"))
        self.btnplat1_4.setObjectName(("btnplat1_4"))
        
        level.setCentralWidget(self.centralwidget)
        self.btnValid.clicked.connect(self.btnvalid_click)
        self.tabBtn=[self.btnplat1,self.btnplat2,self.btnplat3,self.btnplat4,self.btnplat5,self.btnplat6,self.btnplat7,self.btnplat8,self.btnplat9]
        self.retranslateUi(level)
        QtCore.QMetaObject.connectSlotsByName(level)
        
    def _ask_player_move(self,pos,event):
        valid_pos = self._is_move_valid(pos)
        if (valid_pos != None):
           self._update_board(valid_pos, self.player)
           
           

    def _ai_make_move(self,event):
        recognition= ImageRecognition()
        self.lbnotification.setText("Au tour de l'IA")
        QtWidgets.QApplication.processEvents()
        do=recognition.shoot()
        
        self.imageia1.setPixmap(QtGui.QPixmap(("saved.png")))
        
        
        

        self.gameboard=recognition.recongnition()

        if do :
            self.imageia2.setPixmap(QtGui.QPixmap(("output.png")));
            QtWidgets.QApplication.processEvents()

        texto=""
        for index,x in enumerate(self.gameboard):
            r=(index+1)%3
            texto=texto+x
            if r==0 :
                texto=texto+"\n"
           
            if x =='O':
                self.checked=False
                self.currentplayer = self.player
                self._define_color(index,"#197070")
        
            if x=='X':
                self._define_color(index,"#DE310C")

        if self.gameboard!=None:
            img = Image.new('RGB', (400, 400), color = (73, 109, 137))
            fnt = ImageFont.truetype('Roboto-Bold.ttf', 50)
            d = ImageDraw.Draw(img)   
            d.text((20,20),texto,font=fnt, fill=(255,255,0))
            img.save('plateau.png')
            self.imageia2_2.setPixmap(QtGui.QPixmap(("plateau.png")))
            QtWidgets.QApplication.processEvents()
        #self.show_gameboard() 
        
        win=self._winner()
       
        if win==False:
            self.currentplayer = self.enemy
            self.turn=True
            origBoard = self.gameboard
            pos = self.make_best_move(origBoard,self.enemy,self.diff)
            self.dobot.movePawnTo('p'+str(pos+1))
            self._define_color(pos,"#DE310C")
            self._update_board(pos, self.enemy)
            win=self._winner()
            if win==False:
                self.lbnotification.setText("A vous de jouer")
            QtWidgets.QApplication.processEvents()
            self.currentplayer = self.player
            self.turn=False
            

        sleep(1)
            
        
        
        

    def retranslateUi(self, level):
        _translate = QtCore.QCoreApplication.translate
        level.setWindowTitle(_translate("level", "TIC TAC TOE"))
        self.btnValid.setText(_translate("level", "VALIDER"))
        self.btnplat1_2.setText(_translate("level", "1", None))
        self.btnplat1_3.setText(_translate("level", "2", None))
        self.btnplat1_4.setText(_translate("level", "3", None))
    
    def show_gameboard(self, gameboard=None):
        if gameboard==None:
            t = self.gameboard
        else:
            t = gameboard
        print("{0} {1} {2}".format(t[0], t[1], t[2]))
        print("{0} {1} {2}".format(t[3], t[4], t[5]))
        print("{0} {1} {2}".format(t[6], t[7], t[8]))
        
    
    def btnvalid_click(self,event):
        if(self.end):
            self.dobot.disconnectDobot()
            self.dobot=None
            self.keepwindow.close()
            self.level.show()

        #self._make_move(self.currentPos,event)
        self.checked=False
        QtWidgets.QApplication.processEvents() 
        self.show_gameboard()
        
        if self.end==False :
            self._ai_make_move(event)
        QtWidgets.QApplication.processEvents()  
        self.show_gameboard()

    def _winner(self) :
        winner=self.winner()

        if (winner == "tie"):
            self.lbnotification.setText("GAME OVER!")
            self.btnValid.setText("RECOMMENCER")
            self.end=True
            
            QtWidgets.QApplication.processEvents()
            self.stop()
            self.btnValid.setEnabled(True)
            
        elif (winner == self.player):
            self.setpoints()
            self.lbnotification.setText("Vous avez gagné")
            self.btnValid.setText("RECOMMENCER")
            self.end=True
            
            QtWidgets.QApplication.processEvents()
            self.stop()
            self.btnValid.setEnabled(True)
        
        elif (winner == self.enemy):
            self.setpoints()
            
            self.lbnotification.setText("Vous avez perdu")
            self.btnValid.setText("RECOMMENCER")
            self.end=True
            QtWidgets.QApplication.processEvents()
            self.stop()
            self.btnValid.setEnabled(True)
        

        return self.end

    def setpoints(self):
        available_pos = self._get_all_free_pos(self.gameboard)
        if self._is_game_won_player("X", self.gameboard):
            self.score_player = self.score_player
            self.score_ia=self.score_ia + 100
            
           
        elif self._is_game_won_player("O", self.gameboard):
            self.score_ia = self.score_ia
            self.score_player=self.score_player + 100
            
        elif len(available_pos) == 0:
            self.score_ia = self.score_ia +0
            self.score_player=self.score_player + 0
            
        
        
            
    def stop(self):
        for i in range(0,8):
            self.tabBtn[i].setEnabled(False)
        self.btnValid.setEnabled(False)
            
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    level = QtWidgets.QMainWindow()
    ui = Ui_board()
    ui.setupUi(level)
    level.show()
    sys.exit(app.exec_())
