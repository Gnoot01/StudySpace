import html


class QuizBrain:
    def __init__(self, questions_list):
        self.question_number = 0
        self.score = 0
        self.questions_list = questions_list

    def check_answer(self, current_question_set, user_answer):
        if user_answer == current_question_set.answer:
            self.question_number += 1
            self.score += 1
            print("You got it right!")
        else:
            self.question_number += 1
            print("You got it wrong!")
        print(f"The correct answer was: {current_question_set.answer}.\nYour current score is: {self.score}/{self.question_number}.\n")

    def get_questions(self):
        current_question_set = self.questions_list[self.question_number]
        user_answer = input(f"Q{self.question_number+1}: {html.unescape(current_question_set.text)} ([T]rue/[F]alse: ").upper()
        # ALWAYS need to use self. ... if referencing an attribute/method within the same class!
        self.check_answer(current_question_set, user_answer)

    def still_has_questions(self):
        return self.question_number < len(self.questions_list)

    def end(self):
        print("You've completed the quiz")
        print(f"Your final score was {self.score}/{self.question_number}")

