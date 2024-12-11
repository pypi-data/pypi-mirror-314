import unittest
from test_question_bank.test_question_loader import TestQuestionLoader
from test_question_bank.test_question_manager import TestQuestionManager
from test_do_quiz.test_quiz_session import TestQuizSession
from test_do_quiz.test_quiz_timer import TestQuizTimer


def test_suite1():
    suite1 = unittest.TestSuite()
    result1 = unittest.TestResult()
    suite1.addTest(TestQuestionLoader('test_category'))
    suite1.addTest(TestQuestionLoader('test_difficulty'))
    suite1.addTest(TestQuestionLoader('test_random_question'))
    suite1.addTest(TestQuestionManager('test_add_question'))
    suite1.addTest(TestQuestionManager('test_remove_question'))
    suite1.addTest(TestQuestionManager('test_update_question'))
    suite1.addTest(TestQuestionManager('test_get_question'))
    runner = unittest.TextTestRunner()
    print(runner.run(suite1))


def test_suite2():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(TestQuizSession('test_start_quiz'))
    suite.addTest(TestQuizSession('test_submit_answers'))
    suite.addTest(TestQuizSession('test_score_wrong_answer'))
    suite.addTest(TestQuizTimer('test_start_timer'))
    suite.addTest(TestQuizTimer('test_check_time_remaining'))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

test_suite1()
test_suite2()