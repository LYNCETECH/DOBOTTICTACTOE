# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'board2.ui'
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

from scipy.spatial import distance as dist


PLAYERS = ["X","O"]

class Ui_board2(object):
    
    def __init__(self,diff, level,_dobot):
        #self._dm = dobot_manager
        self.gameboard = ["-"]*9
        self.currentbuffer = 0
        self.moves = []
        self.diff = diff
        self.turn=False
        self.checked=False
        self.currentPos=0
        self.active=[0]*9
        self.score_ia = self.level.getIAScore()
        self.score_player=self.level.getPlayerScore()
        self.end=False
        self.level=level
        self._winning_combinations = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])
        self.player="O"
        self.enemy = "X"
        self.currentplayer = "O"
     
        self.recognition= ImageRecognition()
        self.dobot = _dobot
        self.dobot.connectDobot()
        self.dobot.initDobot()

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
        
    #Mise à jour du plateau par les donnés de l'ia
    def update_ai_board(self,pos,player, board):
        board[pos] = player
        return board

    def _make_move(self,pos,event):
        if self.currentplayer == self.player:
            self._ask_player_move(pos,event)
        

    def init_gameboard_ai(self):
        #board = ["X", "-", "-", "O", "-", "O", "-", "X", "-"]
        board = 9*["-"]
        self.gameboard = board
        return board

    def _change_player(self,player):
        if player == "X":
            return "O"
        else:
            return "X"

    def winner(self):
        return self._is_game_won()
        
           
            
    
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

    def _ask_player_move(self,pos,event):
        valid_pos = self._is_move_valid(pos)
        if (valid_pos != None):
           self._update_board(valid_pos, self.player)
           self.currentplayer = self.enemy
           self.turn=True
           self.lbnotification.setText("Au tour de l'IA")
           sleep(1)

    def _ai_make_move(self,event):
        self.gameboard=self.recognition.recongnition()
        origBoard = self.gameboard
        pos = self.make_best_move(origBoard,self.enemy,self.diff)
        self.dobot.movePawnTo('p'+str(pos+1))
        self._define_color(pos)
        self._update_board(pos, self.enemy)
        self.winner()
        self.currentplayer = self.player
        self.turn=False
        self.lbnotification.setText("A vous de jouer")
        sleep(1)

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
            self.level.setIAScore(self.score_ia)
            self.level.setPlayerScore(self.score_player)
            self.level.show()
            
            
        self._make_move(self.currentPos,event)
        QtWidgets.QApplication.processEvents()
        self.show_gameboard()
        self.checked=False
        winner=self.winner()
        QtWidgets.QApplication.processEvents()
        print(winner)
        if (winner == "tie"):
            self.lbnotification.setText("GAME OVER!")
            self.btnValid.setText("RECOMMENCER")
            self.end=True
            
            QtWidgets.QApplication.processEvents()
            self.btnValid.setEnabled(True)
            
        elif (winner == self.player):
            self.setpoints()
            self.lbnotification.setText("Vous avez gagné")
            self.btnValid.setText("RECOMMENCER")
            self.end=True
            
            QtWidgets.QApplication.processEvents()
            self.btnValid.setEnabled(True)
        
        elif (winner == self.enemy):
            self.setpoints()
            
            self.lbnotification.setText("Vous avez perdu")
            self.btnValid.setText("RECOMMENCER")
            self.end=True
            QtWidgets.QApplication.processEvents()
            self.btnValid.setEnabled(True)
            
        if self.currentplayer == self.enemy and winner!="tie" and winner!="X" and winner!="O":
            self._ai_make_move(event)
            QtWidgets.QApplication.processEvents()
            
        self.show_gameboard()
    
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
            
        self.lbScoreValue.setText(str(self.score_player))
        self.lbScoreValueIA.setText(str(self.score_ia))

    def setupUi(self, level):
        level.setObjectName(_fromUtf8("level"))
        level.resize(1600, 1138)
        level.setMaximumSize(QtCore.QSize(1600, 2581))
        level.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("71UU+enQH9L._AC_SY355_.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        level.setWindowIcon(icon)
        level.setLayoutDirection(QtCore.Qt.LeftToRight)
        level.setStyleSheet(_fromUtf8("background-color: rgb(0, 85, 127);"))
        self.centralwidget = QtGui.QWidget(level)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.lbscore = QtGui.QLabel(self.centralwidget)
        self.lbscore.setGeometry(QtCore.QRect(20, 20, 251, 111))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PMingLiU-ExtB"))
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.lbscore.setFont(font)
        self.lbscore.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.lbscore.setObjectName(_fromUtf8("lbscore"))
        self.lbScoreValue = QtGui.QLabel(self.centralwidget)
        self.lbScoreValue.setGeometry(QtCore.QRect(290, 20, 141, 111))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PMingLiU-ExtB"))
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.lbScoreValue.setFont(font)
        self.lbScoreValue.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.lbScoreValue.setObjectName(_fromUtf8("lbScoreValue"))
        self.lbScoreValueIA = QtGui.QLabel(self.centralwidget)
        self.lbScoreValueIA.setGeometry(QtCore.QRect(650, 20, 141, 111))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PMingLiU-ExtB"))
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.lbScoreValueIA.setFont(font)
        self.lbScoreValueIA.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.lbScoreValueIA.setObjectName(_fromUtf8("lbScoreValueIA"))
        self.lbscore_2 = QtGui.QLabel(self.centralwidget)
        self.lbscore_2.setGeometry(QtCore.QRect(450, 20, 191, 111))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PMingLiU-ExtB"))
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.lbscore_2.setFont(font)
        self.lbscore_2.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.lbscore_2.setObjectName(_fromUtf8("lbscore_2"))
        self.btnValid = QtGui.QPushButton(self.centralwidget)
        self.btnValid.setGeometry(QtCore.QRect(230, 810, 161, 121))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("NSimSun"))
        font.setPointSize(12)
        self.btnValid.setFont(font)
        self.btnValid.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    \n"
"background-color: rgb(255, 255, 255);\n"
"    padding: 5px;"))
        self.btnValid.setObjectName(_fromUtf8("btnValid"))
        self.btnValid.clicked.connect(self.btnvalid_click)
        self.l = QtGui.QLabel(self.centralwidget)
        self.l.setGeometry(QtCore.QRect(840, 30, 311, 71))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PMingLiU-ExtB"))
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.l.setFont(font)
        self.l.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.l.setText(_fromUtf8(""))
        self.l.setObjectName(_fromUtf8("l"))
        self.phase1 = QtGui.QLabel(self.centralwidget)
        self.phase1.setGeometry(QtCore.QRect(140, 210, 671, 421))
        self.phase1.setStyleSheet(_fromUtf8("background-color: rgb(207, 207, 207);"))
        self.phase1.setText(_fromUtf8(""))
        self.phase1.setObjectName(_fromUtf8("phase1"))
        self.phase2 = QtGui.QLabel(self.centralwidget)
        self.phase2.setGeometry(QtCore.QRect(850, 210, 641, 411))
        self.phase2.setStyleSheet(_fromUtf8("background-color: rgb(207, 207, 207);"))
        self.phase2.setText(_fromUtf8(""))
        self.phase2.setObjectName(_fromUtf8("phase2"))
        self.phase3 = QtGui.QLabel(self.centralwidget)
        self.phase3.setGeometry(QtCore.QRect(520, 700, 591, 391))
        self.phase3.setStyleSheet(_fromUtf8("background-color: rgb(207, 207, 207);"))
        self.phase3.setText(_fromUtf8(""))
        self.phase3.setObjectName(_fromUtf8("phase3"))
        self.lbscore_3 = QtGui.QLabel(self.centralwidget)
        self.lbscore_3.setGeometry(QtCore.QRect(230, 150, 411, 51))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PMingLiU-ExtB"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbscore_3.setFont(font)
        self.lbscore_3.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.lbscore_3.setObjectName(_fromUtf8("lbscore_3"))
        self.lbscore_4 = QtGui.QLabel(self.centralwidget)
        self.lbscore_4.setGeometry(QtCore.QRect(940, 150, 471, 51))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PMingLiU-ExtB"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbscore_4.setFont(font)
        self.lbscore_4.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.lbscore_4.setObjectName(_fromUtf8("lbscore_4"))
        self.lbscore_5 = QtGui.QLabel(self.centralwidget)
        self.lbscore_5.setGeometry(QtCore.QRect(530, 640, 581, 51))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("PMingLiU-ExtB"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbscore_5.setFont(font)
        self.lbscore_5.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.lbscore_5.setObjectName(_fromUtf8("lbscore_5"))
        self.lbphase = QtGui.QPushButton(self.centralwidget)
        self.lbphase.setGeometry(QtCore.QRect(110, 130, 101, 101))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("NSimSun"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbphase.setFont(font)
        self.lbphase.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    \n"
"background-color: rgb(255, 170, 0);\n"
"    padding: 5px;"))
        self.lbphase.setObjectName(_fromUtf8("lbphase"))
        self.lbphase3 = QtGui.QPushButton(self.centralwidget)
        self.lbphase3.setGeometry(QtCore.QRect(440, 670, 101, 101))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("NSimSun"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbphase3.setFont(font)
        self.lbphase3.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    \n"
"background-color: rgb(255, 170, 0);\n"
"    padding: 5px;"))
        self.lbphase3.setObjectName(_fromUtf8("lbphase3"))
        self.lbphase2 = QtGui.QPushButton(self.centralwidget)
        self.lbphase2.setGeometry(QtCore.QRect(820, 130, 101, 101))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("NSimSun"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbphase2.setFont(font)
        self.lbphase2.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"    border: 2px solid #555;\n"
"    border-radius: 50px;\n"
"    border-style: outset;\n"
"    \n"
"background-color: rgb(255, 170, 0);\n"
"    padding: 5px;"))
        self.lbphase2.setObjectName(_fromUtf8("lbphase2"))
        level.setCentralWidget(self.centralwidget)

        self.retranslateUi(level)
        QtCore.QMetaObject.connectSlotsByName(level)

    def retranslateUi(self, level):
        level.setWindowTitle(_translate("level", "TIC TAC TOE", None))
        self.lbscore.setText(_translate("level", "Score joueur :", None))
        self.lbScoreValue.setText(_translate("level", "00", None))
        self.lbScoreValueIA.setText(_translate("level", "00", None))
        self.lbscore_2.setText(_translate("level", "Score IA :", None))
        self.btnValid.setText(_translate("level", "VALIDER", None))
        self.lbscore_3.setText(_translate("level", "Identification des formes présentes dans  l\'image", None))
        self.lbscore_4.setText(_translate("level", "Identification des couleurs et position de chaque forme ", None))
        self.lbscore_5.setText(_translate("level", "Conversion image en matrice avec positionnement de chaque pièce", None))
        self.lbphase.setText(_translate("level", "1", None))
        self.lbphase3.setText(_translate("level", "3", None))
        self.lbphase2.setText(_translate("level", "2", None))
        


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    level = QtGui.QMainWindow()
    ui = Ui_level()
    ui.setupUi(level)
    level.show()
    sys.exit(app.exec_())

