import os
import tempfile
from worker import convert_pdf_to_text
from fpdf import FPDF
from tabulate import tabulate
import threading
from queue import Queue
from concurrent.futures import Future
from worker import process_pdf_task

def create_temp_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, text)

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(tmp_fd)

    pdf.output(tmp_path)
    return tmp_path

def test_convert_pdf_to_text_simple():
    sample_text = "Hello, world!\nThis is a test PDF."
    pdf_path = create_temp_pdf(sample_text)

    try:
        extracted_text = convert_pdf_to_text(pdf_path)
        assert "Hello, world!" in extracted_text
        assert "This is a test PDF." in extracted_text
    finally:
        os.remove(pdf_path)

def test_convert_empty_pdf():
    tmp_path = create_temp_pdf("")

    try:
        extracted_text = convert_pdf_to_text(tmp_path)
        assert extracted_text == "", "Expected empty string from empty PDF"
    finally:
        os.remove(tmp_path)

def test_convert_multi_page_pdf():
    pdf = FPDF()
    pdf.set_font("Arial", size=14)
    
    for i in range(3):
        pdf.add_page()
        pdf.multi_cell(0, 10, f"This is page {i + 1}")

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(tmp_fd)
    pdf.output(tmp_path)

    try:
        text = convert_pdf_to_text(tmp_path)
        assert "This is page 1" in text
        assert "This is page 2" in text
        assert "This is page 3" in text
    finally:
        os.remove(tmp_path)

def test_convert_pdf_with_table():
    headers = ["Name", "Age", "City"]
    data = [
        ["Alice", "30", "New York"],
        ["Bob", "25", "Los Angeles"],
        ["Charlie", "35", "Chicago"]
    ]
    table_str = tabulate(data, headers=headers, tablefmt="plain")

    tmp_path = create_temp_pdf(table_str)

    try:
        text = convert_pdf_to_text(tmp_path)
        for row in data:
            for cell in row:
                assert cell in text, f"'{cell}' not found in extracted text"
    finally:
        os.remove(tmp_path)

def test_process_pdf_task_end_to_end():
    sample_text = "This is a test for the queue worker."
    pdf_path = create_temp_pdf(sample_text)

    try:
        q = Queue()
        result_future = Future()
        q.put((pdf_path, result_future))

        thread = threading.Thread(target=process_pdf_task, args=(q,), daemon=True)
        thread.start()

        text_result = result_future.result(timeout=5)
        assert "This is a test" in text_result
    finally:
        os.remove(pdf_path)

