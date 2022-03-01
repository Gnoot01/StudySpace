rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

import random
game=[rock,paper,scissors]
myChoice=game[int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors! >:)"))]
print("You chose:\n",myChoice)
computerChoice=game[random.randint(0,2)]
print("Computer chose:\n",computerChoice)
# I feel proud for having thought of the code below and generalising it rather than
# if I were to go thru each individual case :)
for i in range(3):
    if myChoice==game[i]:
        if computerChoice==game[(i+1)%3]:print("\nYou lose, noob!")
        elif computerChoice==game[(i+2)%3]:print("\nYou win, hero!")
        else:print("\nTie! One more?")
