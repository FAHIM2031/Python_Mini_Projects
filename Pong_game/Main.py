from turtle import Turtle,Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time
screen=Screen()
screen.tracer(0)
pad_right=Paddle((350,0))
pad_left=Paddle((-350,0))
ball=Ball()
score_rp=Scoreboard((100,200))
score_lp=Scoreboard((-100,200))



screen.bgcolor("black")
screen.setup(width=800,height=600)
screen.title("Pong Game")
screen.listen()
screen.onkey(fun=pad_right.paddle_move_up,key="Up")
screen.onkey(fun=pad_right.paddle_move_down,key="Down")

screen.onkey(fun=pad_left.paddle_move_up,key="Left")
screen.onkey(fun=pad_left.paddle_move_down,key="Right")


game_is_on=True
ball_fast=0.1
while game_is_on:
    time.sleep(ball_fast)
    screen.update()
    ball.move_ball_screen()
    if ball.ycor()>280 or ball.ycor()<-280:
        ball.ball_bounce_y()

    if ball.distance(pad_right) < 50 and ball.xcor() > 320:
        ball.ball_bounce_x()
    if ball.distance(pad_left)<50 and ball.xcor()<-320:
        ball.ball_bounce_x()

    if ball.xcor()>382:
        ball.return_ball()
        score_lp.update_score()


    if ball.xcor()<-382:
        ball.return_ball()
        score_rp.update_score()




























screen.exitonclick()