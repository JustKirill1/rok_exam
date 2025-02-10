import json
from Levenshtein import distance as levenshtein_distance

# Загрузка вопросов из JSON-файла
def load_questions_and_answers(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Извлекаем все русские вопросы и соответствующие ответы из массива data
    questions_and_answers = []
    for item in data['data']:
        if 'q' in item and 'ru' in item['q']:  # Проверка на наличие ключей
            questions_and_answers.append({
                'question': item['q']['ru'],
                'answer': item['a']['ru']
            })
    return questions_and_answers
# Поиск наиболее подходящего вопроса
def find_most_similar_question(input_question, questions_and_answers):
    min_distance = float('inf')
    most_similar_question = None
    answer = None

    for qa in questions_and_answers:
        # Сравниваем входной вопрос с каждым вопросом в списке
        for question in qa['question']:
            if question and isinstance(question, str):  # Проверка на строку
                dist = levenshtein_distance(input_question, question)
                if dist < min_distance:
                    min_distance = dist
                    most_similar_question = question
                    answer = qa['answer']

    return most_similar_question, answer, min_distance

# Основная функция
def main():
    file_path = 'all-questions.json'  # Укажите путь к вашему JSON-файлу
    questions_and_answers = load_questions_and_answers(file_path)

    input_question = "Какой из этих пг мтг жно использовать, чтобы улучшить накоманлира?"
    most_similar_question, answer, distance = find_most_similar_question(input_question, questions_and_answers)
    return f"{most_similar_question}: {answer}"


if __name__ == "__main__":
    main()
