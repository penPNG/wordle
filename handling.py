import random

def mkWordList(wf):
    word_list = list()
    for line in wf:
        word_list.append(line.rstrip())
    return word_list

def hadNumbers(word):
    for char in word:
        if char.isdigit():
            return True
        else: return False

def checkGuess(guess, word):
    irs = []
    iw = []
    wd = {}
    gd = {}
    
    #Keep track of how many letters have been verified
    for char in word:
        wd[char] += 1
    for char in guess:
        gd[char] += 1

    for gl, wl in zip(guess, word):
        if wd[wl] == 0:
            continue
        if gl in word:
            iw.append(True)
            wd[wl] -= 1
        else:
            iw.append(False)
        if gl == wl:
            irs.append(True)
            wd[wl] -= 1
        else:
            irs.append(False)
    
    return iw, irs

def newWord(wl: list):
    return random.choice(wl)

def split(word: str):
    return [char for char in word]