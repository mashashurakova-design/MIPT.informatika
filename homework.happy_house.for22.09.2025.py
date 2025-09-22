import turtle

screen = turtle.Screen()
screen.bgcolor("lightblue")


t = turtle.Turtle()
t.speed(8)

#Земля 
t.penup()
t.goto(-300, -100)
t.pendown()
t.color("green")
t.begin_fill()
for i in range(2):
    t.forward(600)
    t.right(90)
    t.forward(100)
    t.right(90)
t.end_fill()

#Основание дома
t.penup()
t.goto(-100, -100)
t.pendown()
t.color("brown")
t.begin_fill()
for i in range(4):
    t.forward(200)
    t.left(90)
t.end_fill()

#Крыша
t.penup()
t.goto(-100, 100)
t.pendown()
t.color("red")
t.begin_fill()
t.goto(0, 200)
t.goto(100, 100)
t.goto(-100, 100)
t.end_fill()

#Дверь
t.penup()
t.goto(-30, -100)
t.pendown()
t.color("black")
t.begin_fill()
for i in range(2):
    t.forward(60)
    t.left(90)
    t.forward(80)
    t.left(90)
t.end_fill()

#Ручка двери
t.penup()
t.goto(10, -60)
t.pendown()
t.color("yellow")
t.begin_fill()
t.circle(5)
t.end_fill()

#Окно 1 (левое)
t.penup()
t.goto(-80, 0)
t.pendown()
t.color("blue")
t.begin_fill()
for i in range(4):
    t.forward(40)
    t.left(90)
t.end_fill()

#Окно 2 (правое)
t.penup()
t.goto(40, 0)
t.pendown()
t.begin_fill()
for i in range(4):
    t.forward(40)
    t.left(90)
t.end_fill()

#Рама окна 1 (вертикальная)
t.penup()
t.goto(-60, 0)
t.pendown()
t.color("white")
t.width(3)
t.goto(-60, 40)

#Рама окна 1 (горизонтальная)
t.penup()
t.goto(-80, 20)
t.pendown()
t.goto(-40, 20)

#Рама окна 2 (вертикальная)
t.penup()
t.goto(60, 0)
t.pendown()
t.goto(60, 40)

#Рама окна 2 (горизонтальная)
t.penup()
t.goto(40, 20)
t.pendown()
t.goto(80, 20)

#Солнце
t.penup()
t.goto(200, 150)
t.pendown()
t.color("yellow")
t.begin_fill()
t.circle(30)
t.end_fill()

#Лучи солнца
t.penup()
t.goto(200, 180)
t.pendown()
t.color("orange")
for i in range(8):
    t.penup()
    t.forward(30)
    t.pendown()
    t.forward(30)
    t.backward(30)
    t.penup()
    t.backward(30)
    t.left(45)

#Дерево (ствол)
t.penup()
t.goto(150, -100)
t.pendown()
t.color("brown")
t.begin_fill()
for i in range(2):
    t.forward(20)
    t.left(90)
    t.forward(60)
    t.left(90)
t.end_fill()

#Крона дерева
t.penup()
t.goto(130, -40)
t.pendown()
t.color("green")
t.begin_fill()
t.circle(40)
t.end_fill()

t.penup()
t.goto(150, -60)
t.pendown()
t.color("green")
t.begin_fill()
t.circle(40)
t.end_fill()

t.penup()
t.goto(160, -20)
t.pendown()
t.color("green")
t.begin_fill()
t.circle(40)
t.end_fill()

t.penup()
t.goto(200, 0)
t.pendown()
t.color("green")
t.begin_fill()
t.circle(40)
t.end_fill()

t.hideturtle()
turtle.done()