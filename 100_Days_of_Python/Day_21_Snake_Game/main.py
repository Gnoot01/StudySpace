from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import ScoreBoard
import time

screen = Screen()
screen.setup(width=1000,height=800)
screen.bgcolor("black")
screen.title("SnakeSSSSSSSSSSSSSS!")
screen.colormode(255)
# Without screen tracer, screen update, time.sleep, snake will keep flickering (due to fast movement)
# and will see snake move very erratically, segment by segment (not smooth animation)
screen.tracer(0)    # 0 turns off animation
game_is_ongoing = True

snake = Snake()
food = Food()
scoreboard = ScoreBoard()
screen.listen()

screen.onkey(snake.turn_north, "w")
screen.onkey(snake.turn_north, "Up")
screen.onkey(snake.turn_south, "s")
screen.onkey(snake.turn_south, "Down")
screen.onkey(snake.turn_west, "a")
screen.onkey(snake.turn_west, "Left")
screen.onkey(snake.turn_east, "d")
screen.onkey(snake.turn_east, "Right")



while game_is_ongoing:
    screen.update()  # When game_is_ongoing, first thing you see is the animation updated after everything has moved into place
    time.sleep(0.1)  # To sleep between each while loop. sleep for 0.1 second

    snake.move()
    # Snake head collide with food
    # This method preferred over if snake.head.pos() == food.pos(), as that requires extreme precision
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.grow()
        scoreboard.increase_score()

    # Extra: How to make snake, if exits screen from a side, continue from opp side?
    if snake.head.xcor() > 500:snake.teleport_right_to_left()
    elif snake.head.xcor() < -500:snake.teleport_left_to_right()
    elif snake.head.ycor() > 400: snake.teleport_up_to_down()
    elif snake.head.ycor() < -400: snake.teleport_down_to_up()


    # Alternative: Snake head collide with wall
    # if snake.head.xcor() > 480 or snake.head.xcor() < -480 or snake.head.ycor() > 380 or snake.head.ycor() < -380:
    #     scoreboard.game_over()
    #     game_is_ongoing = False

    # Snake head collide with tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            scoreboard.reset()
            snake.reset()
            # scoreboard.game_over()
            # game_is_ongoing = False

    # TODO: Idea! Pacman..? (How would I make those obstacle collisions though? Coordinates are points) Hmmmm...

screen.exitonclick()
