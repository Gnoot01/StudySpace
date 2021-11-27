from data import data
import random
from art import logo, vs
import os

def getRandom():
  return random.choice(data)

def fetchData(account):
  name = account["name"]
  description = account["description"]
  country = account["country"]
  # print(f'{name}: {account["follower_count"]}')
  return f"{name}, a {description}, from {country}"

def check(guess, followerCountA, followerCountB):
  if followerCountA > followerCountB:return guess == "a"
  else:return guess == "b"


def game():
  print(logo)
  score = 0
  gameEnd = False
  accountA = getRandom()
  accountB = getRandom()

  while not gameEnd:
    '''
FAQ: Why does choice B always become choice A in every round, even when A had more followers? 
Suppose you just started the game and you are comparing the followers of A - Instagram (364k) to B - 
Selena Gomez (174k). Instagram has more followers, so choice A is correct. However, the subsequent comparison
should be between Selena Gomez (the new A) and someone else. The reason is that everything in our list has 
fewer followers than Instagram. If we were to keep Instagram as part of the comparison (as choice A) then 
Instagram would stay there for the rest of the game. This would be quite boring. By swapping choice B for A 
each round, we avoid a situation where the number of followers of choice A keeps going up over the course of 
the game. Hope that makes sense!
Also, simulates scrolling in a sense
    '''
    accountA = accountB
    accountB = getRandom()
    # Edge Case if accountA happens to == accountB
    while accountA == accountB: accountB = getRandom()

    print(f"Compare A: {fetchData(accountA)}.")
    print(vs)
    print(f"Against B: {fetchData(accountB)}.")
    
    guess = input("Who has more followers? Type 'a' or 'b': ").lower()
    followerCountA = accountA["follower_count"]
    followerCountB = accountB["follower_count"]
    correct = check(guess, followerCountA, followerCountB)

    os.system("clear")
    print(logo)
    if correct:
      score += 1
      print(f"You're right! Current score: {score}.")
    else:
      gameEnd = True
      print(f"Sorry, that's wrong. Final score: {score}")

game()
