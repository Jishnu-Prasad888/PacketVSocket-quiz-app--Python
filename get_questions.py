import csv

questions = "questions.csv"


def get_data():
    questions_dict = {}
    with open('questions.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            q_id = row['id']
            question_text = row['Question']
            options = [row['Option A'], row['Option B'],
                       row['Option C'], row['Option D']]
            correct = row['Correct Answer']

            questions_dict[q_id] = {
                'question': question_text,
                'options': options,
                'correct_answer': correct
            }
    return questions_dict
