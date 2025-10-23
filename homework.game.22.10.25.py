import pygame
import random

# Настройка pygame
pygame.init()

# Размеры окна
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ловля яиц")

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Корзина
basket_x = 350
basket_y = 500
basket_width = 100
basket_height = 80
basket_speed = 15

# Яйца
eggs = []
egg_width = 40
egg_height = 50
egg_speed = 3

egg_timer = 0
egg_wait_time = 90

# Счет
score = 0
missed = 0
max_missed = 3
max_score = 20

wasted_sound = pygame.mixer.Sound("WASTED.wav")
YAY_sound = pygame.mixer.Sound("YAY.wav")
PANIC_sound = pygame.mixer.Sound("PANIC.wav")
mine_sound = pygame.mixer.Sound("wilted.wav")
vic_sound = pygame.mixer.Sound("Victori.wav")
# Шрифт
font = pygame.font.Font(None, 36)

# Игровой цикл
clock = pygame.time.Clock()
game_running = True
game_over = False
game_win = False
while game_running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or game_win):
                # Перезапуск игры
                eggs = []
                score = 0
                missed = 0
                game_over = False
                game_win = False
                basket_x = 350
    
    # Управление корзиной
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < width - basket_width:
        basket_x += basket_speed
    
    if not game_over and not game_win:
        # Создание новых яиц по очереди
        egg_timer += 1
        
        if egg_timer >= egg_wait_time and len(eggs) == 0:
            side = random.choice(["left", "right"])
            
            if side == "left":
                # Яйцо с левой стороны
                egg_x = -egg_width
                egg_y = random.randint(100, 300)
                egg_horizontal_speed = random.randint(3, 6)
                egg_direction = "right"
            else:
                # Яйцо с правой стороны
                egg_x = width
                egg_y = random.randint(100, 300)
                egg_horizontal_speed = -random.randint(3, 6)
                egg_direction = "left"
            
            eggs.append({
                "x": egg_x,
                "y": egg_y,
                "speed": egg_horizontal_speed,
                "direction": egg_direction,
                "falling": False,
                "fall_speed": 0
            })
            
            egg_timer = 0  # сбрасываем таймер
        
        # Обновление яиц
        for egg in eggs[:]:
            if not egg["falling"]:
                # Движение по горизонтали
                egg["x"] += egg["speed"]
                
                # Проверка, когда начать падать
                if egg["direction"] == "right" and egg["x"] >= egg["y"]:
                    egg["falling"] = True
                elif egg["direction"] == "left" and egg["x"] <= width - egg["y"]:
                    egg["falling"] = True
            else:
                # Падение вниз
                egg["fall_speed"] += 0.3
                egg["y"] += egg["fall_speed"]
            
            # Проверка столкновения с корзиной
            basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)
            egg_rect = pygame.Rect(egg["x"], egg["y"], egg_width, egg_height)
            
            if basket_rect.colliderect(egg_rect) and egg["falling"]:
                eggs.remove(egg)
                score += 1
                YAY_sound.play()
                if score >= max_score:
                    game_win = True
                    vic_sound.play()



            
            # Проверка, упало ли яйцо на землю
            if egg["y"] > height:
                eggs.remove(egg)
                missed += 1
                PANIC_sound.play()
                if missed >= max_missed:
                    game_over = True
                    wasted_sound.play()
    
    # Отрисовка
    screen.fill(black)
    kuratnick = pygame.image.load("amazing-chicken-coop-tours.jpg")
    kuratnick = pygame.transform.scale(kuratnick, (width, height))
    screen.blit(kuratnick, (0, 0))
    # Рисуем землю
    pygame.draw.rect(screen, (100, 70, 0), (0, height - 10, width, 10))
    
    # Рисуем корзину (простой прямоугольник)
    pygame.draw.rect(screen, blue, (basket_x, basket_y, basket_width, basket_height))
    pygame.draw.rect(screen, (0, 100, 200), (basket_x, basket_y, basket_width, 20))
    
    # Рисуем яйца (белые овалы)
    for egg in eggs:
        pygame.draw.ellipse(screen, white, (egg["x"], egg["y"], egg_width, egg_height))
    
    # Рисуем счет
    score_text = font.render(f"Счет: {score}/{max_score}", True, white)
    screen.blit(score_text, (10, 10))
    
    # Рисуем пропущенные яйца
    missed_text = font.render(f"Пропущено: {missed}/{max_missed}", True, white)
    screen.blit(missed_text, (10, 50))

    
    
    # Если игра окончена
    if game_over:
        # Темный фон
        dark_surface = pygame.Surface((width, height))
        dark_surface.set_alpha(150)
        dark_surface.fill(black)
        screen.blit(dark_surface, (0, 0))
        
        # Красный прямоугольник
        pygame.draw.rect(screen, red, (200, 200, 400, 200))
        pygame.draw.rect(screen, white, (200, 200, 400, 200), 3)
        
        # Текст WASTED
        wasted_text = font.render("WASTED", True, white)
        screen.blit(wasted_text, (350, 250))
        
        # Финальный счет
        final_score = font.render(f"Финальный счет: {score}", True, white)
        screen.blit(final_score, (300, 300))
        
        # Инструкция
        restart_text = font.render("Нажми R для перезапуска", True, white)
        screen.blit(restart_text, (280, 350))

        #wasted_sound.play()

    if game_win:
        # Темный фон
        dark_surface = pygame.Surface((width, height))
        dark_surface.set_alpha(150)
        dark_surface.fill(black)
        screen.blit(dark_surface, (0, 0))
        
        # Красный прямоугольник
        pygame.draw.rect(screen, green, (200, 200, 400, 200))
        pygame.draw.rect(screen, white, (200, 200, 400, 200), 3)
        
        # Текст WASTED
        wasted_text = font.render("Вы победили!!!", True, white)
        screen.blit(wasted_text, (350, 250))
        
        # Финальный счет
        final_score = font.render(f"Финальный счет: {score}", True, white)
        screen.blit(final_score, (300, 300))
        
        # Инструкция
        restart_text = font.render("Нажми R для перезапуска", True, white)
        screen.blit(restart_text, (280, 350))

    pygame.display.update()
    clock.tick(60)

pygame.quit()