import pdfplumber
import os

def convert_pdf_to_text(pdf_path: str) -> str:
    text_output = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Получаем все текстовые блоки с координатами
            words = page.extract_words(use_text_flow=True, keep_blank_chars=True)

            # Сортируем слова сначала по координате y (сверху вниз), затем по x (слева направо)
            words.sort(key=lambda w: (round(w['top'], 1), w['x0']))

            current_y = None
            current_line = []

            for word in words:
                y = round(word['top'], 1)
                x = word['x0']
                text = word['text']

                # Если новая строка (значительно отличается по координате y)
                if current_y is None or abs(y - current_y) > 2:
                    if current_line:
                        text_output.append(''.join(current_line))
                        current_line = []
                    current_y = y
                    # Добавляем отступы по x (1 пробел на ~5px отступа)
                    indent = int(x // 5)
                    current_line.append(' ' * indent + text)
                else:
                    current_line.append(' ' + text)

            # Добавим последнюю строку
            if current_line:
                text_output.append(''.join(current_line))

    return '\n'.join(text_output)
    
def process_pdf_task(queue):
    while True:
        # getting a task from queue
        pdf_path, result_future = queue.get()
        try:
            # trying to convert
            text = convert_pdf_to_text(pdf_path)
            result_future.set_result(text)
        except Exception as e:
            result_future.set_exception(e)
        finally:
            # marking a task done
            queue.task_done()