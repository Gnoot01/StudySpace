import random
ans=random.randint(1,100)
LIVES=10
GAMEEND=False

def decLives():
    # First time using globals, note global usage generally discouraged, should use return statements within func instead.
    global LIVES
    global GAMEEND
    LIVES-=1
    if LIVES==0:
        print("You've run out of guesses, you lose.")
        GAMEEND=True
    else: print("Guess again! ")

# from GuessTheNumberArt import logo
# print(logo)
print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.")
difficulty=input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
if difficulty=="hard":LIVES=5

print(f"Psttt the number is {ans}")

# Should use this instead - initializing then comparing in a while loop, then asking for input 
# instead of global GAMEEND/while int(input("Make a guess: "))!=ans
# guess = 0
# while guess != ans:
#   guess=int(input("Make a guess: "))

while not GAMEEND:
    print(f"You have {LIVES} attempts remaining to guess the number.")
    guess=int(input("Make a guess: "))
    assert 0<guess<101,"Please guess only between 1 and 100."
    if guess==ans:
        print(f"You got it! The answer was {ans}.")
        GAMEEND=True
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
