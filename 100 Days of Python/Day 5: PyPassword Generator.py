import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters= int(input("How many of 52 letters would you like?\n"))
assert 0<=nr_letters<=52
nr_numbers = int(input("How many of 10 numbers would you like?\n"))
assert 0<=nr_numbers<=10
nr_symbols = int(input("How many of 9 symbols would you like?\n"))
assert 0<=nr_symbols<=9

# Ez Level - Order not randomised:
# e.g. 4 letter, 2 symbol, 2 number = JduE&!91

password=""
count_letters=0
count_symbols=0
count_numbers=0
passwordList=[]
result=""
# Simpler: for char in range(1, nr_letters + 1):password+=random.choice(letters)
while count_letters<nr_letters:
    password+=letters[random.randint(0,nr_letters-1)]
    count_letters+=1
while count_symbols<nr_symbols:
    password+=symbols[random.randint(0,nr_symbols-1)]
    count_symbols+=1
while count_numbers<nr_numbers:
    password+=numbers[random.randint(0,nr_numbers-1)]
    count_numbers+=1

# Hard Level - Order of characters randomised:
# e.g. 4 letter, 2 symbol, 2 number = JE&d!9u1

# Simpler: random.shuffle(password_list)
for ch in password: passwordList+=ch
print(passwordList)
for i in range(0,len(password)):
    randomNum=random.randint(0,len(password)-1)
    passwordList[i],passwordList[randomNum]=passwordList[randomNum],passwordList[i]
for ch in passwordList:result+=ch
print(f"Your password is: {result}")
