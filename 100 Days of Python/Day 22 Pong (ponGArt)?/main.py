from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import ScoreBoard
import time

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong!")
screen.tracer(0)
screen.colormode(255)

game_ongoing = True
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
scores = ScoreBoard()
ball = Ball()

screen.listen()
screen.onkeypress(l_paddle.move_up, "w")
screen.onkeypress(r_paddle.move_up, "Up")
screen.onkeypress(l_paddle.move_down, "s")
screen.onkeypress(r_paddle.move_down, "Down")

while game_ongoing:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()
    r_paddle.maintain()
    l_paddle.maintain()

    # Collision with top & bottom walls
    if ball.ycor() >= 290 or ball.ycor() <= -290:
        ball.y_bounce()

    # Collision with paddles
    # Additional condition to check as x.distance(y) calculates distance from center of x to center of y.
    # if x is as long as our rectangular paddle, wont detect y from the edges
    if ball.xcor() > 320 and r_paddle.distance(ball) < 50 or ball.xcor() < -320 and l_paddle.distance(ball) < 50:
        ball.x_bounce()

    # If paddle misses ball
    if ball.xcor() > 380:
        ball.reset()
        scores.increase_l_score()

    if ball.xcor() < -380:
        ball.reset()
        scores.increase_r_score()































screen.exitonclick()