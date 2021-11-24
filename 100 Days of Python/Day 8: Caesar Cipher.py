from CaesarCipherArt import logo
print(logo)

def caesar(text, shift, instruction):
    result = ""
    if instruction=="decode": shift*=-1
    for ch in text:
        if ch not in alphabet: result+=ch
        #Simpler: else: result+=alphabet[(alphabet.index(ch)+shift)%26]
        for i in range(len(alphabet)):
            if ch == alphabet[i]:result+=alphabet[(i+shift)%26]
    print(f"The resulting text is {result}")

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
shouldEnd = False
while not shouldEnd:
    instruction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
    assert instruction=="encode" or instruction=="decode"
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    caesar(text, shift, instruction)
    restart = input("Type 'yes' if you want to go again. Otherwise type 'no'.\n").lower()
    assert restart=="yes" or restart=="no"
    if restart == "no":
        shouldEnd = True
        print("Goodbye")

######################################################################################################
# CaesarCipherArt.py
logo = """           
 ,adPPYba, ,adPPYYba,  ,adPPYba, ,adPPYba, ,adPPYYba, 8b,dPPYba,  
a8"     "" ""     `Y8 a8P_____88 I8[    "" ""     `Y8 88P'   "Y8  
8b         ,adPPPPP88 8PP"""""""  `"Y8ba,  ,adPPPPP88 88          
"8a,   ,aa 88,    ,88 "8b,   ,aa aa    ]8I 88,    ,88 88          
 `"Ybbd8"' `"8bbdP"Y8  `"Ybbd8"' `"YbbdP"' `"8bbdP"Y8 88   
            88             88                                 
           ""             88                                 
                          88                                 
 ,adPPYba, 88 8b,dPPYba,  88,dPPYba,   ,adPPYba, 8b,dPPYba,  
a8"     "" 88 88P'    "8a 88P'    "8a a8P_____88 88P'   "Y8  
8b         88 88       d8 88       88 8PP""""""" 88          
"8a,   ,aa 88 88b,   ,a8" 88       88 "8b,   ,aa 88          
 `"Ybbd8"' 88 88`YbbdP"'  88       88  `"Ybbd8"' 88          
              88                                             
              88           
"""
