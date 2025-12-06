import turtle
import pandas
screen = turtle.Screen()
screen.title("US state finder game")

image="blank_states_img.gif"
turtle.addshape(image)
turtle.shape(image)
correct=0

while correct<=50:
    answer_state= screen.textinput(title=f"{correct}/50 state are correct", prompt="Enter your answer").title()
    state_file=pandas.read_csv("50_states.csv")
    all_state=state_file.state.to_list()

    if answer_state=="Exit":
        break

    if answer_state in all_state:
        correct = correct + 1
        t=turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data=state_file[state_file.state==answer_state]
        t.goto(int(state_data.x),int(state_data.y))
        t.write(answer_state)











#to find the location on click of mouse
# def get_mouse_click(x,y):
#     print(x,y)
#
# turtle.onscreenclick(get_mouse_click)
screen.exitonclick()

