starting_letter = "./Input/Letters/starting_letter.txt"
with open(starting_letter, "r") as handle:
    starting_letter_text_list = handle.readlines()

invited_names = "./Input/Names/invited_names.txt"
with open(invited_names, "r") as handle:
    names_list = handle.readlines()

ready_to_send_directory_list = []
for name in names_list:
    ready_to_send_directory_list.append(f"./Output/ReadyToSend/letter_for_{name.strip()}.txt")

counter = 0
for letter in ready_to_send_directory_list:
    actual_content_list = []
    with open(letter, "w") as handle:
        actual_content_list.append(starting_letter_text_list[0].replace("[name]", f"{names_list[counter].strip()}"))
        for text in starting_letter_text_list[1:]: actual_content_list.append(text)
        for actual_content in actual_content_list: handle.write(actual_content)
        counter += 1


# Solution:
with open("./Input/Names/invited_names.txt") as names_file:
    names = names_file.readlines()

with open("./Input/Letters/starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()
    for name in names:
        new_letter = letter_contents.replace("[name]", name.strip())
        with open(f"./Output/ReadyToSend/letter_for_{name.strip()}.txt", mode="w") as completed_letter:
            completed_letter.write(new_letter)

