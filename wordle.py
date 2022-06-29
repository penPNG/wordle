import pygame, random, pygame.freetype, sys, requests
#import random
from pygame.locals import *
from string import ascii_lowercase

#Initialization
#**********************************************
global word

def mkWordList(wf): #Creates a list of words from a txt file. Still checks for 5 letters, despite them all being 5 letters
    word_list = list()
    for line in wf:
        if len(line.rstrip()) == 5:
            word_list.append(line.rstrip())
    return word_list


def hasNumbers(word): #This whole function is defunct. Program doesn't accept number input anyway.
    for character in word:
        if character.isdigit():
            return True
    else: return False


def checkLetters(guess, word): #Compares these two lists item by item
    inRightSpot = []
    inWord = []

    for letter, guessLetter in zip(guess, word): #This is a cool function, though I don't remember what it does
        if letter in word:
            inWord.append(True)
        else:
            inWord.append(False)
        if letter == guessLetter:
                inRightSpot.append(True)
        else:
            inRightSpot.append(False)

    return inWord, inRightSpot


def newWord(word_list): #Picks a random item from the word list and returns it
    return random.choice(word_list)


def newLetter(letter): #Some hard coded magic that checks which letter is input according to ascii_lowercase
    offset = 97
    for i in range(26):
        if letter == i+offset:
            return ascii_lowercase[i]


def split(word):    #This should already exist in python
    return [char for char in word]

'''try:
    wf = open('5-letter-words.txt') #Probably gonna replace this with the actual wordle list
    word_list = mkWordList(wf)
    wf.close()
except:
    wf = open('10000 words.txt')
    word_list = mkWordList(wf)
    wf.close()'''

wf = open('list-of-words.txt')
word_list = mkWordList(wf)
wf.close()


KEY = "dict.1.1.20220204T191714Z.a816fcf9c81f4386.6a631bf375fcb9af527de4faa837af2e8acecfea"
url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key="+KEY+"&lang=en-en&text="
    #Yandex has a better response time, it is still free and allows a crazy amount of requests per month


letterWhite = Color("#d7dadc")  #All the colors used, some of them arent used tho
lightestGray = Color("#565758")
keyboardGray = Color("#818384")
lighterGray = Color("#3a3a3c")
backgroundGray = Color("#121213")
green = Color("#6aaa64")
keyboardGreen = Color("#538d4e")
yellow = Color("#b59f3b")
#**********************************************

class guessRow():
    def __init__(self, y, guess, count, correct):
        self.y = y
        self.guess = guess
        self.count = count
        self.correct = correct
        self.offset = 66
        self.gameFont = pygame.freetype.SysFont('Arial Bold', 36)
        self.guessRects = {}
    
    def drawRow(self):
        global gs_x
        for i in range(5):
            guess_square = pygame.Rect(gs_x, gs_y, 61, 61)  
            pygame.draw.rect(screen, lighterGray, guess_square, 2)#Draws input squares
            try:
                if self.correct[1][i] == True:
                    pygame.draw.rect(screen, green, guess_square)   #Draws green squares ontop of the input squares
                elif self.correct[0][i] == True:
                    pygame.draw.rect(screen, yellow, guess_square)  #Draws yellow squares ontop of input squares
                else: pygame.draw.rect(screen, lighterGray, guess_square)   #Draws filled in squares ontop of the remaining input squares
            except: pass

            #pygame.draw.rect(screen, lighterGray, guess_square, 2)
            try:
                self.gameFont.render_to(screen, ((gs_x+(guess_square.width/2))-(self.guessRects[i].width/2), ((gs_y+(guess_square.height/2))-(self.guessRects[i].height/2))), self.guess[i].upper(), letterWhite)   #Tries to draw a letter to the screen if it can
            except: pass
            gs_x += self.offset

    def makeRects(self):
        try:
            for i in range(len(self.guess)):
                self.guessRects[i] = self.gameFont.get_rect(self.guess[i].upper())
        except: pass

#Main loop*************************************
def main():

    #More Initialization!**********************
    global word, gs_x, gs_y, screen
    pygame.init()
    pygame.font.init()

    width = 390
    height = 459
    FPS = 60    #This game runs at 60 fps!
    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode([width,height], pygame.NOFRAME)
    headerFont = pygame.freetype.SysFont('Arial Bold', 36, True)
    escFont = pygame.freetype.SysFont('Arial Bold', 28)
    wrongFont = pygame.freetype.SysFont('Arial Bold', 16)

    rows = {}
    guess = []
    guesses = {}
    guessCount = 0
    letterCount = 0
    inWord, inRightSpot = [], []
    correct = {}
    isRight = False
    for i in range(6):
        correct[i] = None
        guesses[i] = None
    for i in range(5):
        inWord.append(None)
        inRightSpot.append(None)

    word = newWord(word_list)
    word = split(word)

    wordle_rect = pygame.freetype.Font.get_rect(headerFont,"WORDLE")
    wordle_top_margin = (12/663)*height

    screen_rect = Rect(0, 0, width, height)
    headerHeight = wordle_rect.height+(wordle_top_margin*2)

    word_rect_rect = pygame.Rect((width-90)/2, 82, 93, 50)

    esc_left_margin = (12/390)*width
    esc_rect = pygame.freetype.Font.get_rect(escFont, "Esc")
    esc_button_rect = pygame.Rect(esc_left_margin-5, ((headerHeight-esc_rect.height)/2)-5, esc_rect.width+10, esc_rect.height+10) #This is a mess that just makes a highlighting box around the word 'Esc'

    gs_left_margin = (35/390)*width
    gs_x = gs_left_margin
    gs_y = headerHeight + 12
    guess_square = pygame.Rect(gs_x, gs_y, 61, 61) #Redundancy, just in case...

    for i in range(6): #Creates a list of objects based on the guess row class
        rows[i] = guessRow(gs_y, guesses[i], guessCount, correct)
        gs_y += gs_y
    #******************************************


    while True:

        mouse = pygame.mouse.get_pos()


        #Header******************************************

        screen.fill(backgroundGray)

        if esc_button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, lighterGray, esc_button_rect)
        else:
            pygame.draw.rect(screen, backgroundGray,esc_button_rect)
        escFont.render_to(screen, (esc_left_margin, (headerHeight-esc_rect.height)/2), "Esc", keyboardGray)


        headerFont.render_to(screen, ((width-wordle_rect.width)/2, wordle_top_margin), "WORDLE", letterWhite)
        pygame.draw.line(screen, lighterGray, (0, headerHeight-1), (width, headerHeight-1))  #Draws a line approx. 12px below the title
        pygame.draw.rect(screen, lighterGray, screen_rect, 1)


        #Body********************************************

        """
        guess_square = pygame.Rect(gs_x, gs_y, 61, 61)              #Depricated code
        gs_y = headerHeight + 12
        pygame.draw.rect(screen, lighterGray, guess_square, 2)
        guess_square = pygame.Rect(gs_x, gs_y, 61, 61)
        gs_y = gs_y + 66
        pygame.draw.rect(screen, lighterGray, guess_square, 2)"""

        gs_y = headerHeight + 12    #Just hanging out in the void


        '''for i in range(6): #Creaates a grid of empty squares     #More Depricated code
            gs_x = gs_left_margin
            for j in range(5):      #(they actually do the same thing)
                guess_square = pygame.Rect(gs_x, gs_y, 61, 61)
                pygame.draw.rect(screen, lighterGray, guess_square, 2)
                gs_x += 66
            gs_y += 66'''   #Inconsistent quotes

        guesses[guessCount] = guess
        correct[guessCount-1] = inWord, inRightSpot
        #print(guesses[guessCount], word) #for debugging purposes
        for i in range(6):  
            rows[i].guess = guesses[i]
            rows[i].count = guessCount
            rows[i].correct = correct[i]
        for i in range(6):
            gs_x = gs_left_margin
            rows[i].makeRects()
            rows[i].drawRow()
            gs_y += 66


        if (guessCount == 6 and isRight == False):
            pygame.draw.rect(screen, letterWhite, word_rect_rect, 0, 5)
            temp = ''.join(str(e) for e in word)
            word_rect = wrongFont.get_rect(temp.upper())
            wrongFont.render_to(screen, ((word_rect_rect.left+word_rect_rect.width/2)-(word_rect.width/2), ((word_rect_rect.top+word_rect_rect.height/2)-word_rect.height/2)), temp.upper(), '#000000')

        #Event Handling**********************************
        
        for event in pygame.event.get():    #This section feels empty... So I'm adding useless comments****
            if event.type == QUIT:          #Literally impossible to do, doesn't need to be here, not getting rid of it.
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:   #If you press escape key, then the game quits
                    pygame.quit()
                    sys.exit()

                if event.key == K_BACKSPACE and letterCount > 0:    #If you press backspace, it gets rid of a character
                        del guess[-1]
                        letterCount -= 1
                        print(guess)
                elif event.key == K_RETURN and letterCount == 5 and isRight == False:   #If you press enter, it does a whole mess of things
                    if guess == word:
                        inWord, inRightSpot = checkLetters(guess, word) #For some reason if you just assign all trues, it breaks it
                        print("Correct!")
                        guessCount += 1
                        letterCount = 0
                        guess = []
                        isRight = True  #Prevents the user from guessing after getting it right
                        
                        word = split(newWord(word_list))
                    elif guess != word:
                        temp = ''.join(str(e) for e in guess)

                        #I could have it check the word list before the api for offline reasons...
                        #but...... this is more fun. Despite how much faster it could be
                        
                        try:
                            r = requests.get(url+temp)
                            response = r.json()
                            if r.status_code == 200:
                                try: #Takes advantage of how the received json is set up
                                    if response['def'][0]['text']:
                                        inWord, inRightSpot = checkLetters(guess, word)
                                        print(inWord, inRightSpot)
                                        letterCount = 0
                                        guessCount += 1

                                        #guesses{for i in guess} = inWord, inRightSpot  #This never worked. I really wanted it to tho
                                        guess = []
                                except: print("Unkown word!") #If not a word, print not a word lol
                            else: print("Connection error!")
                        except: print("Connection error!")
                elif event.key == K_RETURN and (guessCount == 6 or isRight == True):
                    word = split(newWord(word_list))
                    rows = {}
                    guess = []
                    guesses = {}
                    guessCount = 0
                    letterCount = 0
                    inWord, inRightSpot = [], []
                    correct = {}
                    isRight = False
                    for i in range(6):
                        correct[i] = None
                        guesses[i] = None
                    for i in range(5):
                        inWord.append(None)
                        inRightSpot.append(None)
                    for i in range(6): #Creates a list of objects based on the guess row class
                        rows[i] = guessRow(gs_y, guesses[i], guessCount, correct)
                        gs_y += gs_y
                                        
                        
                elif letterCount < 5 and 97 <= event.key <= 122 and isRight == False:
                    guess.append(newLetter(event.key))
                    letterCount += 1
                    print(guess)

            if event.type == MOUSEBUTTONDOWN:   #If you click the mouse button on the escape button, the game quits
                if esc_button_rect.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()   #Updates the screen
        fpsClock.tick(FPS)      #Ticks(?)

        #Old code. A remnant of a previous iteration. Found in simplewordle.py
        """print("Guess a 5 letter word")
        guess = input()
        if hasNumbers(guess):
            print("That is not a word")
        elif len(guess) != 5:
            print("That is not a 5 letter word")
        elif guess == word:
            print("Correct!")
            newWord(word_list)
        elif guess != word:
            inWord, inRightSpot = checkLetters(guess, word)
            print(inWord, inRightSpot)"""
#**********************************************

main()
#Lots of this code is just old code I refuse to get rid of lol