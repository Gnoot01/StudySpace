import json
import os
import fnmatch


def introduce():
    """Introduces the GPA Calculator"""
    print("""
 _____________________
|  _________________  |
| | GPA Calculator! | |
| |_________________| |
|  __ __ __ __ __ __  |
| |__|__|__|__|__|__| |
| |__|__|__|__|__|__| |
| |__|__|__|__|__|__| |
| |__|__|__|__|__|__| |
| |__|__|__|__|__|__| |
| |__|__|__|__|__|__| |
|_____________________|
""")

    while True:

        try:
            calculate_or_edit = input("1. Calculate\n2. Edit\nyour GPA?: ")
            print("")
            assert int(calculate_or_edit) in [1, 2]

            if int(calculate_or_edit) == 1:
                calculate_func()
            else:
                edit_func()

        except ValueError:

            if calculate_or_edit == "q":
                print("")
                break
            else:
                print("Invalid! Input only integers\n")

        except AssertionError:
            print("Invalid! Input 1 or 2\n")
        except FileNotFoundError:
            print("No files found!")


def calculate_func():
    """Calculate mod/term"""

    while True:
        try:
            mod_or_term = input("1. Mod\n2. Term\nCalculate GPA for: ")
            assert int(mod_or_term) in [1, 2]

            while True:
                try:
                    term = input("From which term: ")
                    assert 1 <= int(term) <= 10

                    if int(mod_or_term) == 1:
                        while True:
                            # Only taking first word of user input
                            mod = input(f"Term {term}, input mod: ").lower().split(" ")[0]
                            print("")

                            if mod == "q":
                                print("")
                                break

                            get_term_mods(term, mod)
                    else:
                        while True:
                            try:
                                new_or_existing = input("\n1. New\n2. Use existing data\nCalculate: ")
                                assert int(new_or_existing) in [1, 2]

                                if int(new_or_existing) == 1:
                                    get_term_mods(term)
                                else:
                                    # Finding all mod files
                                    files = fnmatch.filter(os.listdir("Saved_Data"), "[!_]*.txt")
                                    with open("mods.json", mode="r") as f:
                                        content = json.loads(f.read())
                                        term_mods = content.get(term, None).keys()

                                    # If some mod files don't exist, prompt user to do those first
                                    if len(files) != len(term_mods):
                                        print("----------------------------------")
                                        print("No existing data found. Fill in the following mods first\n")
                                        # Eg. [term_1_math.txt,...]
                                        term_mod_filenames = [f"term_{term}_{term_mod.split(' | ')[1].lower()}.txt" for
                                                              term_mod in term_mods]
                                        for term_mod_filename in term_mod_filenames:
                                            if term_mod_filename not in files:
                                                get_term_mods(term, term_mod_filename.strip(".txt").split("_")[-1])

                                    term_grades_text = term
                                    current_term_credits = 0
                                    max_term_credits = 0
                                    for file in files:
                                        with open(f"Saved_Data/{file}", mode="r") as f:
                                            # Accessing files works as a pointer, so reading once through leaves pointer at last char
                                            # Hence f.read() again will read nth. Need to reset pointer or store file contents
                                            content = f.read()
                                            term_grades_text += f"\n\n{content}"
                                            credits_list = content.split("\n")[-1].split(": ")[1].strip("()").split(
                                                ", ")
                                            current_mod_credits, max_mod_credits = tuple(
                                                [float(credits_list[0]), int(credits_list[1])])
                                            current_term_credits += current_mod_credits
                                            max_term_credits += max_mod_credits
                                    save_data(f"Saved_Data/_term_{term}.txt", term_grades_text)
                                    print(
                                        f"Term GPA: {calculate_gpa(max_term_credits, current_credits=current_term_credits)[0]}")

                            except ValueError:
                                if new_or_existing == "q":
                                    print("")
                                    break
                                else:
                                    print("Invalid! Input only integers\n")
                            except AssertionError:
                                print("Invalid! Input 1 or 2\n")


                except ValueError:
                    if term == "q":
                        print("")
                        break
                    else:
                        print("Invalid! Input only integers\n")
                except AssertionError:
                    print("Invalid! Input 1-10\n")

        except ValueError:
            if mod_or_term == "q":
                print("")
                break
            else:
                print("Invalid! Input only integers\n")
        except AssertionError:
            print("Invalid! Input 1 or 2\n")


def edit_func():
    """Edit mod files"""
    files = fnmatch.filter(os.listdir("Saved_Data"), "*.txt")
    len_files = len(files)

    if len_files > 0:
        while True:
            try:
                print("We found the following files")
                # _term.txt files are not supposed to be visible to user to edit
                for i, v in enumerate(files, start=1):
                    print(f"{i}. {v.rstrip('.txt')}") if not v.startswith("_") else None

                file_choice = input("Input file to edit: ")
                assert int(file_choice) in list(range(1, len_files + 1))

                file_choice_name = files[int(file_choice) - 1]
                with open(f"Saved_Data/{file_choice_name}", mode="r+") as file:
                    # json.loads(file.read()) gives JSONDecodeError: Expecting value: line 1 column 1 (char 0)
                    # no matter type of utf-8/utf-8-sig encoding or load/dump/dumps even though legit json
                    grades_dict, credits = text_to_dict(file.read())
                    max_credits = int(credits.split(": ")[1].strip("()").split(", ")[1])
                    term_mod = list(grades_dict.keys())[0]
                    components = list(grades_dict.values())[0].items()
                    len_components = len(components)
                    display_components(term_mod, components, enumerated=True)

                    while True:
                        try:
                            component_choice = input("Input component to edit: ")
                            assert int(component_choice) in list(range(1, len_components + 1))

                            current_pct = 0
                            for i, (component, (grade, weightage)) in enumerate(components, start=1):

                                if i == int(component_choice):
                                    actual, weightage = calculate_component(component, weightage)
                                    grades_dict[term_mod][component] = actual, weightage
                                    current_pct += actual
                                else:
                                    current_pct += grade

                            print("\nSuccess!")
                            display_components(term_mod, components, enumerated=True)
                            # r+ allows read + write, but after reading, pointer is at last byte and writes from there
                            # Hence, seek to position 0, truncate to 0 bytes then write
                            file.seek(0)
                            file.truncate(0)
                            file.write(dict_to_text(
                                grades_dict) + f"\nCredits: ({calculate_gpa(max_credits, current_pct=current_pct)[1]}, {max_credits})")
                            # Force buffer storage to write to file immediately, if not won't write until exception (finish 1 while loop)
                            # https://stackoverflow.com/questions/7127075/what-exactly-is-file-flush-doing
                            file.flush()

                        except ValueError:
                            if component_choice == "q":
                                print("")
                                break
                            else:
                                print("Invalid! Input only integers\n")
                        except AssertionError:
                            print(f"Invalid! Input 1-{len_components}\n")

            except ValueError:
                if file_choice == "q":
                    print("")
                    break
                else:
                    print("Invalid! Input only integers\n")
            except AssertionError:
                print(f"Invalid! Input 1-{len_files}\n")

    else:
        # used at line 44
        raise FileNotFoundError


def get_term_mods(term: str, mod: str = None):
    """Retrieve mods from mods.json"""
    with open("mods.json", mode="r") as file:
        content = json.loads(file.read())
        term_mods = content.get(term, None)

        if term_mods is not None:

            if mod is not None:
                for term_mod, components in term_mods.items():
                    term_mod_split = [word.lower() for word in term_mod.split(" | ")]
                    # Checks if word is Eg. 10.013 | Math | any of Maths/Modelling/Analysis
                    if mod in term_mod_split[:2] or mod in term_mod_split[-1].split(" "):
                        display_components(term_mod, components, enumerated=False)
                        return calculate_mod(term, term_mod, components)

                print("\nMod does not exist! Please input again")

            else:
                print("----------------------------------")
                print(f"Term: {term}\n")
                for term_mod, components in term_mods.items():
                    display_components(term_mod, components, enumerated=False)
                return calculate_term(term, term_mods)

    return "Unable to find mod\n"


def calculate_component(component: str, weightage: int, remaining: int = None):
    """Calculate a component of a mod"""
    actual = 0
    # Only ones user can possibly know max score
    if component in ["Midterm", "Finals"]:
        actual_score = input_validated(f"Actual score for {component}: ", (0, 100))

        # if not "nil"
        if isinstance(actual_score, tuple):
            max_score = input_validated(f"Max score for {component}: ", (actual_score[1], 100))
            actual = round((actual_score[1] / max_score[1]) * weightage, 2)
        else:
            remaining += weightage

    elif component == "Class Participation":
        actual = give_survey(weightage)

    else:
        actual_score = input_validated(f"Actual/Estimated score for {component} out of a possible {weightage}%: ",
                                       (0, weightage))

        if isinstance(actual_score, tuple):
            actual = actual_score[1]
        else:
            remaining += weightage

    if remaining is None:
        return (actual, weightage)
    else:
        return (actual, weightage), remaining


def calculate_mod(term: str, term_mod: str, components: dict):
    """Calculating a mod (all components)"""
    while True:

        try:
            print("Answer accordingly. Input nil if it's not done or you do not know")
            mod_grades_dict = {}
            current_pct = 0
            remaining_pct = 0
            max_mod_credits = list(components.items())[0][1]
            target_pct = input_validated("Target % for the mod: ", (0, 100))[1]

            for component, weightage in list(components.items())[1:]:
                (actual, total), remaining = calculate_component(component, weightage, remaining_pct)
                mod_grades_dict[component] = (actual, total)
                current_pct += (actual / total) * weightage

            os.system("clear")

            print(f"For {term_mod}:\n")
            for k, v in mod_grades_dict.items():
                print(f"{k}: {v[0]}% out of {v[1]}%")

            # Report generated based on user's target and scores
            print(f"\nYour current percentage is {round(current_pct, 1)}%")
            if remaining > 0:
                required = (target_pct - current_pct) / remaining * 100
                if 0 < required <= 100:
                    print(
                        f"\nTo achieve {target_pct}%, you need to score {round(required, 1)}% on average for your remaining assignments")
                    print(advise(mod_grades_dict))
                elif required > 100:
                    print(f"\nSorry, it is impossible to achieve {target_pct}%, try harder next time!")
                    print(advise(mod_grades_dict))

            else:
                if current_pct < target_pct:
                    print("You did not meet your target :(\n")
                    print(advise(mod_grades_dict))
                else:
                    print("Congratulations! You met your target :)\n")

            current_mod_gpa, current_mod_credits, _ = calculate_gpa(max_mod_credits, current_pct=current_pct)
            print(f"Current mod gpa: {current_mod_gpa}")
            print("----------------------------------")

            file_name = term_mod.split(" | ")[1].lower()
            mod_grades_text = dict_to_text(
                {term_mod: mod_grades_dict}) + f"\nCredits: {(current_mod_credits, max_mod_credits)}"
            save_data(f"Saved_Data/term_{term}_{file_name}.txt", mod_grades_text)

            return mod_grades_text, current_mod_credits, max_mod_credits

        except TypeError:
            print("Invalid! Input only integers\n")


def calculate_term(term: str, term_mods: dict):
    """Calculating a term (all mods)"""
    term_grades_text = term
    current_term_credits = 0
    max_term_credits = 0

    for term_mod, components in term_mods.items():
        print(f"Term {term} Mod selected: \n{term_mod}\n")
        mod_grades_text, current_mod_credits, max_mod_credits = calculate_mod(term, term_mod, components)
        term_grades_text += "\n\n" + mod_grades_text
        current_term_credits += current_mod_credits
        max_term_credits += max_mod_credits

    save_data(f"Saved_Data/_term_{term}.txt", term_grades_text)
    print(f"Current term gpa: {(calculate_gpa(max_term_credits, current_credits=current_term_credits))[0]}\n")


def calculate_gpa(max_credits: int, current_pct: float = None, current_credits: float = None) -> tuple:
    """Calculating GPA based on current_pct or current_credits"""
    if current_credits is None:
        current_credits = round((current_pct / 100) * max_credits, 2)
    current_gpa = round((current_credits / max_credits) * 5.0, 2)
    return current_gpa, current_credits, max_credits


################################################ Helper functions ################################################
def input_validated(qn: str, bounds: tuple):
    """Checks if int & within bounds"""
    lower_bound, upper_bound = bounds

    while True:
        try:
            ans = input(qn)
            assert lower_bound <= float(ans) <= upper_bound
            return True, float(ans)

        except ValueError:
            if ans.lower() == "nil":
                return False
            else:
                print("Invalid! Input only numbers\n")
        except AssertionError:
            print(f"Invalid! Input {lower_bound}-{upper_bound}\n")


def give_survey(total_percentage: int) -> float:
    """Gives survey to estimate Class Participation"""
    score = 0
    print("\nOn a scale of 0-10, input")
    qns = [
        "How often you attend classes",
        "How often you ask or answer questions in class?",
        "How often you submit assignments on time",
        "How active you are during group discussions"
    ]
    for i, v in enumerate(qns, start=1):
        ans = input_validated(f"{i}. {v}: ", (0, 10))[1]
        score += ans

    # 32/40 = 4/5
    fraction = round(score / (10 * len(qns)), 1)
    # 80%
    percentage = 100 * fraction
    # 12%
    percentage_out_of_total = round(fraction * total_percentage, 1)
    print(
        f"Your class participation is {percentage}%, giving you {percentage_out_of_total}% out of a possible {total_percentage}%\n")

    return percentage_out_of_total


def advise(grades: dict) -> str:
    """Dynamically generate advice, from easy -> hard"""
    print("We've got some advice for you! Listed easy -> hard:")
    advice_list = []
    advice = ""

    class_part = grades.get("Class Participation", None)
    if class_part is not None and class_part[0] < class_part[1]:
        advice_list.append(
            f"Class Participation: {(class_part[0] / class_part[1]) * 100}%, try participating more in class!\n")

    homework_grades = grades.get("Homework", None)
    if homework_grades is not None and homework_grades[0] < homework_grades[1]:
        advice_list.append(
            f"Homework: {(homework_grades[0] / homework_grades[1]) * 100}%, brush up on your homework!\n")

    midterm = grades.get("Midterm", None)
    finals = grades.get("Finals", None)
    # Midterm and hence finals exists, midterm didn't do the best, so finals can do better
    if midterm is not None and midterm[0] < midterm[1] and finals[0] == 0:
        advice_list.append(
            f"Midterm: {round((midterm[0] / midterm[1]) * 100, 2)}%, study harder for your finals, you can do it!\n")

    grp_project_1D = grades.get("1D", None)
    grp_project_2D = grades.get("2D", None)
    # 1D and hence 2D exists, 1D didn't do the best, so 2D can do better
    if grp_project_1D is not None and grp_project_1D[0] < grp_project_1D[1] and grp_project_2D[0] == 0:
        advice_list.append(
            f"1D: {round((grp_project_1D[0] / grp_project_1D[1]) * 100, 2)}%, you can make up for it in your 2D!\n")

    for i, v in enumerate(advice_list, start=1):
        advice += f"{i}. {v}"

    return advice


def dict_to_text(grades_dict: dict) -> str:
    """Converts dict to text"""
    grades_text = ""
    k, v = list(grades_dict.keys())[0], list(grades_dict.values())[0]

    for component, grades in v.items():
        grades_text += component + ": " + str(grades) + "\n"

    grades_text = f"{k}\n{grades_text}".strip("\n")

    return grades_text


def text_to_dict(grades_text: str) -> dict:
    """Converts text to dict"""
    grades_list = grades_text.split("\n")
    k = grades_list[0]
    credits = grades_list[-1]
    grades_dict = {k: {}}

    for i in range(1, len(grades_list) - 1):
        component, value = grades_list[i].split(": ")
        value = value[1:-1]
        value = tuple(map(float, value.split(', ')))
        grades_dict[k][component] = value

    return grades_dict, credits


def display_components(term_mod: str, components: dict, enumerated: bool):
    """Displays components to user"""
    if enumerated:
        print(f"\nEditing: \n{term_mod}\nComponents: ")
        for i, (component, (grade, weightage)) in enumerate(components, start=1):
            print(f"{i}. {component}: {grade}% out of {weightage}%")
    else:
        print(f"Term Mod: \n{term_mod}\nComponents: ")
        component_items = list(components.items())
        _, the_rest = component_items[0], component_items[1:]
        for component, weightage in the_rest:
            print(f"{component}: {weightage}%")
        print("----------------------------------")


def save_data(file_name: str, grades_text: str):
    """Saves data to specified file"""
    with open(file_name, mode="w") as file:
        file.write(grades_text)