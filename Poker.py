#Copyright Andrew Cabey 2016
#Deliverable #3

from deck import Deck
from handEval import *
from graphics import *

def drawHand(window,hand, startX=100,startY=100):
	#global cards
	startpoint = [startX, startY]

	for image in cards:
		image.undraw()
	cards = []

	for card in hand:
		startpoint[0]+=20
		cards.append(Image(Point(startpoint[0],startpoint[1]),"cards/" + card + ".gif"))
	
	for image in cards:
		image.draw(window)

	return [[startX,startY],startpoint]

def isPressed(r1, clickpoints):
	if not clickpoints: return False
	return ((r1.getP1().getX() <= clickpoints.getX() <= r1.getP2().getX()) and (r1.getP1().getY() >= clickpoints.getY() >= r1.getP2().getY()))

def checkMouseClicks(clickpoints):
	click = clickpoints
	#global bindings
	for binding in bindings:
		if isPressed(binding, click): bindings[binding]()

def doDeal():
	#global w
	mydeck = Deck()
	mydeck.shuffle()
	drawHand(w, mydeck.deal(5))

if __name__ == '__main__':

	cards = [] 		#Global cache for card images
	bindings = {}	#Binds the buttons to actions

	myDeck = Deck()

	typeText = Text(Point(.175*w.width+4,.625*w.height), 'Hand Type: '),
	highText = Text(Point(.175*w.width+4,.65*w.height), 'High Card: ')

	dealButton = Rectangle(Point(.15*windowX,.85*windowY), Point(.23*windowX,.8*windowY))
	dealText = Text(Point(.175*windowX+4,.825*windowY), 'Deal')

	quitButton = Rectangle(Point(.25*windowX,.85*windowY), Point(.33*windowX,.8*windowY))
	quitText = Text(Point(.275*windowX+4,.825*windowY), 'Quit')

	dealButton.setFill('white')
	dealButton.setWidth(2)
	
	quitButton.setFill('white')
	quitButton.setWidth(2)

	dealButton.draw(w)
	dealText.draw(w)
	quitButton.draw(w)
	quitText.draw(w)

	typeText.draw(w)
	highText.draw(w)

	bindings = {
		dealButton:doDeal,
		quitButton:sys.exit
	}

	while True:
		checkMouseClicks(w.checkMouse())
		typeText.update()
		highText.update()
