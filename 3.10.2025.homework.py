import pygame
pygame.init()
font = pygame.font.SysFont(None, 24)

screen = pygame.display.set_mode((750, 850))
pygame.display.set_caption("Физтех.Рыбаков")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 255, 255))
    size = (500, 500)
    
    pygame.Surface(size, pygame.SRCALPHA)

    pygame.draw.rect(screen, (230,230,230), (0,550,750,300))#снег
    pygame.draw.line(screen, (0,0,0), (0,550), (750,550), 1)#горизонт
    
    pygame.draw.circle(screen, (161,249,228), (400,100), 200,30) #солнце
    pygame.draw.line(screen, (161,249,228), (400,0), (370,298), 40)#линия вертикальная на солнце
    pygame.draw.line(screen, (161,249,228), (205, 68), (600,122), 40)#линия горизонтальная на солнце
    pygame.draw.circle(screen, (220,247,218), (391,91), 30)#солнце маленькое_сзади
    pygame.draw.circle(screen, (255,246,213), (391,91), 20)#солнце маленькое
    pygame.draw.circle(screen, (220,247,218), (373,285), 25)#солнце маленькое
    pygame.draw.circle(screen, (255,246,213), (373,285), 15)#солнце маленькое
    pygame.draw.circle(screen, (220,247,218), (583,117), 25)#солнце маленькое
    pygame.draw.circle(screen, (255,246,213), (583,117), 15)#солнце маленькое
    pygame.draw.circle(screen, (220,247,218), (215,69), 25)#солнце маленькое
    pygame.draw.circle(screen, (255,246,213), (215,69), 15)#солнце маленькое
    
    pygame.draw.ellipse(screen, (77,77,77), (420,680,250,70))#стенка_прорубя
    pygame.draw.ellipse(screen, (0,0,0), (420,680,250,70,), 1)#стенка_прорубя_обводка
    pygame.draw.ellipse(screen, (22,80,68), (450,700,200,50))#лужа
    pygame.draw.ellipse(screen, (0,0,0), (450,700,200,50), 1)#лужа_обводка
    
    pygame.draw.ellipse(screen, (230,230,230), (130,330,160,80))#голова_медведя
    pygame.draw.ellipse(screen, (0,0,0), (130,330,160,80), 1)#голова_медведя_обводка
    
    pygame.draw.circle(screen, (0,0,0), (200,356), 8)#глаз
    pygame.draw.circle(screen, (255,255,255), (198,353), 2)#глаз
    pygame.draw.circle(screen, (0,0,0), (287,358), 6)#нос
    pygame.draw.circle(screen, (0,0,0), (283,368), 20, 1, 0, 0, 1)#рот
    pygame.draw.ellipse(screen, (230,230,230), (140,330,30,20))#ухо
    pygame.draw.ellipse(screen, (0,0,0), (140,330,30,20), 1)#ухо_обводка

    pygame.draw.ellipse(screen, (230,230,230), (50,380,200,350))#пузо_медведя
    pygame.draw.ellipse(screen, (0,0,0), (50,380,200,350), 1)#пузо_медведя_обводка

    pygame.draw.ellipse(screen, (230,230,230), (220,475,100,40))#лапа_медведя
    pygame.draw.ellipse(screen, (0,0,0), (220,475,100,40), 1)#лапа_медведя_обводка

    pygame.draw.ellipse(screen, (230,230,230), (180,640,130,100))#лапа_медведя
    pygame.draw.ellipse(screen, (0,0,0), (180,640,130,100), 1)#лапа_медведя_обводка

    pygame.draw.ellipse(screen, (230,230,230), (240,710,110,30))#лапа_медведя
    pygame.draw.ellipse(screen, (0,0,0), (240,710,110,30), 1)#лапа_медведя_обводка

    pygame.draw.circle(screen, (0,0,0), (500,478), 200, 3, 0, 1)#удочка
    pygame.draw.line(screen, (0,0,0), (500,280), (500,745), 1)#нить_удочки

    pygame.draw.ellipse(screen, (221,166,166), (320,760,50,20))#плавник_рыбки
    pygame.draw.ellipse(screen, (0,0,0), (320,760,50,20), 1)#плавник_рыбки_обводка
    pygame.draw.ellipse(screen, (221,166,166), (340,812,50,20))#плавник_рыбки
    pygame.draw.ellipse(screen, (0,0,0), (340,812,50,20),1)#плавник_рыбки
    pygame.draw.polygon(screen, (191,203,200), [(326,798),(295,784),(295,815)])#хвост
    pygame.draw.polygon(screen, (0,0,0), [(326,798),(295,784),(295,815)], 1)#хвост_обводка
    pygame.draw.ellipse(screen, (191,203,200), (320,770,130,50))#тело_рыбки
    pygame.draw.ellipse(screen, (0,0,0), (320,770,130,50),1)#тело_рыбки
    pygame.draw.circle(screen, (121,121,242), (430,792), 6)#глаз_рыбки
    pygame.draw.circle(screen, (0,0,0), (430,792), 6, 1)#глаз_рыбки_обводка
    pygame.draw.circle(screen, (0,0,0), (430,792), 1)#глаз_рыбки_зрачок

    
    mx, my = pygame.mouse.get_pos()
    text = font.render(f"x: {mx}, y: {my}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.display.flip()
    

pygame.quit()