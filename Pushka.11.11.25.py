import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Пушка с мишенями")

# Загрузка изображений
try:
    background = pygame.image.load("scary_fon.jpg")
    background = pygame.transform.scale(background, (600, 400))
except:
    # Создаем простой фон, если изображение не найдено
    background = pygame.Surface((600, 400))
    background.fill((100, 150, 255))

try:
    projectile_image = pygame.image.load("apelsine.jpg")
    # Убираем белый фон, если он есть
    projectile_image.set_colorkey((255, 255, 255))
    projectile_image = pygame.transform.scale(projectile_image, (35, 35))
except:
    # Создаем простой прямоугольник, если изображение не найдено
    projectile_image = pygame.Surface((40, 40))
    projectile_image.fill((255, 0, 0))

# Загрузка двух изображений для мишени - обычное и при попадании
try:
    target_image = pygame.image.load("troll_happy.jpg")
    target_image.set_colorkey((255, 255, 255))
    target_image = pygame.transform.scale(target_image, (70, 70))
    
    target_hit_image = pygame.image.load("troll_sad.png")  # Изображение после попадания
    target_hit_image.set_colorkey((255, 255, 255))
    target_hit_image = pygame.transform.scale(target_hit_image, (70, 70))
except:
    # Создаем простые мишени, если изображения не найдены
    target_image = pygame.Surface((30, 30))
    target_image.fill((255, 255, 0))
    pygame.draw.circle(target_image, (255, 0, 0), (15, 15), 12)
    pygame.draw.circle(target_image, (0, 0, 0), (15, 15), 6)
    
    target_hit_image = pygame.Surface((30, 30))
    target_hit_image.fill((0, 255, 0))  # Зеленая мишень после попадания
    pygame.draw.circle(target_hit_image, (0, 0, 255), (15, 15), 12)
    pygame.draw.circle(target_hit_image, (255, 255, 255), (15, 15), 6)

# Настройка и запуск фоновой музыки
try:
    pygame.mixer.init()
    pygame.mixer.music.load("Emae.mp3")
    pygame.mixer.music.set_volume(0.5)  # Громкость 50%
    pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение
    print("Фоновая музыка запущена")
except Exception as e:
    print(f"Фоновая музыка не найдена: {e}")

try:
    score_sound = pygame.mixer.Sound("ouch.mp3")
    score_sound.set_volume(0.7)  # Громкость звука попадания
except:
    print("Звук попадания не найден")

# Начальные параметры снаряда
start_x, start_y = 50, 350
x, y = start_x, start_y
projectile_width, projectile_height = 40, 20

vx, vy = 0, 0
gravity = 0.5
power = 12
angle = 45
bounce_loss = 0.7
on_ground = True

# Создаем три мишени с маленьким размером и быстрым движением
targets = []
for i in range(3):
    target = {
        'x': random.randint(200, 500),
        'y': 100 + i * 80,  # Располагаем мишени на разных высотах
        'width': 30,
        'height': 30,
        'speed': random.uniform(3.0, 6.0),
        'direction': random.choice([-1, 1]),
        'hit': False,  # Флаг попадания в мишень
        'hit_timer': 0  # Таймер для отображения попадания
    }
    targets.append(target)

font = pygame.font.Font(None, 24)

score = 0
music_playing = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                angle = min(angle + 5, 80)
            elif event.key == pygame.K_DOWN:
                angle = max(angle - 5, 10)
            elif event.key == pygame.K_w:
                power = min(power + 1, 25)
            elif event.key == pygame.K_s:
                power = max(power - 1, 5)
            elif event.key == pygame.K_SPACE and on_ground:
                rad = math.radians(angle)
                vx = power * math.cos(rad)
                vy = -power * math.sin(rad)
                on_ground = False
            elif event.key == pygame.K_m:  # Клавиша M для включения/выключения музыки
                music_playing = not music_playing
                if music_playing:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

    for target in targets:
        target['x'] += target['speed'] * target['direction']
        
    
        if target['hit']:
            target['hit_timer'] += 1
            if target['hit_timer'] > 30:  # Показываем попадание 30 кадров (около 0.5 секунды)
                target['hit'] = False
                target['hit_timer'] = 0
        
        # Проверка границ экрана для мишеней
        if target['x'] <= 0:
            target['x'] = 0
            target['direction'] = 1
        elif target['x'] + target['width'] >= 600:
            target['x'] = 600 - target['width']
            target['direction'] = -1

    if not on_ground:
        vy += gravity
        x += vx
        y += vy

    # Проверка столкновения с землей
    if y + projectile_height >= 400:
        y = 400 - projectile_height
        vy = -vy * bounce_loss
        vx *= bounce_loss
        if abs(vy) < 1 and abs(vx) < 1:
            x, y = start_x, start_y
            vx, vy = 0, 0
            on_ground = True

    # Проверка столкновения со стенами
    if x <= 0:
        x = 0
        vx = -vx * bounce_loss
    elif x + projectile_width >= 600:
        x = 600 - projectile_width
        vx = -vx * bounce_loss

    # Проверка столкновения с мишенями
    projectile_rect = pygame.Rect(x, y, projectile_width, projectile_height)
    
    for target in targets:
        target_rect = pygame.Rect(target['x'], target['y'], target['width'], target['height'])
        
        if projectile_rect.colliderect(target_rect) and not target['hit']:
            target['hit'] = True
            target['hit_timer'] = 0
            score += 1
            try:
                score_sound.play()
            except:
                pass

    # Отрисовка
    screen.blit(background, (0, 0))

    # Отрисовка траектории
    if on_ground:
        points = []
        rad = math.radians(angle)
        temp_vx = power * math.cos(rad)
        temp_vy = -power * math.sin(rad)
        temp_x, temp_y = start_x, start_y
        for i in range(60):
            temp_vy += gravity
            temp_x += temp_vx
            temp_y += temp_vy
            if temp_y + projectile_height >= 400:
                break
            points.append((int(temp_x), int(temp_y)))
        if len(points) > 1:
            pygame.draw.lines(screen, (0, 0, 0), False, points, 2)

    # Отрисовка мишеней
    for target in targets:
        # Выбираем изображение в зависимости от попадания
        if target['hit']:
            screen.blit(target_hit_image, (target['x'], target['y']))
        else:
            screen.blit(target_image, (target['x'], target['y']))

    # Отрисовка снаряда
    rotated_projectile = pygame.transform.rotate(projectile_image, -angle)
    screen.blit(rotated_projectile, (int(x), int(y)))

    # Отрисовка инфы
    text_angle = font.render(f"Угол: {angle}°", True, (255, 0, 0))
    text_power = font.render(f"Сила: {power}", True, (255, 0, 0))
    text_score = font.render(f"Счёт: {score}", True, (255, 0, 0))
    music_status = "ВКЛ" if music_playing else "ВЫКЛ"
    text_music = font.render(f"Музыка: {music_status} (M)", True, (255, 0, 0))
    
    screen.blit(text_angle, (10, 10))
    screen.blit(text_power, (10, 30))
    screen.blit(text_score, (10, 50))
    screen.blit(text_music, (10, 70))

    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()