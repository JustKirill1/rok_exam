import json
from Levenshtein import distance as levenshtein_distance

# Загрузка вопросов из JSON-файла
def load_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Извлекаем все русские вопросы из массива data
    questions = []
    for item in data['data']:
        if 'q' in item and 'ru' in item['q']:  # Проверка, чтобы избежать ошибок
            questions.extend(item['q']['ru'])  # Добавляем все русские вопросы
    return questions

# Поиск наиболее подходящего вопроса
def find_most_similar_question(input_question, questions):
    min_distance = float('inf')
    most_similar_question = None

    for question in questions:
        if question and isinstance(question, str):  # Проверка, чтобы избежать ошибки с None или некорректными значениями
            dist = levenshtein_distance(input_question, question)
            if dist < min_distance:
                min_distance = dist
                most_similar_question = question

    return most_similar_question, min_distance

# Основная функция
def main():
    file_path = 'all-questions.json'  # Укажите путь к вашему JSON-файлу
    questions = load_questions(file_path)

    input_question = "Какой из этих пг мтг жно использовать, чтобы улучшить накоманлира?"
    most_similar_question, distance = find_most_similar_question(input_question, questions)

    print(f"Входной вопрос: {input_question}")
    print(f"Наиболее подходящий вопрос: {most_similar_question}")
    print(f"Расстояние Левенштейна: {distance}")

if __name__ == "__main__":
    main()
