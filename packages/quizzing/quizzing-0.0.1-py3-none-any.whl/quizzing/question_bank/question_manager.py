
class questionmanager:
    """
    Manages a question bank with add, remove, update and display.
    """

    def __init__(self):
        """
        Initializes the question bank and a loader instance.
        """
        self.question_bank = []  # List to store questions

    def add_question(self, question):
        """
        Add a new question to the question bank.

        Parameters:
            question (dict): A dictionary representing the question to add.
                             Must contain a unique "id" key.
        """
        try:
            question_id = int(question.get('id'))
            if not question_id:
                raise ValueError("Question must have a unique 'id' key.")
            for filter_question in self.question_bank:
                if int(filter_question['id']) == question_id:
                    raise ValueError(f"Question with id {question_id} already exists.")

            self.question_bank.append(question)

        except ValueError as e:
            print(e)

    def remove_question(self, question_id):
        """
        Remove a question from the question bank by its unique identifier.

        Parameters:
            question_id (str or int): The ID of the question to be removed.
        """
        try:
            question_id = int(question_id)

            for question in self.question_bank:
                if int(question['id']) == question_id:
                    self.question_bank.remove(question)
                    return

            raise ValueError(f"Question with id {question_id} does not exist.")

        except ValueError as e:
            print(e)

    def update_question(self, question_id, updated_data):
        """
        Update the details of an existing question.

        Parameters:
            question_id (str or int): The ID of the question to update.
            updated_data (dict): A dictionary containing the updated question information.
        """
        try:
            question_id = int(question_id)

            for question in self.question_bank:
                if int(question['id']) == question_id:
                    question.update(updated_data)
                    return

            raise ValueError(f"Question with id {question_id} does not exist.")

        except ValueError as e:
            print(e)

    def get_question_by_id(self, question_id):
        """
        Retrieve a specific question from the question bank by its unique identifier.

        Parameters:
            question_id (str or int): The ID of the question to retrieve.

        Returns:
            dict or None: The question matching the ID or None if not found.
        """
        try:
            question_id = int(question_id)

            for question in self.question_bank:
                if int(question['id']) == int(question_id):
                    return question

            raise ValueError(f"Question with id {question_id} does not exist.")

        except ValueError as e:
            print(e)

    def list_all_questions(self):
        """
        List all the questions currently stored in the question bank.

        Returns:
            list[dict]: A list of all available questions.
        """
        return list(self.question_bank)

