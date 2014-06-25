#!/usr/bin/python
import random

def evaluateCards(cards):
	cards.sort(key=lambda x: x[1])
	suitcount = [0]*4
	rankcount = [0]*13
	groupcount = [0]*5
	for card in cards: 
		suitcount[card[0]] += 1
		rankcount[card[1]] += 1
	straight = False
	run = 1 if rankcount[-1] == 1 else 0
	for count in rankcount:
		groupcount[count] += 1
		if count == 1:
			run += 1
			straight = straight or (run == 5)
		else:
			run = 0
	flush = max(suitcount) == 5
	
	cardNames = "Two Three Four Five Six Seven Eight Nine Ten Jack Queen King Ace".split()
	message = ""
	rank = 0
	if straight and flush and rankcount[-2] == 1 and rankcount[-1] == 1:
		rank = 10
		message += "Royal Straight Flush"	
	elif straight and flush: 
		rank = 9
		message += "Straight Flush"
	elif groupcount[4] == 1: 
		rank = 8
		message += "Four of a Kind"
	elif groupcount[3] == 1 and groupcount[2] == 1: 
		rank = 7
		message += "Full House"
	elif flush: 
		rank = 6
		message += "Flush"
	elif straight: 
		rank = 5
		message += "Straight"
	elif groupcount[3] == 1: 
		rank = 4
		message += "Three of a Kind"
	elif groupcount[2] == 2: 
		rank = 2
		message += "Two Pair"
	elif groupcount[2] == 1: 
		rank = 1
		message += "Pair of %ss" % (cardNames[rankcount.index(2)])
	else: 
		rank = 0
		message += cardNames[cards[-1][1]]+" High"
	return rank, message, cards

def getMax(current, othercards):
	if len(current) == 5:
		return evaluateCards(current)
	if len(current) + len(othercards) == 5:
		return evaluateCards(current+othercards)
	resultA = getMax(current, othercards[1:])
	resultB = getMax(current + othercards[:1], othercards[1:])
	if resultA[0] > resultB[0]:
		return resultA
	return resultB

def getPokerMessage():
	cardNames = "Two Three Four Five Six Seven Eight Nine Ten Jack Queen King Ace".split()
	cardNamesAbbr = "2 3 4 5 6 7 8 9 10 J Q K A".split()
	suitName = "Clubs Spades Hearts Diamonds".split()
	suitNamesAbbr = u"&#9827; &#9824; &#9829; &#9830;".split()
	colors = "white white red red".split()
	cards = [divmod(i,13) for i in range(52)]
	random.shuffle(cards)
	rank, message, cards = getMax([], cards[:8])
	random.shuffle(cards)
	test = "SweetieBot deals you a hand of poker!\n\n"
	abbrMessage = ""
	for card in cards:
		cardUrl = "http://www.random.org/playing-cards/%d.png" % ((12-card[1])*4 +card[0]+1)
		cardName = cardNames[card[1]] + " of " + suitName[card[0]]
		test += "[url][img]%s[/img]%s[/url] " % (cardUrl, cardName)
		abbrMessage += "[color=%s]%s%s[/color] " % (colors[card[0]], cardNamesAbbr[card[1]], suitNamesAbbr[card[0]])
	test += "\n(%s)\n\n[size=4][color=white]%s[/color][/size]" % (abbrMessage.strip(), message)
	return test
	

if __name__ == "__main__":
	for i in range(90): getPokerMessage()
