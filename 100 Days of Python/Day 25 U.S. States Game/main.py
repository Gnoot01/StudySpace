# Idea: can make a country-naming game using country_map.gif (to help me memorize where each country is) & slowly progress to knowing continents, etc
# just need to set up x,y coords

import turtle
import pandas

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

guessed_correct = []
data = pandas.read_csv("50_states.csv")
states = list(data.state)

while len(guessed_correct) < 50:
    answer = screen.textinput(title=f"{len(guessed_correct)}/50 States Correct", prompt="What's another state's name?").title()

    if answer == "Exit":
        not_guessed = [state for state in states if state not in guessed_correct]
        pandas.DataFrame(not_guessed).to_csv("states_to_learn.csv")
        break
    if answer in states:
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_row = data[data.state == answer]
        t.goto(int(state_row.x), int(state_row.y))
        t.write(answer)
        guessed_correct.append(answer)




# to get coords of mouse click on states
# def get_mouse_click_coords(x, y):
#     print(x, y)
# turtle.onscreenclick(get_mouse_click_coords)

turtle.mainloop()
# screen.exitonclick() cannot be used as need to get coordinates by clicking on screen, but this makes screen exit on click

 
