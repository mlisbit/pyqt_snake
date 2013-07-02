#!/usr/bin/python
import sys, time
import thread

from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
	def __init__(self):
		super(Example, self).__init__()
		self.initUI()

	def initUI(self):
		self.text = "snake time!"

		self.snakeLength = 2
		self.x = 0;
		self.y = 0;
		self.lastKeyPress = 'RIGHT'
		self.timer = QtCore.QBasicTimer()
		self.inflection_point = (0,0)

		self.isPaused = False
		self.isOver = False
		self.timer.start(100, self)
		self.setStyleSheet("QWidget { background: #A9F5D0 }") 
		self.setFixedSize(300, 300) 
		self.setWindowTitle('Snake')
		self.show()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		if self.isOver:
			self.gameOver(event, qp)
		self.drawSnake(qp)
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

	def gameOver(self, event, qp):
		qp.setPen(QtGui.QColor(168, 34, 3))
		qp.setFont(QtGui.QFont('Decorative', 10))
		qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "GAME OVER")   

	def checkStatus(self, x, y):
		if y > 288 or x > 288 or x < 0 or y < 0:
			self.pause()
			self.isPaused = True
			self.isOver = True
			return False
		return True

	def drawSnake(self, qp):
		color = QtGui.QColor(0,0,0)
		color.setNamedColor('#ffffff')
		qp.setPen(color)
		qp.setBrush(QtGui.QColor(255, 80, 0, 160))
		qp.drawRect(self.x, self.y, 12, 12)
		

	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			self.direction(self.lastKeyPress)
			self.repaint()
		else:
			QtGui.QFrame.timerEvent(self, event)

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
	

if __name__ == '__main__':
	main()