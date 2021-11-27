from question_model import Question
from data import question_data
# This is quite nice, I thought I needed web scraping knowledge first to get data like this, but apparently I could just
# get them from https://opentdb.com/api_config.php for a trivia DB! Nice! I can actually play this :)
from quiz_brain import QuizBrain

question_bank = []
for question_set in question_data:
    question_bank.append(Question(question_set["question"], question_set["correct_answer"]))

quiz = QuizBrain(question_bank)

while quiz.still_has_questions(): quiz.get_questions()
quiz.end()
 

