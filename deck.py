#Copyright Andrew Cabey 2016
#Deliverable #1

class Deck(object):
	cards = []
	def __init__(self):
		suits = ['spades', 'hearts', 'diamonds', 'clubs']
		ranks = ['ace', 'king', 'queen', 'jack', 'ten', '9', '8', '7', '6', '5', '4', '3', '2']
		self.cards = []
		for suit in suits:
			for rank in ranks:
				self.cards.append(str(rank[0]+suit[0]))

	def shuffle(self):
		import random 				#Technically it is more efficient to import in local scope
		random.shuffle(self.cards)

	def deal(self, numcards):
		retlist = []
		for i in range(0,numcards):
			retlist.append(self.cards.pop(0))
		return retlist

"""
def test_Deck():
	import random
	random.seed(1)
	mydeck = Deck()               
	print mydeck.deal(5), "=['as', 'ks', 'qs', 'js', 'ts']"
	mydeck.shuffle()		
	print mydeck.deal(5), "=['3h', 'th', '7s', 'qc', '5c']"		
	print mydeck.deal(2), "=['5h', '9h']"
"""
if __name__ == '__main__':
	pass
