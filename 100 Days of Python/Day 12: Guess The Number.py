import random
ans=random.randint(1,100)
lives=10
gameEnd=False

def decLives():
    # First time using globals, note global usage generally discouraged, okay for simpler programs
    global lives
    global gameEnd
    lives-=1
    if lives==0:
        print("You've run out of guesses, you lose.")
        gameEnd=True
    else: print("Guess again! ")

# from GuessTheNumberArt import logo
# print(logo)
print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.")
difficulty=input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
if difficulty=="hard":lives=5

print(f"Psttt the number is {ans}")

while not gameEnd:
    print(f"You have {lives} attempts remaining to guess the number.")
    guess=int(input("Make a guess: "))
    assert 0<guess<101,"Please guess only between 1 and 100."
    if guess==ans:
        print(f"You got it! The answer was {ans}.")
        gameEnd=True
    elif guess<ans:
        print("Too low.")
        decLives()
    else:
        print("Too high.")
        decLives()


######################################################################################################
# GuessTheNumberArt.py
logo="""
  ________                                __  .__              _______               ___.                ._.
 /  _____/ __ __   ____   ______ ______ _/  |_|  |__   ____    \      \  __ __  _____\_ |__   ___________| |
/   \  ___|  |  \_/ __ \ /  ___//  ___/ \   __\  |  \_/ __ \   /   |   \|  |  \/     \| __ \_/ __ \_  __ \ |
\    \_\  \  |  /\  ___/ \___ \ \___ \   |  | |   Y  \  ___/  /    |    \  |  /  Y Y  \ \_\ \  ___/|  | \/\|
 \______  /____/  \___  >____  >____  >  |__| |___|  /\___  > \____|__  /____/|__|_|  /___  /\___  >__|   __
        \/            \/     \/     \/             \/     \/          \/            \/    \/     \/       \/
"""
