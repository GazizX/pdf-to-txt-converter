from concurrent import futures
import grpc
import os
from proto import pdf_converter_pb2, pdf_converter_pb2_grpc
from queue import Queue
import tempfile

# tasks queue (pdf tmp files to convert)
tasks_queue = Queue()

class PDFConverterServicer(pdf_converter_pb2_grpc.PDFConverterServicer):
    def UploadPDF(self, request_iterator, context):
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            for chunk in request_iterator:
                tmp.write(chunk.data)
            tmp_path = tmp.name

        tasks_queue.put(tmp_path)
        return pdf_converter_pb2.UploadResponce(success=True)