# CribCounter
# Program to enumerate all possible Cribbage hands and then score them
# Joe Jeffers
# 23 Apr 2015
# License GPL v2.0

# Global variables relating to decyfering the cards
values = {13:10,12:10,11:10,10:10,9:9,8:8,7:7,6:6,5:5,4:4,3:3,2:2,1:1}
suitName = {0:'Spades',1:'Hearts',2:'Clubs',3:'Diamonds'}
suitSym = {0:'\u2660',1:'\u2665',2:'\u2663',3:'\u2666'}

# Functions to turn the card ID into the needed values
def getCard(num):
	# Get the card number (1-13)
	return (((num - 1) % 13) + 1)
def getValue(num):
	# Get the card value (1-10)
	return values[getCard(num)]

# Function to get the suit labels from the card ID
def getSuitNum(num):
	return int((num-1)/13)
def getSuitSym(num):
	return suitSym[getSuitNum(num)]
def getSuitName(num):
	return suitName[getSuitNum(num)]

def makeHands():
	import itertools
	deckLength = 52
	deck = []
	hands = []
	cards = []

	i = 1
	while(i <= deckLength):
		deck.append(i)
		i += 1

	print('Finding card combinations...')
	draws = list(itertools.combinations(deck,4))

	print('Adding the cut card...')
	for card in deck:
		for draw in draws:
			hand = list(draw)
			if(card not in hand):
				hand.append(card)
				hands.append(hand)
	del draws
	return hands

def cribScore(hand):
	scoreBreakdown = {'total':0,'15s':0,'runs':0,'pairs':0,'flushes':0,'nobs':0}

	# -------15s---------
	fifScore  = score15s(hand)
	scoreBreakdown['15s'] += fifScore
	scoreBreakdown['total'] += fifScore

	# -------Runs--------
	runScore = scoreRuns(hand)
	scoreBreakdown['runs'] += runScore
	scoreBreakdown['total'] += runScore

	# ------Pairs--------
	paiScore = scorePairs(hand)
	scoreBreakdown['pairs'] += paiScore
	scoreBreakdown['total'] += paiScore

	#------Flushes-------
	fluScore  = scoreFlushes(hand)
	scoreBreakdown['flushes'] += fluScore
	scoreBreakdown['total'] += fluScore

	# -------Nobs---------
	nobScore = scoreNobs(hand)
	scoreBreakdown['nobs'] += nobScore
	scoreBreakdown['total'] += nobScore

	return scoreBreakdown

def scoreRuns(hand):
	suits = []
	suits.append([])
	suits.append([])
	suits.append([])
	suits.append([])
	score = 0

	for card in hand:
		suits[getSuitNum(card)].append(getCard(card))

	for suit in suits:
		suit.sort()
		length = 0
		saved = 0
		for card in suit:
			if(saved == 0):
				saved = card
				length = 1
			elif((saved+1) == card):
				saved = card
				length += 1
			elif(length >= 3):
				break
			else:
				saved = card
				length = 1
		if(length >= 3):
			score += length
			break

	return score

def score15s(hand):
	score = 0
	hand = powersetMod(hand,2,len(hand))
	values = []
	for comb in hand:
		num = 0
		for card in comb:
			num += getValue(card)
		if num == 15:
			score += 2
	return score

def scoreFlushes(hand):
	suits = []
	suits.append([])
	suits.append([])
	suits.append([])
	suits.append([])
	score = 0

	drawHand = hand[:4]
	cut = hand[-1]
	for card in drawHand:
		suits[getSuitNum(card)].append(getCard(card))

	i = 0
	while(i < 4):
		count = len(suits[i])
		if(count >= 4):
			score += count
			break
		i += 1

	# If the cut matches suit, add 1 to score
	if((score > 0) and (getSuitNum(cut) == i)):
		score += 1
	return score

def scorePairs(hand):
	hand = powersetMod(hand,2,2)
	score = 0
	for comb in hand:
		if(getCard(comb[0]) == getCard(comb[1])):
			score += 2
	return score

def scoreNobs(hand):
	cutSuit = getSuitNum(hand[4])
	hand = hand[:-1]
	score = 0
	for card in hand:
		if((getCard(card) == 11) and (getSuitNum(card) == cutSuit)):
			return 1
	return 0

def powersetMod(hand, minSize, maxSize):
	# Return the subset of the power set that has between min and max items
	import itertools
	sets = []
	for r in range(minSize,(maxSize+1)):
		sets += itertools.combinations(hand,r)
	return sets

def handPrinter(hand,score):
	ans = ''
	ans += str(score['total']) + ','
	ans += str(score['15s']) + ','
	ans += str(score['runs']) + ','
	ans += str(score['pairs']) + ','
	ans += str(score['nobs']) + ','
	ans += str(score['flushes']) + ','
	for card in hand:
		num = getCard(card)
		suit = getSuitSym(card)
		if(num < 11):
			ans += str(num)
		elif(num == 11):
			ans += 'J'
		elif(num == 12):
			ans += 'Q'
		else:
			ans += 'K'
		ans += ',' + suit + ','
	return ans[:-1] + '\n'

if __name__ == '__main__':
	# Find all possible hands
	print('Making hands....')
	x = makeHands()
	hands = len(x)
	print('Made hands, scoring...')

	# Open the Score File for printing
	out = open('cribScores.csv','w')
	out.write('Total,15s,Runs,Pairs,Nobs,Flushes,1c,1s,2c,2s,3c,3s,4c,4s,cutC,cutS\n')

	# Cycle through and score all of the hands
	i = 0
	for y in x:
		scores = cribScore(y)
		i += 1
		if(i%200000 == 0):
			print('At ' + str(i) + ' of ' + str(hands))
		out.write(handPrinter(y,scores))
	out.close()
