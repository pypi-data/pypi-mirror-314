class InvalidAnswerError(Exception):
    """
    Exception for invalid answers.
    """
    
    def __init__(self, info):
        self.info = info
        super().__init__(self.info)

class QuizSession:
    def __init__(self):
        self.score = 0
        self.questions = []
        self.current_question_index = 0
        self.wrong_answers = []  

    def start_quiz(self, questions):
        self.questions = questions
        self.score = 0
        self.current_question_index = 0
        self.wrong_answers = []  # reset the wrong answer list

    def submit_answer(self, answer):
        try:
            valid_answers = {'A', 'B', 'C', 'D'}
            if answer not in valid_answers:
                raise InvalidAnswerError('You can only input A, B, C, D')
            question = self.questions[self.current_question_index]
            if answer == question["answer"]:
                self.score += 1  
            else:
                # save information of wrong quesions
                wr_question = question # make a copy
                wr_question['users_answer'] = answer
                self.wrong_answers.append(wr_question)
            self.current_question_index += 1
        except InvalidAnswerError as error1:
            print('Error: {}'.format(error1.info))
        
    def end_quiz(self):
        total_score = self.score # show the final score to user
        return "Score you got is: {}.\n".format(total_score)

    def get_wrong_answers(self):
        output = ['------ Questions your answered wrong ------']
        for answer in self.wrong_answers:
            output.append('Question {}'.format(answer['id']))
            output.append(answer['text'])
            output.append('Category: {}'.format(answer['category']))
            output.append('Difficulty: {}'.format(answer['difficulty']))
            output.append('Answer: {}'.format(answer['answer']))
            output.append('Your answer: {}'.format(answer['users_answer']))
        output.append('------ Above are all ------')
        output.append('Good luck for next time!')
        return '\n'.join(output)
