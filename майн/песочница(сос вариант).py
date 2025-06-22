import pygame
import random
import math
import sys
import pygame as pg
from pygame.locals import *
import time
import webbrowser
import threading


pygame.init()

flags = FULLSCREEN | DOUBLEBUF


pg.event.set_allowed([pg.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL, pygame.MOUSEWHEEL, pygame.KEYUP])

pygame.font.init()
pg.init()

pygame.display.set_caption('майн')
width = 1600
heith = 800

resolution = (width, heith)
screen = pygame.display.set_mode((width, heith))
#screen = pygame.display.set_mode(resolution, flags, 8)



player = pygame.image.load('images\лыцарь.png').convert_alpha()
player = pygame.transform.scale(player, (32, 64))

#back = pygame.image.load('images\фон3.png').convert_alpha()



#block_images = [pygame.image.load('images/air.png').convert_alpha(),
#pygame.image.load('images\доски.png').convert_alpha(),
#pygame.image.load('images\дерево.png').convert_alpha(),
#pygame.image.load('images\дёрн.png').convert_alpha(),
#pygame.image.load('images\булыжник.png').convert_alpha(),
#pygame.image.load('images\кирпич.png').convert_alpha(),
#pygame.image.load('images\стекло.png').convert_alpha(),
#pygame.image.load('images\камень.png').convert_alpha(),
#pygame.image.load('images\дверь.png').convert_alpha(),
#pygame.image.load('images\листва2.png').convert_alpha(),
#pygame.image.load('images\инвентарь.png').convert_alpha()]

block_images = [pygame.image.load('images/air.png').convert(),
pygame.image.load('images\доски.png').convert(),
pygame.image.load('images\дерево.png').convert(),
pygame.image.load('images\дёрн.png').convert(),
pygame.image.load('images\булыжник.png').convert(),
pygame.image.load('images\кирпич.png').convert(),
pygame.image.load('images\стекло.png').convert(),
pygame.image.load('images\камень.png').convert(),
pygame.image.load('images\дверь.png').convert(),
pygame.image.load('images\листва2.png').convert(),
pygame.image.load('images\инвентарь.png').convert()]


inventory_select = pygame.image.load('images\выбор блока.png').convert_alpha()

block_image_number = 1

inventory = pygame.image.load('images\инвентарь.png').convert()
inventory_select = pygame.image.load('images\выбор блока.png').convert_alpha()
donat = pygame.image.load('images\да2.png').convert_alpha()
inventar = block_images[1]
inventory_selectX = 0
inventory_selectY = 0
donat_rect = donat.get_rect()
donat_rect.x = 1617


build_rect = Rect(0, 0, 320, 320)
mouse_rect = Rect(0, 0, 1, 1)



select_block = pygame.image.load('images\выбор блока.png').convert_alpha()
#player_rect = player.get_rect()
player_rect = Rect(0, 0, 32, 67)
player_R = Rect(0, 0, 5, 67)
player_L = Rect(0, 0, 5, 67)
select_block_rect = select_block.get_rect()


down = False
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


            

block_rect = (0, 0, 33, 33)

#block_rects = [(33, 33, 33, 33), (0, 627, 33, 33), (33, 627, 33, 33), (66, 627, 33, 33), (99, 627, 33, 33), (132, 627, 33, 33), (165, 627, 33, 33), (231, 627, 33, 33), (198, 627, 33, 33)]
block_rects = []



speed = 5
run = True
clock = pygame.time.Clock()
na_zemle = False

jump = 0
down = False
left = False
right = False

def update():
    screen.fill((66, 170, 255))
    #screen.blit(back, (0, 0))
    screen.blit(player, (player_rect.x, player_rect.y))
    blocks.draw(screen)
    if select_block_rect.collidelist(block_rects) >= 0:
        screen.blit(select_block, (select_block_rect.x, select_block_rect.y))
    screen.blit(inventory, (0, 0))
    screen.blit(donat, (1617, 0))
    screen.blit(inventory_select, (inventory_selectX, inventory_selectY))
    #pygame.draw.rect(screen, (255, 255, 255), build_rect)
    pygame.display.flip()


mouseX, mouseY = pygame.mouse.get_pos()

block_index = 0

def select():
    if mouseX > select_block_rect.x:
        select_block_rect.x += 32
    if mouseX < select_block_rect.x:
        select_block_rect.x -= 32
    if mouseY > select_block_rect.y:
        select_block_rect.y += 32
    if mouseY < select_block_rect.y:
        select_block_rect.y -= 32

blocks = pygame.sprite.Group()



player_rect.x = 800
player_rect.y = 66

delite_blocks = False


block_detect = Rect(select_block_rect.x - 2, select_block_rect.y - 2, 36, 36)


def control():
    global block_index
    global speed
    global up
    global down
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
            #if event.key == pygame.K_DOWN:
                #down = True
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
                if event.key == pygame.K_DOWN:
                    down = False
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
speed = 5




#blocks.add(block(block_images[7] , 0, 768))
#block_rects.append(block_rect)


#создание платформы   ####################################


def create_world():
    for b in range(50):
        blocks.add(block(block_images[7] , b * 32, 768))
        block_rect = (b * 32, 768, 33, 33)
        block_rects.append(block_rect)
    for b in range(50):
        blocks.add(block(block_images[7] , b * 32, 736))
        block_rect = (b * 32, 736, 33, 33)
        block_rects.append(block_rect)
    for b in range(50):
        blocks.add(block(block_images[3] , b * 32, 704))
        block_rect = (b * 32, 704, 33, 33)
        block_rects.append(block_rect)

create_world()
############################################################


#def pr():
#    print("hello")
    
#def prr():
#    while True:
#        pr()
#        time.sleep(1)


#thread = threading.Thread(target=prr)
#thread.daemon = True  # Поток будет завершен, когда основной поток завершится
#thread.start()

def video():
    clock.tick(600)
    while True:
        update()

thread_video = threading.Thread(target=video)
thread_video.daemon = True
thread_video.start()


def selectX():
    clock.tick(60)
    while True:
        select()

thread_select = threading.Thread(target=selectX)
thread_select.daemon = True
thread_select.start()


#abc = (1, 3, 4, 6)
#print(abc[0])
#bbb = (abc[0] + 32, abc[1], 4, 6)
#print(bbb)


selectX = 0
selectY = 0


while run:
    if block_image_number > 9:
        block_image_number = 1
    if block_image_number < 0:
        block_image_number = 9
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
    blocks.update()
    inventar = block_images[block_image_number]
    player_R = Rect(player_rect.x + 28, player_rect.y, 5, 55)
    player_L = Rect(player_rect.x, player_rect.y, 5, 55)
    if inventar == block_images[1]:
        inventory_selectX = 0
    if inventar == block_images[2]:
        inventory_selectX = 33
    if inventar == block_images[3]:
        inventory_selectX = 66
    if inventar == block_images[4]:
        inventory_selectX = 99
    if inventar == block_images[5]:
        inventory_selectX = 132
    if inventar == block_images[6]:
        inventory_selectX = 165
    if inventar == block_images[7]:
        inventory_selectX = 198
    if inventar == block_images[8]:
        inventory_selectX = 231
    if inventar == block_images[9]:
        inventory_selectX = 264

    block_rect = (select_block_rect.x, select_block_rect.y, 33, 33)
    clock.tick(FPS)


    if selectX != select_block_rect.x:
        selectX = select_block_rect.x
    
    if selectY != select_block_rect.y:
        selectY = select_block_rect.y

    mouseX, mouseY = pygame.mouse.get_pos()

    if mouse_rect.x != mouseX:
        mouse_rect.x = mouseX

    if mouse_rect.y != mouseY:
        mouse_rect.y = mouseY

    

    
    #if player_rect.collidelist(block_rects) >= 0:
        #if right == True:
            #player_rect.x -= speed
        #if left == True:
            #player_rect.x += speed
        #if down == True:
            #player_rect.y -= speed
    if player_R.collidelist(block_rects) >= 0:
        player_rect.x -= speed
    if player_L.collidelist(block_rects) >= 0:
        player_rect.x += speed
    if player_rect.collidelist(block_rects) <= 0:
        jump -= 1
        player_rect.y -= jump
    #update()
    control()
    #select()




