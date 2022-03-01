# This is not actually part of course projects, just an exercise
# But it seemed interesting, so I did it anyway :)

print("Welcome to the Love Calculator!")
name1 = input("What is your name? \n")
name2 = input("What is their name? \n")

TRUE_count=0
LOVE_count=0
for ch in name1:
    if ch in "TRUEtrue":TRUE_count+=1
for ch in name2:
    # A variation of the above
    if ch.upper() in "TRUE":TRUE_count+=1
for ch in name1:
    if ch in "LOVElove":LOVE_count+=1
for letter in "LOVE":
    # Another varation using .count(" ")
    LOVE_count+=name2.upper().count(letter)

# Alternatively, this would have been more succinct since
# calculator only evaluates no.of matches in both names
# 
# combinedNames=name1+name2
# for letter in "TRUE":
#     TRUE_count+=combinedNames.upper().count(letter)
# for letter in "LOVE":
#     LOVE_count+=combinedNames.upper().count(letter)
    

# Edge Case: 0 should not be at the start of the score if TRUE_count=0
if TRUE_count==0:
    score=str(LOVE_count)
else:
    score=int(str(TRUE_count)+str(LOVE_count))

if (score<=10) or (score>=90):
    print(f"Your score is {score}, you go together like coke and mentos.")
elif 40<=score<=50:
    print(f"Your score is {score}, you are alright together.")
else:
    print(f"Your score is {score}.")

# Guess the longer the name, the better the game! LOL!
