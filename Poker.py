#Copyright Andrew Cabey 2016
#Deliverable #4

import sys
from deck import Deck
from handEval import handType, highCard
from graphics import *
from random import seed

class Card(object):
	def __init__(self, card, lowAce=False, isSelected=False):
		rankvalues = {'t' : 10, 'j' : 11, 'q' : 12, 'k' : 13, 'a' : 14, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9}
		suitvalues = {'h': 'Hearts', 's': 'Spades', 'd': 'Diamonds', 'c': 'Clubs'}
		if lowAce: rankvalues['a']=1
		self.card = card 						 #String containing 'as' or whatever
		self.rank = rankvalues.get(self.card[0]) #Numeric value of the card
		self.suit = suitvalues.get(self.card[1]) #String suit of the card
		self.isSelected = isSelected
		self.image = Image(Point(0,0),"cards/" + self.card + ".gif")
		self.backdrop = None
		self.binding = None
		self.params = None
		self.masterBinding = None
		self.returnValue = None
		#Modified rectangle that matches dimensions of the image
		self.imageRectangle = None
	
	def __str__(self):
		return self.card
	
	def __eq__(self, other):
		if not isinstance(other, Card):
			return self.card == other
		else: return self.card == other.card
	
	def __call__(self, clickpoints):
		if self.checkPress(clickpoints): 
			if not self.masterBinding:
				if self.params:
					self.returnValue = self.binding(self.params)
				else:
					self.returnValue = self.binding()
			else:
				self.returnValue = eval(self.masterBinding)

	def checkPress(self, clickpoints):
		if not clickpoints: return False
		r1 = Rectangle(
			Point(self.image.getAnchor().getX() - (.5*self.image.getWidth()), self.image.getAnchor().getY() + (.5*self.image.getHeight()))
			, Point(self.image.getAnchor().getX() + (.5*self.image.getWidth()), self.image.getAnchor().getY() - (.5*self.image.getHeight()))
			)
		return ((r1.getP1().getX() <= clickpoints.getX() <= r1.getP2().getX()) and (r1.getP1().getY() >= clickpoints.getY() >= r1.getP2().getY()))

	def bind(self, binding, params=None, master=False):
		if not master:
			self.binding = binding
			self.params = params
		else: self.masterBinding = binding

	def select(self, window):
		self.isSelected = not self.isSelected
		if self.isSelected: self.imageRectangle.setWidth(4)
		else: self.imageRectangle.setWidth(0) 

	def draw(self, window, posX, posY):
		self.image.move(posX, posY)
		self.image.draw(window)
		self.imageRectangle = Rectangle(
			Point(self.image.getAnchor().getX() - (.5*self.image.getWidth()), self.image.getAnchor().getY() + (.5*self.image.getHeight())), 
			Point(self.image.getAnchor().getX() + (.5*self.image.getWidth()), self.image.getAnchor().getY() - (.5*self.image.getHeight()))
			)
		self.imageRectangle.setOutline("gold")
		self.imageRectangle.setWidth(0)
		self.imageRectangle.draw(window)

	def undraw(self):
		try:
			self.image.undraw()
			if self.imageRectangle: self.imageRectangle.undraw()
		except: pass

class Hand(object):
	def __init__(self, carddeal):
	 	self.stringcards = carddeal
	 	self.cards = []
	 	for card in carddeal: self.cards.append(Card(card)) 
	 	self.type = handType(self.stringcards)
	 	self.highcard = highCard(self.stringcards)
	
	def __str__(self):
		ret = []
		for card in self.cards:
			ret.append(str(card))
		return ret

	def draw(self, window,startX=50,startY=100, difference=80):
		startpoint = [startX, startY]
		for card in self.cards:
			card.undraw()
			startpoint[0]+=difference
			card.draw(window, startpoint[0], startpoint[1])
		return [[startX,startY],startpoint]

	def undraw(self):
		try: 
			for card in self.cards: card.undraw()
		except: 
			pass

	def discard(self, window):
		global myDeck
		carddeal = []
		
		for card in self.cards:
			card.undraw()
			if not card.isSelected: carddeal.append(card.card)

		while not len(carddeal) == 5:
			carddeal.append(myDeck.deal(1)[0])
		#Make a new instance of this object pretty much
		self.__init__(carddeal)
		self.draw(window)

		return "This is a placeholder"

	def generateHand(cardCount=5):
		mydeck = Deck()
		mydeck.shuffle()
		return Hand(mydeck.deal(cardCount))


class Textbox(object):
	def __init__(self, text, startPoint, endPoint, fill='white', width=2):
		self.button = Rectangle(startPoint, endPoint)
		self.width = abs(self.button.getP1().getX() - self.button.getP2().getX())
		self.height = abs(self.button.getP1().getY() - self.button.getP2().getY())
		self.text = Text(Point(self.button.getP1().getX() + .5*self.width,self.button.getP1().getY() - .5*self.height), text)
		self.button.setFill(fill)
		self.button.setWidth(width)
		self.binding = None
		self.params = None
		self.masterBinding = None
		self.returnValue = None
	
	def __call__(self, clickpoints):
		if self.checkPress(clickpoints): 
			if not self.masterBinding:
				if self.params:
					self.returnValue = self.binding(self.params)
				else:
					self.returnValue = self.binding()
			else:
				self.returnValue = eval(self.masterBinding)

	def checkPress(self, clickpoints):
		if not clickpoints: return False
		r1 = self.button
		return ((r1.getP1().getX() <= clickpoints.getX() <= r1.getP2().getX()) and (r1.getP1().getY() >= clickpoints.getY() >= r1.getP2().getY()))

	def bind(self, binding, params=None, master=False):
		if not master:
			self.binding = binding
			self.params = params
		else: self.masterBinding = binding

	def draw(self,window):
		self.button.draw(window)
		self.text.draw(window)

	def undraw(self):
		try:
			self.button.undraw()
			self.text.undraw()
		except: pass

def deal():
	global myDeck
	myDeck.shuffle()
	return Hand(myDeck.deal(5))

def runDeal(window):
	myHand = deal()
	myHand.draw(window)

def updateText(textObj,handObj,window):
	try:
		textObj.undraw()
	except: pass
	hand = handObj.stringcards

	typeValues = {
		9: "Royal Flush",		#9 Straight flush of highest values
		8: "Straight Flush", 	#8 Straight and a Flush
		7: "Four of a Kind", 	#7 Contains all four cards of a rank
		6: "Full House",		#6 Three matches of one rank and two matches of another
		5: "Flush", 			#5 All cards are of same suit
		4: "Sraight", 			#4 All cards are sequential
		3: "Three of a Kind", 	#3 Three matches in rank
		2: "Two Pair",			#2 Two matches in rank
		1: "Pair", 				#1 One match in rank
		0: "High Card" 			#0 Nothing else, only highest card in hand matters
	}

	rankValues = {
		14: 'High Ace',
		13: 'King', 
		12: 'Queen',
		11: 'Jack',
		10: 'Ten',
		1: 'Low Ace',
		2: 'Two',
		3: 'Three',
		4: 'Four',
		5: 'Five',
		6: 'Six',
		7: 'Seven',
		8: 'Eight',
		9: 'Nine'
	}

	suitValues = {
		'd': 'Diamonds',
		's': 'Spades',
		'c': 'Clubs',
		'h': 'Hearts'
	}
	#Will output "Hand is a {type} with high card {rank} of {suit}"
	textObj.setText('Hand is a ' + typeValues.get(handType(hand)) + ' with high card ' + rankValues.get(highCard(hand)))
	textObj.draw(window)

"""
Deal is bound
Quit is bound
Discard is unbound

Selected has to be stored somewhere... card objects?
Hand objects? 

Button object, yes...

Both Textboxes and cards can be bound with a binding to a function, callable as the object is called
Or they can be bound with a 'master' string which will be evaluated over the original binding to facilitate parameters

Game starts:
	Deal cards into Hand object
	Draw cards from Hand object to screen
	Bind each card to selection... each card is an object with (isSelected...)
	Enable Discard button... bind to discard selected and replace (for loop with index)
		Only do stuff if there is a selected card
		for each card, if it is selected, replace with a new draw... deck has to be maintained throughout sorta
		Unbind/ disable self
	Redraw the deck if the card was replaced
	Print out the highcard and things
"""

if __name__ == '__main__':
	w = GraphWin('Poker Game', 600, 400)
	typeText = Text(Point(300,250), '')
	dealButton = Textbox("Deal", Point(50, 360), Point(125, 320))
	discardButton = Textbox("Discard", Point(200, 360), Point(275, 320))
	quitButton = Textbox("Quit", Point(350, 360), Point(425, 320))
	dealButton.draw(w)
	discardButton.draw(w)
	quitButton.draw(w)
	
	while True:
		myDeck = Deck()
		dealButton.bind("deal()", master=True)
		discardButton.bind("m_hand.discard(w)", master=True)
		quitButton.bind(sys.exit)
		dealButton.button.setOutline('red')

		while not dealButton.returnValue:
			dealButton(w.checkMouse())
			quitButton(w.checkMouse())

		dealButton.bind("", master=True)
		m_hand = dealButton.returnValue
		dealButton.returnValue = None
		m_hand.draw(w)
		updateText(typeText,m_hand,w)
		dealButton.button.setOutline('black')
		discardButton.button.setOutline('red')

		for card in m_hand.cards:
			card.bind(card.select, params=w)

		while not discardButton.returnValue:
			for card in m_hand.cards:
				card(w.checkMouse())
			quitButton(w.checkMouse())
			discardButton(w.checkMouse())

		discardButton.button.setOutline('black')
		discardButton.bind("", master=True)
		discardButton.returnValue = None
		updateText(typeText,m_hand,w)
