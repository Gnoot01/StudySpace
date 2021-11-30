# PacTurtle:
# TODO: Eat food, gain score. Eat special food can gain more score & eat ghosts to gain even more
# normal: +10. cherry: +100 Special: +50. if eat special, ghosts_edible_mode = True. while ghosts_edible_mode: ghosts: +200, speed++. time count(10s?)->ghosts_edible_mode = False
# TODO: Stop on collision with obstacles
# Can draw obstacles, but how to stop & continue in other directions?
# TODO: teleport on collision with wall
# Easy.
# TODO: Ghosts to chase you, stop on collision with obstacles
# while not game_end (head.distance(ghost.head)<15): while not ghosts_edible_mode: speed++, random ghost turn & forward?
# Whenever hit obstacle, turn and forward in clockwise motion

from turtle import Screen
from pacturtle import PacTurtle
from food import Food
from scoreboard import ScoreBoard
from walls import Walls
import time

NORMAL_POINTS = 10
POWERUP_POINTS = 50
CHERRY_POINTS = 100
# GHOST_POINTS = while ghosts_edible_mode: 2*num_of_ghosts_eaten

screen = Screen()
screen.setup(width=650, height=270)
screen.bgcolor("black")
screen.title("PacTurtle!")
screen.tracer(0)
game_ongoing = True

pacturtle = PacTurtle()
food = Food()
walls = Walls()
scoreboard = ScoreBoard()
screen.listen()

screen.onkey(pacturtle.turn_north, "w")
screen.onkey(pacturtle.turn_north, "Up")
screen.onkey(pacturtle.turn_south, "s")
screen.onkey(pacturtle.turn_south, "Down")
screen.onkey(pacturtle.turn_west, "a")
screen.onkey(pacturtle.turn_west, "Left")
screen.onkey(pacturtle.turn_east, "d")
screen.onkey(pacturtle.turn_east, "Right")

while game_ongoing:
    screen.update()
    time.sleep(0.1)
    pacturtle.move()

    # Handles eating food
    for normal_location in food.NORMAL_LOCATIONS:
        if pacturtle.distance(normal_location) < 10:
            scoreboard.increase_score(NORMAL_POINTS)
            food.remove(normal_location)
    for powerup_location in food.POWERUP_LOCATIONS:
        if pacturtle.distance(powerup_location) < 10:
            scoreboard.increase_score(POWERUP_POINTS)
            food.remove(powerup_location)
    for cherry_location in food.CHERRY_LOCATIONS:
        if pacturtle.distance(cherry_location) < 10:
            scoreboard.increase_score(CHERRY_POINTS)
            food.remove(cherry_location)

    # Handles pacturtle going to 1 side of the screen and coming out the other
    if pacturtle.xcor() < -280 and -10 <= pacturtle.ycor() <= 10: pacturtle.tp_l_to_r()
    if pacturtle.xcor() > 280 and -10 <= pacturtle.ycor() <= 10: pacturtle.tp_r_to_l()

    # Handles collision with walls
    # Edges first (because I actually dk how to get this to work)
    # for coords in walls.edges_coords:
    #     if pacturtle.distance(coords) <= 10:
    #         pacturtle.backward(5)

    # Handles collision with ghost
    # scoreboard.decrease_lives()
    # if len(scoreboard.lives) == 0:
    #   scoreboard.game_over()
    #   game_ongoing = False


















screen.exitonclick()
