from itertools import count

import pygame.mouse
from pygame import *
import random

init()
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (160, 160, 160)

win_width, win_height = 1236, 718
FPS = 30
clock = time.Clock()

win = display.set_mode((win_width, win_height), RESIZABLE)
display.set_caption("Monkey_game")

width, height = 192, 197
speed = 6
run_speed = 10

stamina = 100
max_stamina = 100
stamina_decrease = 1
stamina_increase = 0.5
running = False

x, y = 50, 400
bg = image.load('img/bg.png').convert_alpha()
bg = transform.scale(bg, (1236, 718))
bg_x = 0

boomerang = image.load("img/boomerang.png").convert_alpha()
boomerang_x = win_width + 10

coconut = image.load("img/coconut.png").convert_alpha()
coconut_y = -10

petri = image.load("img/petri.png").convert_alpha()
petri_x = win_width + 10

boomerang_list = []
coconut_list = []
petri_list = []

boomerang_time = random.randint(800, 10000)
boomerang_timer = USEREVENT + 1
time.set_timer(boomerang_timer, boomerang_time)

coconut_time = random.randint(1000, 7000)
coconut_timer = USEREVENT + 2
time.set_timer(coconut_timer,coconut_time)

petri_time = random.randint(4300, 11000)
petri_timer = USEREVENT + 3
time.set_timer(petri_timer, petri_time)

playerFace = image.load('img/face.png').convert_alpha()

animCount = 0
left, right = False, False

jumpCount = 10
isJump = False

score = 0

font.init()

font30 = font.SysFont("Gothic", 30)
font50 = font.SysFont("Gothic", 50)
labelGameOver = font50.render("Тебе з'їла Петриченко",0, red)
labelResetGame = font50.render("Почати спочатку?",0, red)
rectResetGame = labelResetGame.get_rect(topleft = (450, 200))

labelWin = font50.render("Ура тебе не з'їла петриченко!",0, green)
labelPlayAgain = font50.render("Спробувати вижити спочатку?",0, green)
rectPlayAgain = labelResetGame.get_rect(topleft = (450, 200))

gameOver = True


walkRight = [image.load('img/right_1.png').convert_alpha(), image.load('img/right_2.png').convert_alpha(), image.load('img/right_3.png').convert_alpha(), image.load('img/right_4.png').convert_alpha(), image.load('img/right_5.png').convert_alpha(),
             image.load('img/right_6.png').convert_alpha(), image.load('img/right_7.png').convert_alpha(), image.load('img/right_8.png').convert_alpha(), image.load('img/right_9.png').convert_alpha(), image.load('img/right_10.png').convert_alpha(),
             image.load('img/right_11.png').convert_alpha(), image.load('img/right_12.png').convert_alpha(), image.load('img/right_13.png').convert_alpha(), image.load('img/right_14.png').convert_alpha(), image.load('img/right_15.png').convert_alpha()]
walkLeft = [image.load('img/left_1.png').convert_alpha(), image.load('img/left_2.png').convert_alpha(), image.load('img/left_3.png').convert_alpha(), image.load('img/left_4.png').convert_alpha(), image.load('img/left_5.png').convert_alpha(),
             image.load('img/left_6.png').convert_alpha(), image.load('img/left_7.png').convert_alpha(), image.load('img/left_8.png').convert_alpha(), image.load('img/left_9.png').convert_alpha(), image.load('img/left_10.png').convert_alpha(),
             image.load('img/left_11.png').convert_alpha(), image.load('img/left_12.png').convert_alpha(), image.load('img/left_13.png').convert_alpha(), image.load('img/left_14.png').convert_alpha(), image.load('img/left_15.png').convert_alpha()]

def draw():
    global stamina
    global petri
    global bg_x
    global animCount
    global score
    global gameOver
    global x, y
    global player_rect
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x + win_width, 0))
    # win.blit(playerFace, (x, y))
    if gameOver:
        player_rect = walkRight[0].get_rect(topleft = (x , y))
        player_rect.width = 200
        player_rect.height = 230
        if boomerang_list:
            for el in boomerang_list:
                win.blit(boomerang, el)
                el.x -= 5

                if player_rect.colliderect(el):
                    boomerang_list.remove(el)
                    score -= 35
                score = round(score + 0.03, 2)
                if score <= -100:
                    gameOver = False

        if coconut_list:
            for co in coconut_list:
                win.blit(coconut, co)
                co.y += 10
            if player_rect.colliderect(co):
                coconut_list.remove(co)
                score -= 15
            if score <= -100:
                gameOver = False

        if petri_list:
            for pr in petri_list:
                win.blit(petri, pr)
                pr.x -= 5
            if player_rect.colliderect(pr):
                petri_list.remove(pr)
                score -= 70
            if score <= -100:
                gameOver = False

        bg_x -= 2

        if bg_x == -win_width:
            bg_x = 0
        if animCount + 1 >= FPS:
            animCount = 0
        if right:
            win.blit(walkRight[animCount // 2], (x , y))
            animCount += 1
        elif left:
            win.blit(walkLeft[animCount // 2], (x, y))
            animCount += 1
        else:
            win.blit(playerFace, (x, y))

        stamina_bar_length = 200
        stamina_ratio = stamina / max_stamina
        pygame.draw.rect(win, grey, (10, 10, stamina_bar_length, 20))
        pygame.draw.rect(win, blue, (10, 10, stamina_bar_length * stamina_ratio, 20))

        scoreMonitor = font30.render("Score: " + str(score), 0, red)
        win.blit(scoreMonitor, (1000, 50))

        if score >= 100:
            win.fill(black)
            win.blit(labelWin, (450, 150))
            win.blit(labelPlayAgain, rectPlayAgain)
            mouse = pygame.mouse.get_pos()
            if rectPlayAgain.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameOver = True
                score = 0
                boomerang_list.clear()
                coconut_list.clear()
                petri_list.clear()
                x, y = 50, 400
                stamina = max_stamina
    else:
        win.fill(black)
        win.blit(labelGameOver, (450, 150))
        win.blit(labelResetGame, rectResetGame)
        mouse = pygame.mouse.get_pos()
        if rectResetGame.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameOver = True
            score = 0
            boomerang_list.clear()
            coconut_list.clear()
            petri_list.clear()
            x, y = 50, 400
            stamina = max_stamina


while True:
    clock.tick(FPS)
    for i in event.get():
        if i.type == QUIT:
            quit()
        elif i.type == boomerang_timer:
            boomerang_list.append(boomerang.get_rect(topleft = (boomerang_x, 520)))
        elif i.type == coconut_timer:
            coconut_list.append(coconut.get_rect(topleft = (player_rect.x, coconut_y)))
        elif i.type == petri_timer:
            petri_list.append(petri.get_rect(topleft = (petri_x, 540)))

    keys = key.get_pressed()
    if not isJump:
        if keys[K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            if jumpCount < 0:
                y += (jumpCount ** 2) / 1.5
            else:
                y -= (jumpCount ** 2) / 1.5
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    if keys[pygame.K_LSHIFT] and stamina > 0:
        current_speed = run_speed
        stamina -= stamina_decrease
        running = True
    else:
        current_speed = speed
        running = False
        if stamina < max_stamina:
            stamina += stamina_increase
    if keys[K_d] and x < win_width - width:
        x += current_speed
        right = True
        left = False
    elif keys[K_a] and x >= 0:
        x -= current_speed
        left = True
        right = False
    else:
        left = False
        right = False
        animCount = 0
    stamina = max(0, min(stamina, max_stamina))
    draw()
    display.update()
