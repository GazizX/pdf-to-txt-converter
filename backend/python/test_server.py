from server import PDFConverterServicer, tasks_queue
from unittest.mock import Mock
from concurrent.futures import Future
from proto import pdf_converter_pb2

def make_request_iterator(data: bytes, chunk_size=10):
    for i in range(0, len(data), chunk_size):
        yield pdf_converter_pb2.PDFChunk(data=data[i:i+chunk_size])

# Проверяем саму работу функции с чанками, не происходит конвертации
def test_servicer_convert_success(monkeypatch):
    servicer = PDFConverterServicer()
    context = Mock()

    input_text = b"This is a test PDF."
    request_iterator = make_request_iterator(input_text)

    real_put = tasks_queue.put

    def fake_put(task):
        path, result_future = task
        result_future.set_result("Mocked response")

    monkeypatch.setattr(tasks_queue, "put", fake_put)

    response = servicer.Convert(request_iterator, context)
    assert response.text == "Mocked response"
    assert context.set_code.call_count == 0


    tasks_queue.put = real_put
