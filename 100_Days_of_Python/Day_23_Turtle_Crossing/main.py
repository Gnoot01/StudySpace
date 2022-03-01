import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(height=600, width=600)
screen.title("Turtle Crossing")
screen.tracer(0)

game_ongoing = True
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()


screen.listen()
screen.onkey(player.move, "w")
screen.onkey(player.move, "Up")

while game_ongoing:
    time.sleep(0.1)
    screen.update()
    car_manager.create()

    # Handles collision with car
    for car in car_manager.all_cars:
        if player.distance(car) <= 20:
            scoreboard.game_over()
            game_ongoing = False

    # Handles successful crossing
    if player.finished():
        scoreboard.increase_level()
        player.advance()
        car_manager.upgrade_cars()




screen.exitonclick()
