import socket
import threading
import pickle
import zlib
from collections import defaultdict

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(100)
        
        self.clients = []
        self.players = {}
        self.blocks = []
        self.lock = threading.Lock()
        
        self.create_world()
        print(f"Сервер запущен на {host}:{port}")

    def create_world(self):
        world_size = 1000
        # Каменное основание
        for b in range(world_size):
            self.blocks.append((7, b * 32, 768))  # Камень
            self.blocks.append((7, b * 32, 736))  # Камень
            self.blocks.append((3, b * 32, 704))  # Дёрн

    def send_data(self, conn, data):
        try:
            serialized = zlib.compress(pickle.dumps(data))
            if len(serialized) > 10 * 1024 * 1024:
                print("Предупреждение: слишком большой объект для отправки")
                return
            
            # Сначала отправляем размер данных (4 байта)
            conn.sendall(len(serialized).to_bytes(4, byteorder='big'))
            # Затем сами данные
            conn.sendall(serialized)
        except Exception as e:
            print(f"Ошибка отправки данных: {e}")
            raise

    def handle_client(self, client, address):
        print(f"Новое подключение: {address}")
        
        try:
            # Отправляем текущее состояние мира новому игроку
            initial_data = {
                'blocks': self.blocks,
                'players': {addr: data for addr, data in self.players.items() if addr != address}
            }
            self.send_data(client, initial_data)
            
            while True:
                try:
                    # Получаем размер данных (4 байта)
                    size_bytes = client.recv(4)
                    if not size_bytes:
                        break
                    
                    data_size = int.from_bytes(size_bytes, byteorder='big')
                    received_data = bytearray()
                    
                    # Получаем данные частями
                    while len(received_data) < data_size:
                        chunk = client.recv(min(4096, data_size - len(received_data)))
                        if not chunk:
                            break
                        received_data.extend(chunk)
                    
                    if len(received_data) != data_size:
                        print("Неполные данные получены")
                        break
                        
                    # Распаковываем данные
                    data = pickle.loads(zlib.decompress(received_data))
                    
                    # Обработка обновления позиции игрока
                    if data.get('type') == 'player_update':
                        with self.lock:
                            self.players[address] = data['data']
                            
                            # Рассылаем обновление всем клиентам
                            update = {
                                'type': 'player_update',
                                'address': address,
                                'data': data['data']
                            }
                            
                            for c in self.clients:
                                if c != client:  # Не отправляем обратно отправителю
                                    self.send_data(c, update)
                    
                    # Обработка изменения блоков
                    elif data.get('type') == 'block_update':
                        with self.lock:
                            block_data = data['data']
                            
                            # Добавление блока
                            if block_data['action'] == 'add':
                                # Проверяем, нет ли уже блока на этой позиции
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
                            
                            # Удаление блока
                            elif block_data['action'] == 'remove':
                                self.blocks = [
                                    b for b in self.blocks 
                                    if not (b[1] == block_data['x'] and b[2] == block_data['y'])
                                ]
                            
                            # Рассылаем обновление блоков всем клиентам
                            for c in self.clients:
                                self.send_data(c, data)
                
                except Exception as e:
                    print(f"Ошибка обработки данных от {address}: {e}")
                    break
        
        except Exception as e:
            print(f"Ошибка соединения с {address}: {e}")
        finally:
            with self.lock:
                # Удаляем клиента из списка
                if client in self.clients:
                    self.clients.remove(client)
                if address in self.players:
                    del self.players[address]
            
            # Уведомляем всех о выходе игрока
            update = {'type': 'player_left', 'address': address}
            for c in self.clients:
                try:
                    self.send_data(c, update)
                except:
                    continue
            
            client.close()
            print(f"Отключение: {address}")

    def start(self):
        while True:
            client, address = self.server.accept()
            
            with self.lock:
                self.clients.append(client)
            
            thread = threading.Thread(target=self.handle_client, args=(client, address))
            thread.start()

if __name__ == "__main__":
    server = GameServer()
    server.start()