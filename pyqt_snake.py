#!/usr/bin/python
import sys, time
import thread
from random import randrange

from PyQt4 import QtGui, QtCore

class Snake(QtGui.QWidget):
	def __init__(self):
		super(Snake, self).__init__()
		self.initUI()

	def initUI(self):
		self.text = "snake time!"

		self.score = 0
		self.x = 12;
		self.y = 36;
		self.lastKeyPress = 'RIGHT'
		self.timer = QtCore.QBasicTimer()
		self.inflection_point = (0,0)

		self.foodx = 0
		self.foody = 0

		self.isPaused = False
		self.isOver = False
		self.FoodPlaced = False
		self.start()
		self.setStyleSheet("QWidget { background: #A9F5D0 }") 
		self.setFixedSize(300, 300)
		self.setWindowTitle('Snake')
		self.show()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		if self.isOver:
			self.gameOver(event, qp)
		self.scoreBoard(qp)
		self.placeFood(qp)
		self.drawSnake(qp)
		self.scoreText(event, qp)
		qp.end()

	def keyPressEvent(self, e):
		if not self.isPaused:
			print "inflection point: ", self.x, " ", self.y
			if e.key() == QtCore.Qt.Key_Up and self.lastKeyPress != 'UP':
				self.direction("UP")
				self.lastKeyPress = 'UP'
			elif e.key() == QtCore.Qt.Key_Down and self.lastKeyPress != 'DOWN':
				self.direction("DOWN")
				self.lastKeyPress = 'DOWN'
			elif e.key() == QtCore.Qt.Key_Left and self.lastKeyPress != 'LEFT':
				self.direction("LEFT")
				self.lastKeyPress = 'LEFT'
			elif e.key() == QtCore.Qt.Key_Right and self.lastKeyPress != 'RIGHT':
				self.direction("RIGHT")
				self.lastKeyPress = 'RIGHT'
			elif e.key() == QtCore.Qt.Key_P:
				self.pause()
		elif e.key() == QtCore.Qt.Key_P:
				self.start()

	def pause(self):
		self.isPaused = True
		self.timer.stop()
		self.update()

	def start(self):
		self.isPaused = False
		self.timer.start(100, self)
		self.update()

	def direction(self, dir):
		if (dir == "DOWN" and self.checkStatus(self.x, self.y+12)):
			for i in range(1, 13):
				time.sleep(0.009)
				self.y += 1
				self.repaint()
		elif (dir == "UP" and self.checkStatus(self.x, self.y-12)):
			for i in range(1, 13):
				time.sleep(0.009)
				self.y -= 1
				self.repaint()
		elif (dir == "RIGHT" and self.checkStatus(self.x+12, self.y)):
			for i in range(1, 13):
				time.sleep(0.009)
				self.x += 1
				self.repaint()
		elif (dir == "LEFT" and self.checkStatus(self.x-12, self.y)):
			for i in range(1, 13):
				time.sleep(0.009)
				self.x -= 1
				self.repaint()

	def scoreBoard(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(25, 80, 0, 160))
		qp.drawRect(0, 0, 300, 24)

	def scoreText(self, event, qp):
		qp.setPen(QtGui.QColor(255, 255, 255))
		qp.setFont(QtGui.QFont('Decorative', 10))
		
		qp.drawText(10, 17, "SCORE: " + str(self.score))   

	def gameOver(self, event, qp):
		qp.setPen(QtGui.QColor(168, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 10))
		qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "GAME OVER")   

	def checkStatus(self, x, y):
		if y > 288 or x > 288 or x < 0 or y < 24:
			self.pause()
			self.isPaused = True
			self.isOver = True
			return False
		elif self.y == self.foody and self.x == self.foodx:
			self.FoodPlaced = False
			self.score += 1
			
			return True

		return True

	def placeFood(self, qp):
		if self.FoodPlaced == False:
			self.foodx = randrange(24)*12
			self.foody = randrange(2, 24)*12
			print "food placed at: ", self.foodx, self.foody
			self.FoodPlaced = True;

		qp.setBrush(QtGui.QColor(80, 180, 0, 160))
		qp.drawRect(self.foodx, self.foody, 12, 12)

	def drawSnake(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(255, 80, 0, 255))
		qp.drawRect(self.x, self.y, 12, 12)

	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.direction(self.lastKeyPress)
			self.repaint()
		else:
			QtGui.QFrame.timerEvent(self, event)

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Snake()
	sys.exit(app.exec_())
	

if __name__ == '__main__':
	main()