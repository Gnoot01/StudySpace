from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Ariel", 20, "bold")
GAME_OVER_FONT = ("Ariel", 30)

class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.penup()
        self.goto(0, 360)
        self.score = 0
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.clear()
        self.score += 1
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(-20, 0)
        self.write("GAME OVER.", align=ALIGNMENT, font=GAME_OVER_FONT)