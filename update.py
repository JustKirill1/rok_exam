import requests
import json
import os
from datetime import datetime

URL = "https://rokstats.online/api/peerless-scholar/all-questions"
LOCAL_FILE = "all-questions.json"
UPDATE_LOG = "updates.txt"


# Функция загрузки JSON-файла с сервера
def download_json():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    return None


# Функция загрузки локального JSON-файла
def load_local_json():
    if os.path.exists(LOCAL_FILE):
        with open(LOCAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"data": []}


# Функция проверки изменений
def check_updates(new_data, old_data):
    old_questions = {q["_id"]: q for q in old_data.get("data", [])}
    new_questions = {q["_id"]: q for q in new_data.get("data", [])}

    updates = []

    # Проверяем новые вопросы
    for q_id, q_info in new_questions.items():
        if q_id not in old_questions:
            question_text = q_info["q"].get("ru", ["Нет текста"])[0] if q_info["q"].get("ru") else "Нет текста"
            updates.append(f"Появился новый вопрос: {question_text}📌")
            print(f"DEBUG: Найден новый вопрос '{question_text}'")  # Отладка

    # Проверяем подтвержденные вопросы
    for q_id, q_info in new_questions.items():
        old_confirmed = old_questions.get(q_id, {}).get("confirmed", False)
        new_confirmed = q_info.get("confirmed", False)

        question_text = q_info["q"].get("ru", ["Нет текста"])[0] if q_info["q"].get("ru") else "Нет текста"

        if not old_confirmed and new_confirmed:
            updates.append(f"У вопроса '{question_text}' появился статус подтвержден✅")
            print(f"DEBUG: Подтверждён статус вопроса '{question_text}'")  # Отладка

    return updates


# Основной код
def main():
    new_data = download_json()
    if not new_data:
        print("Ошибка загрузки JSON с сервера.")
        return

    old_data = load_local_json()

    print("Старые данные загружены.")
    print("Новые данные загружены.")

    updates = check_updates(new_data, old_data)

    if updates:
        with open(UPDATE_LOG, "a", encoding="utf-8") as log:
            log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Обновления:\n")
            for update in updates:
                log.write(update + "\n")
            log.write("---\n")
        print("\n".join(updates))
    else:
        print("Изменений нет.")

    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
