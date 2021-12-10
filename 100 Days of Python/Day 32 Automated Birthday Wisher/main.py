##################### Extra Hard Starting Project ######################
# 1. Update the birthdays.csv
# 2. Check if today matches a birthday in the birthdays.csv
# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
# 4. Send the letter generated in step 3 to that person's email address.
# Own 5: calculate age
# Own 6: vary emails, hence email hosts, hence SMTP_INFO

# To automate this & check for birthday date everyday, need to run in cloud.
# Pythonanywhere>Sign up>Files(Upload Files)> To run once: Consoles(Bash>python3 main.py) / To run daily: Tasks(run python3 main.py at time)

import random
import datetime
import smtplib
import pandas

letter_templates = ["./letter_templates/letter_1.txt", "./letter_templates/letter_2.txt", "./letter_templates/letter_3.txt"]
NOW_YEAR = datetime.datetime.now().year
NOW_MONTH = datetime.datetime.now().month
NOW_DAY = datetime.datetime.now().day

SMTP_INFO = ["smtp.gmail.com", "smtp.mail.yahoo.com", "smtp.live.com", "outlook.office365.com"]
email_addrs = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
my_email = "testestpython@gmail.com"
password = "abcd1234()"

data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(row.month, row.day): row for index, row in data.iterrows()}


def get_smtp_info(receiving_email):
    for addrs in email_addrs:
        if addrs in receiving_email:
            return SMTP_INFO[email_addrs.index(addrs)]


if (NOW_MONTH, NOW_DAY) in birthdays_dict:
    name = birthdays_dict[(NOW_MONTH, NOW_DAY)][0]
    age = NOW_YEAR - birthdays_dict[(NOW_MONTH, NOW_DAY)][2]
    with open(random.choice(letter_templates), "r") as handle:
        content = handle.read()
        content = content.replace("[NAME]", name)
        content = content.replace("[AGE]", f"{age}th")

    receiving_email = birthdays_dict[(NOW_MONTH, NOW_DAY)][1]
    with smtplib.SMTP(get_smtp_info(receiving_email)) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=receiving_email,
            msg=f"Subject:Happy Birthday! \n\n{content}")


 

