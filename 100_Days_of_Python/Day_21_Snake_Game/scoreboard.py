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
        with open("data.txt", 'r') as handle:
            self.high_score = int(handle.read())
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_score()

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", 'w') as handle: handle.write(str(self.high_score))
        self.score = 0

    def game_over(self):
        self.goto(-20, 0)
        self.write("GAME OVER.", align=ALIGNMENT, font=GAME_OVER_FONT)
