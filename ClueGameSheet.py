import tkinter
from tkinter import *

root = Tk()
root.geometry("1200x800")
root.title("Clue")
canvas = Canvas(root ,height=700, width=1100, bg="#263D42")
canvas.grid(row = 0,rowspan = 50, column = 1 ,columnspan = 8)
numberOfPlayers = 3
def undoLastGuesses():
    flag = True
    for p in player.keys():
        if flag:
            flag = False
        else:
            player[p].historyUndo()
    envelope.historyUndo()
undoButton = Button(root, text= "Undo", padx = 10, pady=4, fg ='white', bg = "#4f789c", command = undoLastGuesses)
class PlayerClass:
    class Stack:
        class Node:
            def __init__(self, val, next=None):
                self.val = val
                self.next = next

        def __init__(self):
            self.top = None

        def push(self, val):

            self.top = self.Node(val,self.top)

        def pop(self):

            val = self.top.val

            if self.top.next is not None:
                self.top = self.top.next
                return val
            else:
                return val


    def __init__(self, name, rank, personDict = None, placeDict = None, weaponDict = None):
        self.name = name
        self.personDict = personDict
        self.placeDict = placeDict
        self.weaponDict = weaponDict
        self.textBoxes = []
        self.rank = rank
        self.conflicts = []
        self.stack = PlayerClass.Stack()
        self.confictStack = PlayerClass.Stack()
        if personDict is None:
            self.personDict = {person: None for person in PersonOptions}
        if placeDict is None:
            self.placeDict = {place: None for place in PlaceOptions}
        if weaponDict is None:
            self.weaponDict = {weapon: None for weapon in WeaponOptions}
        self.historySave()

    def NameToLabel(self, name):
        if name in PersonOptions:
            return self.personDict[name]
        if name in PlaceOptions:
            return self.placeDict[name]
        if name in WeaponOptions:
            return self.weaponDict[name]
        return None
    def historyUndo(self):
        history = self.stack.pop()
        self.personDict = history[0]
        self.placeDict = history[1]
        self.weaponDict = history[2]
        self.conflicts = self.confictStack.pop()
        self.removeText()
        self.placeText()
    def historySave(self):

        personHist = dict(self.personDict)
        placeHist = dict(self.placeDict)
        weaponHist= dict(self.weaponDict)
        self.stack.push([personHist,placeHist,weaponHist])

        self.confictStack.push(self.conflicts)
    def PRunGuess(self, person,place,weapon,answer):

        if answer:
            self.conflictAdd(person,place,weapon)
            self.removeText()
            self.placeText()
        else:

            self.setCard(person,False)
            self.setCard(place, False)
            self.setCard(weapon, False)
    def setVal(self,name,ValBOOL):
        Val = ValBOOL
        if Val:
            Val = 1
        else:
            Val = 0
        if name in PersonOptions:
            self.personDict[name] = Val
        if name in PlaceOptions:
            self.placeDict[name] = Val
        if name in WeaponOptions:
            self.weaponDict[name] = Val

    def setCard(self, card, value):
        stop = False
        for x in self.personDict.keys():
            if stop:
                break
            if x == card:
                self.personDict[card] = value
                stop = True
        for x in self.placeDict.keys():
            if stop:
                break
            if x == card:
                self.placeDict[card] = value
                stop = True
        for x in self.weaponDict.keys():
            if stop:
                break
            if x == card:
                self.weaponDict[card] = value
                stop = True

    def conflictAdd(self,person,place,weapon): # NEVER REMOVE AN ITEM FROM A CONFLICT OR USE A CONFLICT WITH OUT ALL VALUES PERSON PLACE AND THING
        c = (person,place,weapon)
        self.conflicts.append(c)
        if self.personDict[person] is None:
            self.personDict[person] = "C"
        if self.placeDict[place] is None:
            self.placeDict[place] = "C"
        if self.weaponDict[weapon] is None:
            self.weaponDict[weapon] = "C"
    def resolveConflict(self): # NEVER REMOVE AN ITEM FROM A CONFLICT OR USE A CONFLICT WITH OUT ALL VALUES PERSON PLACE AND THING
        for tup in self.conflicts:
            if self.personDict[tup[0]] == 1 or self.placeDict[tup[1]] == 1 or self.weaponDict[tup[2]] == 1:
                self.conflicts.remove(tup)

            elif self.personDict[tup[0]] == 0 and self.placeDict[tup[1]] == 0: # if 2 values of the tuple are 0, then the other should be true
                self.weaponDict[tup[2]] = 1
                GridLogic()
            elif self.personDict[tup[0]] == 0 and self.weaponDict[tup[2]] == 0:
                self.placeDict[tup[1]] = 1
                GridLogic()
            elif self.placeDict[tup[1]] == 0 and self.weaponDict[tup[2]] == 0:
                self.personDict[tup[0]] = 1
                GridLogic()
    def placeText(self):
        x = 1
        for person in PersonOptions:
            if self.personDict[person] == 0:
                self.textBoxes.append(Label(root, text = "No ", bg = "#FF0000"))
                self.textBoxes[-1].grid(row = x +2 , column= self.rank+1)
                x += 1
            elif self.personDict[person] == 1:
                self.textBoxes.append(Label(root, text="Yes", bg = "#00FF00"))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank+1)
                x += 1
            elif self.personDict[person] == "C":
                self.textBoxes.append(Label(root, text="C", bg="#FFFF00"))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank + 1)
                x += 1
            else:
                self.textBoxes.append(Label(root, text="???"))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank + 1)
                x += 1
        x += 1
        for place in PlaceOptions:
            if self.placeDict[place] == 0:
                self.textBoxes.append(Label(root, text = "No", bg = "#FF0000"))
                self.textBoxes[-1].grid(row = x +2 , column= self.rank+1)
                x += 1
            elif self.placeDict[place] == 1:
                self.textBoxes.append(Label(root, text="Yes", bg = "#00FF00"))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank+1)
                x += 1
            elif self.placeDict[place] == "C":
                self.textBoxes.append(Label(root, text="C", bg="#FFFF00"))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank + 1)
                x += 1
            else:
                self.textBoxes.append(Label(root, text="???",))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank + 1)
                x += 1
        x += 1
        for weapon in WeaponOptions:
            if self.weaponDict[weapon] == 0:
                self.textBoxes.append(Label(root, text = "No", bg = "#FF0000"))
                self.textBoxes[-1].grid(row = x +2 , column= self.rank+1)
                x += 1
            elif self.weaponDict[weapon] == 1:
                self.textBoxes.append(Label(root, text="Yes", bg = "#00FF00"))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank+1)
                x += 1
            elif self.weaponDict[weapon] == "C":
                self.textBoxes.append(Label(root, text="C", bg="#FFFF00"))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank + 1)
                x += 1
            else:
                self.textBoxes.append(Label(root, text="???"))
                self.textBoxes[-1].grid(row=x + 2, column=self.rank + 1)
                x += 1
    def removeText(self):
        for text in self.textBoxes:
            text.destroy()
class EnvelopeClass:
    class Stack:
        class Node:
            def __init__(self, val, next=None):
                self.val = val
                self.next = next

        def __init__(self):
            self.top = None

        def push(self, val):

            self.top = self.Node(val,self.top)

        def pop(self):

            val = self.top.val

            if self.top.next is not None:
                self.top = self.top.next
                return val
            else:
                return val
    def historyUndo(self):
        history = self.stack.pop()
        self.personDict = history[0]
        self.placeDict = history[1]
        self.weaponDict = history[2]
        self.removeText()
        self.placeText()
    def historySave(self):

        personHist = dict(self.personDict)
        placeHist = dict(self.placeDict)
        weaponHist= dict(self.weaponDict)
        self.stack.push([personHist,placeHist,weaponHist])
    def __init__(self):
        self.personDict = {person:None for person in PersonOptions}
        self.placeDict = {place:None for place in PlaceOptions}
        self.weaponDict = {weapon:None for weapon in WeaponOptions}
        self.textBoxes = []
        self.stack = PlayerClass.Stack()
        self.historySave()
    def removeText(self):
        for text in self.textBoxes:
            text.destroy()
    def placeText(self):
        x = 1
        for person in PersonOptions:
            if self.personDict[person] == 0:
                self.textBoxes.append(Label(root, text = "No ", bg = "#FF0000"))
                self.textBoxes[-1].grid(row = x +2 , column= numberOfPlayers+1)
                x += 1
            elif self.personDict[person] == 1:
                self.textBoxes.append(Label(root, text="Yes", bg = "#00FF00"))
                self.textBoxes[-1].grid(row=x + 2, column=numberOfPlayers+1)
                x += 1
            else:
                self.textBoxes.append(Label(root, text="???"))
                self.textBoxes[-1].grid(row=x + 2, column=numberOfPlayers + 1)
                x += 1
        x += 1
        for place in PlaceOptions:
            if self.placeDict[place] == 0:
                self.textBoxes.append(Label(root, text = "No", bg = "#FF0000"))
                self.textBoxes[-1].grid(row = x +2 , column= numberOfPlayers+1)
                x += 1
            elif self.placeDict[place] == 1:
                self.textBoxes.append(Label(root, text="Yes", bg = "#00FF00"))
                self.textBoxes[-1].grid(row=x + 2, column= numberOfPlayers+1)
                x += 1
            else:
                self.textBoxes.append(Label(root, text="???",))
                self.textBoxes[-1].grid(row=x + 2, column=numberOfPlayers + 1)
                x += 1
        x += 1
        for weapon in WeaponOptions:
            if self.weaponDict[weapon] == 0:
                self.textBoxes.append(Label(root, text = "No", bg = "#FF0000"))
                self.textBoxes[-1].grid(row = x +2 , column= numberOfPlayers+1)
                x += 1
            elif self.weaponDict[weapon] == 1:
                self.textBoxes.append(Label(root, text="Yes", bg = "#00FF00"))
                self.textBoxes[-1].grid(row=x + 2, column=numberOfPlayers+1)
                x += 1
            else:
                self.textBoxes.append(Label(root, text="???"))
                self.textBoxes[-1].grid(row=x + 2, column=numberOfPlayers + 1)
                x += 1
    def NameToLabel(self,name):

        if name in PersonOptions:
            return self.personDict[name]
        if name in PlaceOptions:
            return self.placeDict[name]
        if name in WeaponOptions:
            return self.weaponDict[name]
        return None
    def setVal(self,name,ValBOOL):
        Val = ValBOOL
        if Val:
            Val = 1
        else:
            Val = 0
        if name in PersonOptions:
            self.personDict[name] = Val
        if name in PlaceOptions:
            self.placeDict[name] = Val
        if name in WeaponOptions:
            self.weaponDict[name] = Val

    def __iter__(self):

        for person in PersonOptions:
            yield self.personDict[person]
        for person in PlaceOptions:
            yield self.placeDict[person]
        for weapon in WeaponOptions:
            yield self.weaponDict[weapon]

player = {}
envelope = None
GuesserOptions=[]
def vertiRedLogic():
    count = 0
    for name in PersonOptions:
        if envelope.NameToLabel(name) == 1:
            break
        elif envelope.NameToLabel(name) == 0:
            count += 1
        else:
            temp = name
    if count == len(PersonOptions) - 1:
        envelope.setVal(temp, True)
    count = 0
    for name in PlaceOptions:
        if envelope.NameToLabel(name) == 1:
            break
        elif envelope.NameToLabel(name) == 0:
            count += 1
        else:
            temp = name
    if count == len(PlaceOptions) - 1:
        envelope.setVal(temp, True)
    count = 0
    for name in WeaponOptions:
        if envelope.NameToLabel(name) == 1:
            break
        elif envelope.NameToLabel(name) == 0:
            count += 1
        else:
            temp = name
    if count == len(WeaponOptions) - 1:
        envelope.setVal(temp, True)
def vertiGreenLogic():
    temp = None
    for name in PersonOptions:
        if envelope.NameToLabel(name) == 1:
            temp = name
    if temp is not None:
        for name in PersonOptions:
            if name is not temp:
                envelope.setVal(name,False)
    temp = None
    for name in PlaceOptions:
        if envelope.NameToLabel(name) == 1:
            temp = name
    if temp is not None:
        for name in PlaceOptions:
            if name is not temp:
                envelope.setVal(name, False)
    temp = None
    for name in WeaponOptions:
        if envelope.NameToLabel(name) == 1:
            temp = name
    if temp is not None:
        for name in WeaponOptions:
            if name is not temp:
                envelope.setVal(name,False)
def horizGreenLogic():
    for seq in (PersonOptions,PlaceOptions,WeaponOptions):
        for name in seq:
            if envelope.NameToLabel(name) == 1:
                for p in player.keys():
                    player[p].setVal(name, False)
            temp = None
            for p in player.keys():
                if player[p].NameToLabel(name) == 1:
                    temp = p
            if temp is not None:
                for p in player.keys():
                    if p is not temp:
                        player[p].setVal(name,False)
                envelope.setVal(name, False)
def horizRedLogic():



    for seq in (PersonOptions,PlaceOptions,WeaponOptions):
        for name in seq:
            count = 0
            temp = None
            if envelope.NameToLabel(name) == 0:
                count += 1

            else:
                temp = "Envelope"
            for p in player.keys():
                if player[p].NameToLabel(name) == 0:
                    count += 1

                else:
                    temp = p

            if count == numberOfPlayers:

                if temp == "Envelope":
                    envelope.setVal(name,True)
                else:
                    player[temp].setVal(name,True)
    return

def playerConflictResolve():
    flag = True
    for p in player:
        if flag:
            flag = False
        else:
            player[p].resolveConflict()
def GridLogic():
    horizRedLogic()
    horizGreenLogic()
    vertiGreenLogic()
    vertiRedLogic()
    playerConflictResolve()
    updatePlayerText()
    updateEnvelopeText()

def setBoxes(personDict, placeDict, weaponDict):
    global player
    global PlayerEntryLst
    global GuesserOptions
    global envelope
    global runGuess
    x = 0

    for p in GuesserOptions:
        if x == 0:
            player[p] = PlayerClass(p,x,personDict, placeDict, weaponDict)
            x += 1
        else:
            player[p] = PlayerClass(p,x)
            x += 1


    runGuess.grid(row=51, column=5)
    undoButton.grid(row=51, column=6)

    for key in player.keys():
        player[key].placeText()
    envelope = EnvelopeClass()
    envelope.placeText()

def updatePlayerText():
    for key in player.keys():
        player[key].removeText()
        player[key].placeText()
def updateEnvelopeText():
    envelope.removeText()
    envelope.placeText()
def EnterPlayerCards():
    def NextStep():
        ConfirmCards.destroy()
        personDict = {}
        placeDict = {}
        weaponDict = {}
        for person in PersonOptions:
            personDict[person] = vardict[person].get()
            checkboxdict[person].destroy()
        for place in PlaceOptions:
            placeDict[place] = vardict[place].get()
            checkboxdict[place].destroy()
        for weapon in WeaponOptions:
            weaponDict[weapon] = vardict[weapon].get()
            checkboxdict[weapon].destroy()
        setBoxes(personDict,placeDict,weaponDict)
        horizGreenLogic()
        updatePlayerText()
        updateEnvelopeText()

    x = 0
    checkboxdict = {}
    vardict = {}
    Label(root, text="").grid(row=x + 2, column=0)
    x += 1

    for person in PersonOptions:
        vardict[person] = IntVar()
        Label(root, text = person).grid(row = x+2 , column = 0)
        checkboxdict[person] = Checkbutton(root, bg = "#263D42", variable = vardict[person])
        checkboxdict[person].grid(row = x+2 , column = 1)
        x += 1
    Label(root, text="").grid(row=x + 2, column=0)
    x += 1
    for place in PlaceOptions:
        vardict[place] = IntVar()
        Label(root, text=place).grid(row=x+2, column=0)
        checkboxdict[place] = Checkbutton(root, bg="#263D42",variable= vardict[place])
        checkboxdict[place].grid(row=x + 2, column=1)
        x += 1
    Label(root, text="").grid(row=x + 2, column=0)
    x += 1
    for weapon in WeaponOptions:
        vardict[weapon] = IntVar()
        Label(root, text=weapon).grid(row=x+2, column=0)
        checkboxdict[weapon] = Checkbutton(root, bg="#263D42", variable = vardict[weapon])
        checkboxdict[weapon].grid(row=x + 2, column=1)
        x += 1
    ConfirmCards = Button(root, text= "Confirm Cards", padx = 10, pady=4, fg ='white', bg = "#4f789c", command = NextStep)
    ConfirmCards.grid(row=x+2, column =1)
def getNextGuesser(guesser):
    if GuesserOptions.index(guesser)+1 == len(GuesserOptions):
        return GuesserOptions[0]
    else:
        return GuesserOptions[GuesserOptions.index(guesser)+1]

def returnTrue():
    player[currentGuesser].PRunGuess(GlobalPerson, GlobalPlace,GlobalWeapon, True)
    runGuess.grid(row=51, column=5)
    undoButton.grid(row=51, column=6)
    TrueButton.grid_forget()
    FalseButton.grid_forget()
    GuessLabel.grid_forget()
    GridLogic()
def returnFalse():
    global currentGuesser
    player[currentGuesser].PRunGuess(GlobalPerson, GlobalPlace,GlobalWeapon, False)
    currentGuesser = getNextGuesser(currentGuesser)
    if currentGuesser == GlobalGuesser:

        runGuess.grid(row=51, column=5)
        undoButton.grid(row=51, column=6)
        TrueButton.grid_forget()
        FalseButton.grid_forget()
        GuessLabel.grid_forget()
    elif  currentGuesser == GuesserOptions[0]:

        GuessLabelVar.set("Do you have " + GlobalPerson + ", " + GlobalPlace + ", or " + GlobalWeapon)
    else:
        GuessLabelVar.set("Does " + currentGuesser + " have " + GlobalPerson + ", " + GlobalPlace + ", or " + GlobalWeapon)
    GridLogic()

TrueButton = Button(root, text="Yes", fg='white', bg="#4f789c", command=returnTrue)
    #TrueButton.grid(row=52,column=1)
FalseButton = Button(root, text="No", fg='white', bg="#4f789c", command=returnFalse)
    #FalseButton.grid(row=52,column=2)
GuessLabelVar = StringVar()
GuessLabel = Label(root,textvariable =GuessLabelVar)
def NoOneShowed():
    playerCardShownOptionMenu.grid_forget()
    CardsShownOptionMenu.grid_forget()
    ConfirmCardShown.grid_forget()
    NoneCardsShown.grid_forget()
    cardShown = CardShownVar.get()
    playerShown = playerStringVar.get()
    for x in GuesserOptions:
        if x != GuesserOptions[0]:
            player[x].PRunGuess(GlobalPerson, GlobalPlace, GlobalWeapon, False)

    runGuess.grid(row=51, column=5)
    undoButton.grid(row=51, column=6)
    GridLogic()
def CardShown():
    playerCardShownOptionMenu.grid_forget()
    CardsShownOptionMenu.grid_forget()
    ConfirmCardShown.grid_forget()
    NoneCardsShown.grid_forget()
    cardShown = CardShownVar.get()
    playerShown = playerStringVar.get()
    for x in GuesserOptions:
        if x == playerShown:

            player[playerShown].setCard(cardShown, True)
            break
        elif x != GuesserOptions[0]:
            player[x].PRunGuess(GlobalPerson, GlobalPlace, GlobalWeapon, False)
    runGuess.grid(row=51, column=5)
    undoButton.grid(row=51, column=6)
    GridLogic()

ConfirmCardShown = Button(root, text="Confirm", fg='white', bg="#4f789c", command=CardShown)
NoneCardsShown = Button(root, text="No cards shown", fg='white', bg="#4f789c", command=NoOneShowed)
CardsShownOptionMenu = OptionMenu(root, StringVar(), [])
CardShownVar = StringVar()
playerCardShownOptionMenu = OptionMenu(root, StringVar(), [])
playerStringVar = StringVar()


currentGuesser = ""
GlobalPerson = ""
GlobalPlace = ""
GlobalWeapon = ""
GlobalGuesser = ""
def updateGuessVars(person, place, weapon, guesser):
    global GlobalPerson
    global GlobalPlace
    global GlobalWeapon
    global GlobalGuesser
    GlobalPerson = person
    GlobalPlace = place
    GlobalWeapon = weapon
    GlobalGuesser = guesser
def RunGuess():
    global runGuess
    global currentGuesser
    global GuessLabelVar
    global CardsShownOptionMenu
    global playerCardShownOptionMenu
    runGuess.grid_forget()
    undoButton.grid_forget()
    currentGuesser,person,place,weapon = GuesserVar.get(), PersonVar.get(), PlaceVar.get(), WeaponVar.get()
    updateGuessVars(person,place,weapon,currentGuesser)
    for p in player.keys():
        player[p].historySave()
    envelope.historySave()
    if currentGuesser == GuesserOptions[0]:

        cardsShownOptionMenuOptions = [person, place, weapon]
        CardShownVar.set(cardsShownOptionMenuOptions[0])
        CardsShownOptionMenu = OptionMenu(root, CardShownVar, *cardsShownOptionMenuOptions)

        playerLst = [guesser for guesser in GuesserOptions]
        playerLst.remove(playerLst[0])
        playerStringVar.set(playerLst[0])
        playerCardShownOptionMenu = OptionMenu(root, playerStringVar, *playerLst)



        playerCardShownOptionMenu.grid(row = 53, column = 3)
        CardsShownOptionMenu.grid(row = 53, column = 2)
        NoneCardsShown.grid(row = 53, column = 5)
        ConfirmCardShown.grid(row =53, column = 4)
    else:
        currentGuesser = getNextGuesser(currentGuesser)
        TrueButton.grid(row=53,column=1)
        FalseButton.grid(row=53,column=2)
        GuessLabelVar.set("Does " + currentGuesser + " have " + person + ", " + place + ", or " + weapon)
        GuessLabel.grid(row = 52, column=1 )

runGuess = Button(root, text="Run Guess", padx=10, pady=5, fg='white', bg="#4f789c", command=RunGuess)



def getPlayerCount():
    def SetPlayerCount():
        PCDictionary = {
            "Three" : 3,
            "Four"  : 4,
            "Five"  : 5,
            "Six"   : 6
        }
        global numberOfPlayers
        numberOfPlayers = PCDictionary[PlayerCountVar.get()]
        PlayerCountDrop.destroy()
        confirmPlayerCount.destroy()
        getGuesserNames()
    PlayerCountOptions = ["Three", "Four", "Five", "Six"]
    PlayerCountVar = StringVar()
    PlayerCountVar.set(PlayerCountOptions[0])
    PlayerCountDrop = OptionMenu(root, PlayerCountVar, *PlayerCountOptions)
    PlayerCountDrop.grid(row=1, column=3)

    #Button to confirm player count calls function SetPlayerCount
    confirmPlayerCount = Button(root, text="Confirm Player Count", padx=10, pady=5, fg='white', bg="#4f789c", command= SetPlayerCount )
    confirmPlayerCount.grid(row = 1, column = 7)

GuesserVar = None
PlayerEntryLst = [] #list of all player entry widgets
def getGuesserNames():


    for x in range(numberOfPlayers):
        global PlayerEntryLst
        PlayerEntryLst.append(Entry(root, text="Player" + str(x), justify="center"))
        PlayerEntryLst[x].grid(row=1, column=x + 1)
        if  x == 0:
            PlayerEntryLst[x].insert(0, "You")
        else:
            PlayerEntryLst[x].insert(0, "Player" + str(x))
    #creates a Entry field containing player# for every player in numberOfPlayers

    def UpdateGuesserDrop(): # function that adds the guesser dropdown menu when player names are confirmed
        global GuesserOptions
        global GuesserVar
        GuesserOptions = [i.get() for i in PlayerEntryLst]
        GuesserVar = StringVar()
        GuesserVar.set(GuesserOptions[0])
        GuesserDrop = OptionMenu(root, GuesserVar, *GuesserOptions)
        GuesserDrop.grid(row=51, column=1)
        UpdatePlayerNames.destroy()
        PlayerCountExplain.destroy()
        #destroy and replace Player Entry Widgets
        PlayerNumberVar = 0
        for name in GuesserOptions:
            Label(root, text = name).grid(row=1, column=PlayerNumberVar + 1) #Creates
            PlayerNumberVar += 1
        Label(root, text="Envelope").grid(row=1, column=PlayerNumberVar + 1)
        for entry in PlayerEntryLst:
            entry.destroy()


        displayPersons()
        displayPlaces()
        displayWeapons()



        EnterPlayerCards()

    UpdatePlayerNames = Button(root, text="Set Player Names", padx=10, pady=5, fg='white', bg="#4f789c",command=UpdateGuesserDrop)
    UpdatePlayerNames.grid(row=1, column=numberOfPlayers + 2)

    PlayerCountExplain = Label(root, text="Enter player names starting with you on the left. Enter remaining players in order of rotation such that the person who responds to guesses after you is next")
    PlayerCountExplain.grid(row=0, column=1, columnspan=8)


PersonOptions = ["Mrs. Peacock", "Colonel Mustard", "Mr. Green", "Prof. Plum", "Miss. Scarlet", "Mrs. White"]
PlaceOptions = ["Billiard Room", "Study", "Hall", "Lounge", "Dinning Room", "Ballroom", "Conservatory", "Library", "Kitchen"]
WeaponOptions = ["Revolver", "Dagger", "Lead Pipe", "Rope", "Candlestick", "Wrench"]
PersonVar = None
def displayPersons():
    global PersonOptions
    global PersonVar
    PersonVar = StringVar()
    PersonVar.set(PersonOptions[0])
    PersonDrop = OptionMenu(root, PersonVar, *PersonOptions )
    PersonDrop.grid(row = 51, column = 2)
PlaceVar = None
def displayPlaces():
    global PlaceOptions
    global PlaceVar
    PlaceVar = StringVar()
    PlaceVar.set(PlaceOptions[0])
    PlaceDrop = OptionMenu(root, PlaceVar, *PlaceOptions)
    PlaceDrop.grid(row = 51, column = 3)
WeaponVar = None
def displayWeapons():
    global WeaponOptions
    global WeaponVar
    WeaponVar = StringVar()
    WeaponVar.set(WeaponOptions[0])
    WeaponDrop = OptionMenu(root, WeaponVar, *WeaponOptions )
    WeaponDrop.grid(row = 51, column = 4)






getPlayerCount()



root.mainloop()