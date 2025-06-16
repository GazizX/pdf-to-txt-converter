import pdfplumber
import os

def convert_pdf_to_text(pdf_path: str) -> str:
    result = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            lines_dict = {}

            # Получаем слова с координатами
            words = page.extract_words(use_text_flow=True)

            # Группируем слова по координате 'top' (приближенно — по строкам)
            for word in words:
                top = round(word['top'], 1)  # округляем для устойчивости
                if top not in lines_dict:
                    lines_dict[top] = []
                lines_dict[top].append(word)

            # Сортируем строки по вертикальной позиции
            for top in sorted(lines_dict.keys()):
                line_words = lines_dict[top]
                # Сортируем слова по горизонтали
                line_words.sort(key=lambda w: w['x0'])

                # Получаем отступ первого слова
                indent = int(line_words[0]['x0'] // 7)  # эмпирически 1 пробел ≈ 7px
                line = " " * indent + " ".join(w['text'] for w in line_words)
                result.append(line)

            # Добавляем символ перевода страницы (form feed)
            result.append("\f")

    return "\n".join(result).strip("\f")

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