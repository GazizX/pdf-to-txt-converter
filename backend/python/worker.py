import pdfplumber
import logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def convert_pdf_to_text(pdf_path: str) -> str:
    logging.info(f"Converting PDF: {pdf_path}")
    result = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            lines_dict = {}

            # getting words with coordinates
            words = page.extract_words(use_text_flow=True)

            # groupping words by lines
            for word in words:
                top = round(word['top'], 1)
                if top not in lines_dict:
                    lines_dict[top] = []
                lines_dict[top].append(word)

            # sorting lines by Y coordinate
            for top in sorted(lines_dict.keys()):
                line_words = lines_dict[top]
                # sorting words in line by X coordinate
                line_words.sort(key=lambda w: w['x0'])

                # recieving the indent of the first word in line
                indent = int(line_words[0]['x0'] // 7)  # one space is appr. 7px
                line = " " * indent + " ".join(w['text'] for w in line_words)
                result.append(line)

            # new page symbol
            result.append("\f")
            logging.debug(f"Processed page {page_num} of {pdf_path}")

    text = "\n".join(result).strip("\f")
    logging.info(f"Finished converting PDF: {pdf_path}")
    return text

def process_pdf_task(queue):
    while True:
        # getting a task from queue
        pdf_path, result_future = queue.get()
        logging.info(f"Worker picked up task for: {pdf_path}")
        try:
            # trying to convert
            text = convert_pdf_to_text(pdf_path)
            result_future.set_result(text)
            logging.info(f"Task completed for: {pdf_path}")
        except Exception as e:
            logging.error(f"Error processing {pdf_path}: {e}", exc_info=True)
            result_future.set_exception(e)
        finally:
            # marking a task done
            queue.task_done()