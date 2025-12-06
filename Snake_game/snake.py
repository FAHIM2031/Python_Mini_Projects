# from Main import segment
from turtle import Screen,Turtle
RIGHT=0
UP=90
LEFT=180
DOWN=270

class Snake:
    def __init__(self):
        self.segment=[]
        self.collect_segment=[(0,0),(-20,0),(-40,0)]
        self.create_snake()
        self.head=self.segment[0]


    def create_snake(self):
        for pos in self.collect_segment:
            turtle = Turtle("square")
            turtle.color("red")
            turtle.penup()
            turtle.goto(pos)
            self.segment.append(turtle)
    def extend_segment(self):
        turtle = Turtle("square")
        turtle.penup()
        turtle.goto(self.segment[-1].position())
        turtle.color("white")
        self.segment.append(turtle)
        
        
        
    

    def move_snake(self):
        for seg_num in range(len(self.segment) - 1, 0, -1):
            new_x = self.segment[seg_num - 1].xcor()
            new_y = self.segment[seg_num - 1].ycor()
            self.segment[seg_num].goto(new_x, new_y)
        self.head.forward(20)

    def turn_left(self):
        if self.head.heading()!=RIGHT:
            self.head.setheading(LEFT)

    def turn_right(self):
        if self.head.heading()!=LEFT:
            self.head.setheading(RIGHT)

    def turn_up(self):
        if self.head.heading()!=DOWN:
            self.head.setheading(UP)

    def turn_down(self):
        if self.head.heading()!=UP:
            self.head.setheading(DOWN)
    def reset_snake(self):
        for snake in self.segment:
            snake.goto(1000,1000)
        self.segment.clear()
        self.create_snake()
        self.head=self.segment[0]