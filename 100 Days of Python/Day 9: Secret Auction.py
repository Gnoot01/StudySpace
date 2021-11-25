from SecretAuctionArt import logo
print(logo)

import os
import random

bids={}
end=False
while not end:
    name=input("What is your name? ")
    price=float((input("What is your bid?: $")))
    bids[name]=price
    while True:
        condition=input("Are there any other bidders? y/n ").lower()
        if condition=="n":
            end=True
            break
        elif condition=="y":
            break
        else: print("Only y/n please! ")
    os.system("clear")

highestBid=0
highestBidder=""
bidContestants=[]
# Improvement: could have made def findWinner(): instead
# findWinner()
for bidder in bids:
    if bids[bidder]>highestBid:
        highestBid=bids[bidder]
        highestBidder=bidder
        bidContestants=[]
    elif bids[bidder]==highestBid:
        highestBid=bids[bidder]
        bidContestants.append(bidder)

if len(bidContestants)>0: highestBidder=random.choice(bidContestants)
print(f"The winner is {highestBidder} with a bid of ${'{:.2f}'.format(highestBid)}. Congrats!")

######################################################################################################
# SecretAuctionArt.py
logo = '''
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\\
                       .-------------.
                      /_______________\\
'''
