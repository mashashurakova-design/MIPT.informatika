import pygame
import math
import random
import sys

pygame.init()
pygame.mixer.init()

BASE_WIDTH = 900
BASE_HEIGHT = 900
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
PURPLE = (180, 70, 255)
YELLOW = (255, 255, 50)
CYAN = (0, 200, 200)
ORANGE = (255, 150, 50)
DARK_BLUE = (10, 10, 40)
STAR_COLORS = [(255, 255, 200), (200, 230, 255), (255, 200, 200)]

# Загрузка изображений
def load_image(filename, default_color, width, height):
    try:
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, (width, height))
        image = image.convert_alpha()
        image.set_colorkey((255, 255, 255))  
        return image
    except:
        
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(default_color)
        return surface

# Загрузка звуков
def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except:
        return None

class Star:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.size = random.uniform(0.5, 3)
        self.speed = random.uniform(0.5, 2.0)
        self.color = random.choice(STAR_COLORS)
        self.twinkle = random.uniform(0, 3.14)
        
    def update(self):
        self.x += self.speed
        if self.x > self.screen_width:
            self.x = 0
            self.y = random.randint(0, self.screen_width)
        self.twinkle += 0.05
        
    def draw(self, screen):
        twinkle_factor = abs(math.sin(self.twinkle)) * 0.5 + 0.5
        color = tuple(int(c * twinkle_factor) for c in self.color)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

class Spaceship:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Относительные размеры
        self.width = int(screen_width * 0.078)  # ~70px при 900
        self.height = int(screen_height * 0.078)  # ~70px при 900
        self.x = int(screen_width * 0.111)  # ~100px при 900
        self.y = screen_height // 2
        self.speed = int(screen_height * 0.0086)  # ~8px при 900
        self.health = 100
        self.energy = 100
        self.max_energy = 100
        self.cooldown = 0
        self.cooldown_time = 10
        self.dual_shot = True
        self.thrust = 0
        self.image = load_image("shatl.png", CYAN, self.width, self.height)
        
    def update(self, screen_width, screen_height):
        # Обновляем размеры экрана
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Обновление перезарядки
        if self.cooldown > 0:
            self.cooldown -= 1
            
        # Восстановление энергии
        if self.energy < self.max_energy:
            self.energy += 0.4
            
        # Эффект движения
        self.thrust = max(self.thrust - 0.1, 0)
            
    def move(self, direction):
        self.thrust = 1.0
        new_y = self.y + direction * self.speed
        # Ограничение движения по вертикали с отступами от краев
        border_margin = int(self.screen_height * 0.071)  # ~64px при 900
        if border_margin <= new_y <= self.screen_height - self.height - border_margin:
            self.y = new_y
            
    def fire(self, projectiles, game):
        if self.cooldown == 0 and self.energy >= 8:
            self.cooldown = self.cooldown_time
            self.energy -= 8
            
            # звук выстрела
            if game.shot_sound:
                game.shot_sound.play()
            
            # Двойной выстрел
            projectile_radius = int(self.screen_width * 0.0067)  # ~6px при 900
            projectile_speed = int(self.screen_width * 0.02)  # ~18px при 900
            
            projectiles.append(Projectile(
                self.x + self.width,
                self.y + int(self.height * 0.2), 
                0,  # Угол 0 градусов (прямо)
                projectile_speed,
                projectile_radius,
                CYAN,
                12,
                "laser",
                self.screen_width,
                self.screen_height
            ))
            projectiles.append(Projectile(
                self.x + self.width,
                self.y + self.height - int(self.height * 0.2),
                0,
                projectile_speed,
                projectile_radius,
                CYAN,
                12,
                "laser",
                self.screen_width,
                self.screen_height
            ))
            return True
        return False
        
    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)
        return self.health <= 0
        
    def draw(self, screen):
        #  изображение корабля
        screen.blit(self.image, (self.x, self.y))
        
        # Двигатели (только когда движется)
        if self.thrust > 0:
            for i in range(2):
                engine_y = self.y + int(self.height * 0.3) + i * int(self.height * 0.4)
                flame_length = 15 + random.randint(0, 10)
                
                flame_points = [
                    (self.x - 5, engine_y - 3),
                    (self.x - flame_length, engine_y),
                    (self.x - 5, engine_y + 3)
                ]
                
                flame_color = (
                    random.randint(200, 255),
                    random.randint(100, 150),
                    random.randint(0, 50)
                )
                pygame.draw.polygon(screen, flame_color, flame_points)
            
    def draw_ui(self, screen, screen_width, screen_height):
        # Полоска здоровья
        health_bar_width = int(screen_width * 0.222)  # ~200px при 900
        health_bar_height = int(screen_height * 0.0286)  # ~26px при 900
        
        pygame.draw.rect(screen, (50, 50, 50), 
                        (20, 20, health_bar_width, health_bar_height), 
                        border_radius=3)
        health_width = (self.health / 100) * health_bar_width
        pygame.draw.rect(screen, RED, 
                        (20, 20, health_width, health_bar_height), 
                        border_radius=3)
        
        # Полоска энергии
        energy_bar_width = health_bar_width
        energy_bar_height = int(screen_height * 0.0214)  # ~19px при 900
        
        pygame.draw.rect(screen, (50, 50, 50), 
                        (20, 45, energy_bar_width, energy_bar_height), 
                        border_radius=3)
        energy_width = (self.energy / self.max_energy) * energy_bar_width
        energy_color = BLUE if self.energy > 20 else YELLOW
        pygame.draw.rect(screen, energy_color, 
                        (20, 45, energy_width, energy_bar_height), 
                        border_radius=3)
        
        # Текст
        font_size = int(screen_height * 0.0343)  # ~31px при 900
        font = pygame.font.Font(None, font_size)
        health_text = font.render(f"Здоровье: {int(self.health)}", True, WHITE)
        energy_text = font.render(f"Энергия: {int(self.energy)}", True, WHITE)
        
        screen.blit(health_text, (230, 18))
        screen.blit(energy_text, (230, 43))

class Alien:
    def __init__(self, x, y, alien_type, wave, screen_width, screen_height, game):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = x
        self.y = y
        self.type = alien_type
        self.wave = wave
        self.game = game  
        
        # получаем изображение из игры
        self.image = None
        self.width = 0
        self.height = 0
        
        # Устанавливаем параметры в зависимости от типа
        if alien_type == "scout":
            self.health = 25 + wave * 5
            self.speed_x = 1.5 + wave * 0.3
            self.speed_y = 0.8
            self.color = GREEN
            self.shoot_cooldown = 90 - wave * 10
            self.projectile_type = "alien_laser"
            # Размеры для скаута
            self.width = int(screen_width * 0.05)  # ~45px
            self.height = int(screen_height * 0.05)  # ~45px
            
        elif alien_type == "warrior":
            self.health = 50 + wave * 10
            self.speed_x = 1.0 + wave * 0.2
            self.speed_y = 0.5
            self.color = ORANGE
            self.shoot_cooldown = 70 - wave * 8
            self.projectile_type = "alien_plasma"
            # Размеры для воина
            self.width = int(screen_width * 0.072)  # ~65px
            self.height = int(screen_height * 0.071)  # ~64px
            
        elif alien_type == "boss":
            self.health = 120 + wave * 20
            self.speed_x = 0.6
            self.speed_y = 0.3
            self.color = PURPLE
            self.shoot_cooldown = 50
            self.projectile_type = "alien_missile"
            # Размеры для босса
            self.width = int(screen_width * 0.444)  # ~100px
            self.height = int(screen_height * 0.178)  # ~103px
            
        self.max_health = self.health
        
        
        if game and hasattr(game, 'alien_images') and alien_type in game.alien_images:
            self.image = game.alien_images[alien_type]
            self.image.set_colorkey((255, 255, 255))
        else:
            self.image = None
            
        self.cooldown = random.randint(0, 100)
        self.direction_x = -1  
        self.direction_y = random.choice([-1, 1])
        self.pulse = 0
        self.alive = True
        
    def update(self, ship):
        self.pulse += 0.03
        
        # Зигзагообразное движение
        self.x += self.speed_x * self.direction_x
        self.y += self.speed_y * self.direction_y
        
        # Отскок от верхней и нижней границ
        border_margin = int(self.screen_height * 0.071)  # ~64px при 900
        if self.y <= border_margin or self.y + self.height >= self.screen_height - border_margin:
            self.direction_y *= -1
            
        # Если ушел за левую границу - удаляем
        if self.x + self.width < 0:
            self.alive = False
            return None
            
        # Стрельба в корабль
        self.cooldown += 1
        if self.cooldown >= self.shoot_cooldown:
            self.cooldown = 0
            return self.shoot(ship)
        return None
        
    def shoot(self, ship):
        # Расчет направления к кораблю
        dx = ship.x - self.x
        dy = (ship.y + ship.height//2) - (self.y + self.height//2)
        angle = math.degrees(math.atan2(dy, dx))
        
        speed = 6 if self.type == "scout" else 5 if self.type == "warrior" else 4
        
        if self.type == "boss":
            # Босс выпускает 3 снаряда веером
            projectiles = []
            for angle_offset in [-20, 0, 20]:
                proj_angle = angle + angle_offset
                projectile_radius = int(self.screen_width * 0.011)  # ~10px при 900
                projectiles.append(Projectile(
                    self.x,
                    self.y + self.height//2,
                    proj_angle,
                    speed,
                    projectile_radius,
                    RED,
                    5,
                    self.projectile_type,
                    self.screen_width,
                    self.screen_height
                ))
            return projectiles
        else:
            projectile_radius = int(self.screen_width * 0.0078) if self.type == "warrior" else int(self.screen_width * 0.0056)  # ~7px или ~5px при 900
            return [Projectile(
                self.x,
                self.y + self.height//2,
                angle,
                speed,
                projectile_radius,
                RED if self.type == "warrior" else ORANGE,
                6 if self.type == "warrior" else 4,
                self.projectile_type,
                self.screen_width,
                self.screen_height
            )]
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            # звук смерти пришельца
            if self.game and hasattr(self.game, 'alien_death_sound') and self.game.alien_death_sound:
                self.game.alien_death_sound.play()
            return True
        return False
        
    def draw(self, screen):
        if not self.alive:
            return
            
        # изображение пришельца, если оно есть
        if self.image:
            screen.blit(self.image, (self.x, self.y))
            self.image.set_colorkey((255, 255, 255))
        else:
            # Запасной вариант - геометр. фигуры
            pulse_factor = math.sin(self.pulse) * 0.2 + 0.8
            pulse_color = tuple(int(c * pulse_factor) for c in self.color)
            
            if self.type == "scout":
                pygame.draw.ellipse(screen, pulse_color, 
                               (self.x, self.y, self.width, self.height))
            
                # Глаза
                eye_radius = int(self.width * 0.111)  
                pygame.draw.circle(screen, RED, 
                              (int(self.x + self.width * 0.7), int(self.y + self.height//3)), 
                              eye_radius)
                pygame.draw.circle(screen, RED, 
                              (int(self.x + self.width * 0.7), int(self.y + self.height*2//3)), 
                              eye_radius)
                              
            elif self.type == "warrior":
                points = [
                    (self.x + self.width//2, self.y),
                    (self.x + self.width, self.y + self.height//2),
                    (self.x + self.width//2, self.y + self.height),
                    (self.x, self.y + self.height//2)
                ]
                pygame.draw.polygon(screen, pulse_color, points)
                
                # Центральный глаз
                eye_radius = int(self.width * 0.154) 
                pygame.draw.circle(screen, YELLOW, 
                                  (int(self.x + self.width//2), int(self.y + self.height//2)), 
                                  eye_radius)
                
            elif self.type == "boss":
                # Квадратная форма округленная
                pygame.draw.rect(screen, pulse_color, 
                                (self.x, self.y, self.width, self.height), 
                                border_radius=int(self.width * 0.15)) 
                pygame.draw.rect(screen, WHITE, 
                                (self.x, self.y, self.width, self.height), 
                                border_radius=int(self.width * 0.15), width=3)
                
                # Центральное ядро
                core_radius = int(self.width * 0.3)  
                pygame.draw.circle(screen, (255, 100, 100), 
                                  (int(self.x + self.width//2), int(self.y + self.height//2)), 
                                  core_radius)
                
                # Пульсирующее ядро
                inner_radius = int(self.width * 0.2) + math.sin(self.pulse * 3) * int(self.width * 0.08)  
                pygame.draw.circle(screen, (255, 200, 200), 
                                  (int(self.x + self.width//2), int(self.y + self.height//2)), 
                                  int(inner_radius))
        
        # Полоска здоровья
        if self.health < self.max_health:
            health_bar_height = int(self.screen_height * 0.0071)  
            health_width = (self.health / self.max_health) * self.width
            pygame.draw.rect(screen, RED, 
                            (self.x, self.y - health_bar_height * 2.4, self.width, health_bar_height))
            pygame.draw.rect(screen, GREEN, 
                            (self.x, self.y - health_bar_height * 2.4, health_width, health_bar_height))
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Projectile:
    def __init__(self, x, y, angle, speed, radius, color, damage, proj_type, screen_width, screen_height):
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.speed = speed
        self.radius = radius
        self.color = color
        self.damage = damage
        self.type = proj_type
        self.alive = True
        self.trail = []
        self.max_trail = 8
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def update(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Сохраняем позицию для следа
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
            
        # Движение
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Проверка границ
        if (self.x < -50 or self.x > self.screen_width + 50 or 
            self.y < -50 or self.y > self.screen_height + 50):
            self.alive = False
            
    def draw(self, screen):
        # Рисуем след
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(200 * i / len(self.trail))
            if self.type == "laser":
                trail_color = (100, 200, 255, alpha)
            elif "alien" in self.type:
                trail_color = (255, 100, 100, alpha)
            else:
                trail_color = (*self.color, alpha)
            
            if len(trail_color) == 4:  # RGBA
                trail_surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, trail_color, 
                                  (self.radius, self.radius), 
                                  int(self.radius * i / len(self.trail)))
                screen.blit(trail_surface, (int(trail_x - self.radius), int(trail_y - self.radius)))
        
        # Рисуем снаряд
        if self.type in ["laser", "alien_laser"]:
            # Лазерный луч
            beam_length = int(self.screen_width * 0.0278)  # ~25px при 900
            end_x = self.x + math.cos(self.angle) * beam_length
            end_y = self.y + math.sin(self.angle) * beam_length
            line_width = max(2, self.radius//2)
            pygame.draw.line(screen, self.color, 
                            (self.x, self.y), 
                            (end_x, end_y), 
                            line_width)
        elif self.type in ["alien_plasma"]:
            # Плазменный шар
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 1)
        elif self.type == "alien_missile":
            # Ракета
            missile_length = int(self.screen_width * 0.022)  # ~20px при 900
            missile_width = int(self.screen_width * 0.0067)  # ~6px при 900
            points = [
                (self.x, self.y),
                (self.x - missile_length, self.y - missile_width),
                (self.x - missile_length, self.y + missile_width)
            ]
            pygame.draw.polygon(screen, self.color, points)
                
    def get_rect(self):
        if self.type in ["laser", "alien_laser"]:
            return pygame.Rect(self.x - 4, self.y - 4, 8, 8)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Explosion:
    def __init__(self, x, y, screen_width, screen_height, size=1.0):
        self.x = x
        self.y = y
        self.particles = []
        self.lifetime = 25
        self.size = size
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Создаем частицы взрыва
        num_particles = int(15 * size)
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 6) * size
            life = random.randint(15, 30)
            color = random.choice([(255, 100, 0), (255, 200, 0), (255, 50, 0)])
            particle_size = random.uniform(2, 5) * size
            # Масштабируем размер частицы
            particle_size *= min(screen_width / BASE_WIDTH, screen_height / BASE_HEIGHT)
            self.particles.append({
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': life,
                'max_life': life,
                'color': color,
                'size': particle_size
            })
            
    def update(self):
        self.lifetime -= 1
        
        for p in self.particles:
            p['vx'] *= 0.9
            p['vy'] *= 0.9
            p['life'] -= 1
            
        return self.lifetime <= 0
        
    def draw(self, screen):
        for p in self.particles:
            if p['life'] > 0:
                alpha = int(255 * p['life'] / p['max_life'])
                color = (*p['color'], alpha)
                
                # поверхность и прозрачность(альфа-канал)
                size = int(p['size'])
                surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color, (size, size), size)
                
                # Позиция частицы
                px = self.x + p['vx'] * (p['max_life'] - p['life'])
                py = self.y + p['vy'] * (p['max_life'] - p['life'])
                
                screen.blit(surf, (int(px - size), int(py - size)))

class Game:
    def __init__(self):
        # Начальный размер окна
        self.width = BASE_WIDTH
        self.height = BASE_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Космическая Оборона - 3 волны")
        
       
        # Загрузка звуков
        self.bg_music = load_sound("Electronic Fantasy.ogg")
        self.shot_sound = load_sound("PiuPiu.flac")
        self.alien_death_sound = load_sound("death_nlo.wav")

        if self.bg_music:
            self.bg_music.set_volume(0.5)  
        if self.shot_sound:
            self.shot_sound.set_volume(0.3)  
        if self.alien_death_sound:
            self.alien_death_sound.set_volume(0.4)  
        
        # Загрузка изображений для пришельцев
        self.alien_images = {}
        self.load_alien_images()
        
        # Звездное небо
        self.stars = [Star(self.width, self.height) for _ in range(150)]
            
        # Игровые объекты
        self.ship = Spaceship(self.width, self.height)
        self.projectiles = []
        self.alien_projectiles = []
        self.aliens = []
        self.explosions = []
        self.asteroid_manager = AsteroidManager(self.width, self.height)
        
        # Счет и состояние
        self.score = 0
        self.wave = 1
        self.max_waves = 3
        self.wave_timer = 0
        self.game_over = False
        self.victory = False
        self.victory_shown = False
        self.victory_image = None
        
        # Загрузка победной картинки
        self.load_victory_image()
        
        # Создаем первую волну
        self.spawn_wave()
        
        # Запуск фоновой музыки
        if self.bg_music:
            self.bg_music.play(-1)  
        
    def load_alien_images(self):
        """Загрузка изображений пришельцев"""
        alien_sizes = {
            "scout": (int(BASE_WIDTH * 0.05), int(BASE_HEIGHT * 0.05)),     # ~45x45px
            "warrior": (int(BASE_WIDTH * 0.072), int(BASE_HEIGHT * 0.071)), # ~65x64px  
            "boss": (int(BASE_WIDTH * 0.444), int(BASE_HEIGHT * 0.178))     # ~400x160px
        }
        
       
        alien_filenames = {
            "scout": "NLO.png",      
            "warrior": "NLO2.png",   
            "boss": "NLO3.png"       
        }
        
        for alien_type, size in alien_sizes.items():
            filename = alien_filenames.get(alien_type, f"{alien_type}.png")
            try:
                # Загрузка с прозрачным фоном
                original = pygame.image.load(filename).convert_alpha()
                # Масштабирование
                self.alien_images[alien_type] = pygame.transform.scale(original, size)
                print(f"✓ Загружено: {filename} ({size[0]}x{size[1]})")
            except Exception as e:
                print(f"✗ Не удалось загрузить {filename}: {e}")
                surface = pygame.Surface(size, pygame.SRCALPHA)
                if alien_type == "scout":
                    surface.fill((*GREEN, 200))  
                elif alien_type == "warrior":
                    surface.fill((*ORANGE, 200))  
                elif alien_type == "boss":
                    surface.fill((*PURPLE, 200))  
                self.alien_images[alien_type] = surface
    
    def load_victory_image(self):
        try:
            self.victory_image = pygame.image.load("victory.png") 
            self.scale_victory_image()
        except:
            self.victory_image = None
            
    def scale_victory_image(self):
        if self.victory_image:
            self.victory_image = pygame.transform.scale(self.victory_image, 
                                                       (self.width, self.height))
            
    def spawn_wave(self):
        # Очищаем предыдущих пришельцев
        self.aliens = []
        self.alien_projectiles = []
        
        # В зависимости от волны создаем разных пришельцев
        if self.wave == 1:
            # Первая волна: только скауты
            num_aliens = 4
            for i in range(num_aliens):
                alien = Alien(
                    self.width + 50 + i * int(self.width * 0.111),  # ~100px при 900
                    random.randint(int(self.height * 0.143), self.height - int(self.height * 0.214)),  # ~129-771px
                    "scout",
                    self.wave,
                    self.width,
                    self.height,
                    self  
                )
                self.aliens.append(alien)
                
        elif self.wave == 2:
            # Вторая волна: скауты и воины
            for i in range(3):
                alien = Alien(
                    self.width + 50 + i * int(self.width * 0.133),  # ~120px при 900
                    random.randint(int(self.height * 0.143), self.height - int(self.height * 0.214)),
                    "scout",
                    self.wave,
                    self.width,
                    self.height,
                    self  # ⭐ ВАЖНО: передаем self
                )
                self.aliens.append(alien)
                
            for i in range(2):
                alien = Alien(
                    self.width + 50 + i * int(self.width * 0.167),  # ~150px при 900
                    random.randint(int(self.height * 0.143), self.height - int(self.height * 0.286)),
                    "warrior",
                    self.wave,
                    self.width,
                    self.height,
                    self  
                )
                self.aliens.append(alien)
                
        elif self.wave == 3:
            # Третья волна: босс и поддержка
            # Босс
            alien = Alien(
                self.width + int(self.width * 0.111),  # ~100px при 900
                self.height // 2 - int(self.height * 0.057),  # ~399px
                "boss",
                self.wave,
                self.width,
                self.height,
                self 
            )
            self.aliens.append(alien)
            
            # скауты для поддержки
            for i in range(4):
                alien = Alien(
                    self.width + 50 + i * int(self.width * 0.111),  # ~100px при 900
                    random.randint(int(self.height * 0.143), self.height - int(self.height * 0.214)),
                    "scout",
                    self.wave,
                    self.width,
                    self.height,
                    self  
                )
                self.aliens.append(alien)
                
    def update(self):
        if self.game_over or self.victory:
            return
            
        # Обновление звезд
        for star in self.stars:
            star.screen_width = self.width
            star.screen_height = self.height
            star.update()
            
        # Обновление корабля
        self.ship.update(self.width, self.height)
        
        # Обновление снарядов корабля
        for proj in self.projectiles[:]:
            proj.update(self.width, self.height)
            if not proj.alive:
                self.projectiles.remove(proj)

        # Обновление астероидов
        self.asteroid_manager.update()
        self.asteroid_manager.update_explosions()
        if self.asteroid_manager.check_collisions_with_ship(self.ship):
            pass
    
        # Проверка столкновений астероидов со снарядами игрока
        destroyed = self.asteroid_manager.check_collisions_with_projectiles(
            self.projectiles,
            lambda score: setattr(self, 'score', self.score + score)
        )
                
        # Обновление снарядов пришельцев
        for proj in self.alien_projectiles[:]:
            proj.update(self.width, self.height)
            if not proj.alive:
                self.alien_projectiles.remove(proj)
                
        # Обновление пришельцев
        for alien in self.aliens[:]:
            # Обновляем размеры экрана у пришельца
            alien.screen_width = self.width
            alien.screen_height = self.height
            
            # Стрельба пришельцев
            new_projectiles = alien.update(self.ship)
            if new_projectiles:
                self.alien_projectiles.extend(new_projectiles)
                
            # Удаление мертвых пришельцев
            if not alien.alive:
                self.aliens.remove(alien)
                # Начисление очков в зависимости от типа
                if alien.type == "scout":
                    self.score += 50
                elif alien.type == "warrior":
                    self.score += 100
                elif alien.type == "boss":
                    self.score += 500
                    
                self.explosions.append(Explosion(
                    alien.x + alien.width//2,
                    alien.y + alien.height//2,
                    self.width,
                    self.height,
                    1.5 if alien.type == "boss" else 1.0
                ))
                
        # Обновление взрывов
        for explosion in self.explosions[:]:
            if explosion.update():
                self.explosions.remove(explosion)
                
        # Проверка столкновений снарядов корабля с пришельцами
        for proj in self.projectiles[:]:
            proj_rect = proj.get_rect()
            
            # С пришельцами
            for alien in self.aliens:
                if proj_rect.colliderect(alien.get_rect()):
                    alien.take_damage(proj.damage)
                    proj.alive = False
                    self.explosions.append(Explosion(proj.x, proj.y, self.width, self.height, 0.3))
                    break
                    
        # Проверка столкновений снарядов пришельцев с кораблем
        for proj in self.alien_projectiles[:]:
            proj_rect = proj.get_rect()
            ship_rect = pygame.Rect(self.ship.x, self.ship.y, 
                                   self.ship.width, self.ship.height)
            
            if proj_rect.colliderect(ship_rect):
                self.ship.take_damage(proj.damage)
                proj.alive = False
                self.explosions.append(Explosion(proj.x, proj.y, self.width, self.height, 0.4))
                
                if self.ship.health <= 0:
                    self.game_over = True
                    self.explosions.append(Explosion(
                        self.ship.x + self.ship.width//2,
                        self.ship.y + self.ship.height//2,
                        self.width,
                        self.height,
                        2.0
                    ))
                    
        # Проверка завершения волны
        if not self.aliens and not self.victory:
            self.wave_timer += 1
            if self.wave_timer > 120:  # 2 секунды паузы между волнами
                if self.wave < self.max_waves:
                    self.wave += 1
                    self.spawn_wave()
                    self.wave_timer = 0
                else:
                    self.victory = True
                    
    def draw(self):
        # Фон
        self.screen.fill(DARK_BLUE)
        
        # Звезды
        for star in self.stars:
            star.draw(self.screen)
            
        # Взрывы
        for explosion in self.explosions:
            explosion.draw(self.screen)
            
        # Снаряды пришельцев
        for proj in self.alien_projectiles:
            proj.draw(self.screen)
            
        # Снаряды корабля
        for proj in self.projectiles:
            proj.draw(self.screen)

        # Астероиды 
        self.asteroid_manager.draw(self.screen)
            
        # Пришельцы
        for alien in self.aliens:
            alien.draw(self.screen)
            
        # Корабль
        if not self.game_over or (self.game_over and len(self.explosions) > 0):
            self.ship.draw(self.screen)
            
        # Интерфейс
        self.draw_ui()
        
        # Сообщения
        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()
            
    def draw_ui(self):
        # UI корабля
        self.ship.draw_ui(self.screen, self.width, self.height)
        
        # Шрифты с масштабированием
        font_size_large = int(self.height * 0.103)  # ~93px при 900
        font_size_medium = int(self.height * 0.051)  # ~46px при 900
        font_size_small = int(self.height * 0.04)  # ~36px при 900
        
        self.font_large = pygame.font.Font(None, font_size_large)
        self.font_medium = pygame.font.Font(None, font_size_medium)
        self.font_small = pygame.font.Font(None, font_size_small)
        
        # Счет и волна
        score_text = self.font_medium.render(f"Счёт: {self.score}", True, WHITE)
        wave_text = self.font_medium.render(f"Волна: {self.wave}/{self.max_waves}", True, WHITE)
        
        self.screen.blit(score_text, (self.width - int(self.width * 0.222), 20))
        self.screen.blit(wave_text, (self.width - int(self.width * 0.222), 60))
        
        # Индикатор волны (только между волнами)
        if not self.aliens and not self.victory and self.wave < self.max_waves:
            wave_msg = self.font_large.render(f"Волна {self.wave + 1}", True, YELLOW)
            self.screen.blit(wave_msg, 
                           (self.width//2 - wave_msg.get_width()//2, 
                            self.height//2 - int(self.height * 0.071)))
            
            countdown = 2 - self.wave_timer // 60
            count_text = self.font_medium.render(f"Следующая волна через: {countdown}", True, CYAN)
            self.screen.blit(count_text, 
                           (self.width//2 - count_text.get_width()//2, 
                            self.height//2 + int(self.height * 0.029)))
            
    def draw_game_over(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("ПОРАЖЕНИЕ!", True, RED)
        score_text = self.font_medium.render(f"Итоговый счёт: {self.score}", True, WHITE)
        restart_text = self.font_medium.render("Нажмите R для новой игры", True, YELLOW)
        
        self.screen.blit(game_over_text, 
                        (self.width//2 - game_over_text.get_width()//2, 
                         int(self.height * 0.286)))
        self.screen.blit(score_text,
                        (self.width//2 - score_text.get_width()//2, 
                         int(self.height * 0.429)))
        self.screen.blit(restart_text,
                        (self.width//2 - restart_text.get_width()//2, 
                         int(self.height * 0.5)))
                        
    def draw_victory(self):
        if not self.victory_shown:
            self.victory_shown = True
            
        # Если есть победная картинка, показываем ее
        if self.victory_image:
            self.screen.blit(self.victory_image, (0, 0))
            
            # Поверх картинки показываем результаты
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.screen.blit(overlay, (0, 0))
            
        # Текст победы поверх всего
        victory_text = self.font_large.render("ПОБЕДА!", True, YELLOW)
        mission_text = self.font_medium.render("Все 3 волны отражены!", True, GREEN)
        score_text = self.font_medium.render(f"Финальный счёт: {self.score}", True, WHITE)
        restart_text = self.font_medium.render("Нажмите R для новой игры", True, CYAN)
        
        self.screen.blit(victory_text,
                        (self.width//2 - victory_text.get_width()//2, 
                         int(self.height * 0.143)))
        self.screen.blit(mission_text,
                        (self.width//2 - mission_text.get_width()//2, 
                         int(self.height * 0.286)))
        self.screen.blit(score_text,
                        (self.width//2 - score_text.get_width()//2, 
                         int(self.height * 0.386)))
        self.screen.blit(restart_text,
                        (self.width//2 - restart_text.get_width()//2, 
                         int(self.height * 0.5)))
                        
    # СОБЫТИЯ ИГРЫ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Перезапуск игры с текущим размером окна
                    self.__init__()
                    self.width, self.height = self.screen.get_size()
                    self.scale_victory_image()
                    return
                    
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                elif event.key == pygame.K_SPACE and not self.game_over and not self.victory:
                    self.ship.fire(self.projectiles, self)
                    
            elif event.type == pygame.VIDEORESIZE:
                # Обновляем размер экрана
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                
                # Масштабируем победную картинку
                self.scale_victory_image()
                
                # Пересоздаем звезды под новый размер
                self.stars = [Star(self.width, self.height) for _ in range(150)]
                
                # Обновляем размеры корабля
                self.ship.screen_width = self.width
                self.ship.screen_height = self.height
                
        # Непрерывное управление (движение вверх/вниз)
        if not self.game_over and not self.victory:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.ship.move(-1)  # Вверх
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.ship.move(1)   # Вниз
                
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            clock.tick(FPS)

class Asteroid:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Случайный размер астероида (3 уровня размера)
        self.size_type = random.choice(["small", "medium", "large"])
        
        if self.size_type == "small":
            self.radius = random.randint(15, 25)
            self.health = 30
            self.max_health = 30
            self.damage = 15
            self.speed = random.uniform(3.0, 5.0)
            self.color = (150, 150, 150)  # Серый
        elif self.size_type == "medium":
            self.radius = random.randint(26, 40)
            self.health = 50
            self.max_health = 50
            self.damage = 25
            self.speed = random.uniform(2.0, 4.0)
            self.color = (120, 120, 120)  # Темно-серый
        else:  # large
            self.radius = random.randint(41, 60)
            self.health = 80
            self.max_health = 80
            self.damage = 35
            self.speed = random.uniform(1.0, 2.5)
            self.color = (100, 100, 100)  # Очень темный серый
        
        # Начальная позиция - случайная точка за правым краем экрана
        self.x = screen_width + self.radius
        self.y = random.randint(self.radius, screen_height - self.radius)
        
        # Направление движения (в основном влево, но с небольшим случайным отклонением по вертикаи)
        self.direction_x = -1
        self.direction_y = random.uniform(-0.5, 0.5)
        
        # Вращение астероида
        self.rotation = 0
        self.rotation_speed = random.uniform(-3, 3)
        
        # Трещины на астероиде
        self.cracks = []
        for _ in range(random.randint(2, 5)):
            crack_length = random.uniform(0.3, 0.8) * self.radius
            crack_angle = random.uniform(0, 2 * math.pi)
            crack_width = random.uniform(0.1, 0.3) * self.radius
            self.cracks.append({
                'length': crack_length,
                'angle': crack_angle,
                'width': crack_width
            })
        
        # Частицы пыли вокруг астероида
        self.dust_particles = []
        for _ in range(random.randint(5, 15)):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(self.radius * 1.1, self.radius * 1.5)
            size = random.uniform(1, 3)
            self.dust_particles.append({
                'angle': angle,
                'distance': distance,
                'size': size,
                'speed': random.uniform(0.5, 1.5),
                'offset': random.uniform(0, 2 * math.pi)
            })
        
        self.alive = True
        self.flash_timer = 0  # Таймер для эффекта попадания
    
    def update(self):
        # Движение астероида
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        
        # Вращение
        self.rotation += self.rotation_speed
        
        # Обновление эффекта попадания
        if self.flash_timer > 0:
            self.flash_timer -= 1
        
        # Обновление частиц пыли
        for particle in self.dust_particles:
            particle['angle'] += particle['speed'] * 0.01
        
        # Проверка выхода за границы экрана
        if self.x < -self.radius * 2:
            self.alive = False
        if self.y < -self.radius * 2 or self.y > self.screen_height + self.radius * 2:
            self.alive = False
        
        # Отскок от верхней и нижней границ
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.direction_y = abs(self.direction_y)
        elif self.y + self.radius >= self.screen_height:
            self.y = self.screen_height - self.radius
            self.direction_y = -abs(self.direction_y)
    
    def take_damage(self, damage):
        self.health -= damage
        self.flash_timer = 10  # Активируем эффект попадания
        
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def check_collision_with_ship(self, ship_rect):
        # Простая проверка столкновения через прямоугольники
        asteroid_rect = self.get_rect()
        return asteroid_rect.colliderect(ship_rect)
    
    def check_collision_with_projectile(self, projectile_rect):
        # Проверка столкновения со снарядом
        asteroid_rect = self.get_rect()
        return asteroid_rect.colliderect(projectile_rect)
    
    def get_rect(self):
        # Возвращаем прямоугольник для проверки столкновений
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)
    
    def draw(self, screen):
        # Рисуем частицы пыли
        for particle in self.dust_particles:
            dust_x = self.x + math.cos(particle['angle'] + particle['offset']) * particle['distance']
            dust_y = self.y + math.sin(particle['angle'] + particle['offset']) * particle['distance']
            
            # Частицы становятся более прозрачными по мере удаления от астероида
            alpha = int(150 * (particle['distance'] - self.radius) / (self.radius * 0.5))
            alpha = max(50, min(alpha, 150))
            
            dust_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(dust_surface, (100, 100, 100, alpha), 
                              (int(particle['size']), int(particle['size'])), 
                              int(particle['size']))
            screen.blit(dust_surface, (int(dust_x - particle['size']), int(dust_y - particle['size'])))
        
        # Создаем поверхность для астероида с поддержкой альфа-канала
        asteroid_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        # Рисуем основную форму астероида
        points = []
        num_points = random.randint(8, 12)
        
        # Создаем неровную форму астероида
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points + math.radians(self.rotation)
            # Добавляем случайные отклонения для создания неровной формы
            variation = random.uniform(0.7, 1.3)
            point_x = self.radius + math.cos(angle) * self.radius * variation
            point_y = self.radius + math.sin(angle) * self.radius * variation
            points.append((point_x, point_y))
        
        # Основной цвет астероида
        base_color = self.color
        
        # Эффект попадания (мигание)
        if self.flash_timer > 0:
            flash_intensity = self.flash_timer / 10.0
            base_color = (
                min(255, int(base_color[0] * (1 + flash_intensity))),
                min(255, int(base_color[1] * (1 + flash_intensity * 0.5))),
                min(255, int(base_color[2] * (1 + flash_intensity * 0.5)))
            )
        
        # Рисуем астероид
        pygame.draw.polygon(asteroid_surface, base_color, points)
        
        # Рисуем трещины
        for crack in self.cracks:
            crack_x = self.radius + math.cos(crack['angle']) * crack['length']
            crack_y = self.radius + math.sin(crack['angle']) * crack['length']
            end_x = self.radius + math.cos(crack['angle'] + math.pi) * crack['length'] * 0.5
            end_y = self.radius + math.sin(crack['angle'] + math.pi) * crack['length'] * 0.5
            
            pygame.draw.line(asteroid_surface, (50, 50, 50),
                            (crack_x, crack_y), (end_x, end_y),
                            max(1, int(crack['width'])))
        
        # Добавляем текстуру (маленькие кратеры)
        for _ in range(random.randint(3, 7)):
            crater_x = random.randint(5, self.radius * 2 - 5)
            crater_y = random.randint(5, self.radius * 2 - 5)
            crater_radius = random.randint(2, 5)
            crater_color = (
                max(0, base_color[0] - random.randint(20, 40)),
                max(0, base_color[1] - random.randint(20, 40)),
                max(0, base_color[2] - random.randint(20, 40))
            )
            pygame.draw.circle(asteroid_surface, crater_color,
                              (crater_x, crater_y), crater_radius)
        
        # Обводка
        pygame.draw.polygon(asteroid_surface, (80, 80, 80), points, 2)
        
        # Отображаем астероид на экране
        screen.blit(asteroid_surface, (int(self.x - self.radius), int(self.y - self.radius)))
        
        # Полоска здоровья (только если поврежден)
        if self.health < self.max_health:
            health_width = (self.health / self.max_health) * (self.radius * 2)
            pygame.draw.rect(screen, (150, 0, 0),
                            (self.x - self.radius, self.y - self.radius - 10,
                             self.radius * 2, 4))
            pygame.draw.rect(screen, (0, 150, 0),
                            (self.x - self.radius, self.y - self.radius - 10,
                             health_width, 4))

class AsteroidManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.asteroids = []
        self.spawn_timer = 0
        self.spawn_interval = 120  # Астероиды появляются каждые 2 секунды (при 60 FPS)
        self.explosions = []  # Для хранения взрывов астероидов
    
    def update(self):
        # Обновляем таймер спавна
        self.spawn_timer += 1
        
        # Спавним новый астероид, если пришло время
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_asteroid()
            self.spawn_timer = 0
            # Случайный интервал для следующего астероида
            self.spawn_interval = random.randint(90, 180)  # 1.5-3 секунды
        
        # Обновляем все астероиды
        for asteroid in self.asteroids[:]:
            asteroid.update()
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
                # Создаем взрыв при уничтожении астероида
                self.create_explosion(asteroid.x, asteroid.y, asteroid.radius)
    
    def spawn_asteroid(self):
        # Создаем новый астероид с некоторой вероятностью (не каждый раз)
        if random.random() < 0.7:  # 70% шанс спавна
            asteroid = Asteroid(self.screen_width, self.screen_height)
            self.asteroids.append(asteroid)
    
    def create_explosion(self, x, y, size):
        # Создаем взрыв при уничтожении астероида
        self.explosions.append({
            'x': x,
            'y': y,
            'size': size * 0.5,
            'life': 30,
            'particles': []
        })
        
        # Создаем частицы для взрыва
        for _ in range(int(size * 2)):
            self.explosions[-1]['particles'].append({
                'x': x,
                'y': y,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'life': random.randint(20, 40),
                'color': random.choice([(150, 150, 150), (120, 120, 120), (100, 100, 100)]),
                'size': random.uniform(1, 4)
            })
    
    def update_explosions(self):
        # Обновляем все взрывы
        for explosion in self.explosions[:]:
            explosion['life'] -= 1
            
            # Обновляем частицы
            for particle in explosion['particles']:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vx'] *= 0.95
                particle['vy'] *= 0.95
                particle['life'] -= 1
            
            # Удаляем взрыв, если время жизни истекло
            if explosion['life'] <= 0:
                self.explosions.remove(explosion)
    
    def check_collisions_with_ship(self, ship):
        # Проверяем столкновения астероидов с кораблем
        ship_rect = pygame.Rect(ship.x, ship.y, ship.width, ship.height)
        
        for asteroid in self.asteroids[:]:
            if asteroid.check_collision_with_ship(ship_rect):
                # Наносим урон кораблю
                ship.take_damage(asteroid.damage)
                
                # Уничтожаем астероид
                asteroid.alive = False
                
                # Создаем взрыв
                self.create_explosion(asteroid.x, asteroid.y, asteroid.radius)
                
                return True
        return False
    
    def check_collisions_with_projectiles(self, projectiles, add_score_callback=None):
        # Проверяем столкновения астероидов со снарядами игрока
        destroyed_asteroids = 0
        
        for asteroid in self.asteroids[:]:
            for projectile in projectiles[:]:
                if projectile.alive and asteroid.check_collision_with_projectile(projectile.get_rect()):
                    # Наносим урон астероиду
                    destroyed = asteroid.take_damage(projectile.damage)
                    projectile.alive = False
                    
                    if destroyed:
                        destroyed_asteroids += 1
                        # Начисляем очки за уничтожение астероида
                        if add_score_callback:
                            if asteroid.size_type == "small":
                                add_score_callback(25)
                            elif asteroid.size_type == "medium":
                                add_score_callback(50)
                            else:  # large
                                add_score_callback(100)
                    
                    # Выходим из внутреннего цикла, так как этот снаряд уже попал
                    break
        
        return destroyed_asteroids
    
    def draw(self, screen):
        # Рисуем все астероиды
        for asteroid in self.asteroids:
            asteroid.draw(screen)
        
        # Рисуем взрывы
        for explosion in self.explosions:
            for particle in explosion['particles']:
                if particle['life'] > 0:
                    alpha = int(255 * particle['life'] / 40)
                    particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, (*particle['color'], alpha),
                                      (int(particle['size']), int(particle['size'])),
                                      int(particle['size']))
                    screen.blit(particle_surface, 
                               (int(particle['x'] - particle['size']), 
                                int(particle['y'] - particle['size'])))
    
    def clear(self):
        # Очищаем все астероиды и взрывы
        self.asteroids.clear()
        self.explosions.clear()
        self.spawn_timer = 0

if __name__ == "__main__":
    game = Game()
    game.run()