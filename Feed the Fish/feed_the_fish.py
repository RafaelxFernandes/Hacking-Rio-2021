# Imports
import turtle
import time
import random
import sys
import os
import registershape as rs
import secrets

# Set up the screen
window = turtle.Screen()
window.title("Sea Journey - Feed the Fish")
window.bgcolor("black")
window.setup(width=600, height=400)
window.tracer(0) # Turns off the screen updates
window.bgpic("Images/sea.png")

# Screen delay
delay = 0.1

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 150)
pen.write("Score: 0    High score: 0", align="center", font=("Courier", 24, "normal"))

# Scores
score = 0
high_score = 0


# Player head
head = turtle.Turtle()
head.speed(0)
head.shape(rs.peixe)
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "right"

# Player additional body parts
segments = []


# Food
food = turtle.Turtle()
food.speed(0)
food.shape(rs.comida1)
food.color("red")
food.penup()
food.goto(100, 100)


# Functions
# Go up
def go_up():
    if(head.direction != "down"):
        head.direction = "up"

# Go down
def go_down():
    if(head.direction != "up"):
        head.direction = "down"

# Go right
def go_right():
    if(head.direction != "left"):
        head.direction = "right"

# Go left
def go_left():
    if(head.direction != "right"):
        head.direction = "left"

# Move head
def move():
    
    if(head.direction == "up"):
        y = head.ycor()
        head.sety(y + 20)

    if(head.direction == "down"):
        y = head.ycor()
        head.sety(y - 20)
    
    if(head.direction == "right"):
        x = head.xcor()
        head.setx(x + 20)

    if(head.direction == "left"):
        x = head.xcor()
        head.setx(x - 20)


# Keyboard bindings
window.listen()
window.onkey(go_up, "Up")
window.onkey(go_down, "Down")
window.onkey(go_right, "Right")
window.onkey(go_left, "Left")


# Main game loop
while True:

    window.update()

    # Check collisions with the borders
    if(head.xcor() > 260 or head.xcor() < -260 or head.ycor() > 170 or head.ycor() < -170):

        os.system("aplay Sounds/explosion.wav&")
        pen.clear()

        #  Close game
        pen.write("FIM DE JOGO", align="center", font=("Courier", 24, "normal"))

        pen.setposition(0, 200)
        pen.write("Prepare-se para outro jogo em instantes!", align="center", font=("Courier", 18, "normal"))
        
        pen.clear()

        head.hideturtle()
        for segment in segments:
            segment.hideturtle()
        food.hideturtle()

        #  Open Sea Invaders
        time.sleep(5)

        sys.path.append('Sea invaders')
        import sea_invader

    comidas = [rs.comida1, rs.comida2, rs.comida3, rs.comida4, rs.comida4]

    # Check if the snake ate the food
    if(head.distance(food) < 20):

        escolha = secrets.choice(comidas)

        food.shape(escolha)

        # Move the food to a random spot
        x = random.randint(-260, 260)
        y = random.randint(-150, 150)
        food.goto(x, y)

        # Add a segment to snake's body
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape(rs.peixe_filho)
        new_segment.color("lime")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase score
        score += 1

        # Check high score
        if(score > high_score):
            high_score = score

        pen.clear()
        pen.write("Score: {}    High score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Move the segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):

        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segments[0] to where the head is
    if(len(segments) > 0):

        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    # Move head
    move()

    # Check for collisions with snake's body
    for segment in segments:

        if(segment.distance(head) < 20):

            os.system("aplay Sounds/explosion.wav&")

            #  Close game
            pen.clear()

            pen.write("FIM DE JOGO", align="center", font=("Courier", 24, "normal"))

            pen.setposition(0, 200)
            pen.write("Prepare-se para outro jogo em instantes!", align="center", font=("Courier", 18, "normal"))
            
            pen.clear()

            head.hideturtle()
            for segment in segments:
                segment.hideturtle()
            food.hideturtle()

            #  Open Sea Invaders
            time.sleep(5)
            
            sys.path.append('Sea Invaders')
            import sea_invader
            

    # Adds delay to screen update
    time.sleep(delay)


# Turtle main loop
turtle.mainloop()