import cv2
import numpy as np
import pytesseract
import mss
import re
import time
import threading

# Координаты областей (левая верхняя X, Y, правая нижняя X, Y)
REGIONS = {
    "question": (772, 445, 1789, 547),
    "A": (856, 628, 1349, 720),
    "B": (1434, 630, 1931, 715),
    "C": (854, 752, 1350, 845),
    "D": (1435, 755, 1932, 846),
}

previous_text = ""  # Буфер для хранения предыдущего текста

def capture_region(region):
    """Снимает скриншот указанной области"""
    with mss.mss() as sct:
        x1, y1, x2, y2 = region
        monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        screenshot = sct.grab(monitor)
        return np.array(screenshot)

def preprocess_image(img):
    """Фильтрация изображения для улучшения OCR"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Перевод в ЧБ
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Бинаризация
    return binary

def extract_text(img):
    """Извлекает текст из изображения"""
    text = pytesseract.image_to_string(img, lang='rus', config='--oem 3 --psm 6')
    return re.sub(r'[^А-Яа-яЁё0-9A-Za-z? ,:.]', '', text).strip()  # Очищаем от мусора

def scan_loop():
    """Фоновый процесс, который обновляет текст"""
    global previous_text
    while True:
        data = {}
        for key, region in REGIONS.items():
            img = capture_region(region)
            img = preprocess_image(img)
            text = extract_text(img)
            data[key] = text

        output = f"\n📜 ВОПРОС:\n{data.get('question', 'Ошибка')}\n\n"
        output += "📝 ВАРИАНТЫ ОТВЕТОВ:\n"
        for key in ["A", "B", "C", "D"]:
            output += f"{key}: {data.get(key, 'Ошибка')}\n"

        if output != previous_text:  # Только если текст изменился
            previous_text = output
            print("\n" + "=" * 50)  # Разделитель для удобства копирования
            print(output)

        time.sleep(1)  # Проверка раз в 2 секунды

# Запускаем фоновый поток
threading.Thread(target=scan_loop, daemon=True).start()

# Основной поток остаётся свободным для копирования текста
print("✅ Фоновый процесс запущен. Ожидание изменений текста...\n")
print("📌 Текущий вопрос и ответы будут обновляться только при изменении.")
print("🔄 Обновление каждые 2 секунды. Чтобы остановить, нажми Ctrl+C.")

while True:
    try:
        time.sleep(1)  # Держим основной поток активным
    except KeyboardInterrupt:
        print("\n🛑 Завершение работы.")
        break
