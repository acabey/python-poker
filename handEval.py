#Copyright Andrew Cabey 2016
#Deliverable #2

def handType(hand):
	if isRoyalFlush(hand):		return 9#return "Royal Flush"		#9 Straight flush of highest values
	elif isStraightFlush(hand):	return 8#return "Straight Flush" 	#8 Straight and a Flush
	elif isFourOfAKind(hand): 	return 7#return "Four of a Kind" 	#7 Contains all four cards of a rank
	elif isFullHouse(hand): 	return 6#return "Full House" 		#6 Three matches of one rank and two matches of another
	elif isFlush(hand): 		return 5#return "Flush" 			#5 All cards are of same suit
	elif isStraight(hand): 		return 4#return "Sraight" 			#4 All cards are sequential
	elif isThreeOfAKind(hand): 	return 3#return "Three of a Kind" 	#3 Three matches in rank
	elif isTwoPair(hand): 		return 2#return "Two Pair" 			#2 Two matches in rank
	elif isPair(hand): 			return 1#return "Pair" 				#1 One match in rank
	else: 						return 0#return "High Card" 		#0 Nothing else, only highest card in hand matters

def isRoyalFlush(hand, showHighCard=False):
	"""
	9 Straight flush of highest values (A, K, Q, J, 10)
	(straight begins at 10)
	"""
	_isRoyalFlush = isRoyal(hand) and isFlush(hand) and isStraight(hand)
	if _isRoyalFlush and showHighCard:
		return getHighestCard(hand)
	return _isRoyalFlush

def	isStraightFlush(hand, showHighCard=False):
	"""
	8 Both a straight and a flush
	"""
	_isStraightFlush = isFlush(hand) and isStraight(hand)
	if _isStraightFlush and showHighCard:
		isStraight(hand, showHighCard=True)
	return _isStraightFlush

def	isFourOfAKind(hand, showHighCard=False):
	"""
	7 Contains all four cards of a rank
	"""
	_isFourofAKind = countMostOccurance(countRankOccurance(hand))['Count'] == 4
	if _isFourofAKind and showHighCard:
		return countMostOccurance(countRankOccurance(hand))['Rank']
	else: return _isFourofAKind

def	isFullHouse(hand, showHighCard=False):
	"""
	6 Three matches of one rank and two matches of another
	"""
	_isFullHouse = isThreeOfAKind(hand) and countMostOccurance(countRankOccurance(hand), 2)['Count'] == 2
	if _isFullHouse and showHighCard:
		return countMostOccurance(countRankOccurance(hand))['Rank']
	return _isFullHouse

def	isFlush(hand, showHighCard=False):
	"""
	5 All cards are of same suit
	"""
	if not showHighCard:
		suit = hand[0][1]
		for card in hand:
			if not card[1] == suit: return False
		return True
	elif isFlush(hand):
		return getHighestCard(hand)
	else: return False

def	isStraight(hand, showHighCard=False):
	"""
	4 All cards are sequential
	Checks if all values are different
	Checks if the greatest difference between values is 1
	"""
	_isStraight = getMaxDifference(getRanks(hand)) or getMaxDifference(getRanks(hand,acesLow=True))
	if _isStraight and showHighCard:
		if getMaxDifference(getRanks(hand,acesLow=True)): return getHighestCard(hand, acesLow=True)
		return getHighestCard(hand)
	return _isStraight

def	isThreeOfAKind(hand, showHighCard=False):
	"""
	3 Three matches in rank
	"""
	_isThreeOfAKind = countMostOccurance(countRankOccurance(hand))['Count'] == 3
	if _isThreeOfAKind and showHighCard:
		return countMostOccurance(countRankOccurance(hand))['Rank']
	return _isThreeOfAKind

def	isTwoPair(hand, showHighCard=False):
	"""
	2 Two matches in rank
	Checks if isPair for two different values
	HighCard returns the greater ranked pair
	"""
	_isTwoPair = countMostOccurance(countRankOccurance(hand))['Count'] == 2 and countMostOccurance(countRankOccurance(hand), 2)['Count'] == 2
	if _isTwoPair and showHighCard:
		return getHighestCard([countMostOccurance(countRankOccurance(hand))['Rank'], countMostOccurance(countRankOccurance(hand), 2)['Rank']])
	return _isTwoPair

def	isPair(hand, showHighCard=False):
	"""
	1 Exactly one match in rank
	"""
	_isPair = countMostOccurance(countRankOccurance(hand))['Count'] == 2
	if _isPair and showHighCard:
		return countMostOccurance(countRankOccurance(hand))['Rank']
	return _isPair

def countRankOccurance(hand, rank=None):
	"""
	Returns count of cards as formatted dictionary
	ex. [as, kh, 8h, kd, ac] > {'a':2, 'k':2}
	"""
	if not rank:
		outDict = {}
		possibleRanks = []
		for card in hand:
			if not card[0] in possibleRanks:possibleRanks.append(card[0])
		for rank_i in possibleRanks:
			count = countRankOccurance(hand, rank_i)
			if count: outDict[rank_i] = count
		return outDict
	else:
		i = 0
		for card in hand:
			if card[0] == rank: i+=1
		return i

def sortedRankOccurance(rankOccurance):
	"""
	Returns a sorted list of Rank Count pairs (tuples) by the occurance of the rank in the hand
	itemgetter scales better than dict.get(...) in efficiency
	"""
	import operator
	return sorted(rankOccurance.items(), key=operator.itemgetter(1), reverse=True)


def countMostOccurance(rankOccurance, location=1):
	"""
	Returns most occuring card in hand with amount of occurances (dictionary) in key form 'Rank' and 'Count'
	In a sorted list of occurances, location refers to where on the list (1 being the most occuring, 2 being second most...)
	"""
	scoreboard = sortedRankOccurance(rankOccurance)
	pair = scoreboard[location-1]
	return {'Rank': pair[0], 'Count': pair[1]}

def isRoyal(hand):
	"""
	Helper method for isRoyalFlush()
	Checks if hand contains all royal cards
	"""
	values = []
	for card in hand:
		values.append(card[0])
	return ('a' in values and 'k' in values and 'q' in values and 'j' in values and 't' in values)

def getRanks(hand, sortedList=True, acesLow=False):
	"""
	Returns list of hand's ranks
	"""
	values = {'t' : 10, 'j' : 11, 'q' : 12, 'k' : 13, 'a' : 14, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9}
	if acesLow: values['a']=1
	ranks = []
	for card in hand:
		ranks.append(values.get(card[0]))
	if sortedList: ranks.sort()
	return ranks

def getMaxDifference(sortedList, maxDifference=1):
	"""
	Helper method for isStraight
	Checks the slope of numbers in a list for a given rate of change (maxDifference)
	"""
	differences = []
	for i in range(0,len(sortedList)-1):
		innerdiff = abs(sortedList[i]-sortedList[i+1])
		differences.append(innerdiff)
	for diffs in differences:
		if not diffs == maxDifference: return False
	return True

def getHighestCard(hand, acesLow=False):
	"""
	Returns the highest ranked card in a hand
	"""
	highestcard = "2"
	values = {'t' : 10, 'j' : 11, 'q' : 12, 'k' : 13, 'a' : 14, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9}
	if acesLow: values['a']=1
	for card in hand:
		if values.get(card[0]) > values.get(highestcard[0]): 
			highestcard = card
	return highestcard

def highCard(hand):
	values = {'t' : 10, 'j' : 11, 'q' : 12, 'k' : 13, 'a' : 14, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9}
	fakeswitch = {
		9:isRoyalFlush(hand, showHighCard=True),
		8:isStraightFlush(hand, showHighCard=True),
		7:isFourOfAKind(hand, showHighCard=True),
		6:isFullHouse(hand, showHighCard=True),
		5:isFlush(hand, showHighCard=True),
		4:isStraight(hand, showHighCard=True),
		3:isThreeOfAKind(hand, showHighCard=True),
		2:isTwoPair(hand, showHighCard=True),
		1:isPair(hand, showHighCard=True),
		0:getHighestCard(hand)
	}
	return values.get(fakeswitch.get(handType(hand))[0])

if __name__ == '__main__':
	"""
	print handType(['ts','ks','qs','as','js']), '=9'
	print handType(['5s','6s','7s','9s','8s']), '=8'
	print handType(['as','ac','4s','ad','ah']), '=7'
	print handType(['as','ac','4s','ad','4c']), '=6'
	print handType(['2s','4s','5s','ks','3s']), '=5'
	print handType(['2s','4s','5s','ac','3s']), '=4'
	print handType(['3s','ac','4s','4d','4h']), '=3'
	print handType(['as','ac','4s','4d','kh']), '=2'
	print handType(['as','2s','4s','6s','2c']), '=1'
	print handType(['7s','5c','4s','3s','2s']), '=0'
	
	print highCard(['ts','ks','qs','as','js']), '=14'
	print highCard(['as','ac','4s','ad','ah']), '=14'
	print highCard(['as','ac','4s','ad','4c']), '=14'
	print highCard(['2s','4s','5s','ks','3s']), '=13'
	print highCard(['2s','4s','5s','ac','3s']), '=5'
	print highCard(['3s','ac','4s','4d','4h']), '=4'
	print highCard(['as','ac','4s','4d','kh']), '=14'
	print highCard(['as','2s','4s','6s','2c']), '=2'
	print highCard(['7s','5c','4s','3s','2s']), '=7'
	print highCard(['as','2c','3s','4s','5s']), '=5'
	"""
