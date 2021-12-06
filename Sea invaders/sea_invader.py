# Imports
import turtle
import sys
import os
import math
import random
import time
import registershape_invaders as rs

# Set up the screen
window = turtle.Screen()
window.title("Sea Journey - Sea Invaders")
window.bgcolor("black")
window.setup(width=700, height=600)
window.bgpic("Images/praia.png")
window.tracer(0)

# Draw border
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.setposition(-300, -300)
border.pendown()
border.pensize(3)

for side in range(4):
    border.fd(600)
    border.lt(90)

border.hideturtle()

# Score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 275)
score_string = "Score: {}".format(score)
score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
# player.shape("Images/player.gif")
player.shape("turtle")
player.color("green")
player.shapesize(2, 2, 2)
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

player_speed = 15

# Player movements
def move_left():

    x = player.xcor()
    x -= player_speed

    if(x < -280):
        x = -280

    player.setx(x)

def move_right():
    
    x = player.xcor()
    x += player_speed

    if(x > 280):
        x = 280

    player.setx(x)

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("black")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bullet_speed = 2

# Define bullet state
# Ready to fire
bullet_state = "ready"

def fire_bullet():

    # Declare bullet_state as a global if it needs changed
    global bullet_state 

    if(bullet_state == "ready"):
        os.system("aplay Sounds/laser.wav&")
        bullet_state = "fire"

        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


# Choose a number of enemies
number_enemies = 30
enemies = []

for i in range(number_enemies):
    # Create enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_index = 0
    
for enemy in enemies:
    enemy.shape(rs.plastico)
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_index)
    y = enemy_start_y
    enemy.setposition(x, y)
    enemy_index += 1

    if(enemy_index == 10):
        enemy_start_y -= 50
        enemy_index = 0

enemy_speed = 0.1


# Check bullet and enemy collision
def is_collision(turtle1, turtle2):

    distance = math.sqrt(math.pow(turtle1.xcor() - turtle2.xcor(), 2) + math.pow(turtle1.ycor() - turtle2.ycor(), 2))

    if(distance < 15):
        return True
    else:
        return False


# Create keyboard bindings
window.listen()
window.onkey(move_left, "Left")
window.onkey(move_right, "Right")
window.onkey(fire_bullet, "space")


# Main game loop
while True:

    window.update()

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Move the enemy back and down
        if(enemy.xcor() > 280 or enemy.xcor() < -280):
            
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemy_speed *= -1

        # Check for a collision between the bullet and the enemy
        if(is_collision(bullet, enemy)):
            os.system("aplay Sounds/explosion.wav&")

            # Reset the bullet
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)

            # Reset the enemy
            enemy.setposition(0, 10000)
            number_enemies -= 1

            score += 10
            score_string = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

        if(number_enemies == 0):
            os.system("aplay Sounds/fireworks.wav&")

            score_pen.clear()
            score_pen.setposition(-100, 200)
            score_pen.write("Mandou bem!", font=("Courier", 24, "bold"))

            score_pen.setposition(0, 150)
            score_pen.write("Todos os peixinhos foram salvos!", align="center", font=("Courier", 18, "bold"))

            score_pen.setposition(0, 100)
            score_pen.write("Desenvolvido pela UFRJ Analytica Time 2", align="center", font=("Courier", 16, "bold"))

            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            time.sleep(5)
            sys.exit()

        if(is_collision(player, enemy)):
            os.system("aplay Sounds/pacman-die.wav&")

            score_pen.clear()
            score_pen.setposition(-75, 200)
            score_pen.write("FIM DE JOGO", font=("Courier", 24, "bold"))

            score_pen.setposition(0, 150)
            score_pen.write("Obrigado por ter jogado!", align="center", font=("Courier", 18, "bold"))

            score_pen.setposition(0, 100)
            score_pen.write("Desenvolvido pela UFRJ Analytica Time 2", align="center", font=("Courier", 16, "bold"))

            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            time.sleep(5)
            sys.exit()

    # Move the bullet
    if(bullet_state == "fire"):
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    # Check if the bullet reached the top
    if(bullet.ycor() > 275):
        bullet.hideturtle()
        bullet_state = "ready"