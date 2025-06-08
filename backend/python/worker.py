from pdfminer.high_level import extract_text
import os

def convert_pdf_to_text(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        raise Exception(f"PDF conversion error: {str(e)}")
    
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