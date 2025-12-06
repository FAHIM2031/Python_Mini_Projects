from turtle import Turtle
class Paddle(Turtle):
    def __init__(self,position):
        super().__init__()
        self.shape("square")
        self.color("blue")
        self.turtlesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)
    def paddle_move_up(self):
        self.goto(x=self.xcor(),y=self.ycor()+20)
    def paddle_move_down(self):
        self.goto(x=self.xcor(),y=self.ycor()-20)
        
        
        
        
        
        