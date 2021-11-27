from data import MENU, resources


def isEnough(coffee, resources):
    if enoughWater(coffee, resources) and enoughMilk(coffee, resources) and enoughCoffee(coffee, resources): return True
    return False


def enoughWater(coffee, resources):
    if resources["Water"] >= coffee["ingredients"]["Water"]: return True
    print("Sorry there is not enough water.")
    return False


def enoughMilk(coffee, resources):
    if resources["Milk"] >= coffee["ingredients"]["Milk"]: return True
    print("Sorry there is not enough milk.")
    return False


def enoughCoffee(coffee, resources):
    if resources["Coffee"] >= coffee["ingredients"]["Coffee"]: return True
    print("Sorry there is not enough coffee.")
    return False


def calculate(noOfQuarters, noOfDimes, noOfNickles, noOfPennies):
    quartersValue = 0.25
    dimesValue = 0.10
    nicklesValue = 0.05
    penniesValue = 0.01
    return noOfQuarters*quartersValue + noOfDimes*dimesValue + noOfNickles*nicklesValue + noOfPennies*penniesValue


def formattedMoney(money):
    return "{:.2f}".format(money)


def makeCoffee(coffee, resources):
    resources["Water"] -= coffee["Water"]
    resources["Milk"] -= coffee["Milk"]
    resources["Coffee"] -= coffee["Coffee"]


def start():
    isOn = True

    money = 0

    while isOn:
        isContinue = True
        choice = input("What would you like? (espresso ($1.50) /latte($2.50)/ cappuccino($3.00)): ").lower()
        if choice == "off":
            isContinue = False
            isOn = False
        elif choice == "report":
            print(f"Water: {resources['Water']}ml\nMilk: {resources['Milk']}ml\nCoffee: {resources['Coffee']}g\nMoney: ${formattedMoney(money)}")
        while isContinue:
            if choice in MENU:
                if isEnough(MENU[choice], resources):
                    print("Please insert coins.")
                    noOfQuarters = int(input("How many quarters($0.25)?: "))
                    assert noOfQuarters >= 0, "No hacking!"
                    noOfDimes = int(input("How many dimes?($0.10): "))
                    assert noOfDimes >= 0, "No hacking!"
                    noOfNickles = int(input("How many nickles?($0.05): "))
                    assert noOfNickles >= 0, "No hacking!"
                    noOfPennies = int(input("How many pennies?($0.01): "))
                    assert noOfPennies >= 0, "No hacking!"
                    totalPaid = calculate(noOfQuarters, noOfDimes, noOfNickles, noOfPennies)
                    if totalPaid >= MENU[choice]["cost"]:
                        money += MENU[choice]["cost"]
                        makeCoffee(MENU[choice]["ingredients"], resources)
                        print(f"Here is ${formattedMoney(totalPaid-MENU[choice]['cost'])} in change.")
                        print(f"Here is your {choice} ☕. Enjoy!")
                        isContinue = False
                    else:
                         print("Sorry, that's not enough money. Money refunded. ")
                         isContinue = False
                else: isContinue = False
            else:
                print("Please enter a valid response")
                isContinue = False


start()

