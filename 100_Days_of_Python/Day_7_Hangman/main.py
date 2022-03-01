import random
from data import word_list

chosen_word = random.choice(word_list)
wordLength = len(chosen_word)

gameEnded = False
lives = 6

from art import logo
print(logo)

#Testing code
print(f'Pssst, the solution is {chosen_word}.')

display = []
for _ in range(wordLength):display += "_"

while not gameEnded:
    guess = input("Guess a letter: ").lower()
    
    if guess in display:print(f"You've already guessed {guess}")

    # Check guessed letter
    for i in range(wordLength):
        if  chosen_word[i]==guess: display[i] = guess

    #Check if user is wrong.
    if guess not in chosen_word:
        print(f"You guessed {guess}, that's not in the word. You lose a life.")
        lives -= 1
        if lives == 0:
            gameEnded = True
            print("You lose!")

    #Join all the elements in the list and turn it into a String.
    print(f"{' '.join(display)}")

    #Check if user has got all letters.
    if "_" not in display:
        gameEnded = True
        print("You win!")

    from art import stages
    print(stages[lives])
 
