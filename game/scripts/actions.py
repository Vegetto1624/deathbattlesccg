#------------------------------------------------------------------------------
# Constant and Variables Values
#------------------------------------------------------------------------------
import re
import itertools

shields = []
playerside = None
sideflip = None
diesides = 6
shieldMarker = ('Shield', 'a4ba770e-3a38-4494-b729-ef5c89f561b7')

# Start of Automation code

cardScripts = {
		# ON PLAY EFFECTS
                
		# ON CAST EFFECTS
               
		# ON BANISH EFFECTS
   }

# Functions used in the Automation dictionaries.


def SummonFromGrave(count=1, TypeFilter = "ALL", CivFilter = "ALL", RaceFilter = "ALL", noEvo = True): #Temporary Fix for not allowing Evolutions
	mute()
	for i in range(0,count):
		if TypeFilter != "ALL" and noEvo:
			cardsInGroup_Type_Filtered = [card for card in me.piles["Graveyard"] if re.search(TypeFilter,card.Type) and not re.search("Evolution",card.type)]
		else:
			cardsInGroup_Type_Filtered = [card for card in me.piles["Graveyard"]]
		if CivFilter != "ALL":
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered if re.search(CivFilter,card.properties['Civilization'])]
		else:
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered]
		if RaceFilter != "ALL":
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered if re.search(RaceFilter,card.properties['Race'])]
		else:
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered]
		if len(cardsInGroup_CivTypeandRace_Filtered) == 0: return
		choice = askCard(cardsInGroup_CivTypeandRace_Filtered, 'Choose a Card  to Summon from the Graveyard','Graveyard')
		if type(choice) is not Card: break
		toPlay(choice)

def lookAtTopCards(num, targetZone='hand'):
    mute()
    notify("{} looks at the top {} cards of their deck".format(me,num))
    cardList = [card for card in me.Deck.top(num)]
    choice = askCard(cardList, 'Choose a card to take')
    toHand(choice, show = True)
    for counter in range(num-1, 0, -1):
        cardList = [card for card in me.Deck.top(counter)]
        choice = askCard(cardList, 'Choose card to put to bottom','To Bottom')
        choice.moveToBottom(me.Deck)
        notify("{} moves card #{} to the bottom of their deck.".format(me, num-counter))

def targetDiscard(randomDiscard = False, targetZone = 'grave'):
    mute()
    currentPlayers = getPlayers()
    playerList = []
    cardList = []
    for player in currentPlayers:
        playerList.append(player.name)
    choicePlayer = askChoice("Pick a player:", playerList)
    if choicePlayer < 1: return
    targetPlayer = currentPlayers[choicePlayer-1]
    cardList = [card for card in targetPlayer.hand]
    if randomDiscard:
        remoteCall(targetPlayer,'randomDiscard',targetPlayer.hand)
        return
    cardChoice = askCard(cardList, 'Choose a Card to discard','Discard')
    if type(cardChoice) is not Card: 
        notify("{} - Error".format(type(cardChoice)))
        return
    if targetZone == 'shields': 
        whisper("Setting {} as shield.".format(cardChoice))
        remoteCall(targetPlayer,'toShields',cardChoice) 
    elif targetZone == 'grave':
        remoteCall(targetPlayer,'toDiscard',cardChoice)

def in_play(card, x=0, y=0):
  if card.group != table:
    return False

def flipCard(card, x, y):
    if card.isFaceUp:
        card.isFaceUp = False
        notify("{} ha ribaltato {}.".format(me, card))
    else:
        card.isFaceUp = True
        notify("{} ha ribaltato {} di nuovo.".format(me, card))

def addToken(card, x, y):
    markers = ["markers/fate.png", "markers/political.png"]
    marker = askChoice("Scegli un segnalino da aggiungere alla carta:", markers)
    if marker is not None:
	marker_image = markerImage(markers[marker])
        card.markers[markers[marker]] += 1
    
def discardAll():
	mute()
	currentPlayers = getPlayers()
	playerList = []
	cardList = []
	for player in currentPlayers:
		playerList.append(player.name)
	choicePlayer = askChoice("Pick a player:", playerList)
	if choicePlayer < 1: return
	targetPlayer = currentPlayers[choicePlayer-1]
	cardList = [card for card in targetPlayer.hand]
	for card in cardList:
		remoteCall(targetPlayer, 'toDiscard', card)
        
def fromMana(count = 1, TypeFilter = "ALL", CivFilter = "ALL", RaceFilter = "ALL", show = True, toGrave = False, ApplyToAllPlayers = False):
    mute()
    if ApplyToAllPlayers == True:
        playerList = players
    else:
        playerList = [players[0]]
    for player in playerList:
        for i in range(0,count):
            if TypeFilter != "ALL":
                cardsInGroup_Type_Filtered = [card for card in table if isMana(card) and card.owner==me and re.search(TypeFilter,card.Type)]
            else:
                cardsInGroup_Type_Filtered = [card for card in table if isMana(card) and card.owner==me]
            if CivFilter != "ALL":
                cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered if re.search(CivFilter,card.properties['Civilization'])]
            else:
                cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered]
            if RaceFilter != "ALL":
                cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered if re.search(RaceFilter,card.properties['Race'])]
            else:
                cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered]
            if len(cardsInGroup_CivTypeandRace_Filtered) == 0: return
            choice = askCard(cardsInGroup_CivTypeandRace_Filtered, 'Choose a Card from the Mana Zone','Mana Zone')
            if type(choice) is not Card: break
            if toGrave == True: remoteCall(player,"banish",choice)
            else: remoteCall(player,"toHand",[choice, show])

def killAndSearch(play = False, singleSearch = False):
	mute()
	cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type)]
	if len(cardList)==0: return    
	choice = askCard(cardList, 'Choose a Creature to destroy')
	if type(choice) is not Card: return
	card = choice
	remoteCall(choice.owner,'banish',choice)
	if singleSearch:
		return
	else:
		remoteCall(choice.owner,'loopThroughDeck',[card, play])

def loopThroughDeck(card, play = False):
	group = card.owner.Deck
	if len(group) == 0: return
	newCard = group[0]
	newCard.isFaceUp = True
	notify("{} reveals {}".format(card.owner,newCard.name))
	rnd(1,1000)
	if re.search("Creature", newCard.Type) and not re.search("Evolution Creature", newCard.Type):
		if play == True:
			remoteCall(newCard.owner,'toPlay',newCard)
			return
		else:
			remoteCall(newCard.owner,'moveTo',newCard.owner.hand)
			return
	else:
		remoteCall(newCard.owner,'toDiscard',newCard)
		remoteCall(newCard.owner,'loopThroughDeck',[card, play])

def search(group, count = 1, TypeFilter = "ALL" , CivFilter = "ALL", RaceFilter = "ALL", show = True, x = 0, y = 0):
	mute()
	if len(group) == 0: return
	for i in range(0,count):
		cardsInGroup = [card for card in group]
		if TypeFilter != "ALL":
			cardsInGroup_Type_Filtered = [card for card in group if re.search(TypeFilter,card.Type)]
		else:
			cardsInGroup_Type_Filtered = [card for card in group]
		if CivFilter != "ALL":
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered if re.search(CivFilter,card.properties['Civilization'])]
		else:
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered]
		if RaceFilter != "ALL":
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered if re.search(RaceFilter,card.properties['Race'])]
		else:
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered]
		while (True):
			choice = askCard(cardsInGroup, 'Search card to take to hand (1 at a time)')
			if type(choice) is not Card: 
				group.shuffle()
				notify("{} finishes searching his/her {}.".format(me, group.name))
				return
			if choice in cardsInGroup_CivTypeandRace_Filtered:
				toHand(choice, show)
				break
	group.shuffle()
	notify("{} finishes searching his/her {}.".format(me, group.name))

def kill(powerFilter = 'ALL', tapFilter='ALL', civFilter='ALL', count = 1, targetOwn = False):
    mute()
    if powerFilter == 'ALL':
        powerFilter = float('inf')
    for i in range(0, count):
        if targetOwn:
            cardList = [card for card in table if isCreature(card) and int(card.Power) <= powerFilter]
        else:
            cardList = [card for card in table if isCreature(card) and not card.owner==me and int(card.Power) <= powerFilter]
        if tapFilter != 'ALL':
            if tapFilter == 'Untap':
                cardList = [card for card in cardList if card.orientation == Rot0]
            if tapFilter == 'Tap':
                cardList = [card for card in cardList if card.orientation == Rot90]
        if civFilter != "ALL":
            cardList = [card for card in cardList if re.search(civFilter,card.Civilization)]
        if len(cardList)==0:
            return    
        choice = askCard(cardList, 'Choose a Creature to destroy')
        if type(choice) is not Card:
            return
        if choice.owner == me:
            banish(choice)
        else:
            remoteCall(choice.owner,"banish",choice)

def banishAll(group, condition = False, powerFilter = 'ALL', civFilter = "ALL", AllExceptFiltered = False):
    mute()
    if powerFilter == 'ALL':
        powerfilter = float('inf')
    if condition == False:
        return
    cardlist = []
    if civFilter == "ALL":
        cardList = [card for card in group if isCreature(card) and int(card.Power) <= powerFilter]
    else:
        if AllExceptFiltered:
            cardList = [card for card in group if isCreature(card) and int(card.Power) <= powerFilter and not re.search(civFilter,card.properties['Civilization'])]
        else:
            cardList = [card for card in group if isCreature(card) and int(card.Power) <= powerFilter and re.search(civFilter,card.properties['Civilization'])]
    if len(cardList)==0:
        return
    for card in cardList:
        cardToBeSaved = card
        possibleSavers = [card for card in table if cardToBeSaved != card and isCreature(card) and card.owner == me and re.search("Saver",card.rules) and (re.search(cardToBeSaved.properties['Race'],card.rules) or re.search("Saver: All Races",card.rules))]
        if len(possibleSavers) > 0:
            if confirm("Prevent {}'s destruction by using a Saver on your side of the field?\n\n".format(cardToBeSaved.Name)):
                choice = askCard(possibleSavers, 'Choose Saver to banish')
                if type(choice) is Card:
                    toDiscard(choice)
                    cardList.remove(choice)
                    cardList = [card for card in cardList]
                    notify("{} banishes {} to prevent {}'s destruction.".format(me, choice.name, cardToBeSaved.name))
                    continue
        if cardToBeSaved.owner == me:   
            toDiscard(cardToBeSaved)
            
            if cardScripts.get(card.name,{}).get('onDestroy',{}):
                functionDict = cardScripts.get(card.name).get('onDestroy')
                for function in functionDict:
                    argList = functionDict.get(function)
                    eval(function)(*[eval(arg) for arg in argList])
        else:
            remoteCall(cardToBeSaved.owner,"banish",cardToBeSaved)

def destroyMana(count = 1):
    mute()
    for i in range(0,count):
        cardList = [card for card in table if isMana(card) and not card.owner==me]
        if len(cardList)==0:
            return
        choice = askCard(cardList, 'Choose a Mana Card to destroy')
        if type(choice) is not Card:
            return        
        remoteCall(choice.owner,"banish",choice)

def destroyShield(owner = True):
    mute()
    if owner == True:
            cardList = [card for card in table if isShield(card) and not card.owner==me]
    else:
            cardList = [card for card in table if isShield(card) and card.owner==me]
    if len(cardList)==0:
            return
    choice = askCard(cardList, 'Choose a shield to send to graveyard')
    if type(choice) is not Card:
            return        
    remoteCall(choice.owner,"banish",[choice,True])

def align():
    mute()
    global playerside  ##Stores the Y-axis multiplier to determine which side of the table to align to
    global sideflip  ##Stores the X-axis multiplier to determine if cards align on the left or right half
    if sideflip == 0:  ##the 'disabled' state for alignment so the alignment positioning doesn't have to process each time
        return "BREAK"
    if Table.isTwoSided():
        if playerside == None:  ##script skips this if playerside has already been determined
            if me.hasInvertedTable():
                playerside = 1  #inverted (negative) side of the table
            else:
                playerside = 1
        if sideflip == None:  ##script skips this if sideflip has already been determined
            playersort = sorted(getPlayers(), key=lambda player: player._id)  ##makes a sorted players list so its consistent between all players
            playercount = [p for p in playersort if me.hasInvertedTable() == p.hasInvertedTable()]  ##counts the number of players on your side of the table
            if len(playercount) > 2:  ##since alignment only works with a maximum of two players on each side
                whisper("Cannot align: Too many players on your side of the table.")
                sideflip = 0  ##disables alignment for the rest of the play session
                return "BREAK"
            if playercount[0] == me:  ##if you're the 'first' player on this side, you go on the positive (right) side
                sideflip = 1
            else:
                sideflip = -1
    else:  ##the case where two-sided table is disabled
        whisper("Cannot align: Two-sided table is required for card alignment.")
        sideflip = 0  ##disables alignment for the rest of the play session
        return "BREAK"
    cardorder = [[],[],[]]
    evolveDict = eval(me.getGlobalVariable("evolution"))
    for card in table:
        if card.controller == me and not isFortress(card) and not card._id in list(itertools.chain.from_iterable(evolveDict.values())):
            if isShield(card):
                cardorder[1].append(card)
            elif isMana(card):
                cardorder[2].append(card)
            else: ##collect all creatures
                cardorder[0].append(card)
    xpos = 80
    ypos = 5 + 10*(max([len(evolveDict[x]) for x in evolveDict]) if len(evolveDict) > 0 else 1)
    for cardtype in cardorder:
        if cardorder.index(cardtype) == 1:
            xpos = 80
            ypos += 93
        elif cardorder.index(cardtype) == 2:
            xpos = 80
            ypos += 93
        for c in cardtype:
            x = sideflip * xpos
            y = playerside * ypos + (44*playerside - 44)
            if c.position != (x,y):
                c.moveToTable(x,y)
            xpos += 79
    for evolution in evolveDict:
        count = 0
        for evolvedCard in evolveDict[evolution]:
            x, y = Card(evolution).position
            count += 1
            Card(evolvedCard).moveToTable(x, y - 10*count*playerside)
            Card(evolvedCard).sendToBack()
        
def fromDeck():
    mute()
    notify("{} looks at their Deck.".format(me))
    me.Deck.lookAt(-1)

def fromGrave():
    mute()
    notify("{} looks at their Graveyard.".format(me))
    me.piles['Graveyard'].lookAt(-1)

def lookAtCards(count = 1, isTop = True):
	mute()
	if isTop == False: 
		notify("{} looks at {} cards from bottom of their deck.".format(me, count))
	notify("{} looks at {} cards from top of their deck.".format(me, count))
	me.Deck.lookAt(count, isTop)

def sacrifice(power = float('inf'), count = 1):
	mute()
	for i in range(0, count):
		cardList = [card for card in table if isCreature(card) and card.owner==me and re.search("Creature", card.Type)]
		cardList = [card for card in cardList if int(card.Power) <= power]
		if len(cardList)==0:
			return    
		choice = askCard(cardList, 'Choose a Creature to destroy')
		if type(choice) is not Card:
			return
		banish(choice)
    
def bounce(count = 1, opponentOnly = False):
	mute()
	for i in range(0,count):
		if opponentOnly:
			cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type) and card.owner != me]
		else:   
			cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type)]
		if len(cardList) < 1:
			return
		choice = askCard(cardList,'Choose a Creature to return to Hand')
		if type(choice) is not Card:
			return
		if choice.owner==me:
			toHand(choice)
		else:
			remoteCall(choice.owner,"toHand",choice)
    
def bounceAndDiscard(bcount = 1, opponentOnly = True, randomDiscard=True):
    mute()
    bounce(bcount, opponentOnly)
    targetDiscard(randomDiscard)
    
def gear(str):        
    mute()
    if str == 'kill':
        cardList = [card for card in table if isGear(card)
                    and not card.owner == me]
        if len(cardList) == 0:
            return
        choice = askCard(cardList,'Choose a Cross Gear to send to Graveyard')
        if type(choice) is not Card:
            return
        remoteCall(choice.owner, 'banish', choice)
    elif str == 'bounce':
        cardList = [card for card in table if isGear(card)]
        if len(cardList) == 0:
            return
        choice = askCard(cardList, 'Choose a Cross Gear to send to Hand')
        if type(choice) is not Card:
            return
        if choice.owner == me:
            toHand(choice)
        else:
            remoteCall(choice.owner, 'toHand', choice)
    elif str == 'mana':
        cardList = [card for card in table if isGear(card)]
        if len(cardList) == 0:
            return
        choice = askCard(cardList, 'Choose a Cross Gear to send to Mana')
        if type(choice) is not Card:
            return
        if choice.owner == me:
            toHand(choice)
        else:
            remoteCall(choice.owner, 'toMana', choice)

def sendToShields(count=1):
    mute()
    for i in range(0,count):
            cardList = [card for card in table if isCreature(card) and card.owner != me]
            if len(cardList)==0: return
            choice = askCard(cardList,'Choose a Creature to send to shields')
            if type(choice) is not Card: return
            remoteCall(choice.owner,"toShields",choice)

def sendToMana(count=1):
    mute()
    for i in range(0,count):
            cardList = [card for card in table if isCreature(card) and card.owner != me]
            if len(cardList)==0: return
            choice = askCard(cardList,'Choose a Creature to send to mana')
            if type(choice) is not Card: return
            remoteCall(choice.owner,"toMana",choice)

def tapCreature(count = 1, targetALL = False, includeOwn = False):
    mute()
    if targetALL:
        if includeOwn == True: 
            cardList = [card for card in table if isCreature(card) and card.orientation == Rot0 and re.search("Creature", card.Type)]
        else:
            cardList = [card for card in table if isCreature(card) and card.orientation == Rot0 and not card.owner==me and re.search("Creature", card.Type)]
        if len(cardList)==0:
            return
        for card in cardList:
            remoteCall(card.owner,"tap",card)
    else:
        for i in range(0,count):
            if includeOwn == True: 
                cardList = [card for card in table if isCreature(card) and card.orientation == Rot0 and re.search("Creature", card.Type)]
            else:
                cardList = [card for card in table if isCreature(card) and card.orientation == Rot0 and not card.owner==me and re.search("Creature", card.Type)]
            if len(cardList)==0:
                return
            choice = askCard(cardList, 'Choose a Creature to tap')
            if type(choice) is not Card:
                return
            remoteCall(choice.owner,"tap",choice)
		
def semiReset():
    mute()
    if confirm("Are you sure you want to continue?"):
        currentPlayers = getPlayers()	
        for player in currentPlayers:
            cardsInHand = [c for c in player.hand] 
            cardsInGrave = [c for c in player.piles['Graveyard']]
            if cardsInHand or cardsInGrave:
                for card in cardsInHand: 
                    remoteCall(player, 'toDeckTop', card) 
                for card in cardsInGrave: 
                    remoteCall(player, 'toDeckTop', card)
            remoteCall(player,'shuffle', player.deck)
            remoteCall(player,'draw', [player.deck, False, 5])

def suicide(name, action, arg):
	mute()
	choiceList = ['Yes', 'No']
	colorsList = ['#FF0000', '#FF0000']
	choice = askChoice("Banish the card to activate effect?", choiceList, colorsList)
	if choice == 0 or choice == 2:
		return
	cardList = [card for card in table if isCreature(card) and card.owner==me and re.search("Creature", card.type)]
	cardList = [card for card in cardList if card.name==name]
	toDiscard(cardList[-1])
	notify("{} destroys {}.".format(me, name))
	action(arg)

#End of Automation Code

def awaken(card, x = 0, y = 0):
    mute()
    if (re.search("Psychic", card.Type)):
        altName = card.alternateProperty('awakening', 'name')
        if card.alternate is '':
            card.switchTo('awakening')
            notify("{}'s' {} awakens to {}.".format(me, altName, card))
            align()
            return
        else:
            card.switchTo('')
            notify("{}'s {} reverts to {}.".format(me, altName, card))
            align()
            return

def toHyperspatial(card, x = 0, y = 0, notifymute = False):
    mute()
    if card.alternate is not '' and re.search("{RELEASE}", card.Rules):
        awaken(card)
        return
    else:
        card.moveTo(me.Hyperspatial)
        align()
        if notifymute == False:
            notify("{}'s {} returns to the Hyperspatial Zone.".format(me, card))

def resetGame():
    mute()
    me.setGlobalVariable("shieldCount", "0")

def moveCards(player, card, fromGroup, toGroup, oldIndex, index, oldX, oldY, x, y, highlights, markers, faceup):
    ## This trigger updates the evolution dictionary in the event one of the cards involved in an evolution leaves the battlezone.
    mute()
    if player != me: ##Ignore for cards you don't control
        return
    if table not in fromGroup: ## we only want cases where a card is being moved from table to another group
        return
    evolveDict = eval(me.getGlobalVariable("evolution"))
    for evo in evolveDict.keys():
        if Card(evo) not in table:
            del evolveDict[evo]
        else:
            evolvedList = evolveDict[evo]
            for evolvedCard in evolvedList:
                if Card(evolvedCard) not in table:
                    evolvedList.remove(evolvedCard)
            if len(evolvedList) == 0:
                del evolveDict[evo]
            else:
                evolveDict[evo] = evolvedList
    if evolveDict != eval(me.getGlobalVariable("evolution")):
        me.setGlobalVariable("evolution", str(evolveDict))

def isCreature(card):
    mute()
    if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270 and re.search("Creature", card.Type):
        return True
    else:
        return False

def isGod(card):
    mute()
    if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270 and re.search("Creature", card.Type) and re.search("God", card.Race):
        return True
    else:
        return False

def isGear(card):
    mute()
    if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270 and re.search("Cross Gear", card.Type):
        return True
    else:
        return False

def isFortress(card):
    mute()
    if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270 and re.search("Fortress", card.Type):
        return True
    else:
        return False

def isMana(card):
    mute()
    if card in table and card.isFaceUp and not card.orientation == Rot90 and not card.orientation == Rot0:
        return True
    else:
        return False

def isShield(card):
    mute()
    if card in table and not card.isFaceUp:
        return True
    else:
        return False

def isPsychic(card):
    mute()
    if re.search("Psychic", card.Type):
        return True
    else:
        return False

def metamorph():
    mute()
    cardList = [card for card in table if isMana(card) and card.owner== me]
    if len(cardList) < 7:
        return False
    else:
        return True

def clear(card, x = 0, y = 0):
    mute()
    card.target(False)

def setup(group, x = 0, y = 0):
    mute()
    
    cardsInTable = [c for c in table if c.controller == me and c.owner == me and not isPsychic(c)]
    cardsInHand = [c for c in me.hand if not isPsychic(c)]
    cardsInGrave = [c for c in me.piles['Graveyard'] if not isPsychic(c)]
    
    psychicsInTable = [c for c in table if c.controller == me and c.owner == me and isPsychic(c)]
    psychicsInHand = [c for c in me.hand if isPsychic(c)]
    psychicsInGrave = [c for c in me.piles['Graveyard'] if isPsychic(c)]
    
    if cardsInTable or cardsInHand or cardsInGrave or psychicsInTable or psychicsInGrave or psychicsInHand:
        if confirm("Are you sure you want to setup battlezone? Current setup will be lost"):
            
            for card in cardsInTable:
                card.moveTo(me.Deck)
            for card in cardsInHand:
                card.moveTo(me.Deck)
            for card in cardsInGrave:
                card.moveTo(me.Deck)

            for card in psychicsInTable:
                card.moveTo(me.Hyperspatial)
            for card in psychicsInHand:
                card.moveTo(me.Hyperspatial)
            for card in psychicsInGrave:
                card.moveTo(me.Hyperspatial)
        else:
            return
    if len(me.Deck) < 10: #We need at least 10 cards to properly setup the game
        whisper("Not enough cards in deck")
        return

    cardsInDeck = [c for c in me.Deck]
    for card in cardsInDeck:
        if isPsychic(card):
            whisper("You cannot have Psychic creatures in your main deck")
            return

    me.setGlobalVariable("shieldCount", "0")
    me.setGlobalVariable("evolution", "{}")
    me.Deck.shuffle()
    rnd(1,10)
    for card in me.Deck.top(5): toShields(card, notifymute = True)
    for card in me.Deck.top(5): card.moveTo(card.owner.hand)
    align()
    notify("{} sets up their battle zone.".format(me))
            
def rollDie(group, x = 0, y = 0):
    mute()
    global diesides
    n = rnd(1, diesides)
    notify("{} rolls {} on a {}-sided die.".format(me, n, diesides))

def untapAll(group, x = 0, y = 0):
    mute()
    for card in group:
        if not card.owner == me:
            continue
        if card.orientation == Rot90:
            card.orientation = Rot0
        if card.orientation == Rot270:
            card.orientation = Rot180
    notify("{} untaps all their cards.".format(me))
    
def tap(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} taps {}.'.format(me, card))
    else:
        notify('{} untaps {}.'.format(me, card))

def banish(card, dest = False, x = 0, y = 0):
    mute()
    if isShield(card):
        if dest == True:
            toDiscard(card)
            return
        card.peek()
        rnd(1,10)
        if re.search("{SHIELD TRIGGER}", card.Rules):
            if confirm("Activate Shield Trigger for {}?\n\n{}".format(card.Name, card.Rules)):
                card.isFaceUp = True
                toPlay(card, notifymute = True)
                rnd(1,10)
                notify("{} uses {}'s Shield Trigger.".format(me, card))
                return
        shieldCard = card
        cardsInHandWithStrikeBackAbility = [card for card in me.hand if re.search("Strike Back", card.rules)]
        if len(cardsInHandWithStrikeBackAbility) > 0:
            cardsInHandWithStrikeBackAbilityThatCanBeUsed = [card for card in cardsInHandWithStrikeBackAbility if re.search(card.Civilization, shieldCard.Civilization)]
            if len(cardsInHandWithStrikeBackAbilityThatCanBeUsed) > 0:
                if confirm("Activate Strike Back by sending {} to the graveyard?\n\n{}".format(shieldCard.Name, shieldCard.Rules)):
                    choice = askCard(cardsInHandWithStrikeBackAbilityThatCanBeUsed, 'Choose Strike Back to activate')
                    if type(choice) is Card:
                        shieldCard.isFaceUp = True
                        rnd(1,100)
                        toPlay(choice, notifymute = True)
                        toDiscard(shieldCard)
                        notify("{} banishes {} to use {}'s Strike Back.".format(me, shieldCard.name, choice.name))
                        return
        notify("{}'s shield #{} is broken.".format(me, shieldCard.markers[shieldMarker]))
        shieldCard.moveTo(shieldCard.owner.hand)
    else:
            cardToBeSaved = card
            possibleSavers = [card for card in table if cardToBeSaved != card and isCreature(card) and card.owner == me and re.search("Saver",card.rules) and (re.search(cardToBeSaved.properties['Race'],card.rules) or re.search("Saver: All Races",card.rules))]
            if len(possibleSavers) > 0:
                    if confirm("Prevent {}'s destruction by using a Saver on your side of the field?\n\n".format(cardToBeSaved.Name)):
                            choice = askCard(possibleSavers, 'Choose Saver to banish')
                            if type(choice) is Card:
                                    toDiscard(choice)
                                    notify("{} banishes {} to prevent {}'s destruction.".format(me, choice.name, cardToBeSaved.name))
                                    return
            toDiscard(cardToBeSaved)
            if cardScripts.get(card.name,{}).get('onDestroy',{}):
                functionDict = cardScripts.get(card.name).get('onDestroy')
                for function in functionDict:
                    argList = functionDict.get(function)
                    eval(function)(*[eval(arg) for arg in argList])


def shuffle(group, x = 0, y = 0):
    mute()
    if len(group)==0:return
    for card in group:
        if card.isFaceUp:
            card.isFaceUp = False
    group.shuffle()
    notify("{} shuffled their {}".format(me, group.name))

def draw(group, conditional = False, count = 1, x = 0, y = 0):
    mute()
    for i in range(0,count):
        if len(group) == 0:
            return
        if conditional == True:
            choiceList = ['Yes', 'No']
            colorsList = ['#FF0000', '#FF0000']
            choice = askChoice("Draw a card?", choiceList, colorsList)
            if choice == 0 or choice == 2:
                return 
        card = group[0]
        card.moveTo(card.owner.hand)
        notify("{} draws a card.".format(me))

def drawX(group, x = 0, y = 0):
    if len(group) == 0: return
    mute()
    count = askInteger("Draw how many cards?", 7)
    if count == None: return
    for card in group.top(count): card.moveTo(card.owner.hand)
    notify("{} draws {} cards.".format(me, count))
    
def mill(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group[0]
    toDiscard(card, notifymute = True)
    notify("{} discards top card of Deck.".format(me))
    
def millX(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    count = askInteger("Discard how many cards?", 1)
    if count == None: return
    for card in group.top(count): toDiscard(card, notifymute = True)
    notify("{} discards top {} cards of Deck.".format(me, count))

def randomDiscard(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    card = group.random()
    toDiscard(card, notifymute = True)
    rnd(1,10)
    notify("{} randomly discards {}.".format(me, card))

def mana(group, count = 1, x = 0, y = 0):
	mute()
	for i in range(0,count):
		if len(group) == 0: return
		card = group[0]
		toMana(card, notifymute = True)
		notify("{} charges top card of {} as mana.".format(me, group.name))
		
def massMana(group, conditional = False, x=0, y=0):
    	mute()
    	cardList = [card for card in table if isMana(card) and card.owner== me]
    	count = len(cardList)
    	if conditional == True: 
        	choiceList = ['Yes', 'No'] 
        	colorsList = ['#FF0000', '#FF0000']
        	choice = askChoice("Put top {} cards to mana?".format(count), choiceList, colorsList)
        	if choice == 0 or choice == 2: return 
    	for i in range(0,count):         
        	if len(group) == 0: return
        	card = group[0]         
        	toMana(card, notifymute = True)
        	if card.orientation & Rot90 != Rot90:
            		card.orientation ^= Rot90
    	notify("{} charges top {} cards of {} as mana.".format(me, count, group.name))
    
def endTurn(table,x=0,y=0):
    mute()
    notify("{} ha passato il turno.".format(me))

def gainPE (group,x=0,y=0):
	if me.isActive:
		me.PE += 1
	mute()

def calculate_damage(group, x, y):
    number_from_user = askInteger("Inserisci il valore base per il calcolo", 0)
    if number_from_user is None:  # User cancelled the action
        return
    damage = rnd(1, 6)*number_from_user
    dado = damage/number_from_user
    mute()
    notify("Sono {} danni. Il dado era {}".format(damage, dado))

def calculate_percent(group, x, y):
    number_from_user = askInteger("Inserisci il valore base per il calcolo", 0)
    percentage_from_user = askInteger("Inserisci la percentuale (%) per il calcolo", 0)
    if number_from_user is None:  # User cancelled the action
        return
    if percentage_from_user is None:  # User cancelled the action
        return
    percent = number_from_user*percentage_from_user/100
    mute()
    notify("Risultato: {}.".format(percent))

def cooldownA(card, x = 0, y = 0):
    number_from_user = askInteger("Di quanti turni hai bisogno?", 0)
    if number_from_user is None:  # User cancelled the action
        return
    DelayedNotification(message="{} turns have passed. {} recovered its ability.".format(number_from_user, card.name), turn_delay=number_from_user, card=card)

def cooldownE(card, x = 0, y = 0):
    number_from_user = askInteger("Di quanti turni hai bisogno?", 0)
    if number_from_user is None:  # User cancelled the action
        return
    DelayedNotification(message="{} turns have passed. {}'s effect has ended.".format(number_from_user, card.name), turn_delay=number_from_user, card=card)

class DelayedNotification(object):
    delayed_notifications = []

    def __init__(self, message, turn_delay, card):
        self.message = message
        self.turn_delay = turn_delay
        self.card = card
        self.delayed_notifications.append(self)

    @classmethod
    def on_new_turn(cls):
        for notification in cls.delayed_notifications:
            notification.turn_delay -= 1
            if notification.turn_delay <= 0:
                notify(notification.message)
            else:
                notify("{} turn(s) left for {}'s ability".format(notification.turn_delay, notification.card))

        # We preserve only those notifications with turn_delay above 0, because we've printed the other ones already.
        cls.delayed_notifications = [notification for notification in cls.delayed_notifications if notification.turn_delay > 0]

def on_turn_passed(_args):
    if getActivePlayer() != me:
        return
    DelayedNotification.on_new_turn()

def shields(group, count = 1, conditional = False, x = 0, y = 0):
	mute()
	if conditional == True:
		maxCount = count
		count = askInteger("Set how many cards as shields? (Max = {})".format(maxCount), maxCount)
		if count == 0 or count > maxCount: return
	for card in group.top(count):
		if len(group) == 0: return
		card = group[0]
		toShields(card, notifymute = True)
		notify("{} sets top card of {} as shield.".format(me, group.name))

def toMana(card, x = 0, y = 0, notifymute = False):
    mute()
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be placed into your mana zone.\nWould you like to override this?"):
            return
    if isMana(card):
        whisper("This is already mana")
        return
    if isPsychic(card):
        toHyperspatial(card)
        return
    card.moveToTable(0,0)
    card.orientation = Rot180
    if re.search("/", card.Civilization):
        card.orientation = Rot270
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                Card(evolvedCard).orientation = Rot180
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    align()
    if notifymute == False:
        notify("{} charges {} as mana.".format(me, card))

def toShields(card, x = 0, y = 0, notifymute = False, alignCheck = True, ignoreEvo = False):
    mute()
    if isShield(card):
        whisper("This is already a shield.")
        return
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if ignoreEvo == False and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be placed into your shield zone.\nWould you like to override this?"):
            return
    if isPsychic(card):
        toHyperspatial(card)
        return
    count = int(me.getGlobalVariable("shieldCount")) + 1
    me.setGlobalVariable("shieldCount", convertToString(count))
    if notifymute == False:
        if isCreature(card) or isMana(card):  ##If a visible card in play is turning into a shield, we want to record its name in the notify
            notify("{} sets {} as shield #{}.".format(me, card, count))
        else:
            notify("{} sets a card in {} as shield #{}.".format(me, card.group.name, count))

    card.moveToTable(0,0,True)
    if card.isFaceUp:
        card.isFaceUp = False
    if card.orientation != Rot0:
        card.orientation = Rot0
    card.markers[shieldMarker] = count
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                toShields(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    if alignCheck:
        align()
        
def toPlay(card, x = 0, y = 0, notifymute = False, evolveText = ''):
    mute()
    if card.Type == "Spell":
        if re.search("Charger", card.name):
            toMana(card)
        else:
            card.moveTo(card.owner.piles['Graveyard'])
    else:
        if re.search("Evolution", card.Type):
            targets = [c for c in table
                        if c.controller == me
                        and c.targetedBy
                        and c.targetedBy == me]
            targets = [c for c in targets
                       if isCreature(c)
                       or isGear(c)]
            for c in targets:
                c.target(False) #remove the targets
            if len(targets) == 0:
                whisper("Cannot play card: You must target a creature to evolve first.")
                whisper("Hint: Shift-click a card to target it.")
                return
            else:
                targetList = [c._id for c in targets]
                evolveDict = eval(me.getGlobalVariable("evolution")) ##evolveDict tracks all cards 'underneath' the evolution creature
                for evolveTarget in targets: ##check to see if the evolution targets are also evolution creatures
                    if evolveTarget._id in evolveDict: ##if the card already has its own cards underneath it
                        if isCreature(evolveTarget):
                            targetList += evolveDict[evolveTarget._id] ##add those cards to the new evolution creature
                        del evolveDict[evolveTarget._id]
                evolveDict[card._id] = targetList
                me.setGlobalVariable("evolution", str(evolveDict))
                evolveText = ", evolving {}".format(", ".join([c.name for c in targets]))
        if card.group == table:
            card.moveTo(me.hand)
        card.moveToTable(0,0)
        if shieldMarker in card.markers:
            card.markers[shieldMarker] = 0
        align()
    if notifymute == False:
        notify("{} plays {}{}.".format(me, card, evolveText))
        
    if metamorph():
        if cardScripts.get(card.name,{}).get('onMetamorph',{}):
            functionDict = cardScripts.get(card.name).get('onMetamorph')
            for function in functionDict:
                argList = functionDict.get(function)
                eval(function)(*[eval(arg) for arg in argList])
            return

    if cardScripts.get(card.name,{}).get('onPlay',{}):
        functionDict = cardScripts.get(card.name).get('onPlay')
        for function in functionDict:
            argList = functionDict.get(function)
            eval(function)(*[eval(arg) for arg in argList])
    
def toDiscard(card, x = 0, y = 0, notifymute = False, alignCheck = True, ignoreEvo = False):
    mute()
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if ignoreEvo == False and isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be banished.\nWould you like to override this?"):
            return
    if isPsychic(card):
        toHyperspatial(card)
        return    
    src = card.group
    card.moveTo(card.owner.piles['Graveyard'])
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                toDiscard(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    if notifymute == False:
        if src == table:
            notify("{} banishes {}.".format(me, card))
            if alignCheck:
                align()
        else:
            notify("{} discards {} from {}.".format(me, card, src.name))

def toHand(card, show = True, x = 0, y = 0, alignCheck = True, ignoreEvo = False):
    mute()
    src = card.group
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if ignoreEvo == False and isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be banished.\nWould you like to override this?"):
            return
    if isPsychic(card):
        toHyperspatial(card)
        return
    card.moveTo(card.owner.hand)
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                toHand(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    if show == True: 
        notify("{} moves {} to hand from {}.".format(me, card.name, src.name))
    else:
        whisper("Moved {} to hand from {}.".format(card, src.name))
    if alignCheck:
        align()

def toDeckTop(card, x = 0, y = 0):
    mute()
    toDeck(card)

def toDeckBottom(card, x = 0, y = 0):
    mute()
    toDeck(card, bottom = True)

def toDeck(card, bottom = False):
    mute()
    evolveDict = eval(me.getGlobalVariable('evolution'))
    if isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
        if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be banished.\nWould you like to override this?"):
            return
    if isPsychic(card):
        toHyperspatial(card)
        return
    cardList = [card]
    if card._id in evolveDict:
        evolvedCardList = evolveDict[card._id]
        for evolvedCard in evolvedCardList:
            if Card(evolvedCard) in table:
                cardList.append(Card(evolvedCard))
        del evolveDict[card._id]
        me.setGlobalVariable('evolution', str(evolveDict))
    while len(cardList) > 0:
        if len(cardList) == 1:
            choice = 1
        else:
            choice = askChoice("Choose a card to place it on top of your deck.", [c.name for c in cardList])
        if choice > 0:
            c = cardList.pop(choice - 1)
            if bottom == True:
                notify("{} moves {} to bottom of Deck.".format(me, c))
                c.moveToBottom(c.owner.Deck)
            else:
                notify("{} moves {} to top of Deck.".format(me, c))
                c.moveTo(c.owner.Deck)
    align()
