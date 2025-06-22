import pygame
import socket
import pickle
import zlib
import threading
import sys
import webbrowser
from pygame import Vector2

class NetworkClient:
    def __init__(self, host='192.168.68.113', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(10.0)
        self.host = host
        self.port = port
        self.addr = None
        self.connected = False
        self.player_data = None
        self.other_players = {}
        self.blocks = []
        self.lock = threading.Lock()
    
    def connect(self, player_data):
        try:
            self.client.connect((self.host, self.port))
            self.addr = self.client.getsockname()
            self.player_data = player_data
            self.connected = True
            
            # Получаем начальное состояние мира
            initial_data = self.receive_data()
            if initial_data:
                with self.lock:
                    self.blocks = initial_data.get('blocks', [])
                    self.other_players = initial_data.get('players', {})
            
            # Запускаем поток для получения обновлений
            threading.Thread(target=self.receive_updates, daemon=True).start()
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def send_data(self, data):
        try:
            serialized = zlib.compress(pickle.dumps(data))
            # Сначала отправляем размер данных
            self.client.sendall(len(serialized).to_bytes(4, byteorder='big'))
            # Затем сами данные
            self.client.sendall(serialized)
        except Exception as e:
            print(f"Ошибка отправки данных: {e}")
            self.connected = False
    
    def receive_data(self):
        try:
            # Получаем размер данных
            size_bytes = self.client.recv(4)
            if not size_bytes:
                return None
                
            data_size = int.from_bytes(size_bytes, byteorder='big')
            received_data = bytearray()
            
            # Получаем данные по частям
            while len(received_data) < data_size:
                chunk = self.client.recv(min(4096, data_size - len(received_data)))
                if not chunk:
                    return None
                received_data.extend(chunk)
            
            # Распаковываем данные
            return pickle.loads(zlib.decompress(received_data))
        except Exception as e:
            print(f"Ошибка получения данных: {e}")
            return None
    
    def receive_updates(self):
        while self.connected:
            data = self.receive_data()
            if data is None:
                self.connected = False
                break
                
            with self.lock:
                if data.get('type') == 'player_update':
                    self.other_players[data['address']] = data['data']
                elif data.get('type') == 'player_left':
                    if data['address'] in self.other_players:
                        del self.other_players[data['address']]
                elif data.get('type') == 'block_update':
                    block_data = data['data']
                    if block_data['action'] == 'add':
                        # Проверяем, нет ли уже такого блока
                        existing = False
                        for b in self.blocks:
                            if b[1] == block_data['x'] and b[2] == block_data['y']:
                                existing = True
                                break
                        
                        if not existing:
                            self.blocks.append((
                                block_data['block_type'],
                                block_data['x'],
                                block_data['y']
                            ))
                    elif block_data['action'] == 'remove':
                        self.blocks = [
                            b for b in self.blocks 
                            if not (b[1] == block_data['x'] and b[2] == block_data['y'])
                        ]

class MultiplayerGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        # Настройки экрана
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Майн - Мультиплеер')
        
        # Загрузка изображений
        self.player_img = pygame.image.load('images/лыцарь.png').convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (32, 64))
        
        self.block_images = [
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
        
        # Настройки игры
        self.block_image_number = 1
        self.inventar = self.block_images[1]
        self.speed = 5
        self.jump_power = 15
        self.gravity = 0.8
        self.FPS = 60
        self.run = True
        self.world_size = 1000
        
        # Игрок
        self.player_rect = pygame.Rect(800, 66, 32, 64)
        self.player_velocity = Vector2(0, 0)
        self.left = False
        self.right = False
        self.on_ground = False
        
        # Камера
        self.camera_offset = Vector2(0, 0)
        self.update_camera()
        
        # Сетевое подключение
        self.network = NetworkClient()
        self.connect_to_server()
        
        # Донат
        self.donat = pygame.image.load('images/да2.png').convert_alpha()
        self.donat_rect = self.donat.get_rect()
        self.donat_rect.topleft = (0, 0)
        
        # Выбор блоков
        self.select_block = pygame.image.load('images/выбор блока.png').convert_alpha()
        self.select_block_rect = self.select_block.get_rect()
        
        # Для проверки размещения блоков
        self.can_place_block = False
    
    def connect_to_server(self):
        player_data = {
            'x': self.player_rect.x,
            'y': self.player_rect.y,
            'velocity_x': self.player_velocity.x,
            'velocity_y': self.player_velocity.y,
            'image_num': 0
        }
        
        if not self.network.connect(player_data):
            print("Не удалось подключиться к серверу")
            self.run = False
    
    def update_camera(self):
        self.camera_offset.x = self.player_rect.x - self.SCREEN_WIDTH // 2 + self.player_rect.width // 2
        self.camera_offset.y = self.player_rect.y - self.SCREEN_HEIGHT // 2 + self.player_rect.height // 2
        self.camera_offset.x = max(0, min(self.camera_offset.x, self.world_size * 32 - self.SCREEN_WIDTH))
        self.camera_offset.y = max(0, min(self.camera_offset.y, 800 - self.SCREEN_HEIGHT))
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_world_x = mouse_pos[0] + self.camera_offset.x
        mouse_world_y = mouse_pos[1] + self.camera_offset.y
        
        # Позиция для нового блока
        block_x = (mouse_world_x // 32) * 32
        block_y = (mouse_world_y // 32) * 32
        new_block_rect = pygame.Rect(block_x, block_y, 32, 32)
        
        # Проверяем возможность размещения блока
        self.can_place_block = True
        
        # Проверка коллизии с существующими блоками
        with self.network.lock:
            block_rects = [pygame.Rect(b[1], b[2], 32, 32) for b in self.network.blocks]
            if new_block_rect.collidelist(block_rects) != -1:
                self.can_place_block = False
            
            # Проверка коллизии с игроком
            if new_block_rect.colliderect(self.player_rect):
                self.can_place_block = False
            
            # Проверка коллизии с другими игроками
            for player_data in self.network.other_players.values():
                player_rect = pygame.Rect(player_data['x'], player_data['y'], 32, 64)
                if new_block_rect.colliderect(player_rect):
                    self.can_place_block = False
                    break
        
        # Проверка расстояния
        player_center = Vector2(self.player_rect.center)
        block_center = Vector2(block_x + 16, block_y + 16)
        distance = player_center.distance_to(block_center)
        
        if distance > 150:  # Максимальное расстояние для размещения
            self.can_place_block = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.right = True
                if event.key == pygame.K_a:
                    self.left = True
                if event.key == pygame.K_w and self.on_ground:
                    self.player_velocity.y = -self.jump_power
                    self.on_ground = False
                if event.key == pygame.K_LSHIFT:
                    self.speed = 10
                
                if pygame.K_1 <= event.key <= pygame.K_9:
                    self.block_image_number = event.key - pygame.K_1 + 1
                    if self.block_image_number < len(self.block_images):
                        self.inventar = self.block_images[self.block_image_number]
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.right = False
                if event.key == pygame.K_a:
                    self.left = False
                if event.key == pygame.K_LSHIFT:
                    self.speed = 5
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3 and self.can_place_block:  # Правая кнопка - установка блока
                    block_data = {
                        'type': 'block_update',
                        'data': {
                            'action': 'add',
                            'block_type': self.block_image_number,
                            'x': block_x,
                            'y': block_y
                        }
                    }
                    self.network.send_data(block_data)
                
                if event.button == 1:  # Левая кнопка - разрушение
                    if pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1).colliderect(self.donat_rect):
                        webbrowser.get(using='windows-default').open_new_tab('https://www.donationalerts.com/r/arsyspider')
                    else:
                        with self.network.lock:
                            for block in self.network.blocks[:]:
                                block_world_rect = pygame.Rect(block[1], block[2], 32, 32)
                                if block_world_rect.collidepoint(mouse_world_x, mouse_world_y):
                                    block_data = {
                                        'type': 'block_update',
                                        'data': {
                                            'action': 'remove',
                                            'x': block[1],
                                            'y': block[2]
                                        }
                                    }
                                    self.network.send_data(block_data)
                                    break
            
            if event.type == pygame.MOUSEWHEEL:
                self.block_image_number += event.y
                self.block_image_number = max(1, min(9, self.block_image_number))
                self.inventar = self.block_images[self.block_image_number]
    
    def update_player(self):
        # Горизонтальное движение
        self.player_velocity.x = 0
        if self.right:
            self.player_velocity.x = self.speed
        if self.left:
            self.player_velocity.x = -self.speed
        
        # Гравитация
        self.player_velocity.y += self.gravity
        
        # Сохраняем предыдущую позицию
        old_x, old_y = self.player_rect.x, self.player_rect.y
        
        # Перемещение по X
        self.player_rect.x += self.player_velocity.x
        
        # Проверка коллизий по X
        with self.network.lock:
            block_rects = [pygame.Rect(b[1], b[2], 32, 32) for b in self.network.blocks]
            for block in block_rects:
                if self.player_rect.colliderect(block):
                    if self.player_velocity.x > 0:
                        self.player_rect.right = block.left
                    elif self.player_velocity.x < 0:
                        self.player_rect.left = block.right
                    self.player_velocity.x = 0
                    break
        
        # Перемещение по Y
        self.player_rect.y += self.player_velocity.y
        self.on_ground = False
        
        # Проверка коллизий по Y
        with self.network.lock:
            for block in block_rects:
                if self.player_rect.colliderect(block):
                    if self.player_velocity.y > 0:
                        self.player_rect.bottom = block.top
                        self.on_ground = True
                    elif self.player_velocity.y < 0:
                        self.player_rect.top = block.bottom
                    self.player_velocity.y = 0
                    break
        
        # Границы мира
        self.player_rect.x = max(0, min(self.player_rect.x, self.world_size * 32 - self.player_rect.width))
        self.player_rect.y = max(0, min(self.player_rect.y, 800 - self.player_rect.height))
        
        if self.player_rect.bottom >= 800:
            self.on_ground = True
            self.player_rect.bottom = 800
            self.player_velocity.y = 0
        
        # Отправляем обновление позиции на сервер
        if old_x != self.player_rect.x or old_y != self.player_rect.y:
            self.network.send_data({
                'type': 'player_update',
                'data': {
                    'x': self.player_rect.x,
                    'y': self.player_rect.y,
                    'velocity_x': self.player_velocity.x,
                    'velocity_y': self.player_velocity.y,
                    'image_num': 0
                }
            })
    
    def render(self):
        self.screen.fill((66, 170, 255))
        
        # Отрисовка блоков
        with self.network.lock:
            for block in self.network.blocks:
                block_type, x, y = block
                if 0 <= block_type < len(self.block_images):
                    self.screen.blit(
                        self.block_images[block_type],
                        (x - self.camera_offset.x, y - self.camera_offset.y)
                    )
            
            # Отрисовка других игроков
            for player_data in self.network.other_players.values():
                self.screen.blit(
                    self.player_img,
                    (player_data['x'] - self.camera_offset.x, 
                     player_data['y'] - self.camera_offset.y)
                )
        
        # Отрисовка текущего игрока
        self.screen.blit(
            self.player_img,
            (self.player_rect.x - self.camera_offset.x, 
             self.player_rect.y - self.camera_offset.y)
        )
        
        # Отрисовка доната
        self.screen.blit(self.donat, self.donat_rect)
        
        # Отрисовка выделения блока
        mouse_pos = pygame.mouse.get_pos()
        mouse_world_x = (mouse_pos[0] + self.camera_offset.x) // 32 * 32
        mouse_world_y = (mouse_pos[1] + self.camera_offset.y) // 32 * 32
        self.select_block_rect.x = mouse_world_x - self.camera_offset.x
        self.select_block_rect.y = mouse_world_y - self.camera_offset.y
        
        # Рисуем красный контур, если блок нельзя поставить
        if not self.can_place_block:
            pygame.draw.rect(self.screen, (255, 0, 0), self.select_block_rect, 2)
        self.screen.blit(self.select_block, self.select_block_rect)
        
        pygame.display.flip()
    
    def run_game(self):
        clock = pygame.time.Clock()
        while self.run:
            self.handle_events()
            self.update_player()
            self.update_camera()
            self.render()
            clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MultiplayerGame()
    game.run_game()
