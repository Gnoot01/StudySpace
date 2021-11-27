from art import logo
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
 
