import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
pygame.display.set_caption("Солнечная система")
WIDTH, HEIGHT = 1000, 800
cx = WIDTH // 2
cy = HEIGHT // 2   
FPS = 60
clock = pygame.time.Clock()

pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.music.load("Numbers.mp3")  
    pygame.mixer.music.set_volume(0.7)  
    pygame.mixer.music.play(-1)  
    print("Фоновая музыка запущена")
except:
    print("Не удалось загрузить фоновую музыку")


try:
    explosion_sound = pygame.mixer.Sound("zvuk-vzryva.mp3")
except:
    print("Не удалось загрузить звук взрыва")
    explosion_sound = None

class Explosion:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.particles = []
        self.lifetime = 0.8  # Время жизни взрыва в секундах
        self.timer = 0
        
        # Создаем частицы взрыва
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            size = random.uniform(2, 6)
            lifetime = random.uniform(0.5, 1.0)
            color = (
                random.randint(200, 255),
                random.randint(100, 200),
                random.randint(0, 100)
            )
            
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': size,
                'color': color,
                'lifetime': lifetime,
                'timer': 0
            })
    
    def update(self, dt):
        self.timer += dt
        
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['timer'] += dt
            
            # Замедляем частицы со временем
            particle['vx'] *= 0.95
            particle['vy'] *= 0.95
            
        # Удаляем частицы, которые прожили дольше своего времени жизни
        self.particles = [p for p in self.particles if p['timer'] < p['lifetime']]
        
        # Взрыв завершен, когда все частицы исчезли или истекло время жизни
        return self.timer < self.lifetime and len(self.particles) > 0
    
    def draw(self, screen):
        
        if screen is None:
            return
            
        for particle in self.particles:
            try:
               
                progress = particle['timer'] / particle['lifetime']
                alpha = int(255 * (1 - progress))
                
                
                r, g, b = particle['color']
                color = (r, g, b, alpha)
                
                
                size = max(1, int(particle['size']))  
                particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (size, size), size)
                
                # Рисуем частицу
                screen.blit(particle_surface, 
                           (int(particle['x'] - size), 
                            int(particle['y'] - size)))
            except (ValueError, TypeError) as e:
                
                continue


class Planet:
    def __init__(self, screen, radius, orbit_radius, color=None, speed=0, angle=0, image_path=None, name=""):
        self.screen = screen
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.color = color
        self.speed = speed
        self.angle = angle
        self.x = 0
        self.y = 0
        self.image = None
        self.name = name
        self.exploded = False
        
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image.set_colorkey((255, 255, 255))
                original_width, original_height = self.image.get_size()
                aspect_ratio = original_width / original_height
                
                
                if aspect_ratio > 1:  # Шире, чем выше
                    new_width = radius * 2
                    new_height = int(radius * 2 / aspect_ratio)
                else:  # Выше, чем шире
                    new_height = radius * 2
                    new_width = int(radius * 2 * aspect_ratio)
                
                self.image = pygame.transform.scale(self.image, (new_width, new_height))
            except:
                print(f"Не удалось загрузить изображение: {image_path}")
                self.image = None
    
    def update(self, dt):
        if not self.exploded:
            self.angle += self.speed * dt
            self.x = cx + self.orbit_radius * math.cos(self.angle)
            self.y = cy + self.orbit_radius * math.sin(self.angle)
    
    def draw(self):
        if not self.exploded:
            if self.image:
                try:
                    image_width, image_height = self.image.get_size()
                    self.screen.blit(self.image, (int(self.x - image_width // 2), int(self.y - image_height // 2)))
                except:
                    # Если что-то пошло не так с изображением, рисуем круг
                    pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)
            else:
                pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_clicked(self, pos):
        if self.exploded:
            return False
            
        # Проверяем, находится ли точка клика внутри планеты
        distance = math.sqrt((self.x - pos[0])**2 + (self.y - pos[1])**2)
        return distance <= self.radius
    
    def explode(self):
        self.exploded = True
        try:
            return Explosion(self.x, self.y, self.radius)
        except:
            print("Ошибка при создании взрыва")
            return None
class Moon:
    def __init__(self, screen, planet, radius, orbit_radius, color=(200, 200, 200), speed=5, angle=0):
        self.screen = screen
        self.planet = planet
        self.radius = radius
        self.orbit_radius = orbit_radius
        self.color = color
        self.speed = speed
        self.angle = angle

    def update(self, dt):
        self.angle += self.speed * dt

    def draw(self):
        x = self.planet.x + self.orbit_radius * math.cos(self.angle)
        y = self.planet.y + self.orbit_radius * math.sin(self.angle)
        pygame.draw.circle(self.screen, self.color, (int(x), int(y)), self.radius)

class AsteroidBelt:
    def __init__(self, screen, num_asteroids=100):
        self.screen = screen
        self.asteroids = []
        for _ in range(num_asteroids):
            orbit_radius = random.uniform(300, 350)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.2, 0.4) * (300 / orbit_radius)
            self.asteroids.append({
                'orbit_radius': orbit_radius,
                'angle': angle,
                'speed': speed,
                'size': random.randint(1, 3)
            })

    def update(self, dt):
        for asteroid in self.asteroids:
            asteroid['angle'] += asteroid['speed'] * dt

    def draw(self):
        for asteroid in self.asteroids:
            x = cx + asteroid['orbit_radius'] * math.cos(asteroid['angle'])
            y = cy + asteroid['orbit_radius'] * math.sin(asteroid['angle'])
            pygame.draw.circle(self.screen, (150, 150, 150), (int(x), int(y)), asteroid['size'])

class Comet:
    def __init__(self, screen):
        self.screen = screen
        self.reset()
        self.tail_particles = []
        self.max_tail_length = 20
        
    def reset(self):
        # Начальная позиция за пределами экрана
        side = random.randint(0, 3)
        if side == 0:  # сверху
            self.x = random.randint(0, self.screen.get_width())
            self.y = -20
        elif side == 1:  # справа
            self.x = self.screen.get_width() + 20
            self.y = random.randint(0, self.screen.get_height())
        elif side == 2:  # снизу
            self.x = random.randint(0, self.screen.get_width())
            self.y = self.screen.get_height() + 20
        else:  # слева
            self.x = -20
            self.y = random.randint(0, self.screen.get_height())
            
        # Случайное направление к центру экрана
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        dx = center_x - self.x
        dy = center_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Базовая скорость
        base_speed = random.uniform(50, 100)
        self.speed_x = (dx / distance) * base_speed
        self.speed_y = (dy / distance) * base_speed
        
        # немного случайности к направлению
        self.speed_x += random.uniform(-20, 20)
        self.speed_y += random.uniform(-20, 20)
        
        # Параметры кометы
        self.size = random.randint(3, 6)
        self.color = (100, 150, 255)  # Голубой цвет
        self.change_direction_timer = 0
        self.life_timer = 0
        self.max_life_time = random.uniform(5, 15)  # Время жизни кометы в секундах

    def update(self, dt):
        # Сохраняем старую позицию для создания хвоста
        old_x, old_y = self.x, self.y
        
        # Обновляем позицию
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        
        # Добавляем частицу в хвост
        self.tail_particles.append({
            'x': old_x,
            'y': old_y,
            'size': self.size * 0.8,
            'alpha': 255  # Начальная непрозрачность
        })
        
        # Обновляем частицы хвоста
        for particle in self.tail_particles[:]:
            particle['alpha'] -= 255 / self.max_tail_length  # Уменьшаем непрозрачность
            particle['size'] *= 0.95  # Уменьшаем размер
            
            if particle['alpha'] <= 0:
                self.tail_particles.remove(particle)
        
        # Ограничиваем длину хвоста
        if len(self.tail_particles) > self.max_tail_length:
            self.tail_particles.pop(0)
        
        # меняем направление
        self.change_direction_timer += dt
        if self.change_direction_timer > 2.0:
            self.speed_x += random.uniform(-30, 30)
            self.speed_y += random.uniform(-30, 30)
            self.change_direction_timer = 0
            
        # Ограничиваем максимальную скорость
        speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        max_speed = 150
        if speed > max_speed:
            self.speed_x = (self.speed_x / speed) * max_speed
            self.speed_y = (self.speed_y / speed) * max_speed
        
        # Проверяем время жизни
        self.life_timer += dt
        if (self.life_timer > self.max_life_time or 
            self.x < -100 or self.x > self.screen.get_width() + 100 or 
            self.y < -100 or self.y > self.screen.get_height() + 100):
            self.reset()
            self.life_timer = 0

    def draw(self):
        # Рисуем хвост
        for i, particle in enumerate(self.tail_particles):
            # Цвет хвоста 
            color = (100, 150, 255, int(particle['alpha']))
            
            particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, 
                              (int(particle['size']), int(particle['size'])), 
                              int(particle['size']))
            self.screen.blit(particle_surface, 
                            (int(particle['x'] - particle['size']), 
                             int(particle['y'] - particle['size'])))
        
        # Рисуем ядро кометы
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.size)
        
        # Добавляем яркое ядро
        bright_core_color = (200, 220, 255)
        pygame.draw.circle(self.screen, bright_core_color, (int(self.x), int(self.y)), self.size // 2)

# Создание объектов
planets = [
    Planet(screen, radius=4, orbit_radius=55, color=(150, 100, 100), speed=3.0),  # Меркурий
    Planet(screen, radius=9, orbit_radius=70, color=(255, 200, 100), speed=2.0, image_path = "venera.png"),  # Венера
    Planet(screen, radius=13, orbit_radius=100, speed=1.7, color=(100, 100, 255), image_path = "zemla.jpg"),  # Земля
    Planet(screen, radius=5, orbit_radius=130, color=(255, 100, 80), speed=1.5),  # Марс
    Planet(screen, radius=27, orbit_radius=180, color=(210, 180, 140), speed=0.45, image_path = "Jupiter.png"),  # Юпитер
    Planet(screen, radius=20, orbit_radius=230, color=(220, 200, 120), speed=0.47, image_path = "saturn.png"),  # Сатурн
    Planet(screen, radius=18, orbit_radius=280, color=(100, 200, 255), speed=0.40, image_path = "uran.png"),  # Уран
    Planet(screen, radius=13, orbit_radius=330, color=(50, 100, 255), speed=0.3, image_path = "neptun.png"),  # Нептун
    Planet(screen, radius=7, orbit_radius=380, color=(200, 180, 160), speed=0.1, image_path = "pluton.png")   # Плутон
]
explosions = []
# Создание Луны
earth = planets[2]  # Земля
moon = Moon(screen, earth, radius=3, orbit_radius=20, speed=10)

# Создание пояса астероидов и кометы
asteroid_belt = AsteroidBelt(screen, num_asteroids=170)
comet = Comet(screen)

class Sun:
    def __init__(self, screen, image_path, radius=40):
        self.screen = screen
        self.radius = radius
        self.x = cx
        self.y = cy
        
        
        try:
            
            original_image = pygame.image.load(image_path).convert_alpha()
           
            self.image = pygame.transform.scale(original_image, (radius*2, radius*2))
            self.has_image = True
        except:
            print(f"Не удалось загрузить изображение Солнца: {image_path}")
            self.has_image = False
            self.color = (255, 200, 0) 
    
    def draw(self):
        if self.has_image:
            
            self.screen.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))
        else:
           
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)


sun = Sun(screen, "sun.png", radius=40)  


running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            cx = WIDTH // 2
            cy = HEIGHT // 2
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                # Проверяем клик по каждой планете
                for planet in planets:
                    if planet.is_clicked(event.pos):
                      explosions.append(planet.explode())
                      if explosion_sound:
                          explosion_sound.play()
                      break
 
    # Обновление позиций
    for planet in planets:
        planet.update(dt)
    moon.update(dt)
    asteroid_belt.update(dt)
    comet.update(dt)
    active_explosions = []
    for explosion in explosions:
        if explosion.update(dt):  # Если взрыв еще активен
            active_explosions.append(explosion)
    explosions = active_explosions
    # Отрисовка
    screen.fill((0, 0, 0))
    
    # Солнце
    sun.draw()
    # Планеты
    for planet in planets:
        planet.draw()
    
    for explosion in explosions:
        try:
            explosion.draw(screen)
        except Exception as e:
            print(f"Ошибка при отрисовке взрыва: {e}")
    
    # Луна
    moon.draw()
    
    # Пояс астероидов
    asteroid_belt.draw()
    
    # Комета
    comet.draw()
    
    pygame.display.flip()

pygame.quit()