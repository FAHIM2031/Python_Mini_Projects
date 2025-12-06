from turtle import Turtle
import random
COLORS=["red","green","yellow","orange","purple","blue","pink"]
STARTING_MOVE_DISTANCE=5
MOVE_INCREMENT=5
class CarManager():
    def __init__(self):
        self.all_cars=[]
        self.spreed=STARTING_MOVE_DISTANCE
    def create_cars(self):
        random_number=random.randint(1,5)
        if random_number==2:
            new_car=Turtle("square")
            new_car.shapesize(stretch_wid=1,stretch_len=2)
            new_car.penup()
            new_car.color(random.choice(COLORS))
            new_car.goto(300,random.randint(-250,250))
            self.all_cars.append(new_car)
    def move_cars(self):
        for car in self.all_cars:
            car.backward(self.spreed)

    def speed_of_car(self):
        self.spreed+=MOVE_INCREMENT


