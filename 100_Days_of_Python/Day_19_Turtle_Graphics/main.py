# Turtle Graphics Documentation: https://docs.python.org/3/library/turtle.html#turtle.position
import turtle as t

######## Challenge 1 - Draw a Square ############
# tim = t.Turtle()
# tim.shape("turtle")
# tim.color("lime")
# for _ in range(4):
#     tim.forward(100)
#     tim.left(90)

######## Challenge 2 - Draw a Dashed Line ############
# tim = t.Turtle()
# tim.shape("turtle")
# tim.color("lime")

# def draw_dash(n):
#     tim.pendown()
#     tim.forward(n)
#     tim.penup()
#     tim.forward(n)
#
#
# def draw_dash_in_square(n):
#     for _ in range(4):
#         draw_dash(n)
#         tim.left(90)
#         n += 10
#
#
# n = 50
# for _ in range(15): draw_dash_in_square(n)

######## Challenge 3 - Draw Overlaying Shapes ############
# Triangle>Square>Pentagon>Hexagon>Heptagon>Octagon>Nonagon>decagon

# tim = t.Turtle()
# tim.shape("turtle")
# tim.color("lime")

# import random
# side_length = 100
#
#
# def draw_shape(no_of_sides):
#     for _ in range(no_of_sides):
#         tim.forward(side_length)
#         tim.right(360/no_of_sides)
#
#
# for i in range(3, 11):
#     draw_shape(i)
#     tim.color(random.choice(["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]))

######## Challenge 4 - Generating random walk ############
# tim = t.Turtle()
# tim.shape("turtle")
# tim.color("lime")

# import random
# t.colormode(255)        # need to change colormode in actual turtle module to use RGB values
#
# tim.speed("fastest")
# tim.pensize(10)
#
#
# for _ in range(100):
#     tim.forward(25)
#     tim.color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     # vs random.choice(["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"])
#     tim.right(random.choice([0, 90, 180, 270]))

######## Challenge 4 - Drawing a spirograph ############
# tim = t.Turtle()
# tim.shape("turtle")
# tim.color("lime")

# import random
# t.colormode(255)
#
# tim.speed("fastest")
#
## To ensure no overlapping of circles, only want to draw 1 set of spirograph, so should stop after a full rotation of 360°
# def draw_spirograph(size_between_gaps):
#     for _ in range(int(360/size_between_gaps)):
#         tim.circle(150)
#         tim.color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#         tim.setheading(tim.heading()+size_between_gaps)
#
#
# draw_spirograph(5)
## This creates the screen then allows u to exit on click, so cannot put before all other code
# screen = t.Screen()
# screen.exitonclick()

######## Challenge 5 - Hirst Painting ############
# tim = t.Turtle()
# tim.shape("turtle")
# tim.color("lime")

## Extracting colors
# import colorgram
# colors = []
#
# for color in colorgram.extract('image.jpg', 30):
#     colors.append((color.rgb.r, color.rgb.g, color.rgb.b))
# print(colors)
# import random
# t.colormode(255)
#
# colors = [(202, 164, 110), (149, 75, 50), (152, 201, 136),
#           (53, 93, 123), (170, 154, 41), (138, 31, 20), (134, 163, 184), (197, 92, 73), (47, 121, 86), (73, 43, 35),
#           (145, 178, 149), (14, 98, 70), (232, 176, 165), (160, 142, 158), (54, 45, 50), (101, 75, 77), (183, 205, 171),
#           (36, 60, 74), (19, 86, 89), (82, 148, 129), (147, 17, 19), (27, 68, 102), (12, 70, 64), (107, 127, 153),
#           (176, 192, 208), (168, 99, 102)]
# tim.speed("fastest")
# tim.penup()
# tim.hideturtle()
# interval = 0
#
# for _ in range(10):
#     tim.setpos(-250, 250-interval)
#     interval += 50
#     for _ in range(10):
#         tim.dot(20, random.choice(colors))
#         tim.forward(50)
#
# screen = t.Screen()
# screen.exitonclick()

######## Challenge 6 - Etch-A-Sketch ############
# tim = t.Turtle()
# tim.shape("turtle")
# tim.color("lime")

##
# screen = t.Screen()
# tim.shape("arrow")
#
# def move_forward():
#     return tim.forward(10)
#
#
# def move_backward():
#     return tim.backward(10)
#
#
# def turn_left():
#     return tim.left(10)
#
#
# def turn_right():
#     return tim.right(10)
#
#
# def clear():
#     tim.clear()
#     tim.penup()
#     tim.setpos(0, 0)
#     tim.pendown()
#
#
## onkeypress for holding key down
# screen.onkeypress(move_forward, "w")
# screen.onkeypress(move_backward, "s")
# screen.onkeypress(turn_left, "a")
# screen.onkeypress(turn_right, "d")
## onkey for press key once
# screen.onkey(clear, "c")
#
# screen.listen()
# screen.exitonclick()

######## Challenge 7 - Turtle Racing! ############
import random
screen = t.Screen()
# Use keyword arguments over positional arguments in this case so reader can understand easily without having to refer
# to documentation too!
screen.setup(width=500, height=400)
has_bet = screen.textinput(title="Make your bet!", prompt="Which turtle will win the race? (red/orange/yellow/green/blue/purple/brown/black/white) Enter a color: ")
colors = ["red", "orange", "yellow", "green", "blue", "purple", "brown", "black", "white"]
y_positions = [80, 60, 40, 20, 0, -20, -40, -60, -80]
turtles = []
has_race_end = True

for turtle_i in range(0, 9):
    jim = t.Turtle(shape="turtle")
    jim.color(colors[turtle_i])
    jim.penup()
    jim.goto(x=-230, y=y_positions[turtle_i])
    turtles.append(jim)

if has_bet: has_race_end = False

while not has_race_end:
    for turtle in turtles:
        turtle.forward(random.randint(5, 15))
        if turtle.xcor() >= 230:
            if turtle.pencolor() == has_bet: print(f"You've won! The {turtle.pencolor()} turtle is the winning color!")
            else: print(f"You've lost! The {turtle.pencolor()} turtle is the winning color!")
            has_race_end = True



screen.exitonclick()

 

