from turtle import Screen,Turtle
from snake import Snake
import time
from food import Food
from scoreboard import Scoreboard
screen=Screen()
screen.setup(width=600,height=600)
screen.bgcolor("Black")
screen.title("Welcome to the snake game")
screen.tracer(0)


snake=Snake()
food=Food()
score=Scoreboard()
screen.listen()
screen.onkey(snake.turn_up,"Up")
screen.onkey(snake.turn_down,"Down")
screen.onkey(snake.turn_left,"Left")
screen.onkey(snake.turn_right,"Right")

is_game_on=True
cnt=3
while(is_game_on):
    screen.update()
    time.sleep(0.2)
    snake.move_snake()
    if snake.head.distance(food)<20:
        score.increase_score()
        food.refresh()
        snake.extend_segment()
    if snake.head.xcor()<-300 or snake.head.xcor()>280 or snake.head.ycor()<-280 or snake.head.ycor()>300:
        score.game_over()
        snake.reset_snake()
    for segment in snake.segment[1:]:
        if snake.head.distance(segment)<10:
            score.game_over()
            snake.reset_snake()



    # for segment in snake.segment:
    #     if snake.head==segment:
    #         pass
    #     elif snake.head.distance(segment)<10:
    #         print("Game Over")
    #         is_game_on=False
    #         score.game_over()


































screen.exitonclick()