import os

def add(n1,n2):
    return n1+n2
def subtract(n1,n2):
    return n1-n2
def divide(n1,n2):
    return n1/n2
def multiply(n1,n2):
    return n1*n2
def powerOf(n1,n2):
    return n1**n2
def quotient(n1,n2):
    return n1//n2
def remainder(n1,n2):
    return n1%n2

operations= {
    "+":add,
    "-":subtract,
    "/":divide,
    "*":multiply,
    "**":powerOf,
    "//":quotient,
    "%":remainder,
}
def calculator():
    # from CalculatorArt import logo
    # print(logo)
    n1=float(input("n1: "))
    toEnd=False

    while not toEnd:
      # Something I've recently seen, but unsure how to use it yet. Seems succinct and cool
        print(" ".join(symbol for symbol in operations))
        instruction=input("Operation? ")
        operation=operations[instruction]
        n2=float(input("n2: "))
        result=operation(n1,n2)
        print(f"{n1} {instruction} {n2} = {result}")
        while True:
            condition=input(f"Type 'y' to continue calculating with {result}, or type 'n' to exit: ").lower()
            if condition == 'y':
                n1=result
                break
            elif condition == 'n':
                toEnd=True
                os.system("clear")
                # To recurse back, a running program like a real calculator
                # Looping program via recursion instead of while loops
                calculator()        
                break
            else: print("Type only y/n")

calculator()

######################################################################################################
# CalculatorArt.py
logo = """
 _____________________
|  _________________  |
| | Pythonista   0. | |  .----------------.  .----------------.  .----------------.  .----------------. 
| |_________________| | | .--------------. || .--------------. || .--------------. || .--------------. |
|  ___ ___ ___   ___  | | |     ______   | || |      __      | || |   _____      | || |     ______   | |
| | 7 | 8 | 9 | | + | | | |   .' ___  |  | || |     /  \     | || |  |_   _|     | || |   .' ___  |  | |
| |___|___|___| |___| | | |  / .'   \_|  | || |    / /\ \    | || |    | |       | || |  / .'   \_|  | |
| | 4 | 5 | 6 | | - | | | |  | |         | || |   / ____ \   | || |    | |   _   | || |  | |         | |
| |___|___|___| |___| | | |  \ `.___.'\  | || | _/ /    \ \_ | || |   _| |__/ |  | || |  \ `.___.'\  | |
| | 1 | 2 | 3 | | x | | | |   `._____.'  | || ||____|  |____|| || |  |________|  | || |   `._____.'  | |
| |___|___|___| |___| | | |              | || |              | || |              | || |              | |
| | . | 0 | = | | / | | | '--------------' || '--------------' || '--------------' || '--------------' |
| |___|___|___| |___| |  '----------------'  '----------------'  '----------------'  '----------------' 
|_____________________|
"""
