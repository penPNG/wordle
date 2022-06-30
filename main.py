import sys
import pygame, pygame.freetype, random, os
from pygame.locals import *
from box import Box
from handling import *

pygame.init()
pygame.font.init()

WHITE = Color("#d7dadc")
WHITEGRAY = Color("#565758")
KEYBOARDGRAY = Color("#818384")
LIGHTGRAY = ("#3a3a3c")
GRAY = Color("#121213")
GREEN = Color("#6aaa64")
KEYGREEN = Color("#538d4e")
YELLOW = Color("#b59f3b")

WIDTH = 390
HEIGHT = 663
FPS = 60

HEADER_TOP_MARIGN = (12/663)*HEIGHT
BOX_LEFT_MARGIN = (35/390)*WIDTH

HERE = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(HERE, 'list-of-words.txt')

def main():

    clock = pygame.time.Clock()

    wf = open(FILENAME)
    word_list = mkWordList(wf)
    wf.close()

    word = newWord(word_list)
    word = split(word)

    print(word)

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    headerFont = pygame.freetype.SysFont('Arial Bold', 36, True)
    escFont = pygame.freetype.SysFont('Arial Bold', 28)
    wrongFont = pygame.freetype.SysFont('Arial Bold', 16)

    all_sprites_list = pygame.sprite.Group()

    titleRect = headerFont.get_rect("WORDLE")
    headerHeight = (HEADER_TOP_MARIGN*2)+titleRect.height

    escRect = escFont.get_rect("Esc")
    print(escRect.height, escRect.width)
    escBox = pygame.Rect((headerHeight/2)-15, (headerHeight/2)-15, escRect.width+10, escRect.height+10)

    box_y = headerHeight + 12
    for i in range(6):
        for i in range(5):
            box = Box(LIGHTGRAY, 61, 61, None, 'e')
            box.rect.x = BOX_LEFT_MARGIN + i*66
            box.rect.y = box_y
            all_sprites_list.add(box)
        box_y += 66


    while True:
        mouse = pygame.mouse.get_pos()

        all_sprites_list.update()

        #Background
        screen.fill(GRAY)

        #The highliting box around "Esc"
        if escBox.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHTGRAY, escBox)
        else:
            pygame.draw.rect(screen, GRAY, escBox)
        escFont.render_to(screen, (escBox.left+5, escBox.top+5), "Esc", KEYBOARDGRAY)

        #WORDLE
        headerFont.render_to(screen, ((WIDTH/2)-(titleRect.width/2), HEADER_TOP_MARIGN), "WORDLE", WHITE)

        #Stylish lines
        pygame.draw.line(screen, LIGHTGRAY, (0, headerHeight), (WIDTH, headerHeight))
        pygame.draw.rect(screen, LIGHTGRAY, (0, 0, screen.get_width(), screen.get_height()), 1)


        all_sprites_list.draw(screen)

        #Draws the game then ticks forward
        pygame.display.flip()
        clock.tick(FPS)

        #Event Handling
        for event in pygame.event.get():
            if event.type == QUIT: #X button
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if 97 <= event.key <= 122:
                    pass
            if event.type == MOUSEBUTTONDOWN:
                if escBox.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()