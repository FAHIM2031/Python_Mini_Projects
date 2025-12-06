from turtle import Turtle
FONT=("Courier",14,"normal")
class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score=0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-270, 260)
        self.write(f"The Level is = {self.score}", align="left", font=FONT)

    def count_score(self):
        self.score+=1
        self.clear()
        self.goto(-270, 260)
        self.write(f"The Level is = {self.score}", align="left", font=FONT)
    def game_over(self):
        self.goto(0,0)
        self.write(f"GAME OVER",align="center",font=FONT)