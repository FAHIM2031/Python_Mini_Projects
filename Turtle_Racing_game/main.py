import time
from turtle import Turtle,Screen
from car_manager import CarManager
from player import Player
from scoreboard import Scoreboard


screen=Screen()
screen.setup(width=600,height=600)
screen.bgcolor("black")
screen.tracer(0)
player=Player()
screen.listen()
screen.onkey(fun=player.move_player, key="Up")
car_manager=CarManager()
scoreboard=Scoreboard()


game_is_on=True
while game_is_on:
    time.sleep(0.2)
    screen.update()
    car_manager.create_cars()
    car_manager.move_cars()
    if (player.ycor()>280):
        scoreboard.count_score()
        player.return_player()
        car_manager.speed_of_car()
    for car in car_manager.all_cars:
        if player.distance(car)<25:
            scoreboard.game_over()
            game_is_on=False


















screen.exitonclick()