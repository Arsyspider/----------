import pygame
import random
#import math
import sys
import pygame as pg
from pygame.locals import *
import time
import webbrowser
import threading


pygame.init()
pygame.font.init()


pg.event.set_allowed([pg.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL, pygame.MOUSEWHEEL, pygame.KEYUP])

#pg.init()

pygame.display.set_caption('майн')
width = 1600
heith = 800

screen = pygame.display.set_mode((width, heith))



player = pygame.image.load('images\лыцарь.png').convert_alpha()
player = pygame.transform.scale(player, (32, 64))




block_images = [pygame.image.load('images/air.png').convert_alpha(),
pygame.image.load('images\доски.png').convert_alpha(),
pygame.image.load('images\дерево.png').convert_alpha(),
pygame.image.load('images\дёрн.png').convert_alpha(),
pygame.image.load('images\булыжник.png').convert_alpha(),
pygame.image.load('images\кирпич.png').convert_alpha(),
pygame.image.load('images\стекло.png').convert_alpha(),
pygame.image.load('images\камень.png').convert_alpha(),
pygame.image.load('images\дверь.png').convert_alpha(),
pygame.image.load('images\листва2.png').convert_alpha(),
pygame.image.load('images\инвентарь.png').convert_alpha()]





block_image_number = 1

donat = pygame.image.load('images\да2.png').convert_alpha()
inventar = block_images[1]
donat_rect = donat.get_rect()
donat_rect.x = 0


build_rect = Rect(0, 0, 320, 320)
mouse_rect = Rect(0, 0, 1, 1)



select_block = pygame.image.load('images\выбор блока.png').convert_alpha()
#player_rect = player.get_rect()
player_rect = pygame.Rect(0, 0, 32, 67)
player_R = pygame.Rect(0, 0, 5, 67)
player_L = pygame.Rect(0, 0, 5, 67)
select_block_rect = select_block.get_rect()

player_rect.x = 800
player_rect.y = 66


left = False
right = False

speed = 5
del_block_rect = Rect(-100, -100, 10, 10)






class block(pygame.sprite.Sprite):
    def __init__( self, image, x, y, ):
        pygame.sprite.Sprite.__init__(self)
        self.image    = image
        self.rect     = self.image.get_rect()
        self.rect.center = ( x + 16, y + 16)
    def update(self):
        #self.rect.move_ip(0,5)
        if self.rect.colliderect(del_block_rect):
            self.kill()
        if self.rect.colliderect(mouse_rect):
            select_block_rect.x = self.rect.x
            select_block_rect.y = self.rect.y
        if right:
            i = block_rects.index((self.rect[0], self.rect[1], 33, 33))
            block_rects[i] = ((self.rect[0] - speed * 1, self.rect[1], 33, 33))
            self.rect.move_ip(speed * -1,0)
            select_block_rect.x = self.rect.x
            #block_rects.clear()
            #block_rects.append(self.rect)
        if left:
            i = block_rects.index((self.rect[0], self.rect[1], 33, 33))
            block_rects[i] = ((self.rect[0] - speed * -1, self.rect[1], 33, 33))
            self.rect.move_ip(speed,0)
            select_block_rect.x = self.rect.x


            

block_rect = pygame.Rect(0, 0, 33, 33)


block_rects = []



speed = 5
run = True
clock = pygame.time.Clock()
na_zemle = False

jump = 0

def update():
    screen.fill((66, 170, 255))
    #screen.blit(back, (0, 0))
    screen.blit(player, (player_rect.x, player_rect.y))
    blocks.draw(screen)
    if select_block_rect.collidelist(block_rects) >= 0:
        screen.blit(select_block, (select_block_rect.x, select_block_rect.y))
    screen.blit(donat, (0, 0))
    #pygame.draw.rect(screen, (255, 255, 255), build_rect)
    pygame.display.flip()



block_index = 0

def select():
    if mouse_rect.x > select_block_rect.x:
        select_block_rect.x += 32
    if mouse_rect.x < select_block_rect.x:
        select_block_rect.x -= 32
    if mouse_rect.y > select_block_rect.y:
        select_block_rect.y += 32
    if mouse_rect.y < select_block_rect.y:
        select_block_rect.y -= 32

blocks = pygame.sprite.Group()





delite_blocks = False


block_detect = Rect(select_block_rect.x - 2, select_block_rect.y - 2, 36, 36)


def control():
    global block_index
    global speed
    global up
    global right
    global left
    global blocks
    global select_block_rect
    global inventar
    global jump
    global block_image_number
    global block_image_number
    global del_block_rect
    global delite_blocks
    global build_rect
    global mouse_rect
    global player_rect
    global select_block_rect
    build_rect.x = player_rect.x - 160
    build_rect.y = player_rect.y - 160
    block_detect = Rect(select_block_rect.x - 2, select_block_rect.y - 2, 36, 36)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # window close X pressed
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_w:
                if player_rect.collidelist(block_rects) >= 0:
                    jump = 15
                    player_rect.y -= jump
            if event.key == pygame.K_LSHIFT:
                speed = 10
                    
            if event.key == pygame.K_1:
                block_image_number = 1
                inventar = block_images[block_image_number]
            if event.key == pygame.K_2:
                block_image_number = 2
                inventar = block_images[block_image_number]
            if event.key == pygame.K_3:
                block_image_number = 3
                inventar = block_images[block_image_number]
            if event.key == pygame.K_4:
                block_image_number = 4
                inventar = block_images[block_image_number]
            if event.key == pygame.K_5:
                block_image_number = 5
                inventar = block_images[block_image_number]
            if event.key == pygame.K_6:
                block_image_number = 6
                inventar = block_images[block_image_number]
            if event.key == pygame.K_7:
                block_image_number = 7
                inventar = block_images[block_image_number]
            if event.key == pygame.K_8:
                block_image_number = 8
                inventar = block_images[block_image_number]
            if event.key == pygame.K_9:
                block_image_number = 9
                inventar = block_images[block_image_number]
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  #  правая кнопка мыши
                if not right:
                    if not left:
                        block_detect.x = select_block_rect.x
                        block_detect.y = select_block_rect.y
                        if block_detect.collidelist(block_rects) >= 0:
                            if build_rect.colliderect(select_block_rect) > 0:
                                blocks.add(block(inventar, select_block_rect.x, select_block_rect.y))
                                block_rects.append(block_rect)
            if event.button == 1:#  левая кнопка мыши
                if mouse_rect.colliderect(donat_rect):
                    webbrowser.get(using='windows-default').open_new_tab('https://www.donationalerts.com/r/arsyspider')
                elif block_rects:
                    if build_rect.colliderect(select_block_rect) > 0:
                        if block_rect in block_rects:
                            delite_blocks = True
                            block_index = block_rects.index(block_rect)
                            block_rects.pop(block_index)
                            blocks.remove(block)
                            ##delite_blocks = False
                            #blocks.add(air(block_images[0], select_block_rect.x, select_block_rect.y))
                            #blocks.remove(0)
                            ##delite_blocks = True
                            #del_block_rect.x = -100
                            #del_block_rect.y = -100
                    if not block_rect in block_rects:
                        block_index = 0
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                    delite_blocks = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                block_image_number -= 1
            if event.y == -1:
                block_image_number += 1
                    
                        #blocks.remove(0) НАДО СДЕЛАТЬ НОРМАЛЬНОЕ УДАЛЕНИЕ!!!!!!!!
                #block(unitaz, 16.5, 16.5).kill()
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = False
                if event.key == pygame.K_a:
                    left = False
                if event.key == pygame.K_w:
                    up = False
                if event.key == pygame.K_LSHIFT:
                    speed = 5
                

########################################################################################
    #if right == True:
        #player_rect.x += speed
    #if left == True:
        #player_rect.x -= speed
    #if down == True:
        #player_rect.y += speed
FPS = 60









def create_world():
    for b in range(500):
        blocks.add(block(block_images[7] , b * 32, 768))
        block_rect = (b * 32, 768, 33, 33)
        block_rects.append(block_rect)
    for b in range(500):
        blocks.add(block(block_images[7] , b * 32, 736))
        block_rect = (b * 32, 736, 33, 33)
        block_rects.append(block_rect)
    for b in range(500):
        blocks.add(block(block_images[3] , b * 32, 704))
        block_rect = (b * 32, 704, 33, 33)
        block_rects.append(block_rect)

create_world()




#def video():
#    clock.tick(600)
#    while True:
#        update()

#thread_video = threading.Thread(target=video)
#thread_video.daemon = True
#thread_video.start()


#def selectX():
#    clock.tick(60)
#    while True:
#        select()

#thread_select = threading.Thread(target=selectX)
#thread_select.daemon = True
#thread_select.start()





selectX = 0
selectY = 0


def delite_blocks_toogle():
    global delite_blocks
    if delite_blocks:
        del_block_rect.x = select_block_rect.x + 16
        del_block_rect.y = select_block_rect.y + 16
        if block_rect in block_rects:
            delite_blocks = True
            block_index = block_rects.index(block_rect)
            block_rects.pop(block_index)
            blocks.remove(block)
    if not delite_blocks:
        del_block_rect.x = -100
        del_block_rect.y = -100

while run:
    if block_image_number > 9:
        block_image_number = 1
    if block_image_number < 0:
        block_image_number = 9


    delite_blocks_toogle()

    blocks.update()
    inventar = block_images[block_image_number]


    #block_rect.x = select_block_rect.x 
    #block_rect.y = select_block_rect.y

    block_rect = (select_block_rect.x, select_block_rect.y, 33, 33)
    clock.tick(FPS)


    if selectX != select_block_rect.x:
        selectX = select_block_rect.x
    if selectY != select_block_rect.y:
        selectY = select_block_rect.y



    mouse_rect.x, mouse_rect.y = pygame.mouse.get_pos()




    
    if player_rect.collidelist(block_rects) <= 0:
        jump -= 1
        player_rect.y -= jump
    update()
    control()
    select()



