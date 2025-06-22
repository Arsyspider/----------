import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Платформер с улучшенными коллизиями')

# Цвета
SKY_BLUE = (66, 170, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Параметры игрока
PLAYER_WIDTH, PLAYER_HEIGHT = 32, 64
PLAYER_SPEED = 5
JUMP_FORCE = 15
GRAVITY = 0.5
MAX_FALL_SPEED = 20

# Класс игрока
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing_right = True
        
        # Дополнительные хитбоксы для более точных коллизий
        self.feet_rect = pygame.Rect(0, 0, PLAYER_WIDTH - 10, 10)
        self.head_rect = pygame.Rect(0, 0, PLAYER_WIDTH - 10, 10)
        self.left_rect = pygame.Rect(0, 0, 5, PLAYER_HEIGHT - 20)
        self.right_rect = pygame.Rect(0, 0, 5, PLAYER_HEIGHT - 20)
        self.update_hitboxes()
    
    def update_hitboxes(self):
        """Обновление дополнительных хитбоксов"""
        self.feet_rect.midbottom = self.rect.midbottom
        self.head_rect.midtop = self.rect.midtop
        self.left_rect.midleft = (self.rect.left, self.rect.centery)
        self.right_rect.midright = (self.rect.right, self.rect.centery)
    
    def move(self, blocks):
        """Обновление позиции с проверкой коллизий"""
        # Применяем гравитацию
        self.velocity.y = min(self.velocity.y + GRAVITY, MAX_FALL_SPEED)
        
        # Движение по X
        self.rect.x += self.velocity.x
        self.update_hitboxes()
        self.check_horizontal_collisions(blocks)
        
        # Движение по Y
        self.rect.y += self.velocity.y
        self.update_hitboxes()
        self.check_vertical_collisions(blocks)
    
    def check_horizontal_collisions(self, blocks):
        """Проверка коллизий по горизонтали"""
        for block in blocks:
            if self.rect.colliderect(block):
                if self.velocity.x > 0:  # Движение вправо
                    self.rect.right = block.left
                elif self.velocity.x < 0:  # Движение влево
                    self.rect.left = block.right
                self.update_hitboxes()
    
    def check_vertical_collisions(self, blocks):
        """Проверка коллизий по вертикали"""
        self.on_ground = False
        for block in blocks:
            if self.rect.colliderect(block):
                if self.velocity.y > 0:  # Падение вниз
                    self.rect.bottom = block.top
                    self.on_ground = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:  # Прыжок вверх
                    self.rect.top = block.bottom
                    self.velocity.y = 0
                self.update_hitboxes()
    
    def draw(self, surface):
        """Отрисовка игрока и хитбоксов (для отладки)"""
        pygame.draw.rect(surface, RED, self.rect)
        # Отрисовка дополнительных хитбоксов (можно убрать в финальной версии)
        pygame.draw.rect(surface, (0, 255, 0), self.feet_rect, 1)
        pygame.draw.rect(surface, (0, 0, 255), self.head_rect, 1)
        pygame.draw.rect(surface, (255, 255, 0), self.left_rect, 1)
        pygame.draw.rect(surface, (255, 255, 0), self.right_rect, 1)

# Создание мира
def create_world():
    blocks = []
    # Пол (земля)
    for x in range(0, WIDTH, 32):
        blocks.append(pygame.Rect(x, HEIGHT - 32, 32, 32))
        blocks.append(pygame.Rect(x, HEIGHT - 64, 32, 32))
    
    # Несколько платформ для теста
    blocks.append(pygame.Rect(300, HEIGHT - 200, 200, 20))
    blocks.append(pygame.Rect(600, HEIGHT - 300, 200, 20))
    blocks.append(pygame.Rect(900, HEIGHT - 400, 200, 20))
    
    return blocks

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    player = Player(100, HEIGHT - 100)
    blocks = create_world()
    
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Управление
        keys = pygame.key.get_pressed()
        player.velocity.x = 0
        
        if keys[pygame.K_d]:
            player.velocity.x = PLAYER_SPEED
            player.facing_right = True
        if keys[pygame.K_a]:
            player.velocity.x = -PLAYER_SPEED
            player.facing_right = False
        if keys[pygame.K_w] and player.on_ground:
            player.velocity.y = -JUMP_FORCE
            player.on_ground = False
        
        # Обновление игрока
        player.move(blocks)
        
        # Отрисовка
        screen.fill(SKY_BLUE)
        
        # Отрисовка блоков
        for block in blocks:
            pygame.draw.rect(screen, (100, 100, 100), block)
        
        # Отрисовка игрока
        player.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()