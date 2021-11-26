#Difficulty Normal 😎: Use all Hints below to complete the project.
#Difficulty Hard 🤔: Use only Hints 1, 2, 3 to complete the project.
#Difficulty Extra Hard 😭: Only use Hints 1 & 2 to complete the project.
#Difficulty Expert 🤯: Only use Hint 1 to complete the project.        DONE!

############### Our Blackjack House Rules #####################

## The deck is unlimited in size. 
## There are no jokers. 
## The Jack/Queen/King all count as 10.
## The Ace can count as 11 or 1.
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.

## Suggestion 1: make only 4 decks, removed as drawn                    DONE!
## Suggestion 2: special conditions to win: 5 cards<=21 -> win          DONE!
## Suggestion 3: Add currency (risk!)                                   DONE!

# Learning points:
# List of dicts are useful
# "{:.2f}".format(var) OR format(var,"{:.2f}")
# For anything to save Eg. BTC, need to use arrays/list/tuple/dict due to scope.
# Unlike java, main is not directly specified, so anything outside naturally is global
# Looping via recursion instead of while loops, dict.get(...,...), del dict[key]
# while input("...")=="y": to while-loop inputs without assigning to variable / catch 21 conundrum (Day 9)

import random

BTC={
    "dealerBTC":1000,
    "yourBTC":0.2,
    }

# 
def play():
    deck=["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]*4
    yourCards=[{"score":0,},{},{"count":0}]
    dealerCards=[{"score":0,},{},{"count":0}]
    gameEnd=False

    def getValue(card):
        if card in "2345678910":return int(card)
        elif card in "JQK":return 10
        else:return 11

    def youDraw(yourCards):
        yourDraw=random.choice(deck)
        deck.remove(yourDraw)
        yourCards[2]['count']+=1
        yourCards[1][yourDraw]=yourCards[1].get(yourDraw,0)+1
        yourCards[0]['score']+=getValue(yourDraw)
        print(f"You drew a {yourDraw}")

    def dealerDraws(dealerCards):
        dealerDraw=random.choice(deck)
        deck.remove(dealerDraw)
        dealerCards[2]['count']+=1
        dealerCards[1][dealerDraw]=dealerCards[1].get(dealerDraw,0)+1
        dealerCards[0]['score']+=getValue(dealerDraw)
        print(f"Dealer drew a {dealerDraw}")

    def yourMoves():
        """While you type 'y', before passing over the turn to dealer"""
        if yourCards[0]['score']==21:
            prntFinal(yourCards,dealerCards)
            print("You win!", winMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
            endRound()
        elif yourCards[0]['score']>21:
            # Need to figure out how to better implement this... since I used a dictionary to store
            if "A" in yourCards[1]:
                del yourCards[1]["A"]
                yourCards[1]["tempA"]=yourCards[1].get("tempA",0)+1
                yourCards[0]['score']-=10
                yourMoves()
            else:
                prntFinal(yourCards,dealerCards)
                print("You bust!", lossMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
                endRound()
        elif yourCards[0]['score']<21 and yourCards[2]['count']>=5:
            prntFinal(yourCards,dealerCards)
            print("You win by number of cards!", winMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
            endRound()
        else:prntCurrent(yourCards,dealerCards)

    def dealerMoves():
        """After passing the turn to dealer"""
        while dealerCards[0]['score']<17: dealerDraws(dealerCards)
        if dealerCards[0]['score']==21:
            prntFinal(yourCards,dealerCards)
            print("You lose!",lossMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
            endRound()
        elif dealerCards[0]['score']>21:
            if "A" in dealerCards[1]:
                del dealerCards[1]["A"]
                dealerCards[1]["tempA"]=dealerCards[1].get("tempA",0)+1
                dealerCards[0]['score']-=10
                dealerMoves()
            else:
                prntFinal(yourCards,dealerCards)
                print("Dealer bust!", winMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
                endRound()
        elif dealerCards[0]['score']<21 and dealerCards[2]['count']>=5:
            prntFinal(yourCards,dealerCards)
            print("Dealer wins by number of cards!", lossMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
            endRound()
        else:
            evaluateScores(dealerCards[0]['score'],yourCards[0]['score'])
            endRound()

    def prntCurrent(yourCards,dealerCards):
        print()
        print(f"Your hand: {yourCards[1]}, current score: {yourCards[0]['score']}")
        print(f"Dealer's first card: {dealerCards[1]}, current score: {dealerCards[0]['score']}")

    def prntFinal(yourCards,dealerCards):
        if "tempA" in yourCards[1]:
            yourCards[1]["A"]=yourCards[1]["tempA"]
            del yourCards[1]["tempA"]
        if "tempA" in dealerCards[1]:
            dealerCards[1]["A"]=dealerCards[1]["tempA"]
            del dealerCards[1]["tempA"]
        print()
        print(f"Your final hand: {yourCards[1]}, final score: {yourCards[0]['score']}")
        print(f"Dealer's final hand: {dealerCards[1]}, final score: {dealerCards[0]['score']}")

    def evaluateScores(dealerScore,yourScore):
        """After you & the dealer have made moves, and above written conditions didn't trigger"""
        if dealerScore>yourScore:
            prntFinal(yourCards,dealerCards)
            print("Dealer has higher score.",lossMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
            
        elif dealerScore==yourScore:
            prntFinal(yourCards,dealerCards)
            print("Tie, no one wins!")
            print(f"You've {BTC['yourBTC']} BTC(${format((amountInFiat(BTC['yourBTC'])),'.2f')}) left.\n")
        else:
            prntFinal(yourCards,dealerCards)
            print("You have higher score.",winMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
            
    def winMessage(betAmountInBtc,dealerBTC,yourBTC):
        BTC['dealerBTC']-=betAmountInBtc
        BTC['yourBTC']+=betAmountInBtc
        return f"You've won {betAmountInBtc} BTC(${format((amountInFiat(betAmountInBtc)),'.2f')})! :)\nYou've {BTC['yourBTC']} BTC(${format((amountInFiat(BTC['yourBTC'])),'.2f')}) left.\n"

    def lossMessage(betAmountInBtc,dealerBTC,yourBTC):
        BTC['dealerBTC']+=betAmountInBtc
        BTC['yourBTC']-=betAmountInBtc
        return f"You've lost {betAmountInBtc} BTC(${format((amountInFiat(betAmountInBtc)),'.2f')})! :(\nYou've {BTC['yourBTC']} BTC(${format((amountInFiat(BTC['yourBTC'])),'.2f')}) left.\n"

    def amountInFiat(amountInBtc):
        return amountInBtc*56000

    def endRound():
        gameEnd=True
        play()




    # from BJArt import logo
    # print(logo)
    if input("Do you want to play a game of BlackJack? Type 'y' or 'n': ").lower()=="y":
        print(f"You've {BTC['yourBTC']} BTC(${format((amountInFiat(BTC['yourBTC'])),'.2f')}).")
        betAmountInBtc=float(input("How lucky are we feelin'? Bet in BTC: "))
        assert 0<betAmountInBtc<=BTC['yourBTC']
        # Note: I should learn to extract actual real-time value of BTC in future.
        # Shorts just skyrocketed, BTC's struggling to keep above 56k as of now. 
        print(f"Wow, going big are we? Betting: {betAmountInBtc} BTC(${format((amountInFiat(betAmountInBtc)),'.2f')}).\n")

        for _ in range(2): youDraw(yourCards)
        dealerDraws(dealerCards)
        prntCurrent(yourCards,dealerCards)
        if yourCards[0]['score']==21: 
            print("My my! BlackJack!", winMessage(betAmountInBtc,BTC['dealerBTC'],BTC['yourBTC']))
            endRound()

        while not gameEnd:
            while input("Type 'y' to draw another card, type 'n' to pass: ")=="y":
                youDraw(yourCards)
                yourMoves()
                        
            # Dealer has to draw a card under 17
            dealerMoves()
            break

play()





##################### Hints #####################

#Hint 1: Go to this website and try out the Blackjack game: 
#   https://games.washingtonpost.com/games/blackjack/
#Then try out the completed Blackjack project here: 
#   http://blackjack-final.appbrewery.repl.run

#Hint 2: Read this breakdown of program requirements: 
#   http://listmoz.com/view/6h34DJpvJBFVRlZfJvxF
#Then try to create your own flowchart for the program.

#Hint 3: Download and read this flow chart I've created: 
#   https://drive.google.com/uc?export=download&id=1rDkiHCrhaf9eX7u7yjM1qwSuyEk-rPnt

#Hint 4: Create a deal_card() function that uses the List below to *return* a random card.
#11 is the Ace.
#cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

#Hint 5: Deal the user and computer 2 cards each using deal_card() and append().
#user_cards = []
#computer_cards = []

#Hint 6: Create a function called calculate_score() that takes a List of cards as input 
#and returns the score. 
#Look up the sum() function to help you do this.

#Hint 7: Inside calculate_score() check for a blackjack (a hand with only 2 cards: ace + 10) and return 0 instead of the actual score. 0 will represent a blackjack in our game.

#Hint 8: Inside calculate_score() check for an 11 (ace). If the score is already over 21, remove the 11 and replace it with a 1. You might need to look up append() and remove().

#Hint 9: Call calculate_score(). If the computer or the user has a blackjack (0) or if the user's score is over 21, then the game ends.

#Hint 10: If the game has not ended, ask the user if they want to draw another card. If yes, then use the deal_card() function to add another card to the user_cards List. If no, then the game has ended.

#Hint 11: The score will need to be rechecked with every new card drawn and the checks in Hint 9 need to be repeated until the game ends.

#Hint 12: Once the user is done, it's time to let the computer play. The computer should keep drawing cards as long as it has a score less than 17.

#Hint 13: Create a function called compare() and pass in the user_score and computer_score. If the computer and user both have the same score, then it's a draw. If the computer has a blackjack (0), then the user loses. If the user has a blackjack (0), then the user wins. If the user_score is over 21, then the user loses. If the computer_score is over 21, then the computer loses. If none of the above, then the player with the highest score wins.

#Hint 14: Ask the user if they want to restart the game. If they answer yes, clear the console and start a new game of blackjack and show the logo from art.py.


######################################################################################################
# BJArt.py
logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""
