from turtle import Turtle
STARTING_POSITION=(0,-280)
MOVE_DISTANCE=10
FINISH_LINE_Y=280
class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("white")
        self.setheading(90)
        self.penup()
        self.goto(STARTING_POSITION)
        self.y_cor=STARTING_POSITION[1]
        
    
    def move_player(self):
        self.forward(MOVE_DISTANCE)
        
    def return_player(self):
        self.goto(0,-280)