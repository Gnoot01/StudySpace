"""
SUTD's very own GPA Calculator, designed for Term 1 1D CTD 2022
Refer to
CTD1D_Description_F06_grpF for the Inspiration, Target Audience, Features and Enhancements
CTD1D_Documentation_F06_grpF for the in-depth Documentation
https://youtu.be/MHRz9V4ldvU for a Video Demonstration
CTD1D_Reflection_F06 for my Thoughts and Reflection
CTD1D_Presentation_F06_grpF for the Presentation to the examiners
"""

import os
import GPACalculator


def start(choice: str):
    """Starts the chosen program"""
    while True:

        if choice == "1":
            GPACalculator.introduce()
        else:
            print("Sorry, this feature is not implemented yet!")
            break


def boot_up():
    """Boots up the menu of options"""
    to_quit = False

    while not to_quit:
        print("Welcome to the SUTDent Life Calculator!\n"
              "Listed below are our programs\n"
              "**At any time, input q to quit**\n")
        programs = [
            "GPA Calculator",
            "Grad Requirement Calculator (Not Implemented)",
            "Professors (Not Implemented)",
            "Best places to sleep/hobo (Not Implemented)",
            "Hacks (Not Implemented)"
        ]
        for i, v in enumerate(programs, start=1):
            print(f"{i}: {v}")

        no_of_programs = len(programs)

        while True:

            try:
                choice = input(f"\nSo what would you like to explore? Input 1-{no_of_programs}: ").lower()
                assert int(choice) in range(1, no_of_programs + 1)
                start(choice)

            except ValueError:

                if choice == "q":
                    to_quit = True
                    # Windows:
                    # os.system("cls")
                    # Linux:
                    os.system("clear")
                    print("Hope you've had a pleasant experience!\n"
                          "Report any bugs to @")
                    break
                else:
                    print(f"Input only 1-{no_of_programs}\n")

            except AssertionError:
                print(f"Input only 1-{no_of_programs}\n")


if __name__ == "__main__":
    boot_up()