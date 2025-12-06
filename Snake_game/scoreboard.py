from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score=0
        with open("highscore.txt") as file:
            self.highscore=int(file.read())
        self.color("white")
        self.penup()
        self.goto(0,270)
        self.pendown()
        self.write(f"Score = {self.score}    Highscore = {self.highscore}",align="center",font=("Arial",15,"normal"))
        self.hideturtle()
    def update_score(self):
        self.clear()
        self.write(f"Score = {self.score}    Highscore = {self.highscore}",align="center",font=("Arial",15,"normal"))
        
    def game_over(self):
        if self.score>self.highscore:
            self.highscore=self.score
            with open("highscore.txt",mode="w") as file:
                file.write(f"{self.highscore}")
        self.score=0
        self.update_score()

    def increase_score(self):
        self.score+=1;
        self.update_score();