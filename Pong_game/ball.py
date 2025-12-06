from turtle import Turtle
import random
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.shapesize(stretch_wid=1,stretch_len=1)
        self.goto(0,0)
        self.penup()
        self.speed("slow")
        self.x_move=10
        self.y_move=10
        self.ball_spedd=0.1
    def move_ball_screen(self):
        self.goto(self.xcor()+self.x_move,self.ycor()+self.y_move)
    def ball_bounce_y(self):
        self.y_move *=-1
    def ball_bounce_x(self):
        self.x_move*=-1
        self.ball_spedd*=0.9
        
    def return_ball(self):
        self.home()
        self.ball_bounce_x()
        self.ball_spedd=0.1

        