import pygame
import sys
import webbrowser

pygame.init()
pygame.font.init()

# Настройки экрана
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Майн')

# Загрузка изображений
player_img = pygame.image.load('images/лыцарь.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (32, 64))

block_images = [
    pygame.image.load('images/air.png').convert_alpha(),
    pygame.image.load('images/доски.png').convert_alpha(),
    pygame.image.load('images/дерево.png').convert_alpha(),
    pygame.image.load('images/дёрн.png').convert_alpha(),
    pygame.image.load('images/булыжник.png').convert_alpha(),
    pygame.image.load('images/кирпич.png').convert_alpha(),
    pygame.image.load('images/стекло.png').convert_alpha(),
    pygame.image.load('images/камень.png').convert_alpha(),
    pygame.image.load('images/дверь.png').convert_alpha(),
    pygame.image.load('images/листва2.png').convert_alpha(),
    pygame.image.load('images/инвентарь.png').convert_alpha()
]

# Основные переменные
block_image_number = 1
inventar = block_images[1]
speed = 5
jump_power = 15
gravity = 0.8
FPS = 60
run = True
world_size = 1000
block_build_place = pygame.Rect(32, 32, 34, 34)

# Игрок
player_rect = pygame.Rect(800, 66, 32, 64)
player_velocity = pygame.math.Vector2(0, 0)
left = False
right = False
on_ground = False

# Камера
camera_offset = pygame.math.Vector2(0, 0)
camera_offset.x = player_rect.x - SCREEN_WIDTH // 2 + player_rect.width // 2
camera_offset.y = player_rect.y - SCREEN_HEIGHT // 2 + player_rect.height // 2

# Блоки
blocks = []
block_rects = []

# Донат
donat = pygame.image.load('images/да2.png').convert_alpha()
donat_rect = donat.get_rect()
donat_rect.topleft = (0, 0)

# Выбор блоков
select_block = pygame.image.load('images/выбор блока.png').convert_alpha()
select_block_rect = select_block.get_rect()

class Block:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = pygame.Rect(x, y, 32, 32)
        self.original_pos = (x, y)
    
    def draw(self, surface, camera_offset):
        surface.blit(self.image, (self.original_pos[0] - camera_offset.x, 
                                self.original_pos[1] - camera_offset.y))

def create_world():
    for b in range(world_size):
        blocks.append(Block(block_images[7], b * 32, 768))
        block_rects.append(pygame.Rect(b * 32, 768, 32, 32))
    
    for b in range(world_size):
        blocks.append(Block(block_images[7], b * 32, 736))
        block_rects.append(pygame.Rect(b * 32, 736, 32, 32))
    
    for b in range(world_size):
        blocks.append(Block(block_images[3], b * 32, 704))
        block_rects.append(pygame.Rect(b * 32, 704, 32, 32))

create_world()

def update_camera():
    camera_offset.x = player_rect.x - SCREEN_WIDTH // 2 + player_rect.width // 2
    camera_offset.y = player_rect.y - SCREEN_HEIGHT // 2 + player_rect.height // 2
    camera_offset.x = max(0, min(camera_offset.x, world_size * 32 - SCREEN_WIDTH))
    camera_offset.y = max(0, min(camera_offset.y, 800 - SCREEN_HEIGHT))

def handle_events():
    global run, left, right, block_image_number, inventar, player_velocity, on_ground
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_world_x = mouse_pos[0] + camera_offset.x
    mouse_world_y = mouse_pos[1] + camera_offset.y
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_w and on_ground:
                player_velocity.y = -jump_power
                on_ground = False
            if event.key == pygame.K_LSHIFT:
                speed = 10
            
            if pygame.K_1 <= event.key <= pygame.K_9:
                block_image_number = event.key - pygame.K_1 + 1
                if block_image_number < len(block_images):
                    inventar = block_images[block_image_number]
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_LSHIFT:
                speed = 5
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Правая кнопка - установка блока
                block_x = (mouse_world_x // 32) * 32
                block_y = (mouse_world_y // 32) * 32
                block_build_place.x = (mouse_world_x // 32) * 32 - 1
                block_build_place.y = (mouse_world_y // 32) * 32 - 1
                new_block_rect = pygame.Rect(block_x, block_y, 32, 32)
                #if new_block_rect.collidelist(block_rects) == 1:
                if block_build_place.collidelist(block_rects) >= 1:
                    blocks.append(Block(inventar, block_x, block_y))
                    block_rects.append(new_block_rect)
            
            if event.button == 1:  # Левая кнопка - разрушение
                if pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1).colliderect(donat_rect):
                    webbrowser.get(using='windows-default').open_new_tab('https://www.donationalerts.com/r/arsyspider')
                else:
                    for i, block in enumerate(blocks[:]):
                        block_world_rect = pygame.Rect(
                            block.original_pos[0], block.original_pos[1], 32, 32
                        )
                        if block_world_rect.collidepoint(mouse_world_x, mouse_world_y):
                            del block_rects[i]
                            del blocks[i]
                            break
        
        if event.type == pygame.MOUSEWHEEL:
            block_image_number += event.y
            block_image_number = max(1, min(9, block_image_number))
            inventar = block_images[block_image_number]

def update_player():
    global on_ground
    
    # Горизонтальное движение
    player_velocity.x = 0
    if right:
        player_velocity.x = speed
    if left:
        player_velocity.x = -speed
    
    # Гравитация
    player_velocity.y += gravity
    
    # Сохраняем предыдущую позицию для корректного определения коллизий
    old_x, old_y = player_rect.x, player_rect.y
    
    # Предварительное перемещение по X
    player_rect.x += player_velocity.x
    
    # Проверка коллизий по X
    for block in block_rects:
        if player_rect.colliderect(block):
            if player_velocity.x > 0:  # Движение вправо
                player_rect.right = block.left
            elif player_velocity.x < 0:  # Движение влево
                player_rect.left = block.right
            player_velocity.x = 0
            break
    
    # Предварительное перемещение по Y
    player_rect.y += player_velocity.y
    on_ground = False
    
    # Проверка коллизий по Y
    for block in block_rects:
        if player_rect.colliderect(block):
            if player_velocity.y > 0:  # Падение вниз
                player_rect.bottom = block.top
                on_ground = True
            elif player_velocity.y < 0:  # Прыжок вверх
                player_rect.top = block.bottom
            player_velocity.y = 0
            break
    
    # Ограничение границами мира
    player_rect.x = max(0, min(player_rect.x, world_size * 32 - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, 800 - player_rect.height))
    
    # Если игрок на нижней границе - он на земле
    if player_rect.bottom >= 800:
        on_ground = True
        player_rect.bottom = 800
        player_velocity.y = 0

def render():
    screen.fill((66, 170, 255))
    
    # Отрисовка блоков
    for block in blocks:
        block.draw(screen, camera_offset)
    
    # Отрисовка игрока
    screen.blit(player_img, (player_rect.x - camera_offset.x, player_rect.y - camera_offset.y))
    
    # Отрисовка доната
    screen.blit(donat, donat_rect)
    
    # Отрисовка выделения блока
    mouse_pos = pygame.mouse.get_pos()
    mouse_world_x = (mouse_pos[0] + camera_offset.x) // 32 * 32
    mouse_world_y = (mouse_pos[1] + camera_offset.y) // 32 * 32
    select_block_rect.x = mouse_world_x - camera_offset.x
    select_block_rect.y = mouse_world_y - camera_offset.y
    screen.blit(select_block, select_block_rect)
    
    pygame.display.flip()

# Основной игровой цикл
clock = pygame.time.Clock()
while run:
    handle_events()
    update_player()
    update_camera()
    render()
    clock.tick(FPS)

pygame.quit()
