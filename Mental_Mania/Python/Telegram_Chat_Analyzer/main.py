"""
"pip install chromedriver-autoinstaller" for up-to-date selenium chromedriver, installed in C:\Program Files\Google\Chrome\Application

"import nltk" + "nltk.download("stopwords")" for Natural Language Toolkit (NLTK) stop words (common meaningless words)
Can go to ...\venv\Lib\site-packages\nltk\data.py to edit "SEARCH PATH" if want to move stopwords from downloaded location

Enhancement: Can be converted to Data Analysis Project by simply integrating matplotlib
             Replace emoji/emoticons w meaningful text: https://medium.com/geekculture/text-preprocessing-how-to-handle-emoji-emoticon-641bbfa6e9e7
Issues: Untested with > 2 users (group chat)
"""

import os
import fnmatch
import json
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from collections import OrderedDict
from nltk.corpus import stopwords

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
MSGS_FOLDER = "..."
# All files and folders: len(os.listdir(r'C:\Users\Andrew\Desktop\ChatExport_2022-05-29'))
# All files: len(next(os.walk(r'C:\Users\Andrew\Desktop\ChatExport_2022-05-29'))[2])
# Super fast, all files matching extension only
FILES = fnmatch.filter(os.listdir(MSGS_FOLDER), '*.html')
# can be edited in nltk_data\corpora\stopwords\english
STOP_WORDS = set(stopwords.words("english"))
MEANINGLESS_WORDS = ["v", "s", "t", "ll", "d", "am", "m", "im", "o", "re", "ve", "y", "ma", "mma", "u", "r", "re",
                     "you", "we", "my", "me", "i", "la", "no", "not", "so", "in", "on", "out", "up", "to", "of", "at",
                     "by", "as", "or", "if", "a", "an", "the", "do", "be", "is", "it", "its", "she", "her", "his", "him", "he",
                     "ur", "ud", "ull"]
THRESHOLD_TO_DELETE = 5


def init_users_and_word_count():
    ALL_USERS = get_all_users()
    word_count = {}
    for user in ALL_USERS: word_count[user] = {}

    return word_count, ALL_USERS


def get_all_users() -> list:
    prev_users = []
    all_users = []
    for file in FILES:
        driver.get(MSGS_FOLDER + f"/{file}")
        # 21 is arbitrary number to sieve out @users displaying as users Eg. 'AktiveSGBot 02.05.2022 00:28:17'. Enough to accommodate the average full name.
        current_users = list(set((name.text for name in driver.find_elements("css selector", ".from_name") if len(name.text) < 21)))
        if prev_users != current_users:
            all_users = list(set(all_users + prev_users + current_users))
            prev_users = current_users
    return all_users


def tally_word_count(driver, user, word_count, a):
    try:
        msg = driver.find_element("css selector", f"#message{a} .text").text
        for key in word_count.keys():
            if key == user:
                bracketed_phrase = ""
                bracketed_phrase_count = 0
                for word in msg.split(" "):
                    # from nltk.stem.porter import PorterStemmer + ps = PorterStemmer() + ps.stem(word)
                    # Conjugations Eg. loved/ing -> love. But what happens to emoji/emoticons?
                    word = word.lower().rstrip("!?$%^.,").replace(r"\n", "").replace("’", "").replace("'", "")
                    if "(" in word:
                        # Accounting for the case with multiple bracketed phrases in 1 msg
                        num_bracketed_phrases = len(msg.split("(")) - 1
                        if num_bracketed_phrases > 1 and num_bracketed_phrases > bracketed_phrase_count:
                            bracketed_phrase = msg.split("(")[bracketed_phrase_count + 1].split(")")[0]
                            bracketed_phrase_count += 1
                        else: bracketed_phrase = msg.split("(")[num_bracketed_phrases].split(")")[0]
                        word = "(" + bracketed_phrase + ")"
                    if word.replace(")", "") not in bracketed_phrase:
                        word_count[user][word] = word_count[user].get(word, 0) + 1
        a += 1
    except NoSuchElementException:
        a += 1
    return word_count, a


word_count, users = init_users_and_word_count()
for file in FILES:
    driver.get(MSGS_FOLDER + f"/{file}")
    # Getting first and last element ids
    a = int(driver.find_element("css selector", ".page_body .default").get_attribute("id").replace("message", ""))
    z = int(driver.find_elements("css selector", ".page_body .default")[-1].get_attribute("id").replace("message", ""))
    while True:
        try:
            user = driver.find_element("css selector", f"#message{a} .from_name").text
            word_count, a = tally_word_count(driver, user, word_count, a)
        except NoSuchElementException:
            word_count, a = tally_word_count(driver, user, word_count, a)
        if a > z: break

for user in users:
    # need .copy() to iterate & change-on-the-fly if not RuntimeError: dictionary changed size during iteration
    for word in word_count[user].copy():
        if word in MEANINGLESS_WORDS:
            word_count[user].pop(word, None)
        else:
            for stop_word in STOP_WORDS:
                if word.startswith(stop_word):
                    word_count[user].pop(word, None)
    # Specific to this project
    word_count[user]["big brain"] = min(word_count[user].pop("big", None), word_count[user].pop("brain", None))

    # From all msgs accumulated over a period of time, deletes if that word appears < 5 times
    for word in word_count[user].copy():
        if word_count[user][word] < THRESHOLD_TO_DELETE: word_count[user].pop(word, None)

    # sorted ALW returns a list. OrderedDict returns a dict with preserved order after sorting.
    # .items() returns tuple of (k, v). Within this tuple, key[1] returns v to sort by, X word_count[user][key]!
    word_count[user] = OrderedDict(sorted(word_count[user].items(), key=lambda key: key[1], reverse=True))

# NEED BOTH encoding="utf-8" & ensure_ascii=False to force UNICODE-representation (i'm instead of i\u2019m)
with open("word_count.json", "w", encoding="utf-8") as handler: json.dump(word_count, handler, indent=2, ensure_ascii=False)

driver.quit()
