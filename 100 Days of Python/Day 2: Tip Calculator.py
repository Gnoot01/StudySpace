print("Welcome to the Tip Calculator!")
total = float(input("What was the total bill? $"))
tipInPercentage = float(input("What percentage tip would you like to give? "))
numOfPeople = int(input("How many people to split the bill? "))
totalWithTip = total + total*(tipInPercentage/100)
finalAmount = "{:.2f}".format(totalWithTip/numOfPeople)
print(type(finalAmount))
print(f"Each person should pay: ${finalAmount}")

# finalAmount = round(totalWithTip/numOfPeople,2)
# Would give 50.0 if there's not enough decimal places as specified. 
# Hence, use format which formats finalAmount into type:str, more suited to represent currency
