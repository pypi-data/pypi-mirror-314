import csv
import json
from collections import defaultdict
from random import sample

from quizzing.question_bank.question_manager import questionmanager

class questionloader:
    """
    Handles loading, classifying, and analyzing quiz questions.
    """
    def __init__(self, manager = questionmanager):
        self.manager = manager

    def load_questions_from_file(self, filepath):
        """
        Load questions from a JSON or CSV file.

        Parameters:
            filepath (str): The file path to the JSON or CSV file.

        Returns:
            list[dict]: A list of question dictionaries.
        """
        try:
            if filepath.endswith(".json"):
                with open(filepath, "r") as file:
                    questions = json.load(file)
            elif filepath.endswith(".csv"):
                with open(filepath, "r", encoding='ISO-8859–1') as file:
                    reader = csv.DictReader(file)
                    questions = [row for row in reader]
            else:
                raise ValueError("Unsupported file format. Use JSON or CSV.")

            for question in questions:
                self.manager.add_question(question)

            return questions

        except (json.JSONDecodeError, csv.Error) as e:
            print('Error parsing JSON or CSV file.')


    def classify_questions_by_category(self, questions):
        """
        Classify questions by category and calculate stats.

        Parameters:
            questions (list[dict]): A list of question dictionaries.

        Returns:
            dict: {
                "classification": Questions grouped by category,
                "stats": Counts of questions per category.
            }
        """
        classification = defaultdict(list)
        for question in questions:
            category = question.get("category", "Unknown")
            if category not in classification:
                classification[category] = 1
            else:
                classification[category] += 1
        return classification

    def classify_questions_by_difficulty(self, questions):
        """"
        Classify questions by difficulty and calculate stats.

        Parameters:
            questions (list[dict]): A list of question dictionaries.

        Returns:
            dict: {
                "classification": Questions grouped by difficulty,
                "stats": Counts of questions per difficulty.
            }
        """
        classification = defaultdict(list)
        for question in questions:
            difficulty = question.get("difficulty", "Unknown")
            if difficulty not in classification:
                classification[difficulty] = 1
            else:
                classification[difficulty] += 1
        return classification

class random_question(questionloader):
    """
        Get random quiz questions.
    """
    def __init__(self, question_bank):
        questionloader.__init__(self, questionmanager)
        self.question_bank = question_bank

    def get_random_questions(self, category, difficulty, number):
        """
        Retrieve random questions based on category and difficulty.

        Parameters:
            questions (list[dict]): A list of available questions.
            category (str): Category to filter by.
            difficulty (str): Difficulty level to filter by.
            number (int): Number of random questions to retrieve.

        Returns:
            list[dict]: A list of random questions.
        """
        try:
            filtered = [
                q for q in self.question_bank
                if q.get("category") == category and q.get("difficulty") == difficulty
            ]

            if len(filtered) < number:
                raise ValueError("Not enough questions available for the specified criteria.")
            return sample(filtered, number)

        except ValueError as e:
            print(e)
