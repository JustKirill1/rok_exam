import json
from Levenshtein import distance as levenshtein_distance

def load_questions_and_answers(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    questions_and_answers = []
    for item in data['data']:
        if 'q' in item and 'ru' in item['q']:
            questions_and_answers.append({
                'question': item['q']['ru'],
                'answer': item['a']['ru'],
                'confirmed': item.get('confirmed', False)
            })
    return questions_and_answers


# Поиск наиболее подходящего вопроса
def find_most_similar_question(input_question, questions_and_answers):
    min_distance = float('inf')
    most_similar_question = None
    answer = None
    is_confirmed = False

    for qa in questions_and_answers:
        for question in qa['question']:
            if question and isinstance(question, str):
                dist = levenshtein_distance(input_question, question)
                if dist < min_distance:
                    min_distance = dist
                    most_similar_question = question
                    answer = qa['answer']
                    is_confirmed = qa['confirmed']

    return most_similar_question, answer, min_distance, is_confirmed


# Основная функция
def main(input_question):
    file_path = 'all-questions.json'
    questions_and_answers = load_questions_and_answers(file_path)
    most_similar_question, answer, distance, is_confirmed = find_most_similar_question(input_question,
                                                                                       questions_and_answers)
    confirmed_symbol = "✅" if is_confirmed else ""

    return f"{most_similar_question}: {answer} {confirmed_symbol}"


if __name__ == "__main__":
    print(main("Какой из этих пг мтг жно использовать, чтобы улучшить накоманлира?"))
