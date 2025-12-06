from turtle import Turtle,Screen
import random
scr=Screen()
scr.setup(width=600,height=600)
scr.listen()
user_answer=scr.textinput(title="Make a bet on a Turtle=",prompt="Enter the color of the tutle")
color=["red","blue","green","orange","purple","yellow","black"]
y_index=[-150,-100,-50,0,50,100,150]
movement=[5,6,7,8,9,10,11,12,13,14,15]
is_race_on=False
all_turles=[]
ending_point=280

for turtle_index in range(0,7):
    tim=Turtle(shape="turtle")
    tim.color(color[turtle_index])
    tim.penup()
    tim.goto(x=-280,y=y_index[turtle_index])
    all_turles.append(tim)

if user_answer:
    is_race_on=True
while is_race_on:
    for turtle in all_turles:
        wining_color = turtle.pencolor()
        move_point = random.choice(movement)
        turtle.forward(move_point)
        if turtle.xcor()>260:
            is_race_on=False
            if user_answer==wining_color:
                print(f"You win! the winner is ={wining_color} turtle")
            else:
                print(f"You Loose! the winner is ={wining_color} turtle")









    
    


















scr.exitonclick()